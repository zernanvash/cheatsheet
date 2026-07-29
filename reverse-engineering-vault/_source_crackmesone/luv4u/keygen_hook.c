/*
   luv4u Crackme LD_PRELOAD Keygen

   Bypasses all anti debug and anti VM checks, then auto solves the license.

   How it works

   1. Hook srand() and rand() to detect the license generation pattern.
      generate_license calls srand once then rand 64 times (32 chars + 32 shuffle).
      The first license has 65 rand calls because FUN_001022b0 sneaks one in
      before the next srand.
   2. Reconstruct the license from captured rand() outputs.
   3. Auto inject via fgets() hook when stdin is read.
   4. Patch out the VM checksum check in validate_license. The VM bytecodes
      are seeded with rdtsc so the XOR of all 6 channel results is random.
      It almost never equals 0x42.

   Build
      gcc -shared -fPIC -o luv4u_support.so keygen_hook.c -ldl

   Run
      LD_PRELOAD=./luv4u_support.so ./luv4u
*/

#define _GNU_SOURCE
#include <dlfcn.h>
#include <link.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/ptrace.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <stdint.h>

/* State tracking */
static int rand_count_since_srand = 0;
static int rand_values[1024] = {0};
static char generated_license[64] = {0};
static int license_ready = 0;

/*
   Binary patch for validate_license

   At ELF VA 0x4607 (Ghidra 0x104607) there is AND EAX, EDX (21 D0).
   EAX holds the hash match result. EDX holds the VM checksum result.
   The VM checksums are rdtsc seeded so they produce random values.
   We NOP this instruction so only the hash comparison matters.
*/

static int find_exe_base(struct dl_phdr_info *info, size_t size, void *data) {
    /* Main executable has an empty name */
    if (info->dlpi_name[0] == '\0') {
        *(uintptr_t *)data = info->dlpi_addr;
        return 1;
    }
    return 0;
}

__attribute__((constructor))
static void patch_validate_license(void) {
    uintptr_t base = 0;
    dl_iterate_phdr(find_exe_base, &base);

    if (base == 0) {
        fprintf(stderr, "  [!] Could not find executable base address\n");
        return;
    }

    /* AND EAX, EDX lives at ELF VA 0x4607 */
    unsigned char *patch_addr = (unsigned char *)(base + 0x4607);

    /* Make the page writable. The binary calls mprotect_rwx later but we need it now. */
    uintptr_t page = (uintptr_t)patch_addr & ~(uintptr_t)0xFFF;
    if (mprotect((void *)page, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC) != 0) {
        fprintf(stderr, "  [!] mprotect failed for patch\n");
        return;
    }

    /* Verify we found the right instruction */
    if (patch_addr[0] == 0x21 && patch_addr[1] == 0xD0) {
        patch_addr[0] = 0x90;  /* NOP */
        patch_addr[1] = 0x90;  /* NOP */
        fprintf(stderr, "  [+] Patched VM checksum check (AND EAX,EDX -> NOP NOP)\n");
    } else {
        fprintf(stderr, "  [!] Unexpected bytes at patch target: %02x %02x\n",
                patch_addr[0], patch_addr[1]);
    }
}

/* Hooked functions */

char *getenv(const char *name) {
    char *(*real_getenv)(const char *) = dlsym(RTLD_NEXT, "getenv");
    if (name && (strcmp(name, "LD_PRELOAD") == 0 || strcmp(name, "LD_DEBUG") == 0)) {
        return NULL;
    }
    return real_getenv(name);
}

void srand(unsigned int seed) {
    void (*real_srand)(unsigned int) = dlsym(RTLD_NEXT, "srand");

    /* Detect the license generation pattern.
       Regenerated licenses produce exactly 64 rand calls (32 chars + 32 shuffle).
       The first license produces 65 because FUN_001022b0 adds one extra. */
    if (rand_count_since_srand == 64 || rand_count_since_srand == 65) {
        /* Reconstruct the license. First 32 values become characters, next 32 are swap indices. */
        for (int i = 0; i < 32; i++) {
            generated_license[i] = (char)(rand_values[i] % 26) + 'A';
        }
        generated_license[32] = '\0';

        for (int i = 0; i < 16; i++) {
            int a = rand_values[32 + i * 2] % 32;
            int b = rand_values[32 + i * 2 + 1] % 32;
            char tmp = generated_license[a];
            generated_license[a] = generated_license[b];
            generated_license[b] = tmp;
        }

        license_ready = 1;

        fprintf(stderr, "\n");
        fprintf(stderr, "  ╔══════════════════════════════════════════╗\n");
        fprintf(stderr, "  ║         luv4u KEYGEN - ACTIVE            ║\n");
        fprintf(stderr, "  ╠══════════════════════════════════════════╣\n");
        fprintf(stderr, "  ║  License: %.32s  ║\n", generated_license);
        fprintf(stderr, "  ╚══════════════════════════════════════════╝\n");
        fprintf(stderr, "\n");
    }

    rand_count_since_srand = 0;
    real_srand(seed);
}

int rand(void) {
    int (*real_rand)(void) = dlsym(RTLD_NEXT, "rand");
    int r = real_rand();

    if (rand_count_since_srand < 1024) {
        rand_values[rand_count_since_srand] = r;
    }
    rand_count_since_srand++;

    return r;
}

char *fgets(char *s, int size, FILE *stream) {
    char *(*real_fgets)(char *, int, FILE *) = dlsym(RTLD_NEXT, "fgets");

    if (fileno(stream) == STDIN_FILENO && license_ready && generated_license[0]) {
        snprintf(s, size, "%s\n", generated_license);
        fprintf(stderr, "  [*] Auto-injected license: %s\n\n", generated_license);
        license_ready = 0;
        return s;
    }

    return real_fgets(s, size, stream);
}

long ptrace(enum __ptrace_request request, ...) {
    return 0;
}

FILE *fopen(const char *pathname, const char *mode) {
    FILE *(*real_fopen)(const char *, const char *) = dlsym(RTLD_NEXT, "fopen");

    if (pathname) {
        if (strcmp(pathname, "/proc/self/maps") == 0) {
            return NULL;
        }
        if (strcmp(pathname, "/sys/class/dmi/id/product_name") == 0) {
            return NULL;
        }
    }

    return real_fopen(pathname, mode);
}

int uname(struct utsname *buf) {
    int (*real_uname)(struct utsname *) = dlsym(RTLD_NEXT, "uname");
    return real_uname(buf);
}

int access(const char *pathname, int mode) {
    int (*real_access)(const char *, int) = dlsym(RTLD_NEXT, "access");

    if (pathname &&
        (strcmp(pathname, "/.dockerenv") == 0 ||
         strcmp(pathname, "/run/.containerenv") == 0)) {
        return -1;
    }

    return real_access(pathname, mode);
}
