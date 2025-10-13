
/workspace/scanner_files/pwn_scanner/scanner:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	48 83 ec 08          	sub    rsp,0x8
    1004:	48 8b 05 4d 22 00 00 	mov    rax,QWORD PTR [rip+0x224d]        # 3258 <__gmon_start__@Base>
    100b:	48 85 c0             	test   rax,rax
    100e:	74 02                	je     1012 <_init+0x12>
    1010:	ff d0                	call   rax
    1012:	48 83 c4 08          	add    rsp,0x8
    1016:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <free@plt-0x10>:
    1020:	ff 35 e2 2f 00 00    	push   QWORD PTR [rip+0x2fe2]        # 4008 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 e4 2f 00 00    	jmp    QWORD PTR [rip+0x2fe4]        # 4010 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000001030 <free@plt>:
    1030:	ff 25 e2 2f 00 00    	jmp    QWORD PTR [rip+0x2fe2]        # 4018 <free@GLIBC_2.2.5>
    1036:	68 00 00 00 00       	push   0x0
    103b:	e9 e0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001040 <strncmp@plt>:
    1040:	ff 25 da 2f 00 00    	jmp    QWORD PTR [rip+0x2fda]        # 4020 <strncmp@GLIBC_2.2.5>
    1046:	68 01 00 00 00       	push   0x1
    104b:	e9 d0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001050 <puts@plt>:
    1050:	ff 25 d2 2f 00 00    	jmp    QWORD PTR [rip+0x2fd2]        # 4028 <puts@GLIBC_2.2.5>
    1056:	68 02 00 00 00       	push   0x2
    105b:	e9 c0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001060 <fread@plt>:
    1060:	ff 25 ca 2f 00 00    	jmp    QWORD PTR [rip+0x2fca]        # 4030 <fread@GLIBC_2.2.5>
    1066:	68 03 00 00 00       	push   0x3
    106b:	e9 b0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001070 <clock@plt>:
    1070:	ff 25 c2 2f 00 00    	jmp    QWORD PTR [rip+0x2fc2]        # 4038 <clock@GLIBC_2.2.5>
    1076:	68 04 00 00 00       	push   0x4
    107b:	e9 a0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001080 <printf@plt>:
    1080:	ff 25 ba 2f 00 00    	jmp    QWORD PTR [rip+0x2fba]        # 4040 <printf@GLIBC_2.2.5>
    1086:	68 05 00 00 00       	push   0x5
    108b:	e9 90 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001090 <memset@plt>:
    1090:	ff 25 b2 2f 00 00    	jmp    QWORD PTR [rip+0x2fb2]        # 4048 <memset@GLIBC_2.2.5>
    1096:	68 06 00 00 00       	push   0x6
    109b:	e9 80 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010a0 <memcmp@plt>:
    10a0:	ff 25 aa 2f 00 00    	jmp    QWORD PTR [rip+0x2faa]        # 4050 <memcmp@GLIBC_2.2.5>
    10a6:	68 07 00 00 00       	push   0x7
    10ab:	e9 70 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010b0 <fgets@plt>:
    10b0:	ff 25 a2 2f 00 00    	jmp    QWORD PTR [rip+0x2fa2]        # 4058 <fgets@GLIBC_2.2.5>
    10b6:	68 08 00 00 00       	push   0x8
    10bb:	e9 60 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010c0 <getchar@plt>:
    10c0:	ff 25 9a 2f 00 00    	jmp    QWORD PTR [rip+0x2f9a]        # 4060 <getchar@GLIBC_2.2.5>
    10c6:	68 09 00 00 00       	push   0x9
    10cb:	e9 50 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010d0 <memmem@plt>:
    10d0:	ff 25 92 2f 00 00    	jmp    QWORD PTR [rip+0x2f92]        # 4068 <memmem@GLIBC_2.2.5>
    10d6:	68 0a 00 00 00       	push   0xa
    10db:	e9 40 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010e0 <malloc@plt>:
    10e0:	ff 25 8a 2f 00 00    	jmp    QWORD PTR [rip+0x2f8a]        # 4070 <malloc@GLIBC_2.2.5>
    10e6:	68 0b 00 00 00       	push   0xb
    10eb:	e9 30 ff ff ff       	jmp    1020 <_init+0x20>

00000000000010f0 <setvbuf@plt>:
    10f0:	ff 25 82 2f 00 00    	jmp    QWORD PTR [rip+0x2f82]        # 4078 <setvbuf@GLIBC_2.2.5>
    10f6:	68 0c 00 00 00       	push   0xc
    10fb:	e9 20 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001100 <__isoc99_scanf@plt>:
    1100:	ff 25 7a 2f 00 00    	jmp    QWORD PTR [rip+0x2f7a]        # 4080 <__isoc99_scanf@GLIBC_2.7>
    1106:	68 0d 00 00 00       	push   0xd
    110b:	e9 10 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001110 <exit@plt>:
    1110:	ff 25 72 2f 00 00    	jmp    QWORD PTR [rip+0x2f72]        # 4088 <exit@GLIBC_2.2.5>
    1116:	68 0e 00 00 00       	push   0xe
    111b:	e9 00 ff ff ff       	jmp    1020 <_init+0x20>

Disassembly of section .plt.got:

0000000000001120 <__cxa_finalize@plt>:
    1120:	ff 25 42 21 00 00    	jmp    QWORD PTR [rip+0x2142]        # 3268 <__cxa_finalize@GLIBC_2.2.5>
    1126:	66 90                	xchg   ax,ax

Disassembly of section .text:

0000000000001130 <_start>:
    1130:	31 ed                	xor    ebp,ebp
    1132:	49 89 d1             	mov    r9,rdx
    1135:	5e                   	pop    rsi
    1136:	48 89 e2             	mov    rdx,rsp
    1139:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    113d:	50                   	push   rax
    113e:	54                   	push   rsp
    113f:	4c 8d 05 6a 08 00 00 	lea    r8,[rip+0x86a]        # 19b0 <__libc_csu_fini>
    1146:	48 8d 0d 03 08 00 00 	lea    rcx,[rip+0x803]        # 1950 <__libc_csu_init>
    114d:	48 8d 3d 76 06 00 00 	lea    rdi,[rip+0x676]        # 17ca <main>
    1154:	ff 15 f6 20 00 00    	call   QWORD PTR [rip+0x20f6]        # 3250 <__libc_start_main@GLIBC_2.2.5>
    115a:	f4                   	hlt
    115b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000001160 <deregister_tm_clones>:
    1160:	48 8d 3d 39 2f 00 00 	lea    rdi,[rip+0x2f39]        # 40a0 <stdout@GLIBC_2.2.5>
    1167:	48 8d 05 32 2f 00 00 	lea    rax,[rip+0x2f32]        # 40a0 <stdout@GLIBC_2.2.5>
    116e:	48 39 f8             	cmp    rax,rdi
    1171:	74 15                	je     1188 <deregister_tm_clones+0x28>
    1173:	48 8b 05 ce 20 00 00 	mov    rax,QWORD PTR [rip+0x20ce]        # 3248 <_ITM_deregisterTMCloneTable@Base>
    117a:	48 85 c0             	test   rax,rax
    117d:	74 09                	je     1188 <deregister_tm_clones+0x28>
    117f:	ff e0                	jmp    rax
    1181:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1188:	c3                   	ret
    1189:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001190 <register_tm_clones>:
    1190:	48 8d 3d 09 2f 00 00 	lea    rdi,[rip+0x2f09]        # 40a0 <stdout@GLIBC_2.2.5>
    1197:	48 8d 35 02 2f 00 00 	lea    rsi,[rip+0x2f02]        # 40a0 <stdout@GLIBC_2.2.5>
    119e:	48 29 fe             	sub    rsi,rdi
    11a1:	48 89 f0             	mov    rax,rsi
    11a4:	48 c1 ee 3f          	shr    rsi,0x3f
    11a8:	48 c1 f8 03          	sar    rax,0x3
    11ac:	48 01 c6             	add    rsi,rax
    11af:	48 d1 fe             	sar    rsi,1
    11b2:	74 14                	je     11c8 <register_tm_clones+0x38>
    11b4:	48 8b 05 a5 20 00 00 	mov    rax,QWORD PTR [rip+0x20a5]        # 3260 <_ITM_registerTMCloneTable@Base>
    11bb:	48 85 c0             	test   rax,rax
    11be:	74 08                	je     11c8 <register_tm_clones+0x38>
    11c0:	ff e0                	jmp    rax
    11c2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    11c8:	c3                   	ret
    11c9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000011d0 <__do_global_dtors_aux>:
    11d0:	80 3d f1 2e 00 00 00 	cmp    BYTE PTR [rip+0x2ef1],0x0        # 40c8 <completed.0>
    11d7:	75 2f                	jne    1208 <__do_global_dtors_aux+0x38>
    11d9:	55                   	push   rbp
    11da:	48 83 3d 86 20 00 00 	cmp    QWORD PTR [rip+0x2086],0x0        # 3268 <__cxa_finalize@GLIBC_2.2.5>
    11e1:	00 
    11e2:	48 89 e5             	mov    rbp,rsp
    11e5:	74 0c                	je     11f3 <__do_global_dtors_aux+0x23>
    11e7:	48 8b 3d aa 2e 00 00 	mov    rdi,QWORD PTR [rip+0x2eaa]        # 4098 <__dso_handle>
    11ee:	e8 2d ff ff ff       	call   1120 <__cxa_finalize@plt>
    11f3:	e8 68 ff ff ff       	call   1160 <deregister_tm_clones>
    11f8:	c6 05 c9 2e 00 00 01 	mov    BYTE PTR [rip+0x2ec9],0x1        # 40c8 <completed.0>
    11ff:	5d                   	pop    rbp
    1200:	c3                   	ret
    1201:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    1208:	c3                   	ret
    1209:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001210 <frame_dummy>:
    1210:	e9 7b ff ff ff       	jmp    1190 <register_tm_clones>

0000000000001215 <scanner_naive1>:
    1215:	55                   	push   rbp
    1216:	48 89 e5             	mov    rbp,rsp
    1219:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    121d:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
    1221:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
    1225:	48 89 4d d0          	mov    QWORD PTR [rbp-0x30],rcx
    1229:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    1230:	eb 75                	jmp    12a7 <scanner_naive1+0x92>
    1232:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1235:	48 63 d0             	movsxd rdx,eax
    1238:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    123c:	48 01 d0             	add    rax,rdx
    123f:	0f b6 10             	movzx  edx,BYTE PTR [rax]
    1242:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1246:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1249:	38 c2                	cmp    dl,al
    124b:	75 56                	jne    12a3 <scanner_naive1+0x8e>
    124d:	c6 45 fb 01          	mov    BYTE PTR [rbp-0x5],0x1
    1251:	c7 45 f4 01 00 00 00 	mov    DWORD PTR [rbp-0xc],0x1
    1258:	eb 33                	jmp    128d <scanner_naive1+0x78>
    125a:	8b 55 fc             	mov    edx,DWORD PTR [rbp-0x4]
    125d:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    1260:	01 d0                	add    eax,edx
    1262:	48 63 d0             	movsxd rdx,eax
    1265:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1269:	48 01 d0             	add    rax,rdx
    126c:	0f b6 10             	movzx  edx,BYTE PTR [rax]
    126f:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    1272:	48 63 c8             	movsxd rcx,eax
    1275:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1279:	48 01 c8             	add    rax,rcx
    127c:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    127f:	38 c2                	cmp    dl,al
    1281:	74 06                	je     1289 <scanner_naive1+0x74>
    1283:	c6 45 fb 00          	mov    BYTE PTR [rbp-0x5],0x0
    1287:	eb 0f                	jmp    1298 <scanner_naive1+0x83>
    1289:	83 45 f4 01          	add    DWORD PTR [rbp-0xc],0x1
    128d:	8b 45 f4             	mov    eax,DWORD PTR [rbp-0xc]
    1290:	48 98                	cdqe
    1292:	48 39 45 d0          	cmp    QWORD PTR [rbp-0x30],rax
    1296:	77 c2                	ja     125a <scanner_naive1+0x45>
    1298:	80 7d fb 00          	cmp    BYTE PTR [rbp-0x5],0x0
    129c:	74 05                	je     12a3 <scanner_naive1+0x8e>
    129e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    12a1:	eb 12                	jmp    12b5 <scanner_naive1+0xa0>
    12a3:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
    12a7:	81 7d fc ff 0f 00 00 	cmp    DWORD PTR [rbp-0x4],0xfff
    12ae:	7e 82                	jle    1232 <scanner_naive1+0x1d>
    12b0:	b8 ff ff ff ff       	mov    eax,0xffffffff
    12b5:	5d                   	pop    rbp
    12b6:	c3                   	ret

00000000000012b7 <scanner_naive2>:
    12b7:	55                   	push   rbp
    12b8:	48 89 e5             	mov    rbp,rsp
    12bb:	48 83 ec 30          	sub    rsp,0x30
    12bf:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    12c3:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
    12c7:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
    12cb:	48 89 4d d0          	mov    QWORD PTR [rbp-0x30],rcx
    12cf:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    12d6:	eb 49                	jmp    1321 <scanner_naive2+0x6a>
    12d8:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    12db:	48 63 d0             	movsxd rdx,eax
    12de:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    12e2:	48 01 d0             	add    rax,rdx
    12e5:	0f b6 10             	movzx  edx,BYTE PTR [rax]
    12e8:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    12ec:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    12ef:	38 c2                	cmp    dl,al
    12f1:	75 2a                	jne    131d <scanner_naive2+0x66>
    12f3:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    12f6:	48 63 d0             	movsxd rdx,eax
    12f9:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    12fd:	48 8d 0c 02          	lea    rcx,[rdx+rax*1]
    1301:	48 8b 55 d0          	mov    rdx,QWORD PTR [rbp-0x30]
    1305:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1309:	48 89 c6             	mov    rsi,rax
    130c:	48 89 cf             	mov    rdi,rcx
    130f:	e8 8c fd ff ff       	call   10a0 <memcmp@plt>
    1314:	85 c0                	test   eax,eax
    1316:	75 05                	jne    131d <scanner_naive2+0x66>
    1318:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    131b:	eb 12                	jmp    132f <scanner_naive2+0x78>
    131d:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
    1321:	81 7d fc ff 0f 00 00 	cmp    DWORD PTR [rbp-0x4],0xfff
    1328:	7e ae                	jle    12d8 <scanner_naive2+0x21>
    132a:	b8 ff ff ff ff       	mov    eax,0xffffffff
    132f:	c9                   	leave
    1330:	c3                   	ret

0000000000001331 <scanner_memmem>:
    1331:	55                   	push   rbp
    1332:	48 89 e5             	mov    rbp,rsp
    1335:	48 83 ec 30          	sub    rsp,0x30
    1339:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    133d:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
    1341:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
    1345:	48 89 4d d0          	mov    QWORD PTR [rbp-0x30],rcx
    1349:	48 8b 4d d0          	mov    rcx,QWORD PTR [rbp-0x30]
    134d:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
    1351:	48 8b 75 e0          	mov    rsi,QWORD PTR [rbp-0x20]
    1355:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    1359:	48 89 c7             	mov    rdi,rax
    135c:	e8 6f fd ff ff       	call   10d0 <memmem@plt>
    1361:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
    1365:	48 83 7d f8 00       	cmp    QWORD PTR [rbp-0x8],0x0
    136a:	75 07                	jne    1373 <scanner_memmem+0x42>
    136c:	b8 ff ff ff ff       	mov    eax,0xffffffff
    1371:	eb 08                	jmp    137b <scanner_memmem+0x4a>
    1373:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
    1377:	48 2b 45 e8          	sub    rax,QWORD PTR [rbp-0x18]
    137b:	c9                   	leave
    137c:	c3                   	ret

000000000000137d <run_scanner>:
    137d:	55                   	push   rbp
    137e:	48 89 e5             	mov    rbp,rsp
    1381:	48 83 ec 30          	sub    rsp,0x30
    1385:	89 7d fc             	mov    DWORD PTR [rbp-0x4],edi
    1388:	48 89 75 f0          	mov    QWORD PTR [rbp-0x10],rsi
    138c:	48 89 55 e8          	mov    QWORD PTR [rbp-0x18],rdx
    1390:	48 89 4d e0          	mov    QWORD PTR [rbp-0x20],rcx
    1394:	4c 89 45 d8          	mov    QWORD PTR [rbp-0x28],r8
    1398:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
    139c:	78 08                	js     13a6 <run_scanner+0x29>
    139e:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    13a1:	83 f8 02             	cmp    eax,0x2
    13a4:	76 16                	jbe    13bc <run_scanner+0x3f>
    13a6:	48 8d 3d 5b 0c 00 00 	lea    rdi,[rip+0xc5b]        # 2008 <_IO_stdin_used+0x8>
    13ad:	e8 9e fc ff ff       	call   1050 <puts@plt>
    13b2:	bf 01 00 00 00       	mov    edi,0x1
    13b7:	e8 54 fd ff ff       	call   1110 <exit@plt>
    13bc:	48 83 7d f0 00       	cmp    QWORD PTR [rbp-0x10],0x0
    13c1:	74 07                	je     13ca <run_scanner+0x4d>
    13c3:	48 83 7d e0 00       	cmp    QWORD PTR [rbp-0x20],0x0
    13c8:	75 16                	jne    13e0 <run_scanner+0x63>
    13ca:	48 8d 3d 48 0c 00 00 	lea    rdi,[rip+0xc48]        # 2019 <_IO_stdin_used+0x19>
    13d1:	e8 7a fc ff ff       	call   1050 <puts@plt>
    13d6:	bf 01 00 00 00       	mov    edi,0x1
    13db:	e8 30 fd ff ff       	call   1110 <exit@plt>
    13e0:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    13e4:	48 3b 45 e8          	cmp    rax,QWORD PTR [rbp-0x18]
    13e8:	76 16                	jbe    1400 <run_scanner+0x83>
    13ea:	48 8d 3d 3f 0c 00 00 	lea    rdi,[rip+0xc3f]        # 2030 <_IO_stdin_used+0x30>
    13f1:	e8 5a fc ff ff       	call   1050 <puts@plt>
    13f6:	bf 01 00 00 00       	mov    edi,0x1
    13fb:	e8 10 fd ff ff       	call   1110 <exit@plt>
    1400:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1403:	48 63 d0             	movsxd rdx,eax
    1406:	48 89 d0             	mov    rax,rdx
    1409:	48 01 c0             	add    rax,rax
    140c:	48 01 d0             	add    rax,rdx
    140f:	48 c1 e0 03          	shl    rax,0x3
    1413:	48 89 c2             	mov    rdx,rax
    1416:	48 8d 05 03 1c 00 00 	lea    rax,[rip+0x1c03]        # 3020 <scanners>
    141d:	4c 8b 04 02          	mov    r8,QWORD PTR [rdx+rax*1]
    1421:	48 8b 4d d8          	mov    rcx,QWORD PTR [rbp-0x28]
    1425:	48 8b 55 e0          	mov    rdx,QWORD PTR [rbp-0x20]
    1429:	48 8b 75 e8          	mov    rsi,QWORD PTR [rbp-0x18]
    142d:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
    1431:	48 89 c7             	mov    rdi,rax
    1434:	41 ff d0             	call   r8
    1437:	c9                   	leave
    1438:	c3                   	ret

0000000000001439 <print_scanner_output>:
    1439:	55                   	push   rbp
    143a:	48 89 e5             	mov    rbp,rsp
    143d:	48 83 ec 10          	sub    rsp,0x10
    1441:	89 7d fc             	mov    DWORD PTR [rbp-0x4],edi
    1444:	83 7d fc 00          	cmp    DWORD PTR [rbp-0x4],0x0
    1448:	79 0e                	jns    1458 <print_scanner_output+0x1f>
    144a:	48 8d 3d 06 0c 00 00 	lea    rdi,[rip+0xc06]        # 2057 <_IO_stdin_used+0x57>
    1451:	e8 fa fb ff ff       	call   1050 <puts@plt>
    1456:	eb 16                	jmp    146e <print_scanner_output+0x35>
    1458:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    145b:	89 c6                	mov    esi,eax
    145d:	48 8d 3d fe 0b 00 00 	lea    rdi,[rip+0xbfe]        # 2062 <_IO_stdin_used+0x62>
    1464:	b8 00 00 00 00       	mov    eax,0x0
    1469:	e8 12 fc ff ff       	call   1080 <printf@plt>
    146e:	90                   	nop
    146f:	c9                   	leave
    1470:	c3                   	ret

0000000000001471 <get_scanner_index>:
    1471:	55                   	push   rbp
    1472:	48 89 e5             	mov    rbp,rsp
    1475:	48 83 ec 20          	sub    rsp,0x20
    1479:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    147d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    1484:	eb 42                	jmp    14c8 <get_scanner_index+0x57>
    1486:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1489:	48 63 d0             	movsxd rdx,eax
    148c:	48 89 d0             	mov    rax,rdx
    148f:	48 01 c0             	add    rax,rax
    1492:	48 01 d0             	add    rax,rdx
    1495:	48 c1 e0 03          	shl    rax,0x3
    1499:	48 8d 15 80 1b 00 00 	lea    rdx,[rip+0x1b80]        # 3020 <scanners>
    14a0:	48 01 d0             	add    rax,rdx
    14a3:	48 8d 48 08          	lea    rcx,[rax+0x8]
    14a7:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    14ab:	ba 10 00 00 00       	mov    edx,0x10
    14b0:	48 89 c6             	mov    rsi,rax
    14b3:	48 89 cf             	mov    rdi,rcx
    14b6:	e8 85 fb ff ff       	call   1040 <strncmp@plt>
    14bb:	85 c0                	test   eax,eax
    14bd:	75 05                	jne    14c4 <get_scanner_index+0x53>
    14bf:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    14c2:	eb 11                	jmp    14d5 <get_scanner_index+0x64>
    14c4:	83 45 fc 01          	add    DWORD PTR [rbp-0x4],0x1
    14c8:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    14cb:	83 f8 02             	cmp    eax,0x2
    14ce:	76 b6                	jbe    1486 <get_scanner_index+0x15>
    14d0:	b8 ff ff ff ff       	mov    eax,0xffffffff
    14d5:	c9                   	leave
    14d6:	c3                   	ret

00000000000014d7 <read_parameters>:
    14d7:	55                   	push   rbp
    14d8:	48 89 e5             	mov    rbp,rsp
    14db:	48 83 ec 30          	sub    rsp,0x30
    14df:	48 89 7d e8          	mov    QWORD PTR [rbp-0x18],rdi
    14e3:	48 89 75 e0          	mov    QWORD PTR [rbp-0x20],rsi
    14e7:	48 89 55 d8          	mov    QWORD PTR [rbp-0x28],rdx
    14eb:	48 8d 45 f0          	lea    rax,[rbp-0x10]
    14ef:	ba 10 00 00 00       	mov    edx,0x10
    14f4:	be 00 00 00 00       	mov    esi,0x0
    14f9:	48 89 c7             	mov    rdi,rax
    14fc:	e8 8f fb ff ff       	call   1090 <memset@plt>
    1501:	48 8d 3d 69 0b 00 00 	lea    rdi,[rip+0xb69]        # 2071 <_IO_stdin_used+0x71>
    1508:	b8 00 00 00 00       	mov    eax,0x0
    150d:	e8 6e fb ff ff       	call   1080 <printf@plt>
    1512:	48 8b 55 d8          	mov    rdx,QWORD PTR [rbp-0x28]
    1516:	48 8d 45 f0          	lea    rax,[rbp-0x10]
    151a:	48 89 c6             	mov    rsi,rax
    151d:	48 8d 3d 60 0b 00 00 	lea    rdi,[rip+0xb60]        # 2084 <_IO_stdin_used+0x84>
    1524:	b8 00 00 00 00       	mov    eax,0x0
    1529:	e8 d2 fb ff ff       	call   1100 <__isoc99_scanf@plt>
    152e:	83 f8 02             	cmp    eax,0x2
    1531:	74 16                	je     1549 <read_parameters+0x72>
    1533:	48 8d 3d 52 0b 00 00 	lea    rdi,[rip+0xb52]        # 208c <_IO_stdin_used+0x8c>
    153a:	e8 11 fb ff ff       	call   1050 <puts@plt>
    153f:	bf 01 00 00 00       	mov    edi,0x1
    1544:	e8 c7 fb ff ff       	call   1110 <exit@plt>
    1549:	e8 72 fb ff ff       	call   10c0 <getchar@plt>
    154e:	48 8d 45 f0          	lea    rax,[rbp-0x10]
    1552:	48 89 c7             	mov    rdi,rax
    1555:	e8 17 ff ff ff       	call   1471 <get_scanner_index>
    155a:	48 8b 55 e8          	mov    rdx,QWORD PTR [rbp-0x18]
    155e:	89 02                	mov    DWORD PTR [rdx],eax
    1560:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1564:	8b 00                	mov    eax,DWORD PTR [rax]
    1566:	3d 00 10 00 00       	cmp    eax,0x1000
    156b:	76 16                	jbe    1583 <read_parameters+0xac>
    156d:	48 8d 3d 2c 0b 00 00 	lea    rdi,[rip+0xb2c]        # 20a0 <_IO_stdin_used+0xa0>
    1574:	e8 d7 fa ff ff       	call   1050 <puts@plt>
    1579:	bf 01 00 00 00       	mov    edi,0x1
    157e:	e8 8d fb ff ff       	call   1110 <exit@plt>
    1583:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1587:	8b 00                	mov    eax,DWORD PTR [rax]
    1589:	89 c0                	mov    eax,eax
    158b:	48 89 c7             	mov    rdi,rax
    158e:	e8 4d fb ff ff       	call   10e0 <malloc@plt>
    1593:	48 89 c2             	mov    rdx,rax
    1596:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    159a:	48 89 10             	mov    QWORD PTR [rax],rdx
    159d:	48 8b 15 0c 2b 00 00 	mov    rdx,QWORD PTR [rip+0x2b0c]        # 40b0 <stdin@GLIBC_2.2.5>
    15a4:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    15a8:	8b 00                	mov    eax,DWORD PTR [rax]
    15aa:	89 c6                	mov    esi,eax
    15ac:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    15b0:	48 8b 00             	mov    rax,QWORD PTR [rax]
    15b3:	48 89 d1             	mov    rcx,rdx
    15b6:	ba 01 00 00 00       	mov    edx,0x1
    15bb:	48 89 c7             	mov    rdi,rax
    15be:	e8 9d fa ff ff       	call   1060 <fread@plt>
    15c3:	e8 f8 fa ff ff       	call   10c0 <getchar@plt>
    15c8:	90                   	nop
    15c9:	c9                   	leave
    15ca:	c3                   	ret

00000000000015cb <run_performance_test>:
    15cb:	55                   	push   rbp
    15cc:	48 89 e5             	mov    rbp,rsp
    15cf:	48 83 ec 60          	sub    rsp,0x60
    15d3:	89 7d cc             	mov    DWORD PTR [rbp-0x34],edi
    15d6:	48 89 75 c0          	mov    QWORD PTR [rbp-0x40],rsi
    15da:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
    15de:	48 89 4d b0          	mov    QWORD PTR [rbp-0x50],rcx
    15e2:	4c 89 45 a8          	mov    QWORD PTR [rbp-0x58],r8
    15e6:	48 c7 45 d8 00 00 00 	mov    QWORD PTR [rbp-0x28],0x0
    15ed:	00 
    15ee:	48 8d 3d be 0a 00 00 	lea    rdi,[rip+0xabe]        # 20b3 <_IO_stdin_used+0xb3>
    15f5:	b8 00 00 00 00       	mov    eax,0x0
    15fa:	e8 81 fa ff ff       	call   1080 <printf@plt>
    15ff:	48 8d 45 d8          	lea    rax,[rbp-0x28]
    1603:	48 89 c6             	mov    rsi,rax
    1606:	48 8d 3d c3 0a 00 00 	lea    rdi,[rip+0xac3]        # 20d0 <_IO_stdin_used+0xd0>
    160d:	b8 00 00 00 00       	mov    eax,0x0
    1612:	e8 e9 fa ff ff       	call   1100 <__isoc99_scanf@plt>
    1617:	e8 a4 fa ff ff       	call   10c0 <getchar@plt>
    161c:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1620:	48 85 c0             	test   rax,rax
    1623:	75 16                	jne    163b <run_performance_test+0x70>
    1625:	48 8d 3d a8 0a 00 00 	lea    rdi,[rip+0xaa8]        # 20d4 <_IO_stdin_used+0xd4>
    162c:	e8 1f fa ff ff       	call   1050 <puts@plt>
    1631:	bf 01 00 00 00       	mov    edi,0x1
    1636:	e8 d5 fa ff ff       	call   1110 <exit@plt>
    163b:	e8 30 fa ff ff       	call   1070 <clock@plt>
    1640:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax
    1644:	48 c7 45 f8 00 00 00 	mov    QWORD PTR [rbp-0x8],0x0
    164b:	00 
    164c:	eb 22                	jmp    1670 <run_performance_test+0xa5>
    164e:	48 8b 7d a8          	mov    rdi,QWORD PTR [rbp-0x58]
    1652:	48 8b 4d b0          	mov    rcx,QWORD PTR [rbp-0x50]
    1656:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
    165a:	48 8b 75 c0          	mov    rsi,QWORD PTR [rbp-0x40]
    165e:	8b 45 cc             	mov    eax,DWORD PTR [rbp-0x34]
    1661:	49 89 f8             	mov    r8,rdi
    1664:	89 c7                	mov    edi,eax
    1666:	e8 12 fd ff ff       	call   137d <run_scanner>
    166b:	48 83 45 f8 01       	add    QWORD PTR [rbp-0x8],0x1
    1670:	48 8b 45 d8          	mov    rax,QWORD PTR [rbp-0x28]
    1674:	48 39 45 f8          	cmp    QWORD PTR [rbp-0x8],rax
    1678:	72 d4                	jb     164e <run_performance_test+0x83>
    167a:	e8 f1 f9 ff ff       	call   1070 <clock@plt>
    167f:	48 89 45 e8          	mov    QWORD PTR [rbp-0x18],rax
    1683:	48 8d 3d 68 0a 00 00 	lea    rdi,[rip+0xa68]        # 20f2 <_IO_stdin_used+0xf2>
    168a:	b8 00 00 00 00       	mov    eax,0x0
    168f:	e8 ec f9 ff ff       	call   1080 <printf@plt>
    1694:	48 8b 7d a8          	mov    rdi,QWORD PTR [rbp-0x58]
    1698:	48 8b 4d b0          	mov    rcx,QWORD PTR [rbp-0x50]
    169c:	48 8b 55 b8          	mov    rdx,QWORD PTR [rbp-0x48]
    16a0:	48 8b 75 c0          	mov    rsi,QWORD PTR [rbp-0x40]
    16a4:	8b 45 cc             	mov    eax,DWORD PTR [rbp-0x34]
    16a7:	49 89 f8             	mov    r8,rdi
    16aa:	89 c7                	mov    edi,eax
    16ac:	e8 cc fc ff ff       	call   137d <run_scanner>
    16b1:	89 c7                	mov    edi,eax
    16b3:	e8 81 fd ff ff       	call   1439 <print_scanner_output>
    16b8:	48 8b 45 e8          	mov    rax,QWORD PTR [rbp-0x18]
    16bc:	48 2b 45 f0          	sub    rax,QWORD PTR [rbp-0x10]
    16c0:	66 0f ef c0          	pxor   xmm0,xmm0
    16c4:	f2 48 0f 2a c0       	cvtsi2sd xmm0,rax
    16c9:	f2 0f 10 0d af 0a 00 	movsd  xmm1,QWORD PTR [rip+0xaaf]        # 2180 <_IO_stdin_used+0x180>
    16d0:	00 
    16d1:	f2 0f 5e c1          	divsd  xmm0,xmm1
    16d5:	f2 0f 11 45 e0       	movsd  QWORD PTR [rbp-0x20],xmm0
    16da:	48 8b 45 e0          	mov    rax,QWORD PTR [rbp-0x20]
    16de:	66 48 0f 6e c0       	movq   xmm0,rax
    16e3:	48 8d 3d 11 0a 00 00 	lea    rdi,[rip+0xa11]        # 20fb <_IO_stdin_used+0xfb>
    16ea:	b8 01 00 00 00       	mov    eax,0x1
    16ef:	e8 8c f9 ff ff       	call   1080 <printf@plt>
    16f4:	90                   	nop
    16f5:	c9                   	leave
    16f6:	c3                   	ret

00000000000016f7 <menu>:
    16f7:	55                   	push   rbp
    16f8:	48 89 e5             	mov    rbp,rsp
    16fb:	48 83 ec 10          	sub    rsp,0x10
    16ff:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [rbp-0x4],0xffffffff
    1706:	48 8d 3d ff 09 00 00 	lea    rdi,[rip+0x9ff]        # 210c <_IO_stdin_used+0x10c>
    170d:	e8 3e f9 ff ff       	call   1050 <puts@plt>
    1712:	48 8d 3d 04 0a 00 00 	lea    rdi,[rip+0xa04]        # 211d <_IO_stdin_used+0x11d>
    1719:	e8 32 f9 ff ff       	call   1050 <puts@plt>
    171e:	48 8d 3d 16 0a 00 00 	lea    rdi,[rip+0xa16]        # 213b <_IO_stdin_used+0x13b>
    1725:	e8 26 f9 ff ff       	call   1050 <puts@plt>
    172a:	48 8d 3d 19 0a 00 00 	lea    rdi,[rip+0xa19]        # 214a <_IO_stdin_used+0x14a>
    1731:	e8 1a f9 ff ff       	call   1050 <puts@plt>
    1736:	48 8d 3d 15 0a 00 00 	lea    rdi,[rip+0xa15]        # 2152 <_IO_stdin_used+0x152>
    173d:	b8 00 00 00 00       	mov    eax,0x0
    1742:	e8 39 f9 ff ff       	call   1080 <printf@plt>
    1747:	48 8d 45 fc          	lea    rax,[rbp-0x4]
    174b:	48 89 c6             	mov    rsi,rax
    174e:	48 8d 3d 00 0a 00 00 	lea    rdi,[rip+0xa00]        # 2155 <_IO_stdin_used+0x155>
    1755:	b8 00 00 00 00       	mov    eax,0x0
    175a:	e8 a1 f9 ff ff       	call   1100 <__isoc99_scanf@plt>
    175f:	e8 5c f9 ff ff       	call   10c0 <getchar@plt>
    1764:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    1767:	c9                   	leave
    1768:	c3                   	ret

0000000000001769 <setup>:
    1769:	55                   	push   rbp
    176a:	48 89 e5             	mov    rbp,rsp
    176d:	48 8b 05 3c 29 00 00 	mov    rax,QWORD PTR [rip+0x293c]        # 40b0 <stdin@GLIBC_2.2.5>
    1774:	b9 00 00 00 00       	mov    ecx,0x0
    1779:	ba 02 00 00 00       	mov    edx,0x2
    177e:	be 00 00 00 00       	mov    esi,0x0
    1783:	48 89 c7             	mov    rdi,rax
    1786:	e8 65 f9 ff ff       	call   10f0 <setvbuf@plt>
    178b:	48 8b 05 0e 29 00 00 	mov    rax,QWORD PTR [rip+0x290e]        # 40a0 <stdout@GLIBC_2.2.5>
    1792:	b9 00 00 00 00       	mov    ecx,0x0
    1797:	ba 02 00 00 00       	mov    edx,0x2
    179c:	be 00 00 00 00       	mov    esi,0x0
    17a1:	48 89 c7             	mov    rdi,rax
    17a4:	e8 47 f9 ff ff       	call   10f0 <setvbuf@plt>
    17a9:	48 8b 05 10 29 00 00 	mov    rax,QWORD PTR [rip+0x2910]        # 40c0 <stderr@GLIBC_2.2.5>
    17b0:	b9 00 00 00 00       	mov    ecx,0x0
    17b5:	ba 02 00 00 00       	mov    edx,0x2
    17ba:	be 00 00 00 00       	mov    esi,0x0
    17bf:	48 89 c7             	mov    rdi,rax
    17c2:	e8 29 f9 ff ff       	call   10f0 <setvbuf@plt>
    17c7:	90                   	nop
    17c8:	5d                   	pop    rbp
    17c9:	c3                   	ret

00000000000017ca <main>:
    17ca:	55                   	push   rbp
    17cb:	48 89 e5             	mov    rbp,rsp
    17ce:	48 81 ec 10 10 00 00 	sub    rsp,0x1010
    17d5:	b8 00 00 00 00       	mov    eax,0x0
    17da:	e8 8a ff ff ff       	call   1769 <setup>
    17df:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [rbp-0x4],0x0
    17e6:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [rbp-0x8],0x0
    17ed:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
    17f4:	00 
    17f5:	48 8d 85 f0 ef ff ff 	lea    rax,[rbp-0x1010]
    17fc:	ba 00 10 00 00       	mov    edx,0x1000
    1801:	be 00 00 00 00       	mov    esi,0x0
    1806:	48 89 c7             	mov    rdi,rax
    1809:	e8 82 f8 ff ff       	call   1090 <memset@plt>
    180e:	b8 00 00 00 00       	mov    eax,0x0
    1813:	e8 df fe ff ff       	call   16f7 <menu>
    1818:	83 f8 03             	cmp    eax,0x3
    181b:	0f 84 b2 00 00 00    	je     18d3 <main+0x109>
    1821:	83 f8 03             	cmp    eax,0x3
    1824:	0f 8f 02 01 00 00    	jg     192c <main+0x162>
    182a:	83 f8 02             	cmp    eax,0x2
    182d:	74 52                	je     1881 <main+0xb7>
    182f:	83 f8 02             	cmp    eax,0x2
    1832:	0f 8f f4 00 00 00    	jg     192c <main+0x162>
    1838:	85 c0                	test   eax,eax
    183a:	74 0a                	je     1846 <main+0x7c>
    183c:	83 f8 01             	cmp    eax,0x1
    183f:	74 0f                	je     1850 <main+0x86>
    1841:	e9 e6 00 00 00       	jmp    192c <main+0x162>
    1846:	bf 00 00 00 00       	mov    edi,0x0
    184b:	e8 c0 f8 ff ff       	call   1110 <exit@plt>
    1850:	48 8d 3d 01 09 00 00 	lea    rdi,[rip+0x901]        # 2158 <_IO_stdin_used+0x158>
    1857:	b8 00 00 00 00       	mov    eax,0x0
    185c:	e8 1f f8 ff ff       	call   1080 <printf@plt>
    1861:	48 8b 15 48 28 00 00 	mov    rdx,QWORD PTR [rip+0x2848]        # 40b0 <stdin@GLIBC_2.2.5>
    1868:	48 8d 85 f0 ef ff ff 	lea    rax,[rbp-0x1010]
    186f:	be 00 10 00 00       	mov    esi,0x1000
    1874:	48 89 c7             	mov    rdi,rax
    1877:	e8 34 f8 ff ff       	call   10b0 <fgets@plt>
    187c:	e9 c1 00 00 00       	jmp    1942 <main+0x178>
    1881:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
    1885:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
    1889:	48 8d 45 fc          	lea    rax,[rbp-0x4]
    188d:	48 89 ce             	mov    rsi,rcx
    1890:	48 89 c7             	mov    rdi,rax
    1893:	e8 3f fc ff ff       	call   14d7 <read_parameters>
    1898:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    189b:	89 c1                	mov    ecx,eax
    189d:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
    18a1:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    18a4:	48 8d b5 f0 ef ff ff 	lea    rsi,[rbp-0x1010]
    18ab:	49 89 c8             	mov    r8,rcx
    18ae:	48 89 d1             	mov    rcx,rdx
    18b1:	ba 00 10 00 00       	mov    edx,0x1000
    18b6:	89 c7                	mov    edi,eax
    18b8:	e8 0e fd ff ff       	call   15cb <run_performance_test>
    18bd:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
    18c1:	48 89 c7             	mov    rdi,rax
    18c4:	e8 67 f7 ff ff       	call   1030 <free@plt>
    18c9:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
    18d0:	00 
    18d1:	eb 6f                	jmp    1942 <main+0x178>
    18d3:	48 8d 55 f8          	lea    rdx,[rbp-0x8]
    18d7:	48 8d 4d f0          	lea    rcx,[rbp-0x10]
    18db:	48 8d 45 fc          	lea    rax,[rbp-0x4]
    18df:	48 89 ce             	mov    rsi,rcx
    18e2:	48 89 c7             	mov    rdi,rax
    18e5:	e8 ed fb ff ff       	call   14d7 <read_parameters>
    18ea:	8b 45 f8             	mov    eax,DWORD PTR [rbp-0x8]
    18ed:	89 c1                	mov    ecx,eax
    18ef:	48 8b 55 f0          	mov    rdx,QWORD PTR [rbp-0x10]
    18f3:	8b 45 fc             	mov    eax,DWORD PTR [rbp-0x4]
    18f6:	48 8d b5 f0 ef ff ff 	lea    rsi,[rbp-0x1010]
    18fd:	49 89 c8             	mov    r8,rcx
    1900:	48 89 d1             	mov    rcx,rdx
    1903:	ba 00 10 00 00       	mov    edx,0x1000
    1908:	89 c7                	mov    edi,eax
    190a:	e8 6e fa ff ff       	call   137d <run_scanner>
    190f:	89 c7                	mov    edi,eax
    1911:	e8 23 fb ff ff       	call   1439 <print_scanner_output>
    1916:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]
    191a:	48 89 c7             	mov    rdi,rax
    191d:	e8 0e f7 ff ff       	call   1030 <free@plt>
    1922:	48 c7 45 f0 00 00 00 	mov    QWORD PTR [rbp-0x10],0x0
    1929:	00 
    192a:	eb 16                	jmp    1942 <main+0x178>
    192c:	48 8d 3d 38 08 00 00 	lea    rdi,[rip+0x838]        # 216b <_IO_stdin_used+0x16b>
    1933:	e8 18 f7 ff ff       	call   1050 <puts@plt>
    1938:	bf 01 00 00 00       	mov    edi,0x1
    193d:	e8 ce f7 ff ff       	call   1110 <exit@plt>
    1942:	e9 c7 fe ff ff       	jmp    180e <main+0x44>
    1947:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
    194e:	00 00 

0000000000001950 <__libc_csu_init>:
    1950:	41 57                	push   r15
    1952:	4c 8d 3d a7 16 00 00 	lea    r15,[rip+0x16a7]        # 3000 <__frame_dummy_init_array_entry>
    1959:	41 56                	push   r14
    195b:	49 89 d6             	mov    r14,rdx
    195e:	41 55                	push   r13
    1960:	49 89 f5             	mov    r13,rsi
    1963:	41 54                	push   r12
    1965:	41 89 fc             	mov    r12d,edi
    1968:	55                   	push   rbp
    1969:	48 8d 2d 98 16 00 00 	lea    rbp,[rip+0x1698]        # 3008 <__do_global_dtors_aux_fini_array_entry>
    1970:	53                   	push   rbx
    1971:	4c 29 fd             	sub    rbp,r15
    1974:	48 83 ec 08          	sub    rsp,0x8
    1978:	e8 83 f6 ff ff       	call   1000 <_init>
    197d:	48 c1 fd 03          	sar    rbp,0x3
    1981:	74 1b                	je     199e <__libc_csu_init+0x4e>
    1983:	31 db                	xor    ebx,ebx
    1985:	0f 1f 00             	nop    DWORD PTR [rax]
    1988:	4c 89 f2             	mov    rdx,r14
    198b:	4c 89 ee             	mov    rsi,r13
    198e:	44 89 e7             	mov    edi,r12d
    1991:	41 ff 14 df          	call   QWORD PTR [r15+rbx*8]
    1995:	48 83 c3 01          	add    rbx,0x1
    1999:	48 39 dd             	cmp    rbp,rbx
    199c:	75 ea                	jne    1988 <__libc_csu_init+0x38>
    199e:	48 83 c4 08          	add    rsp,0x8
    19a2:	5b                   	pop    rbx
    19a3:	5d                   	pop    rbp
    19a4:	41 5c                	pop    r12
    19a6:	41 5d                	pop    r13
    19a8:	41 5e                	pop    r14
    19aa:	41 5f                	pop    r15
    19ac:	c3                   	ret
    19ad:	0f 1f 00             	nop    DWORD PTR [rax]

00000000000019b0 <__libc_csu_fini>:
    19b0:	c3                   	ret

Disassembly of section .fini:

00000000000019b4 <_fini>:
    19b4:	48 83 ec 08          	sub    rsp,0x8
    19b8:	48 83 c4 08          	add    rsp,0x8
    19bc:	c3                   	ret
