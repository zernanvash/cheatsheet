# MCM 5.0 Writeup

Challenge_URL: https://crackmes.one/crackme/699da9a00b6d36e727710a49

this crackme uses a parent-child debug protocol:

- parent process runs as debugger/guardian
- child intentionally executes UD2 instructions
- parent catches the illegal-instruction debug event
- parent reads encrypted child memory, XOR-decrypts it, and writes it back

so large parts of verify logic are not valid statically in the on-disk image.

- Entry: 0x140004a80
- Main mode dispatch: 0x1402052c0
- RunChild path: 0x1401fde90
- RunParent path: 0x1401ed240

mode gate:
- argv[1] compared to literal: --type=utility


- Parent mode: supervises child with debug-event loop.
- Child mode: triggers parent-assisted decrypt and runs password verification.



Child -> Parent Signal Mechanism (UD2 Protocol)

inside the unpacked image:
- 0x14020c101 path sets RAX=1 then UD2 (VehCheck signal)
- 0x14020c17c path sets RAX=2 then UD2 (SMC decrypt request)

(deliberate software interrupts via invalid opcode)

parent XOR trace

-child intentionally raises UD2 with command in RAX

000000014020c0f0 <.data+0x320f0>:
   14020c0f0: 48 33 c0              xor    rax,rax
   14020c0f3: 4d 87 c0              xchg   r8,r8
   14020c0f6: 0f 0b                 ud2
   14020c0f8: 90                    nop
   14020c0f9: 49 8b c2              mov    rax,r10
   14020c0fc: 48 83 c0 00           add    rax,0x0
   14020c100: c3                    ret
   14020c101: 0f 1b c0              nop    eax
   14020c104: 53                    push   rbx
   14020c105: 48 c7 c3 cd ab 00 00  mov    rbx,0xabcd
   14020c10c: 48 81 f3 78 56 00 00  xor    rbx,0x5678
   14020c113: 48 83 eb 01           sub    rbx,0x1
   14020c117: 5b                    pop    rbx
   14020c118: 48 33 c0              xor    rax,rax
   14020c11b: 48 ff c0              inc    rax
   14020c11e: 4d 87 c9              xchg   r9,r9
   14020c121: 0f 0b                 ud2
   14020c123: 49 8b c2              mov    rax,r10
   14020c126: 48 33 c9              xor    rcx,rcx
   14020c129: 48 0b c0              or     rax,rax
   14020c12c: c3                    ret
   14020c12d: 4c 8b da              mov    r11,rdx
   14020c130: 4d 8b d0              mov    r10,r8
   14020c133: 49 8b d1              mov    rdx,r9
   14020c136: 4c 8b 44 24 28        mov    r8,QWORD PTR [rsp+0x28]
   14020c13b: 4c 8b 4c 24 30        mov    r9,QWORD PTR [rsp+0x30]
   14020c140: 48 8b 44 24 38        mov    rax,QWORD PTR [rsp+0x38]
   14020c145: 48 89 44 24 28        mov    QWORD PTR [rsp+0x28],rax
   14020c14a: 48 8b 44 24 40        mov    rax,QWORD PTR [rsp+0x40]
   14020c14f: 48 89 44 24 30        mov    QWORD PTR [rsp+0x30],rax
   14020c154: 8b c1                 mov    eax,ecx
   14020c156: 66 0f ef c0           pxor   xmm0,xmm0
   14020c15a: 66 0f ef c9           pxor   xmm1,xmm1
   14020c15e: 66 0f ef d2           pxor   xmm2,xmm2
   14020c162: 66 0f ef db           pxor   xmm3,xmm3
   14020c166: 66 0f ef e4           pxor   xmm4,xmm4
   14020c16a: 66 0f ef ed           pxor   xmm5,xmm5
   14020c16e: 41 ff e3              jmp    r11
   14020c171: 0f 1a c0              nop    eax
   14020c174: 0f 0b                 ud2
   14020c176: 90                    nop
   14020c177: 90                    nop
   14020c178: 49 8b c2              mov    rax,r10
   14020c17b: c3                    ret
   14020c17c: 48 33 c0              xor    rax,rax
   14020c17f: 48 83 c0 02           add    rax,0x2
   14020c183: 0f 0b                 ud2
   14020c185: c3                    ret
   14020c186: 90                    nop
   14020c187: cc                    int3
   14020c188: 48 89 5c 24 08        mov    QWORD PTR [rsp+0x8],rbx
   14020c18d: 57                    push   rdi
   14020c18e: 48 83 ec 20           sub    rsp,0x20
   14020c192: 48 8b f9              mov    rdi,rcx
   14020c195: f0 ff 05 64 28 03 00  lock inc DWORD PTR [rip+0x32864]        # 0x14023ea00
   14020c19c: 75 1f                 jne    0x14020c1bd
   14020c19e: 48 8d 1d 5b 3c 03 00  lea    rbx,[rip+0x33c5b]        # 0x14023fe00
   14020c1a5: 48 8b cb              mov    rcx,rbx
   14020c1a8: e8 13 1d 00 00        call   0x14020dec0
   14020c1ad: 48 8d 05 8c 3d 03 00  lea    rax,[rip+0x33d8c]        # 0x14023ff40
   14020c1b4: 48 83 c3 28           add    rbx,0x28
   14020c1b8: 48 3b d8              cmp    rbx,rax
   14020c1bb: 75 e8                 jne    0x14020c1a5
   14020c1bd: 48 8b 5c              mov    rbx,QWORD PTR [rsp+0x30]

parent parses _SMC_T as RVA:Size:Key
  1270       local_1790 = ~local_1790;
  1271       local_18f0 = (longlong)&DAT_14020c0e0 - local_18f0;
  1272       local_1738 = 0;
  1273       bVar4 = false;
  1274       local_18f8[0] = 0;
  1275       uStack_1944 = 0;
  1276       local_18e0._0_4_ = 0;
  1277       local_1288 = 0;
  1278       uStack_1280 = 0;
  1279       local_1278 = 0;
  1280       uStack_1270 = 0;
  1281       local_1268 = 0;
  1282       uStack_1260 = 0;
  1283       local_1258 = 0;
  1284       uStack_1250 = 0;
  1285       iVar9 = (*DAT_140245a08)(s__SMC_T_1401ea7dc,&local_1288,0x40);
  1286       if (iVar9 == 0) {
  1287         local_1368 = 0;
  1288         uStack_1360 = 0;
  1289         local_1358 = 0;
  1290         local_1350 = 0;
  1291         FUN_140208590(&local_1368,s_RunParent___SMC_T_variable_not_f_1401ea880,0x25);
  1292         FUN_140206490(&local_1368);
  1293       }
  1294       else {
  1295         puStack_1978 = &local_18e0;
  1296         iVar9 = FUN_1401f20e0(&local_1288,s__x__x__x_1401ea7e8,local_18f8,&uStack_1944);
  1297         if (iVar9 == 3) {
  1298           if ((uStack_1944 == 0) || (local_18f8[0] == 0)) {
  1299             local_1388 = 0;
  1300             uStack_1380 = 0;
  1301             local_1378 = 0;
  1302             local_1370 = 0;
  1303             FUN_140208590(&local_1388,s_RunParent___SMC_T_parsed_but_val_1401ea828,0x2e);
  1304             FUN_140206490(&local_1388);
  1305           }
  1306           else {
  1307             bVar4 = true;
  1308             FUN_1402069e0(local_358);
  1309             plVar18 = (longlong *)
  1310                       FUN_140206100(local_348,s_RunParent___SMC_T_parsed__RVA__1401ea808);
  1311             iVar9 = *(int *)(*plVar18 + 4);
  1312             puVar1 = (uint *)((longlong)iVar9 + 0x18 + (longlong)plVar18);
  1313             *puVar1 = *puVar1 & 0xfffff9ff;
  1314             puVar1 = (uint *)((longlong)iVar9 + 0x18 + (longlong)plVar18);
  1315             *puVar1 = *puVar1 | 0x800;
  1316             uVar20 = FUN_140207750(plVar18,local_18f8[0]);
  1317             uVar20 = FUN_140206100(uVar20,s___Size__1401ea800);
  1318             uVar20 = FUN_140207750(uVar20,uStack_1944);
  1319             uVar20 = FUN_140206100(uVar20,s___Key__1401ea7f4);
  1320             FUN_140207750(uVar20,(undefined4)local_18e0);
  1321             FUN_140206770(local_358,local_aa8);
  1322             FUN_140206490(local_aa8);
  1323             FUN_1401fcf60(local_358);

parent handles RAX==2 path and XOR-decrypts buffer
  2621       local_14e8 = 0;
  2622       uStack_14e0 = 0;
  2623       local_14d8 = 0;
  2624       local_14d0 = 0;
  2625       FUN_140208590(&local_14e8,s_RunParent__Received_SMC_Decrypti_1401ea9f0,0x32);
  2626       if (0xf < local_14d0) {
  2627         FUN_14020b080(&local_14e8,local_14e8);
  2628       }
  2629       local_14d8 = 0;
  2630       local_14d0 = 0xf;
  2631       local_14e8 = local_14e8 & 0xffffffffffffff00;
  2632       if ((bVar4) && (local_7a8 != 0)) {
  2633         pcVar21 = (code *)((ulonglong)local_18f8[0] + local_7a8);
  2634         uVar29 = (ulonglong)uStack_1944;
  2635         local_1710 = 0;
  2636         lStack_1708 = 0;
  2637         uVar24 = 0;
  2638         local_1700 = 0;
  2639         if (uVar29 != 0) {
  2640           if (uVar29 < 0x1000) {
  2641             local_1710 = FUN_14020e318(uVar29);
  2642           }
  2643           else {
  2644             if (uVar29 + 0x27 <= uVar29) goto LAB_1401f1d24;
  2645             lVar14 = FUN_14020e318();
  2646             if (lVar14 == 0) {
  2647 LAB_1401f1568:
  2648               pcVar12 = (code *)swi(0x29);
  2649               (*pcVar12)(5);
  2650               puVar31 = auStack_1990;
  2651               goto LAB_1401f156f;
  2652             }
  2653             local_1710 = lVar14 + 0x27U & 0xffffffffffffffe0;
  2654             *(longlong *)(local_1710 - 8) = lVar14;
  2655           }
  2656           lVar14 = local_1710 + uVar29;
  2657           local_1700 = lVar14;
  2658           FUN_140234100(local_1710,0,uVar29);
  2659           local_1478 = 0;
  2660           lStack_1708 = lVar14;
  2661           FUN_14020af90(&local_1478);
  2662         }
  2663         local_1720 = 0;
  2664         local_1728 = 0;
  2665         FUN_1402069e0(local_258);
  2666         plVar18 = (longlong *)FUN_140206100(local_248,s_RunParent__Decrypting_SMC__Addr__1401eaa30);
  2667         iVar9 = *(int *)(*plVar18 + 4);
  2668         puVar1 = (uint *)((longlong)iVar9 + 0x18 + (longlong)plVar18);
  2669         *puVar1 = *puVar1 & 0xfffff9ff;
  2670         puVar1 = (uint *)((longlong)iVar9 + 0x18 + (longlong)plVar18);
  2671         *puVar1 = *puVar1 | 0x800;
  2672         uVar20 = FUN_1402072f0(plVar18,pcVar21);
  2673         uVar20 = FUN_140206100(uVar20,s_Size__1401eaa24);
  2674         FUN_140207750(uVar20,uStack_1944);
  2675         FUN_140206770(local_258,local_a68);
  2676         FUN_140206490(local_a68);
  2677         puStack_1978 = &local_1720;
  2678         iVar9 = (*DAT_140245a30)(local_1878,pcVar21,local_1710,uStack_1944);
  2679         if ((iVar9 == 0) || (local_1720 != uStack_1944)) {
  2680           local_1628 = 0;
  2681           uStack_1620 = 0;
  2682           local_1618 = 0;
  2683           local_1610 = 0;
  2684           FUN_140208590(&local_1628,s_RunParent__Failed_to_read_SMC_me_1401eaaf0,0x25);
  2685           if (0xf < local_1610) {
  2686             FUN_14020b080(&local_1628,local_1628);
  2687           }
  2688           local_1618 = 0;
  2689           local_1610 = 0xf;
  2690           local_1628 = local_1628 & 0xffffffffffffff00;
  2691         }
  2692         else {
  2693           if (uStack_1944 != 0) {
  2694             do {
  2695               *(byte *)(local_1710 + uVar24) =
  2696                    *(byte *)(local_1710 + uVar24) ^
  2697                    *(byte *)((longlong)&local_18e0 + (ulonglong)((uint)uVar24 & 3));
  2698               uVar24 = uVar24 + 1;
  2699             } while (uVar24 < uStack_1944);
  2700           }
  2701           puStack_1978 = (ulonglong *)&local_1880;
  2702           iVar9 = (*DAT_140245a20)(local_1878,pcVar21,uStack_1944,0x40);
  2703           if (iVar9 == 0) {
  2704             local_1328 = 0;
  2705             uStack_1320 = 0;
  2706             local_1318 = 0;
  2707             local_1310 = 0;
  2708             FUN_140208590(&local_1328,s_RunParent__Failed_to_VirtualProt_1401eaab8,0x30);
  2709             FUN_140206490(&local_1328);
  2710           }
  2711           else {
  2712             puStack_1978 = &local_1728;
  2713             iVar9 = (*DAT_140245a00)(local_1878,pcVar21,local_1710,uStack_1944);
  2714             if ((iVar9 == 0) || (local_1728 != uStack_1944)) {
  2715               local_1648 = 0;
  2716               uStack_1640 = 0;
  2717               local_1638 = 0;
  2718               local_1630 = 0;
  2719               FUN_140208590(&local_1648,s_RunParent__Failed_to_write_SMC_m_1401eaa88,0x2b);
  2720               if (0xf < local_1630) {
  2721                 FUN_14020b080(&local_1648,local_1648);
  2722               }
  2723               local_1638 = 0;
  2724               local_1630 = 0xf;
  2725               local_1648 = local_1648 & 0xffffffffffffff00;
  2726             }
  2727             else {
  2728               local_14c8 = 0;
  2729               uStack_14c0 = 0;
  2730               local_14b8 = 0;
  2731               local_14b0 = 0;
  2732               FUN_140208590(&local_14c8,s_RunParent__SMC_memory_written_su_1401eaa58,0x2b);
  2733               if (0xf < local_14b0) {
  2734                 FUN_14020b080(&local_14c8,local_14c8);
  2735               }
  2736               local_14b8 = 0;
  2737               local_14b0 = 0xf;
  2738               local_14c8 = local_14c8 & 0xffffffffffffff00;
  2739             }
  2740             puStack_1978 = (ulonglong *)&local_1880;
  2741             (*DAT_140245a20)(local_1878,pcVar21,uStack_1944,local_1880);
  2742           }
  2743         }
  2744         bVar4 = false;

strings embedded in the binary:
    RunParent: EXCEPTION_DEBUG_EVENT. Code: 0x
    RunParent: CrashStub (0x1337) detected.
    RunParent: Set keyPart1 in child R10.
    RunParent: VehCheckAsm (RAX=0 or 1) detected.
    RunParent: Child stub integrity check failed!
    RunParent: Set keyPart2/mask in child R10.
    RunParent: Received SMC Decryption Request (RAX=2)
    RunParent: Decrypting SMC. Addr=
    RunParent: SMC memory written successfully.
    RunParent: Failed to write SMC memory back.
    RunParent: Failed to VirtualProtectEx SMC memory
    RunParent: Failed to read SMC memory.
    RunParent: Ignored SMC request (already decrypted or context invalid)
    RunParent: Unhandled UD2 exception.





parent SMC Parameters (_SMC_T)
reads an environment variable
 _SMC_T (with format "%x:%x:%x")

value during runs
- 5f000:38b9:a0f893fd

which is:
- RVA/base offset: 0x5f000
- size: 0x38b9
- XOR key dword: 0xa0f893fd


this is how i traced parent XOR Decryption
1. find RunParent strings:
   - "RunParent: Received SMC Decryption Request (RAX=2)"
   - "RunParent: Decrypting SMC. Addr="
   - "RunParent: SMC memory written successfully."

2. xrefs to RunParent handler in 0x1401ed240

3. in RAX==2 branch
   - compute child address from parsed _SMC_T tuple
   - ReadProcessMemory/NtReadVirtualMemory into local buffer
   - XOR each byte with rotating byte of 32-bit key
   - VirtualProtectEx for write permissions
   - WriteProcessMemory/NtWriteVirtualMemory back to child

loop logic (equivalent ):

for i in [0 .. size-1]:
    buf[i] ^= ((uint8_t*)&key)[i & 3]

this behavior appears in FUN_1401ed240




i also wasted a lot of time because i couldn't really get this to work reliably
on my linux / wine env xD (ended up having to rest on real windows hardware)

like for example the parent attempted CreateProcess on malformed child token/name
or child spawn failed unless an alias file matching that malformed token existed


something very important is that VerifyPasswordSMC consumes first 64 password bytes in mix phase..
before realizing that, the tools i instrumented kept producing garbage and i wasted bunch of time :(

everything started to make more sense after i enforced 64-byte candidate length in oracle/search tooling



my "oracle" setup (instrumented for linux with wine but the high level concept is the same..)
hook:
- LD_PRELOAD hook polls process memory from inside process context
- watches:
  - 0x140065f00 (argument/eval tuple area)
  - 0x140065640 (state indicator)
- writes log

decisive marker:
- arg5 = 0338578a

oracle objective:
- take the LAST observed eval for arg5=0338578a in each run
- target success condition: eval == 0x00000000

but why LAST eval?
earlier eval lines can be intermediate states... final value is the stable decision signal!



search: (search_password_final_eval.py)

- start from several 64-byte seeds
- mutate characters / occasional swaps
- evaluate each candidate across multiple rounds
- robust objective minimizes worst observed distance to target
- accept improvements and occasional exploratory moves



Final Answer: CCCCCChCCCCiCM&CCCCCCCGCCCCCCX#CCKCCC9CCCCCCCCCCCCCCCCCCCCmVC*CC

