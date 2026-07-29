#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * Keygen for "obfuscated" crackme
 *
 * The binary validates a serial by dispatching each character through a
 * ptrace-based VM. Success requires three registers to reach target values:
 *   r12d = 0xdeadbeef (via XOR operations)
 *   r13d = 0x42318657 (via stack push/swap/pop)
 *   r14d = 0xcafebabe (via ADD operations)
 * A final CHECK character triggers the comparison.
 *
 * Characters are categorized by their VM handler:
 *   XOR handlers  - XOR a constant into r12d
 *   ADD handlers  - ADD a constant into r14d
 *   PUSH          - push values 1-8 onto VM stack
 *   POP           - pop 8 values into r13d as nibbles
 *   SWAP handlers - rearrange VM stack positions
 *   CHECK         - compare registers against targets, emit int3 on success
 *   NOP handlers  - no effect on target registers
 */

// XOR handlers for r12d
// Required combination: 0x87e78e82 ^ 0x1c71472b ^ 0x90bfe692 ^ 0xd58491d4 = 0xdeadbeef
static const char *xor_chars[] = {
    "I",          // XOR 0x87e78e82 (handler 0x11ca)
    "#3~",        // XOR 0x1c71472b (handler 0x1220)
    "Ymt",        // XOR 0x90bfe692 (handler 0x126a)
    "1MO",        // XOR 0xd58491d4 (handler 0x1434)
};

// ADD handlers for r14d (each used exactly once sums to 0xcafebabe)
static const struct { unsigned int val; const char *chars; } add_handlers[] = {
    { 0x0e,       "):v" },       // handler 0x11b9
    { 0x0a000000, "$Aq}" },      // handler 0x1233
    { 0xc0000000, "Q" },         // handler 0x1247
    { 0x000e0000, "f" },         // handler 0x12bf
    { 0x0000b000, "5FX" },       // handler 0x12ea
    { 0x000000b0, " +" },        // handler 0x1343
    { 0x00f00000, "8e" },        // handler 0x13d2
    { 0x00000a00, ",RWi" },      // handler 0x145a
};

// Stack operations for r13d
// PUSH: '*', 'h', 'x', 'z'
// POP:  'd'
// Required swap sequence: swap46, swap30, swap47
// swap46: '!', 'J', 'K', '`', 'p', '%', 'U', 'b', 'g' (handlers 0x1281, 0x132c, 0x12fe)
// swap30: '@', 'a', '{'                                  (handler 0x1389)
// swap47: '-', 'T'                                       (handler 0x13bb)

static const char *push_chars = "*hxz";
static const char *pop_chars = "d";
static const char *swap46_chars = "!JK`p%Ubg";
static const char *swap30_chars = "@a{";
static const char *swap47_chars = "-T";

// CHECK handler (triggers final comparison)
static const char *check_chars = "Hjr";

// NOP-like handlers (no effect on r12/r13/r14)
static const char *nop_chars = "]^;";

static char pick(const char *set) {
    int len = strlen(set);
    return set[rand() % len];
}

static void shuffle(char *buf, int len) {
    for (int i = len - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        char tmp = buf[i];
        buf[i] = buf[j];
        buf[j] = tmp;
    }
}

int main(void) {
    srand(time(NULL));

    char serial[64];
    int pos = 0;

    // Part 1: XOR chars for r12d (order doesn't matter, pick one from each group)
    char xor_part[5];
    for (int i = 0; i < 4; i++)
        xor_part[i] = pick(xor_chars[i]);
    xor_part[4] = '\0';
    shuffle(xor_part, 4);

    // Part 2: ADD chars for r14d (one from each handler, order doesn't matter)
    char add_part[9];
    for (int i = 0; i < 8; i++)
        add_part[i] = pick(add_handlers[i].chars);
    add_part[8] = '\0';
    shuffle(add_part, 8);

    // Part 3: Stack ops for r13d (must be: PUSH, swap46, swap30, swap47, POP)
    char stack_part[6];
    stack_part[0] = pick(push_chars);
    stack_part[1] = pick(swap46_chars);
    stack_part[2] = pick(swap30_chars);
    stack_part[3] = pick(swap47_chars);
    stack_part[4] = pick(pop_chars);
    stack_part[5] = '\0';

    // Part 4: CHECK (must be last)
    char check = pick(check_chars);

    // Combine: XOR + ADD + STACK can be interleaved freely as long as:
    //   - stack ops maintain their internal order (push, swap46, swap30, swap47, pop)
    //   - CHECK is last
    // For simplicity, concatenate in blocks with optional NOPs for variety

    // XOR and ADD parts can go in any order relative to each other
    pos = 0;
    memcpy(serial + pos, xor_part, 4); pos += 4;
    memcpy(serial + pos, add_part, 8); pos += 8;
    memcpy(serial + pos, stack_part, 5); pos += 5;

    // Optionally insert some NOPs
    int num_nops = rand() % 3;
    for (int i = 0; i < num_nops; i++)
        serial[pos++] = pick(nop_chars);

    serial[pos++] = check;
    serial[pos] = '\0';

    printf("%s\n", serial);
    return 0;
}
