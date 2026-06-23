
---
> Date: 4/6/2026 :beaver:   
> Purpose : Understand FLRSCRNSVR.SRC Execution Flow and Get Flag  
> Owner: Khoi nguyen - Nova :dragon_face:   
> Tools reverse : Ghidra   
> Challenge from crackme-ctf-2026
> Target: FLRSCRNSVR.SRC  
> Platform: Windows  
--- 

<p align = "center" style = "color:red"> Info file </p>


File name `FLRSCRNSVR.src`  
From crackme-ctf-2026  
Test file :<!-- ![Database](images/test-1.png) -->
<img src = "images/test-1.png" >

---
<p align = "center" style = "color:red">Analysis</p>

<p align = "left" style = "color:#4A90E2">File type</p>

file FLRSCRNSVR.SCR  
=> `FLRSCRNSVR.SCR: PE32+ executable (GUI) x86-64, for MS Windows `  
=> file .scr is file Screen Saver   
=> Like file .exe it can run  
=> When pc not use window will run screensaver  

<p align = "center" style = "color:#4A90E2">Import</p>

```
-----
ADVAPI32.DLL
API-MS-WIN-CRT-CONVERT-L1-1-0.DLL
API-MS-WIN-CRT-HEAP-L1-1-0.DLL
API-MS-WIN-CRT-LOCALE-L1-1-0.DLL
API-MS-WIN-CRT-MATH-L1-1-0.DLL
API-MS-WIN-CRT-RUNTIME-L1-1-0.DLL
API-MS-WIN-CRT-STDIO-L1-1-0.DLL
API-MS-WIN-CRT-STRING-L1-1-0.DLL
API-MS-WIN-CRT-TIME-L1-1-0.DLL
API-MS-WIN-CRT-UTILITY-L1-1-0.DLL
GDI32.DLL
KERNEL32.DLL
MSIMG32.DLL
USER32.DLL
VCRUNTIME140.DLL
 -----
```
+ Split to group by func:
```
-----
API-MS-WIN-CRT-CONVERT-L1-1-0.DLL
API-MS-WIN-CRT-HEAP-L1-1-0.DLL
API-MS-WIN-CRT-LOCALE-L1-1-0.DLL
API-MS-WIN-CRT-MATH-L1-1-0.DLL
API-MS-WIN-CRT-RUNTIME-L1-1-0.DLL
API-MS-WIN-CRT-STDIO-L1-1-0.DLL
API-MS-WIN-CRT-STRING-L1-1-0.DLL
API-MS-WIN-CRT-TIME-L1-1-0.DLL
API-MS-WIN-CRT-UTILITY-L1-1-0.DLL
VCRUNTIME140.DLL
 -----
```

=> Lib for VSC   
=> file make by MSVC  

`KERNEL32.DLL`  
=> Lib core system API of Windows  
`USER32.DLL`  
=> GUI for user => Use to create frame  
`GDI32.DLL`  
=> Graphics Device Interface  
=> Used for drawing graphics without needing knowledge of the underlying hardware  
=> It can draw lines, rectangles, pixels, etc  
=> Displays text  
=> Processes images  
`MSIMG32.DLL`  
=>  Image processing library, graphic effects, images   

<p align = "center" style = "color:#4A90E2"> Defined Strings</p>

I found some string very suspect:  
-str1:  

![Database](images/define_str_1.png)  

-str2:  

![Database](images/define_str_2.png)

-str3:  

![Database](images/define_str_3.png)

Check function used with each string i found:
- str1:

```c
void FUN_140001300(longlong param_1)

{
  ushort *puVar1;
  undefined2 uVar2;
  DWORD DVar3;
  BOOL BVar4;
  LSTATUS LVar5;
  UINT UVar6;
  HWND pHVar7;
  HDC pHVar8;
  HDC pHVar9;
  HBITMAP pHVar10;
  HGDIOBJ pvVar11;
  wchar_t *pwVar12;
  HANDLE pvVar13;
  longlong lVar14;
  ulonglong uVar15;
  undefined2 *puVar16;
  ulonglong uVar17;
  longlong lVar18;
  ulonglong uVar19;
  ulonglong uVar20;
  undefined1 auStackY_6b8 [32];
  short local_688 [12];
  DWORD local_670;
  undefined4 uStack_66c;
  HKEY local_668;
  HKEY local_660;
  DWORD local_658 [2];
  undefined1 local_650 [16];
  undefined1 local_640 [16];
  undefined1 local_630 [24];
  _WIN32_FIND_DATAW local_618;
  WCHAR local_3c8 [32];
  wchar_t local_388 [80];
  wchar_t local_2e8 [80];
  WCHAR local_248 [264];
  ulonglong local_38;
  
  local_38 = DAT_140008000 ^ (ulonglong)auStackY_6b8;
  DVar3 = GetTickCount();
  local_670 = DVar3 % 100 + 5;
  SetLastError(local_670);
  wcscpy_s(local_388,0x50,L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP");
  pHVar7 = GetDesktopWindow();
  IsWindow(pHVar7);
  wcscat_s(local_388,0x50,L"QRSTUVWXYZ0123456789}_{=-");
  local_658[0] = 0x20;
  BVar4 = GetComputerNameW(local_3c8,local_658);
  if (BVar4 != 0) {
    local_670 = (DWORD)(ushort)local_3c8[0];
  }
  wcscpy_s(local_2e8,0x50,L"-={_}9876543210ZYXWVUTSRQPONMLKJIHGF");
  pHVar8 = GetDC((HWND)0x0);
  pHVar9 = CreateCompatibleDC(pHVar8);
  pHVar10 = CreateCompatibleBitmap(pHVar8,1,1);
  DeleteObject(pHVar10);
  DeleteDC(pHVar9);
  ReleaseDC((HWND)0x0,pHVar8);
  pHVar8 = GetDC((HWND)0x0);
  pHVar9 = CreateCompatibleDC(pHVar8);
  pHVar10 = CreateCompatibleBitmap(pHVar8,1,1);
  DeleteObject(pHVar10);
  DeleteDC(pHVar9);
  ReleaseDC((HWND)0x0,pHVar8);
  wcscat_s(local_2e8,0x50,L"EDCBAzyxwvutsrqponmlkjihgfedcba");
  pvVar11 = GetStockObject(4);
  GetObjectW(pvVar11,0x10,local_650);
  uVar19 = 0xffffffffffffffff;
  uVar20 = 0xffffffffffffffff;
  do {
    uVar20 = uVar20 + 1;
  } while (*(short *)(param_1 + uVar20 * 2) != 0);
  uVar17 = 0;
  lVar18 = 5;
  local_670 = 0;
  lVar14 = 5;
  do {
    local_670 = local_670 + 1;
    lVar14 = lVar14 + -1;
  } while (lVar14 != 0);
  uVar15 = uVar17;
  if (uVar20 != 0) {
    do {
      pHVar7 = GetDesktopWindow();
      IsWindow(pHVar7);
      pwVar12 = wcschr(local_388,*(wchar_t *)(param_1 + uVar15 * 2));
      if (pwVar12 != (wchar_t *)0x0) {
        local_670 = 0;
        lVar14 = 5;
        do {
          local_670 = local_670 + 1;
          lVar14 = lVar14 + -1;
        } while (lVar14 != 0);
        *(wchar_t *)(param_1 + uVar15 * 2) = local_2e8[(longlong)pwVar12 - (longlong)local_388 >> 1]
        ;
      }
      LVar5 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,&local_668)
      ;
      if (LVar5 == 0) {
        RegCloseKey(local_668);
      }
      uVar15 = uVar15 + 1;
    } while (uVar15 < uVar20);
  }
  pvVar11 = GetStockObject(4);
  GetObjectW(pvVar11,0x10,local_640);
  local_688[0] = 0x46;
  local_688[1] = 0x4c;
  local_670 = 0;
  do {
    local_670 = local_670 + 1;
    lVar18 = lVar18 + -1;
  } while (lVar18 != 0);
  local_688[2] = 0x41;
  local_688[3] = 0x52;
  local_688[4] = 0x45;
  local_688[5] = 0x52;
  pvVar11 = GetStockObject(4);
  GetObjectW(pvVar11,0x10,local_630);
  DVar3 = GetTickCount();
  local_670 = DVar3 % 100 + 5;
  SetLastError(local_670);
  local_688[6] = 0x41;
  local_688[7] = 0x4c;
  local_670 = GetSystemMetrics(0);
  local_688[8] = 0x46;
  local_688[9] = 0;
  pHVar8 = GetDC((HWND)0x0);
  pHVar9 = CreateCompatibleDC(pHVar8);
  pHVar10 = CreateCompatibleBitmap(pHVar8,1,1);
  DeleteObject(pHVar10);
  DeleteDC(pHVar9);
  ReleaseDC((HWND)0x0,pHVar8);
  do {
    uVar19 = uVar19 + 1;
  } while (local_688[uVar19] != 0);
  LVar5 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,&local_660);
  if (LVar5 == 0) {
    RegCloseKey(local_660);
  }
  uVar15 = uVar17;
  if (uVar20 != 0) {
    do {
      UVar6 = GetWindowsDirectoryW(local_248,0x104);
      if (UVar6 != 0) {
        wcscat_s(local_248,0x104,L"*.dll");
        pvVar13 = FindFirstFileW(local_248,&local_618);
        if (pvVar13 != (HANDLE)0xffffffffffffffff) {
          FindClose(pvVar13);
        }
      }
      puVar1 = (ushort *)(param_1 + uVar15 * 2);
      *puVar1 = *puVar1 ^ (short)uVar15 + local_688[uVar15 % uVar19];
      uVar15 = uVar15 + 1;
    } while (uVar15 < uVar20);
  }
  if (uVar20 >> 1 != 0) {
    puVar16 = (undefined2 *)(param_1 + -2 + uVar20 * 2);
    do {
      LVar5 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,&local_668)
      ;
      if (LVar5 == 0) {
        RegCloseKey(local_668);
      }
      uVar2 = *(undefined2 *)(param_1 + uVar17 * 2);
      UVar6 = GetWindowsDirectoryW(local_248,0x104);
      if (UVar6 != 0) {
        wcscat_s(local_248,0x104,L"*.dll");
        pvVar13 = FindFirstFileW(local_248,&local_618);
        if (pvVar13 != (HANDLE)0xffffffffffffffff) {
          FindClose(pvVar13);
        }
      }
      *(undefined2 *)(param_1 + uVar17 * 2) = *puVar16;
      *puVar16 = uVar2;
      LVar5 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,
                            (PHKEY)&local_670);
      if (LVar5 == 0) {
        RegCloseKey((HKEY)CONCAT44(uStack_66c,local_670));
      }
      uVar17 = uVar17 + 1;
      puVar16 = puVar16 + -1;
    } while (uVar17 < uVar20 >> 1);
  }
  FUN_140004510(local_38 ^ (ulonglong)auStackY_6b8);
  return;
}

```
Clear code i have   
```c
str1:
wcscpy_s(str_1,0x50,L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP");
wcscat_s(str_1,0x50,L"QRSTUVWXYZ0123456789}_{=-");
```
=>`str_1="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}_{=-"`
```c
str2:
wcscpy_s(str_2,0x50,L"-={_}9876543210ZYXWVUTSRQPONMLKJIHGF");
wcscat_s(str_2,0x50,L"EDCBAzyxwvutsrqponmlkjihgfedcba");
```
=>`str_2="-={_}9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba"`
```c
ulonglong len_input;
len_input = 0xffffffffffffffff;
do {
  len_input = len_input + 1;
} while (*(short *)(input + len_input * 2) != 0);
```
=> `len_input` will run from 0 to the end of index input => it will get len of input
```c
i_0 = 0; 
i = i_0;
if (len_input != 0) {
  do {
    addr_i_str1 = wcschr(str_1,*(wchar_t *)(input + i * 2));
    if (addr_i_str1 != (wchar_t *)0x0) {
      *(wchar_t *)(input + i * 2) = str_2[(longlong)addr_i_str1 - (longlong)str_1 >> 1];
    }
    i = i + 1;
  } while (i < len_input);
}
```
We run step by step with i = 0 :  
`addr_i_str1 = wcschr(str_1,*(wchar_t *)(input + 0 * 2 )); `  
=>wchar_t is 2 byte   
=> `(input + i * 2)` cover to `(wchar_t *) ` so that maybe like this `wchar_t * input[]; `  
=> `addr_i_str1 = wcschr(str_1,input[0]); `  
=> `wcschr` will return address of the first character of `str_1` match will `input[0]`

`*(wchar_t *)(input + 0 * 2)` = `str_2[(longlong)addr_i_str1 - (longlong)str_1 >> 1];`  
=> `addr_i_str1 - str_1 >>1 ` is  calculate offset of addr_i_str1 and /2 to find index of addr_i_str1   
=> `input[0] = str_2[index of char input[0] in str_1]`

***=>*** it will mapping each character of input to new character by find it index in `str_1` and replancing it with char in the same povision in `str_2`   

```c
short str_FLARE [12];
ushort *xor_input_FLARE;
len_FLARE = 0xffffffffffffffff;
i_0 = 0; 
str_FLARE[0] = 0x46;
str_FLARE[1] = 0x4c;
str_FLARE[2] = 0x41;
str_FLARE[3] = 0x52;
str_FLARE[4] = 0x45;
str_FLARE[5] = 0x52;
str_FLARE[6] = 0x41;
str_FLARE[7] = 0x4c;
str_FLARE[8] = 0x46;
str_FLARE[9] = 0;
do {
  len_FLARE = len_FLARE + 1;
} while (str_FLARE[len_FLARE] != 0);
i = i_0;
if (len_input != 0) {
  do {
      input_xor = (ushort *)(input + i * 2);
      *input_xor = *input_xor ^ (short)i + str_FLARE[i % len_FLARE];
      i = i + 1;
    } while (i < len_input);
}
```
=> `0x464c41524552414c46` <=> FLARERALF

We run step by step with i = 0 :  
`input_xor = (ushort *)(input + 0 * 2);`  
=> `(input + i * 2) conver to (ushort *)` <=>`ushort*  input[]`  
=> `input_xor  = &input[0]`   

`*input_xor = *input_xor ^ (short)0 + str_FLARE[0 % len_FLARE];`  
=> `*input_xor = input[0]`  
=> `(short)0` = 0 in logic    
=>` str_FLARE[0 % len_FLARE]` =`str_FLARE[0]`= `0x46`  
=>`*input_xor  = *input_xor ^ (0 +0x46)`  

**=>**  It xor each value of `input` with each value of `str_FLARE + i`  
```c
if (len_input >> 1 != 0) {
  last_input = (undefined2 *)(input + -2 + len_input * 2);
  do {
    input_2 = *(undefined2 *)(input + i_0 * 2);
    *(undefined2 *)(input + i_0 * 2) = *last_input;
    *last_input = input_2;
    i_0 = i_0 + 1;
    last_input = last_input + -1;
  } while (i_0 < len_input >> 1);
}
```
`last_input = (undefined2 *)(input + -2 + len_input * 2);`  
=>`last_input = &input[len_input -1];`  

`input_2 = *(undefined2 *)(input + i_0 * 2);`  
=>` input_2 = input[i_0];`  

`*(undefined2 *)(input + i_0 * 2) = *last_input;`  
=> `input[i_0] = input[len_input -1];`  

`*last_input = input_2;`  
=> `input[len_input -1] = input[i_0];`  

**=>** this code used to reverse input

Summary this function we have:  

```c
void handling_input(longlong input){
  -- mapping input to new input
  wcscpy_s(str_1,0x50,L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP");
  wcscat_s(str_1,0x50,L"QRSTUVWXYZ0123456789}_{=-");
  wcscpy_s(str_2,0x50,L"-={_}9876543210ZYXWVUTSRQPONMLKJIHGF");
  wcscat_s(str_2,0x50,L"EDCBAzyxwvutsrqponmlkjihgfedcba");
  ulonglong len_input;
  len_input = 0xffffffffffffffff;
  do {
    len_input = len_input + 1;
  } while (*(short *)(input + len_input * 2) != 0);
  i_0 = 0; 
  i = i_0;
  if (len_input != 0) {
    do {
      addr_i_str1 = wcschr(str_1,*(wchar_t *)(input + i * 2));
      if (addr_i_str1 != (wchar_t *)0x0) {
        *(wchar_t *)(input + i * 2) = str_2[(longlong)addr_i_str1 - (longlong)str_1 >> 1];
      }
      i = i + 1;
    } while (i < len_input);
  }
  --  xor input with str_FLARE + i
  short str_FLARE [12];
  ushort *xor_input_FLARE;
  len_FLARE = 0xffffffffffffffff;
  i_0 = 0; 
  str_FLARE[0] = 0x46;
  str_FLARE[1] = 0x4c;
  str_FLARE[2] = 0x41;
  str_FLARE[3] = 0x52;
  str_FLARE[4] = 0x45;
  str_FLARE[5] = 0x52;
  str_FLARE[6] = 0x41;
  str_FLARE[7] = 0x4c;
  str_FLARE[8] = 0x46;
  str_FLARE[9] = 0;
  do {
    len_FLARE = len_FLARE + 1;
  } while (str_FLARE[len_FLARE] != 0);
  i = i_0;
  if (len_input != 0) {
    do {
        input_xor = (ushort *)(input + i * 2);
        *input_xor = *input_xor ^ (short)i + str_FLARE[i % len_FLARE];
        i = i + 1;
      } while (i < len_input);
  }

  ---  Reverse input
  if (len_input >> 1 != 0) {
    last_input = (undefined2 *)(input + -2 + len_input * 2);
    do {
      input_2 = *(undefined2 *)(input + i_0 * 2);
      *(unefine2 *)(input + i_0 * 2) = *last_input;
      *last_input = input_2;
      i_0 = i_0 + 1;
      last_input = last_input + -1;
    } while (i_0 < len_input >> 1);
  }
}
```

<p align = "center" style = "color:#4A90E2"> Symbol table </p>

I check Symbol table, pass func of GDI because GDI is handle Graphics and i discover func suspect:    
![symbol-table-wcsncmp](images/symbol-table-wcsncmp.png)
wcsncmp  
=> Lib: API-MS-WIN-CRT-STRING-L1-1-0.DLL	  
=> Reference count 7  
=> I think it function is use to check some things  

Check Symbol references of wcsncmp we found:  
![symbol-ref-wcsncmp](images/symbol-ref-wcsncmp.png)
```c
void handle_command_line_argv(HINSTANCE param_1,undefined8 param_2,wchar_t *argv,int param_4)
{
  bool bVar1;
  bool bVar2;
  DWORD DVar3;
  int iVar4;
  UINT UVar5;
  ulong uVar6;
  LSTATUS LVar7;
  int iVar8;
  BOOL BVar9;
  HWND pHVar10;
  ulonglong uVar11;
  HANDLE hFindFile;
  HGDIOBJ pvVar12;
  HACCEL hAccTable;
  HDC pHVar13;
  HDC pHVar14;
  HBITMAP pHVar15;
  longlong lVar16;
  longlong lVar17;
  HWND pHVar18;
  int iVar19;
  undefined1 auStackY_588 [32];
  HKEY local_558;
  tagMSG local_550;
  DWORD local_520 [2];
  undefined1 local_518 [16];
  undefined1 local_508 [16];
  undefined1 local_4f8 [16];
  _WIN32_FIND_DATAW local_4e8;
  WCHAR local_298 [32];
  WCHAR local_258 [264];
  ulonglong local_48;
  
  local_48 = DAT_140008000 ^ (ulonglong)auStackY_588;
  local_520[0] = GetSystemMetrics(2);
  if (0 < (int)local_520[0]) {
    local_520[0] = local_520[0] + 1;
  }
  pHVar10 = GetDesktopWindow();
  IsWindow(pHVar10);
  iVar8 = 0;
  iVar19 = 0;
  DVar3 = GetTickCount();
  local_520[0] = DVar3 % 100 + 5;
  SetLastError(local_520[0]);
  bVar2 = false;
  DVar3 = GetTickCount();
  local_520[0] = DVar3 % 100 + 5;
  SetLastError(local_520[0]);
  pHVar10 = (HWND)0x0;
  pHVar18 = (HWND)0x0;
  DVar3 = GetTickCount();
  local_520[0] = DVar3 % 100 + 5;
  SetLastError(local_520[0]);
  lVar17 = 5;
  bVar1 = false;
  if (argv != (wchar_t *)0x0) {
    uVar11 = 0xffffffffffffffff;
    do {
      uVar11 = uVar11 + 1;
    } while (argv[uVar11] != L'\0');
    bVar1 = bVar2;
    if (1 < uVar11) {
      iVar4 = wcsncmp(argv,L"/c",2);
      if ((iVar4 == 0) || (iVar4 = wcsncmp(argv,L"-c",2), iVar4 == 0)) {
        local_520[0] = 0x20;
        GetComputerNameW(local_298,local_520);
        bVar1 = true;
        pHVar10 = pHVar18;
        iVar8 = iVar19;
      }
      else {
        iVar4 = wcsncmp(argv,L"/p",2);
        if ((iVar4 == 0) || (iVar4 = wcsncmp(argv,L"-p",2), iVar4 == 0)) {
          pHVar13 = GetDC((HWND)0x0);
          pHVar14 = CreateCompatibleDC(pHVar13);
          pHVar15 = CreateCompatibleBitmap(pHVar13,1,1);
          DeleteObject(pHVar15);
          DeleteDC(pHVar14);
          ReleaseDC((HWND)0x0,pHVar13);
          uVar6 = wcstoul(argv + 3,(wchar_t **)0x0,10);
          lVar16 = 5;
          do {
            lVar16 = lVar16 + -1;
          } while (lVar16 != 0);
          param_4 = 4;
          pHVar10 = (HWND)(ulonglong)uVar6;
          iVar8 = 1;
        }
        else {
          iVar4 = wcsncmp(argv,L"/s",2);
          if ((iVar4 == 0) || (iVar4 = wcsncmp(argv,L"-s",2), iVar4 == 0)) {
            param_4 = 3;
            local_520[0] = GetSystemMetrics(0);
            DAT_140008980 = 1;
            UVar5 = GetWindowsDirectoryW(local_258,0x104);
            pHVar10 = pHVar18;
            iVar8 = iVar19;
            if (UVar5 != 0) {
              wcscat_s(local_258,0x104,L"*.dll");
              hFindFile = FindFirstFileW(local_258,&local_4e8);
              if (hFindFile != (HANDLE)0xffffffffffffffff) {
                FindClose(hFindFile);
              }
            }
          }
        }
      }
    }
  }
  local_520[0] = 0;
  lVar16 = 5;
  do {
    local_520[0] = local_520[0] + 1;
    lVar16 = lVar16 + -1;
  } while (lVar16 != 0);
  LoadStringW(param_1,0x67,(LPWSTR)&DAT_1400089b0,100);
  LVar7 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,&local_558);
  if (LVar7 == 0) {
    RegCloseKey(local_558);
  }
  LoadStringW(param_1,0x6d,(LPWSTR)&DAT_1400088a0,100);
  pvVar12 = GetStockObject(4);
  GetObjectW(pvVar12,0x10,local_518);
  FUN_140002950(param_1);
  lVar16 = 5;
  local_520[0] = 0;
  do {
    local_520[0] = local_520[0] + 1;
    lVar16 = lVar16 + -1;
  } while (lVar16 != 0);
  iVar8 = FUN_140002bf0(param_1,param_4,iVar8,pHVar10);
  if (iVar8 == 0) {
    local_520[0] = 0x20;
    BVar9 = GetComputerNameW(local_298,local_520);
    if (BVar9 != 0) {
      local_520[0] = (DWORD)(ushort)local_298[0];
    }
  }
  else if (bVar1) {
    DVar3 = GetTickCount();
    local_520[0] = DVar3 % 100 + 5;
    SetLastError(local_520[0]);
    DialogBoxParamW(param_1,(LPCWSTR)0x82,(HWND)0x0,FUN_140001f30,0);
    local_520[0] = 0;
    do {
      local_520[0] = local_520[0] + 1;
      lVar17 = lVar17 + -1;
    } while (lVar17 != 0);
  }
  else {
    hAccTable = LoadAcceleratorsW(param_1,(LPCWSTR)0x6d);
    pHVar10 = GetDesktopWindow();
    IsWindow(pHVar10);
    iVar8 = GetMessageW(&local_550,(HWND)0x0,0,0);
    while (iVar8 != 0) {
      pvVar12 = GetStockObject(4);
      GetObjectW(pvVar12,0x10,local_508);
      iVar8 = TranslateAcceleratorW(local_550.hwnd,hAccTable,&local_550);
      if (iVar8 == 0) {
        pvVar12 = GetStockObject(4);
        GetObjectW(pvVar12,0x10,local_4f8);
        TranslateMessage(&local_550);
        pHVar13 = GetDC((HWND)0x0);
        pHVar14 = CreateCompatibleDC(pHVar13);
        pHVar15 = CreateCompatibleBitmap(pHVar13,1,1);
        DeleteObject(pHVar15);
        DeleteDC(pHVar14);
        ReleaseDC((HWND)0x0,pHVar13);
        DispatchMessageW(&local_550);
      }
      iVar8 = GetMessageW(&local_550,(HWND)0x0,0,0);
    }
    pHVar10 = GetDesktopWindow();
    IsWindow(pHVar10);
  }
  FUN_140004510(local_48 ^ (ulonglong)auStackY_588);
  return;
}

```
clear jurk code we have 
```c
void handle_command_line_argv(HINSTANCE param_1,undefined8 param_2,wchar_t *argv,int param_4){
  local_48 = DAT_140008000 ^ (ulonglong)auStackY_588;
  v_false = false;
  check = false;
  if (argv != (wchar_t *)0x0) {
    i = 0xffffffffffffffff;
    do {
      i = i + 1;
    } while (argv[i] != L'\0');
    if (1 < i) {
      r_cmp = wcsncmp(argv,L"/c",2);
      if ((r_cmp == 0) || (r_cmp = wcsncmp(argv,L"-c",2), r_cmp == 0)) {
        check = true;
      }
      else {
        r_cmp = wcsncmp(argv,L"/p",2);
        if ((r_cmp == 0) || (r_cmp = wcsncmp(argv,L"-p",2), r_cmp == 0)) {
          uVar3 = wcstoul(argv + 3,(wchar_t **)0x0,10);
        }
        else {
          r_cmp = wcsncmp(argv,L"/s",2);
          if ((r_cmp == 0) || (r_cmp = wcsncmp(argv,L"-s",2), r_cmp == 0)) {
            param_4 = 3;
            DAT_140008980 = 1;
          }
        }
      }
    }
  }

  else if (check) {
    DialogBoxParamW(param_1,(LPCWSTR)0x82,(HWND)0x0,handle_box_c,0);
  }
  else {}
  check_something(local_48 ^ (ulonglong)auStackY_588);
  return;
}
```
=> It handling argv from command line because it have cmp with L"/c", L"/p", L"/s"  
=> after test  L"/c", L"/p", L"/s" we see /c have something so we will go deep in how it handle /c  

Flow it we have  
```c
r_cmp = wcsncmp(argv,L"/c",2);
if ((r_cmp == 0) || (r_cmp = wcsncmp(argv,L"-c",2), r_cmp == 0)) {
  check = true;
}
  else if (check) {
    DialogBoxParamW(param_1,(LPCWSTR)0x82,(HWND)0x0,handle_box_c,0);
  }
```
check FUN_140001f30 we found  
```c
void handle_box_c(HWND param_1,int param_2,short param_3)
{
  short *psVar1;
  BOOL BVar2;
  LSTATUS LVar3;
  UINT UVar4;
  DWORD DVar5;
  HDC pHVar6;
  HDC pHVar7;
  HBITMAP pHVar8;
  HANDLE hFindFile;
  longlong lVar9;
  HGDIOBJ h;
  HWND pHVar10;
  ulonglong uVar11;
  undefined1 auStackY_958 [32];
  HKEY local_900;
  undefined8 local_8f8;
  DWORD local_8f0 [2];
  undefined1 local_8e8 [16];
  _WIN32_FIND_DATAW local_8d8;
  WCHAR local_688 [32];
  WCHAR local_648;
  short asStack_646 [255];
  WCHAR local_448 [264];
  WCHAR local_238 [256];
  ulonglong local_38;
  
  local_38 = DAT_140008000 ^ (ulonglong)auStackY_958;
  local_8f0[0] = 0x100;
  BVar2 = GetComputerNameW(local_238,local_8f0);
  if ((BVar2 != 0) && (local_8f0[0] != 0)) {
    uVar11 = (ulonglong)local_8f0[0];
    do {
      uVar11 = uVar11 - 1;
    } while (uVar11 != 0);
  }
  pHVar6 = GetDC((HWND)0x0);
  pHVar7 = CreateCompatibleDC(pHVar6);
  pHVar8 = CreateCompatibleBitmap(pHVar6,1,1);
  DeleteObject(pHVar8);
  DeleteDC(pHVar7);
  ReleaseDC((HWND)0x0,pHVar6);
  if (param_2 == 0x110) {
    FUN_140001ae0(&local_648);
    SetDlgItemTextW(param_1,0x3e9,&local_648);
  }
  else if (param_2 == 0x111) {
    if (param_3 == 1) {
      GetDlgItemTextW(param_1,0x3e9,&local_648,0x100);
      GetSystemMetrics(0);
      pHVar6 = GetDC((HWND)0x0);
      pHVar7 = CreateCompatibleDC(pHVar6);
      pHVar8 = CreateCompatibleBitmap(pHVar6,1,1);
      DeleteObject(pHVar8);
      DeleteDC(pHVar7);
      ReleaseDC((HWND)0x0,pHVar6);
      local_8f8._0_4_ = GetSystemMetrics(0);
      LVar3 = RegCreateKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,(LPWSTR)0x0,0,
                              0x20006,(LPSECURITY_ATTRIBUTES)0x0,&local_900,(LPDWORD)0x0);
      if (LVar3 == 0) {
        local_8f8._0_4_ = 0x20;
        GetComputerNameW(local_688,(LPDWORD)&local_8f8);
        UVar4 = GetWindowsDirectoryW(local_448,0x104);
        if (UVar4 != 0) {
          wcscat_s(local_448,0x104,L"*.dll");
          hFindFile = FindFirstFileW(local_448,&local_8d8);
          if (hFindFile != (HANDLE)0xffffffffffffffff) {
            FindClose(hFindFile);
          }
        }
        lVar9 = -1;
        do {
          psVar1 = asStack_646 + lVar9;
          lVar9 = lVar9 + 1;
        } while (*psVar1 != 0);
        RegSetValueExW(local_900,L"Text",0,1,(BYTE *)&local_648,(int)lVar9 * 2 + 2);
        DVar5 = GetTickCount();
        SetLastError(DVar5 % 100 + 5);
        RegCloseKey(local_900);
      }
      h = GetStockObject(4);
      GetObjectW(h,0x10,local_8e8);
      LVar3 = RegCreateKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,(LPWSTR)0x0,0,
                              0x20006,(LPSECURITY_ATTRIBUTES)0x0,&local_900,(LPDWORD)0x0);
      if (LVar3 == 0) {
        LVar3 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,
                              (PHKEY)&local_8f8);
        if (LVar3 == 0) {
          RegCloseKey((HKEY)CONCAT44(local_8f8._4_4_,(DWORD)local_8f8));
        }
        pHVar10 = GetDesktopWindow();
        IsWindow(pHVar10);
        RegSetValueExW(local_900,L"Quak",0,1,"<",0x34);
        pHVar10 = GetDesktopWindow();
        IsWindow(pHVar10);
        RegCloseKey(local_900);
      }
      EndDialog(param_1,1);
    }
    else if (param_3 == 2) {
      EndDialog(param_1,2);
    }
  }
  FUN_140004510(local_38 ^ (ulonglong)auStackY_958);
  return;
}


```

=> it is handle dialog when user use /c  

i clean up jurk code and rename value i have:  
```c
void handle_box_c(HWND param_1,int param_2,short param_3)
{
  if (param_2 == 0x110) {
    set_default_value_in(&input_field);
    SetDlgItemTextW(param_1,0x3e9,&input_field);
  }
  else if (param_2 == 0x111){
    #Button OK
    if (button == 1 ){
      GetDlgItemTextW(param_1,0x3e9,&input_field,0x100);

      regkey = RegCreateKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,(LPWSTR)0x0,0,0x20006,(LPSECURITY_ATTRIBUTES)0x0,&local_900,(LPDWORD)0x0);
       if (regkey == 0) {
        lVar8 = -1;
        do {
          psVar1 = asStack_646 + lVar8;
          lVar8 = lVar8 + 1;
        } while (*psVar1 != 0);
        RegSetValueExW(local_900,L"Text",0,1,(BYTE *)&input_field,(int)lVar8 * 2 + 2);
        RegCloseKey(local_900);
      }

      regkey = RegCreateKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,(LPWSTR)0x0,0, 0x20006,(LPSECURITY_ATTRIBUTES)0x0,&local_900,(LPDWORD)0x0);
      if (regkey == 0) {
        regkey = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,(PHKEY)&local_8f8);
        if (regkey == 0)  RegCloseKey((HKEY)CONCAT44(local_8f8._4_4_,(DWORD)local_8f8));
        RegSetValueExW(local_900,L"Quak",0,1,"<",0x34);
        RegCloseKey(local_900);
     }
    EndDialog(param_1,1);
    }
    #Button out
    else if (button == 2) {
      EndDialog(param_1,2);
    } 
  }
  ......
}

```
I identified several core functions:

SetDlgItemTextW  
```c
BOOL SetDlgItemTextW(
  [in] HWND    hDlg,
  [in] int     nIDDlgItem,
  [in] LPCWSTR lpString
);
```
=> set new value   

RegCreateKeyExW  
```c
LSTATUS RegCreateKeyExW(
  [in]            HKEY                        hKey,
  [in]            LPCWSTR                     lpSubKey,
                  DWORD                       Reserved,
  [in, optional]  LPWSTR                      lpClass,
  [in]            DWORD                       dwOptions,
  [in]            REGSAM                      samDesired,
  [in, optional]  const LPSECURITY_ATTRIBUTES lpSecurityAttributes,
  [out]           PHKEY                       phkResult,
  [out, optional] LPDWORD                     lpdwDisposition
);
```
=> create if not exists or open registry key  

RegSetValueExW      
```c
LSTATUS RegSetValueExW(
  [in]           HKEY       hKey, 
  [in, optional] LPCWSTR    lpValueName, # Value name
                 DWORD      Reserved,
  [in]           DWORD      dwType,
  [in]           const BYTE *lpData,
  [in]           DWORD      cbData
);
```

=> use to write or read value    

And we have:  
`RegCreateKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,(LPWSTR)0x0,0, 0x20006,(LPSECURITY_ATTRIBUTES)0x0,&local_900,(LPDWORD)0x0);`  
=> open hkey user ...\Software\\FLRSCRNSVR if it have will return 0  

`RegSetValueExW(local_900,L"Text",0,1,(BYTE *)&input_field,(int)lVar8 * 2 + 2);`  
=>  Value Name is Text  
=> Value data is in (BYTE *) &input_field  
=> Value size is (int)lVar8 * 2 + 2 => to much large  
=> Write value input + dump data to value Text  

`RegSetValueExW(local_900,L"Quak",0,1,"<",0x34);`  
=>  Value Name is Quak  
=> Value data is in "<"  
=> Value size is 0x34 => 52  

i traced Quak found : 
```c
3c 00 51 00 6a 00 09 00 02 00 07 00 25 00 03 00 30 00 08 00 04 00 29 00 68 00 24 00 01 00 24 00 18 00 6b 00 77 00 0f 00 70 00 36 00 02 00 0e 00 0b 00 00 00 
```
=> Value size is 0x34 => 52 / 2 = 26 digit  

We have `WM_INITDIALOG `message is:  
```c
#define WM_INITDIALOG                   0x0110
```
=> send to dialog box before a dialog => use to initialize  
So 0x0110 is WM_INITDIALOG:  

```c
if (param_2 == 0x110) {
  set_default_value_in(&input_field);
  SetDlgItemTextW(param_1,0x3e9,&input_field);
}
```
we focus Analyse function `set_default_value_in`  

Origin function
```c
void set_default_value_in(wchar_t *param_1)
{
  wchar_t wVar1;
  wchar_t wVar2;
  LSTATUS LVar3;
  int iVar4;
  UINT UVar5;
  HDC pHVar6;
  HDC pHVar7;
  HBITMAP pHVar8;
  HANDLE hFindFile;
  HWND pHVar9;
  size_t sVar10;
  longlong lVar11;
  wchar_t *pwVar12;
  HGDIOBJ h;
  longlong lVar13;
  undefined1 auStackY_af8 [32];
  undefined8 local_ac0;
  HKEY local_ab8;
  HKEY local_ab0;
  DWORD local_aa8 [2];
  LARGE_INTEGER local_aa0 [3];
  _WIN32_FIND_DATAW local_a88;
  wchar_t local_838 [256];
  WCHAR local_638 [264];
  wchar_t local_428 [256];
  BYTE local_228 [512];
  ulonglong local_28;
  
  local_28 = DAT_140008000 ^ (ulonglong)auStackY_af8;
  local_aa8[1] = 0x200;
  LVar3 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,&local_ab8);
  if (LVar3 == 0) {
    LVar3 = RegQueryValueExW(local_ab8,L"Wallpaper",(LPDWORD)0x0,(LPDWORD)0x0,local_228,
                             local_aa8 + 1);
    if (LVar3 == 0) {
      local_ac0._0_4_ = 1;
    }
    RegCloseKey(local_ab8);
  }
  pHVar6 = GetDC((HWND)0x0);
  pHVar7 = CreateCompatibleDC(pHVar6);
  pHVar8 = CreateCompatibleBitmap(pHVar6,1,1);
  DeleteObject(pHVar8);
  DeleteDC(pHVar7);
  ReleaseDC((HWND)0x0,pHVar6);
  LVar3 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,0x20019,&local_ab0);
  lVar13 = 5;
  if (LVar3 == 0) {
    QueryPerformanceCounter(local_aa0);
    iVar4 = FUN_140001010();
    local_ac0._0_4_ = iVar4 + 1;
    GetSystemMetrics(0);
    local_aa8[0] = 0x200;
    UVar5 = GetWindowsDirectoryW(local_638,0x104);
    if (UVar5 != 0) {
      wcscat_s(local_638,0x104,L"*.dll");
      hFindFile = FindFirstFileW(local_638,&local_a88);
      if (hFindFile != (HANDLE)0xffffffffffffffff) {
        FindClose(hFindFile);
      }
    }
    LVar3 = RegQueryValueExW(local_ab0,L"Text",(LPDWORD)0x0,(LPDWORD)&local_ac0,(LPBYTE)param_1,
                             local_aa8);
    if (LVar3 == 0) {
      lVar11 = 5;
      do {
        lVar11 = lVar11 + -1;
      } while (lVar11 != 0);
      sVar10 = wcsnlen(param_1,0x100);
      if (sVar10 == 0) {
        wcscpy_s(param_1,0x100,L"Crackmes.one");
      }
    }
    else {
      pHVar9 = GetDesktopWindow();
      IsWindow(pHVar9);
      wcscpy_s(param_1,0x100,L"Crackmes.one");
      pHVar6 = GetDC((HWND)0x0);
      pHVar7 = CreateCompatibleDC(pHVar6);
      pHVar8 = CreateCompatibleBitmap(pHVar6,1,1);
      DeleteObject(pHVar8);
      DeleteDC(pHVar7);
      ReleaseDC((HWND)0x0,pHVar6);
    }
    GetSystemMetrics(0);
    RegCloseKey(local_ab0);
  }
  else {
    wcscpy_s(param_1,0x100,L"Crackmes.one");
  }
  lVar11 = -1;
  do {
    lVar11 = lVar11 + 1;
  } while (param_1[lVar11] != L'\0');
  if (lVar11 == 0x19) {
    lVar11 = 5;
    do {
      lVar11 = lVar11 + -1;
    } while (lVar11 != 0);
    wcscpy_s(local_838,0x100,param_1);
    local_ac0._0_4_ = GetSystemMetrics(0);
    handling_input((longlong)local_838);
    pHVar9 = GetDesktopWindow();
    IsWindow(pHVar9);
    FUN_140001890(local_428);
    local_ac0._0_4_ = GetSystemMetrics(0);
    do {
      lVar13 = lVar13 + -1;
    } while (lVar13 != 0);
    pwVar12 = local_838;
    lVar13 = (longlong)local_428 - (longlong)pwVar12;
    do {
      wVar1 = *pwVar12;
      wVar2 = *(wchar_t *)((longlong)pwVar12 + lVar13);
      if (wVar1 != wVar2) break;
      pwVar12 = pwVar12 + 1;
    } while (wVar2 != L'\0');
    if (wVar1 == wVar2) {
      h = GetStockObject(4);
      GetObjectW(h,0x10,local_aa0);
      DAT_140008898 = 1;
    }
    else {
      pHVar6 = GetDC((HWND)0x0);
      pHVar7 = CreateCompatibleDC(pHVar6);
      pHVar8 = CreateCompatibleBitmap(pHVar6,1,1);
      DeleteObject(pHVar8);
      DeleteDC(pHVar7);
      ReleaseDC((HWND)0x0,pHVar6);
    }
  }
  else {
    LVar3 = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019,
                          (PHKEY)&local_ac0);
    if (LVar3 == 0) {
      RegCloseKey((HKEY)CONCAT44(local_ac0._4_4_,(DWORD)local_ac0));
    }
  }
  FUN_140004510(local_28 ^ (ulonglong)auStackY_af8);
  return;
}
```

Function after clear  

```c
void set_default_value_in(wchar_t *input)

{
   LSTATUS status_key;
  HGDIOBJ h;
  undefined1 auStackY_af8 [32];
  undefined8 tmp_junk;
  HKEY key_handle;
  DWORD buffer_size [2];

  size_t len_input;
  longlong i;
  longlong offset;
  wchar_t *input_after_handle;
  wchar_t str_input [256];
  wchar_t quak_value [256];
  wchar_t wchar_1;
  wchar_t wchar_2;
  
  local_28 = DAT_140008000 ^ (ulonglong)auStackY_af8;
  status_key = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,0x20019,&key_handle);
  if (status_key == 0) {
    value_text[0] = 0x200;
    status_key = RegQueryValueExW(key_handle, L"Text", (LPDWORD)0x0, (LPDWORD)&tmp_junk,(LPBYTE)input, buffer_size);
    if (status_key == 0) {
      len_input = wcsnlen(input,0x100);
      if (len_input == 0)  wcscpy_s(input,0x100,L"Crackmes.one");
    }
    else  wcscpy_s(input,0x100,L"Crackmes.one");
    RegCloseKey(key_handle);
  }
  else {
    wcscpy_s(input,0x100,L"Crackmes.one");
  }

  i = -1;
  do {
    i = i + 1;
  } while (input[i] != L'\0');
  if (i == 0x19) {
    wcscpy_s(str_input,0x100,input);
    handling_input((longlong)str_input);
    create_value(quak_value);
    input_after_handle = str_input;
    offset = (longlong)quak_value - (longlong)input_after_handle;

    do {
      wchar_1 = *input_after_handle;
      wchar_2 = *(wchar_t *)((longlong)input_after_handle + offset);
      if (wchar_1 != wchar_2) break;
      input_after_handle = input_after_handle + 1;
    } while (wchar_2 != L'\0');
    
    if (wchar_1 == wchar_2) {
      h = GetStockObject(4);
      GetObjectW(h,0x10,local_aa0);
      DAT_140008898 = 1;
    }
    else {}
  }
  else {
    status_key = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Control Panel\\Desktop",0,0x20019, (PHKEY)&tmp_junk);
    if (status_key == 0) RegCloseKey((HKEY)CONCAT44(tmp_junk._4_4_,(DWORD)tmp_junk));
  }
  check_something(local_28 ^ (ulonglong)auStackY_af8);
  return;
}
```

We have:

```c
LSTATUS RegQueryValueExW(
  [in]                HKEY    hKey,
  [in, optional]      LPCWSTR lpValueName,
                      LPDWORD lpReserved,
  [out, optional]     LPDWORD lpType,
  [out, optional]     LPBYTE  lpData,
  [in, out, optional] LPDWORD lpcbData
);
```
=> RegQueryValueExW use to get data, type  by specified value name  
```c
tatus_key = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,0x20019,&key_handle);
  if (status_key == 0) {
    value_text[0] = 0x200;
    status_key = RegQueryValueExW(key_handle, L"Text", (LPDWORD)0x0, (LPDWORD)&tmp_junk,(LPBYTE)input, buffer_size);
    if (status_key == 0) {
      len_input = wcsnlen(input,0x100);
      if (len_input == 0)  wcscpy_s(input,0x100,L"Crackmes.one");
    }
    else  wcscpy_s(input,0x100,L"Crackmes.one");
    RegCloseKey(key_handle);
  }
  else {
    wcscpy_s(input,0x100,L"Crackmes.one");
  }
```
- Open key `HKEY_CURRENT_USER\Software\\FLRSCRNSVR` if have return 0 if it have  
- next is open `Text Value` and store in `input`  
- if `status_key of RegOpenKeyExW != 0` or `status_key of RegQueryValueExW != 0` or `len (input) == 0` will set `input = L"Crackmes.one"`  
=> So we input will replace by Text Value <=> `input` = `Text Value data`  
```c
 i = -1;
  do {
    i = i + 1;
  } while (input[i] != L'\0');
  if (i == 0x19)
  {
    .....
  }
```
=>  0x19 = 25 decimal  
=> i will start from 0 to 25 =>  `input[i] != L'\0` will stop so `input[25] == L'\0`  
=> So input will have 25 element  
```c
 if (i == 0x19) {
    wcscpy_s(str_input,0x100,input);
    handling_input((longlong)str_input);
    create_value(quak_value);
    input_after_handle = str_input;
    offset = (longlong)quak_value - (longlong)input_after_handle;
    do {
      wchar_1 = *input_after_handle;
      wchar_2 = *(wchar_t *)((longlong)input_after_handle + offset);
      if (wchar_1 != wchar_2) break;
      input_after_handle = input_after_handle + 1;
    } while (wchar_2 != L'\0');
    
    if (wchar_1 == wchar_2) {
      h = GetStockObject(4);
      GetObjectW(h,0x10,local_aa0);
      DAT_140008898 = 1;
    }
    else {}
  }
```
- Copy `input` to variable `str_input`  
- And use function `handling_input` to handle `str_input`    
- And use function `create_value` to create value `quak_value`  
```c
void create_value(wchar_t *quak_value)
{
  local_10 = DAT_140008000 ^ (ulonglong)auStackY_58;
  status = RegOpenKeyExW((HKEY)0xffffffff80000001,L"Software\\FLRSCRNSVR",0,0x20019,&local_20);
  if (status == 0) {
    local_14 = 1;
    size = 0x200;
    status = RegQueryValueExW(local_20,L"Quak",(LPDWORD)0x0,&local_14,(LPBYTE)quak_value,&size);
    if (status == 0) {}
    else {
      wcscpy_s(quak_value,0x100,L"<Qj\t\x02\a%\x030\b\x04)h$\x01$\x18kw\x0fp6\x02\x0e\v");
    }
    RegCloseKey(local_20);
  }
  else {
    wcscpy_s(quak_value,0x100,u_Crackmes.one_140008080);
  }
  check_something(local_10 ^ (ulonglong)auStackY_58);
  return;
}
```
=> It open `Quak Value` and store in `quak_value`  
=> if open false will set `quak_value` = `<Qj\t\x02\a%\x030\b\x04)h$\x01$\x18kw\x0fp6\x02\x0e\v`  
=> check `<Qj\t\x02\a%\x030\b\x04)h$\x01$\x18kw\x0fp6\x02\x0e\v` we found  
`3c 00 51 00 6a 00 09 00 02 00 07 00 25 00 03 00 30 00 08 00 04 00 29 00 68 00 24 00 01 00 24 00 18 00 6b 00 77 00 0f 00 70 00 36 00 02 00 0e 00 0b 00 00 00 `  
=> So `<Qj\t\x02\a%\x030\b\x04)h$\x01$\x18kw\x0fp6\x02\x0e\v ` is the `Quak Value`  

```c
input_after_handle = str_input;
offset = (longlong)quak_value - (longlong)input_after_handle;
do {
  wchar_1 = *input_after_handle; 
  wchar_2 = *(wchar_t *)((longlong)input_after_handle + offset);
  if (wchar_1 != wchar_2) break;
  input_after_handle = input_after_handle + 1;
} while (wchar_2 != L'\0');

if (wchar_1 == wchar_2) {
  h = GetStockObject(4);
  GetObjectW(h,0x10,local_aa0);
  DAT_140008898 = 1;
}
else {}
```
=> It store `str_input` in `input_after_handle`  
=> Calculate offset   
```c
  wchar_1 = input_after_handle[0]
  wchar_2 = *(wchar_t *)(input_after_handle + offset); = quak_value[0]
```
<=>
```c
i = 0
do {
  wchar_1 = input_after_handle[i]
  wchar_2 = quak_value[i]
  if (wchar_1 != wchar_2) break;
  i = i + 1;
} while (wchar_2 != L'\0');
```
<p align = "center" style = "color:red">Summary of flow we found </p>

![database](images/FLRSCRNSVR.png)

=> So we will reverse `Quak value` with funtion `handling_input` reverse  
Code python reverse Quak value   
```python
import struct 

#Variable 
quak = "3c 00 51 00 6a 00 09 00 02 00 07 00 25 00 03 00 30 00 08 00 04 00 29 00 68 00 24 00 01 00 24 00 18 00 6b 00 77 00 0f 00 70 00 36 00 02 00 0e 00 0b 00 "
quak_b = bytes.fromhex(quak)
flare_b = bytes.fromhex("464c41524552414c46")
str1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}_{=-"
str2 = "-={_}9876543210ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba"
map_str = dict(zip(str2, str1))

#Handle quak byte to ushort
quak_short = struct.unpack("<25H", quak_b)

#Reverse quak short
re_quak = quak_short[::-1]

# XOR Short quak with  FLARE
xor_quak = []
for i in range(len(re_quak)):
    xor_quak.append( re_quak[i] ^ i + flare_b[i % len(flare_b)])

# Mapping str2 to str1
flag = ""
for i in xor_quak:
    flag += map_str[chr(i)]

print(f"Quak value {quak} \n ")
print(f"Short Quak {quak_short} \n ")
print(f"Reverse ushort Quak {re_quak} \n ")
print(f"Flare {flare_b} len = {len(flare_b)} \n")
print(f"Quak xor Flare {xor_quak}\n" )
print(f"Text Value =  {flag}")
```
Result   
```c 
Quak value 3c 00 51 00 6a 00 09 00 02 00 07 00 25 00 03 00 30 00 08 00 04 00 29 00 68 00 24 00 01 00 24 00 18 00 6b 00 77 00 0f 00 70 00 36 00 02 00 0e 00 0b 00  
 
Short Quak (60, 81, 106, 9, 2, 7, 37, 3, 48, 8, 4, 41, 104, 36, 1, 36, 24, 107, 119, 15, 112, 54, 2, 14, 11) 
 
Reverse ushort Quak (11, 14, 2, 54, 112, 15, 119, 107, 24, 36, 1, 36, 104, 41, 4, 8, 48, 3, 37, 7, 2, 9, 106, 81, 60) 
 
Flare b'FLARERALF' len = 9 

Quak xor Flare [77, 67, 65, 99, 57, 88, 48, 56, 86, 107, 87, 104, 54, 123, 100, 88, 108, 84, 125, 88, 87, 110, 49, 56,101]

Text Value =  CMO{frogt4s7ic_r3vers1ng}
```

