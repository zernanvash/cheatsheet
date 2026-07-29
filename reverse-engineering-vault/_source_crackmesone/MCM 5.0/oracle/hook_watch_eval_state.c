#define _GNU_SOURCE
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/uio.h>

static const uintptr_t kAddr = 0x140065f00ULL;
static const uintptr_t kState = 0x140065640ULL;

static int read_cmdline(char *out, size_t out_sz) {
    FILE *f = fopen("/proc/self/cmdline", "rb");
    if (!f) return 0;
    size_t n = fread(out, 1, out_sz - 1, f);
    fclose(f);
    if (n == 0) return 0;
    for (size_t i = 0; i < n; i++) if (out[i] == '\0') out[i] = ' ';
    out[n] = '\0';
    return 1;
}

static int read_self(uintptr_t addr, void *buf, size_t len) {
    struct iovec local = { .iov_base = buf, .iov_len = len };
    struct iovec remote = { .iov_base = (void*)addr, .iov_len = len };
    ssize_t n = process_vm_readv(getpid(), &local, 1, &remote, 1, 0);
    return n == (ssize_t)len;
}

static void *thr(void *arg) {
    (void)arg;
    pid_t pid = getpid();
    char cmd[4096] = {0};
    read_cmdline(cmd, sizeof(cmd));
    if (!strstr(cmd, "live_cap_allargs_eval2.bin")) return NULL;

    char path[256];
    snprintf(path, sizeof(path), "/tmp/hook_watch_eval_state_%d.log", (int)pid);
    FILE *f = fopen(path, "w");
    if (!f) return NULL;
    fprintf(f, "pid=%d cmd=%s\n", (int)pid, cmd);
    fflush(f);

    uint64_t last[5] = {~0ULL,~0ULL,~0ULL,~0ULL,~0ULL};
    uint64_t last_state = ~0ULL;
    for (int i = 0; i < 120000; i++) {
        uint64_t v[5] = {0,0,0,0,0};
        uint64_t st = 0;
        int ok1 = read_self(kAddr, v, sizeof(v));
        int ok2 = read_self(kState, &st, sizeof(st));
        if (ok2 && st != last_state) {
            fprintf(f, "t=%d state64=%016llx state8=%02x\n", i, (unsigned long long)st, (unsigned)((unsigned char)st));
            fflush(f);
            last_state = st;
        }
        if (ok1 && memcmp(v,last,sizeof(v)) != 0) {
            uint32_t esi = (uint32_t)(v[0] & 0xffffffffu);
            uint32_t arg5 = (uint32_t)((v[0] >> 32) & 0xffffffffu);
            uint32_t eval = (uint32_t)(v[4] & 0xffffffffu);
            fprintf(f, "t=%d esi=%08x arg5=%08x r8=%016llx r9=%016llx rcx=%016llx eval=%08x\n",
                    i, esi, arg5,
                    (unsigned long long)v[1],
                    (unsigned long long)v[2],
                    (unsigned long long)v[3],
                    eval);
            fflush(f);
            memcpy(last,v,sizeof(v));
        }
        usleep(100);
    }
    fclose(f);
    return NULL;
}

__attribute__((constructor)) static void init(void) {
    pthread_t t;
    if (pthread_create(&t, NULL, thr, NULL) == 0) pthread_detach(t);
}
