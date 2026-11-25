; function start found at 004209c3
004209c3  b5 71                          mov     ch, 0x71                            
004209c5  00 3b                          add     byte ptr [ebx], bh                  
004209c7  c3                             ret                                         
004209c8  74 06                          je      0x4209d0                               ; -> sub_004209d0
004209ca  8b 10                          mov     edx, dword ptr [eax]                
004209cc  50                             push    eax                                 
004209cd  ff 52 08                       call    dword ptr [edx + 8]                 
004209d0  a1 08 b6 71 00                 mov     eax, dword ptr [0x71b608]           
004209d5  89 1d d8 b5 71 00              mov     dword ptr [0x71b5d8], ebx           
004209db  3b c3                          cmp     eax, ebx                            
004209dd  74 06                          je      0x4209e5                               ; -> sub_004209e5
004209df  8b 08                          mov     ecx, dword ptr [eax]                
004209e1  50                             push    eax                                 
004209e2  ff 51 20                       call    dword ptr [ecx + 0x20]              
004209e5  a1 0c b6 71 00                 mov     eax, dword ptr [0x71b60c]           
004209ea  89 1d 08 b6 71 00              mov     dword ptr [0x71b608], ebx           
004209f0  3b c3                          cmp     eax, ebx                            
004209f2  74 06                          je      0x4209fa                               ; -> sub_004209fa
004209f4  8b 10                          mov     edx, dword ptr [eax]                
004209f6  50                             push    eax                                 
004209f7  ff 52 20                       call    dword ptr [edx + 0x20]              
004209fa  a1 04 b6 71 00                 mov     eax, dword ptr [0x71b604]           
004209ff  89 1d 0c b6 71 00              mov     dword ptr [0x71b60c], ebx           
00420a05  3b c3                          cmp     eax, ebx                            
00420a07  74 06                          je      0x420a0f                               ; -> sub_00420a0f
00420a09  8b 08                          mov     ecx, dword ptr [eax]                
00420a0b  50                             push    eax                                 
00420a0c  ff 51 08                       call    dword ptr [ecx + 8]                 
00420a0f  b9 60 6a 71 00                 mov     ecx, 0x716a60                       
00420a14  89 1d 04 b6 71 00              mov     dword ptr [0x71b604], ebx           
00420a1a  e8 c1 32 fe ff                 call    0x403ce0                               ; -> sub_00403ce0
00420a1f  a1 10 b6 71 00                 mov     eax, dword ptr [0x71b610]           
00420a24  3b c3                          cmp     eax, ebx                            
00420a26  74 17                          je      0x420a3f                               ; -> sub_00420a3f
00420a28  8b 10                          mov     edx, dword ptr [eax]                
00420a2a  50                             push    eax                                 
00420a2b  ff 52 10                       call    dword ptr [edx + 0x10]              
00420a2e  a1 10 b6 71 00                 mov     eax, dword ptr [0x71b610]           
00420a33  50                             push    eax                                 
00420a34  8b 08                          mov     ecx, dword ptr [eax]                
00420a36  ff 51 08                       call    dword ptr [ecx + 8]                 
00420a39  89 1d 10 b6 71 00              mov     dword ptr [0x71b610], ebx           
00420a3f  a1 b8 b5 71 00                 mov     eax, dword ptr [0x71b5b8]           
00420a44  3b c3                          cmp     eax, ebx                            
00420a46  74 3c                          je      0x420a84                               ; -> sub_00420a84
00420a48  8b 10                          mov     edx, dword ptr [eax]                
00420a4a  50                             push    eax                                 
00420a4b  ff 52 4c                       call    dword ptr [edx + 0x4c]              
00420a4e  b8 10 3b 52 00                 mov     eax, 0x523b10                       
00420a53  85 c0                          test    eax, eax                            
00420a55  74 28                          je      0x420a7f                               ; -> sub_00420a7f
00420a57  39 1d 38 3b 52 00              cmp     dword ptr [0x523b38], ebx           
00420a5d  74 20                          je      0x420a7f                               ; -> sub_00420a7f
00420a5f  b9 10 3b 52 00                 mov     ecx, 0x523b10                       
00420a64  e8 77 4d ff ff                 call    0x4157e0                               ; -> sub_004157e0
00420a69  3b c3                          cmp     eax, ebx                            
00420a6b  74 12                          je      0x420a7f                               ; -> sub_00420a7f
00420a6d  8b 0d b8 b5 71 00              mov     ecx, dword ptr [0x71b5b8]           
00420a73  8b 40 1c                       mov     eax, dword ptr [eax + 0x1c]         
00420a76  6a 08                          push    8                                   
00420a78  50                             push    eax                                 
00420a79  8b 11                          mov     edx, dword ptr [ecx]                
00420a7b  51                             push    ecx                                 
00420a7c  ff 52 50                       call    dword ptr [edx + 0x50]              
00420a7f  a1 b8 b5 71 00                 mov     eax, dword ptr [0x71b5b8]           
00420a84  8b 0d bc b5 71 00              mov     ecx, dword ptr [0x71b5bc]           
00420a8a  3b cb                          cmp     ecx, ebx                            
00420a8c  74 0b                          je      0x420a99                               ; -> sub_00420a99
00420a8e  8b 11                          mov     edx, dword ptr [ecx]                
00420a90  51                             push    ecx                                 
00420a91  ff 52 08                       call    dword ptr [edx + 8]                 
00420a94  a1 b8 b5 71 00                 mov     eax, dword ptr [0x71b5b8]           
00420a99  8b 0d c0 b5 71 00              mov     ecx, dword ptr [0x71b5c0]           
00420a9f  89 1d bc b5 71 00              mov     dword ptr [0x71b5bc], ebx           
00420aa5  3b cb                          cmp     ecx, ebx                            
00420aa7  74 0b                          je      0x420ab4                               ; -> sub_00420ab4
00420aa9  8b 01                          mov     eax, dword ptr [ecx]                
00420aab  51                             push    ecx                                 
00420aac  ff 50 08                       call    dword ptr [eax + 8]                 
00420aaf  a1 b8 b5 71 00                 mov     eax, dword ptr [0x71b5b8]           
00420ab4  3b c3                          cmp     eax, ebx                            
00420ab6  89 1d c0 b5 71 00              mov     dword ptr [0x71b5c0], ebx           
00420abc  74 06                          je      0x420ac4                               ; -> sub_00420ac4
00420abe  8b 08                          mov     ecx, dword ptr [eax]                
00420ac0  50                             push    eax                                 
00420ac1  ff 51 08                       call    dword ptr [ecx + 8]                 
00420ac4  a1 b4 b5 71 00                 mov     eax, dword ptr [0x71b5b4]           
00420ac9  89 1d b8 b5 71 00              mov     dword ptr [0x71b5b8], ebx           
00420acf  3b c3                          cmp     eax, ebx                            
00420ad1  74 06                          je      0x420ad9                               ; -> sub_00420ad9
00420ad3  8b 10                          mov     edx, dword ptr [eax]                
00420ad5  50                             push    eax                                 
00420ad6  ff 52 08                       call    dword ptr [edx + 8]                 
00420ad9  b9 f8 69 71 00                 mov     ecx, 0x7169f8                       
00420ade  89 1d b4 b5 71 00              mov     dword ptr [0x71b5b4], ebx           
00420ae4  e8 a7 2c 01 00                 call    0x433790                               ; -> sub_00433790
00420ae9  ff 15 f8 1a 8b 00              call    dword ptr [0x8b1af8]                   ; ole32.dll!CoUninitialize
00420aef  5f                             pop     edi                                 
00420af0  89 1d b4 b5 71 00              mov     dword ptr [0x71b5b4], ebx           
00420af6  5e                             pop     esi                                 
00420af7  5b                             pop     ebx                                 
00420af8  c3                             ret                                         
00420af9  90                             nop                                         
00420afa  90                             nop                                         
00420afb  90                             nop                                         
00420afc  90                             nop                                         
00420afd  90                             nop                                         
00420afe  90                             nop                                         
00420aff  90                             nop                                         
00420b00  6a ff                          push    -1                                  
00420b02  68 d7 95 48 00                 push    0x4895d7                            
00420b07  64 a1 00 00 00 00              mov     eax, dword ptr fs:[0]               
00420b0d  50                             push    eax                                 
00420b0e  64 89 25 00 00 00 00           mov     dword ptr fs:[0], esp               
00420b15  83 ec 0c                       sub     esp, 0xc                            
00420b18  8b 0d a8 63 4a 00              mov     ecx, dword ptr [0x4a63a8]              ; "糲J"
00420b1e  56                             push    esi                                 
00420b1f  c7 44 24 08 00 00 00 00        mov     dword ptr [esp + 8], 0              
00420b27  89 4c 24 04                    mov     dword ptr [esp + 4], ecx            
00420b2b  8b 44 24 24                    mov     eax, dword ptr [esp + 0x24]         
00420b2f  c7 44 24 18 01 00 00 00        mov     dword ptr [esp + 0x18], 1           
00420b37  83 f8 1e                       cmp     eax, 0x1e                           
00420b3a  0f 87 4b 02 00 00              ja      0x420d8b                               ; -> sub_00420d8b
00420b40  ff 24 85 14 0e 42 00           jmp     dword ptr [eax*4 + 0x420e14]        
00420b47  68 48 0d 4a 00                 push    0x4a0d48                               ; "m00"
00420b4c  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420b50  e8 00 ef 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420b55  e9 81 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420b5a  68 44 0d 4a 00                 push    0x4a0d44                               ; "m01"
00420b5f  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420b63  e8 ed ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420b68  e9 6e 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420b6d  68 40 0d 4a 00                 push    0x4a0d40                               ; "m02"
00420b72  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420b76  e8 da ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420b7b  e9 5b 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420b80  68 3c 0d 4a 00                 push    0x4a0d3c                               ; "m03"
00420b85  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420b89  e8 c7 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420b8e  e9 48 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420b93  68 38 0d 4a 00                 push    0x4a0d38                               ; "m04"
00420b98  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420b9c  e8 b4 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420ba1  e9 35 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420ba6  68 34 0d 4a 00                 push    0x4a0d34                               ; "m05"
00420bab  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420baf  e8 a1 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420bb4  e9 22 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420bb9  68 30 0d 4a 00                 push    0x4a0d30                               ; "m06"
00420bbe  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420bc2  e8 8e ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420bc7  e9 0f 02 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420bcc  68 2c 0d 4a 00                 push    0x4a0d2c                               ; "m07"
00420bd1  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420bd5  e8 7b ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420bda  e9 fc 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420bdf  68 28 0d 4a 00                 push    0x4a0d28                               ; "m08"
00420be4  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420be8  e8 68 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420bed  e9 e9 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420bf2  68 24 0d 4a 00                 push    0x4a0d24                               ; "m09"
00420bf7  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420bfb  e8 55 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c00  e9 d6 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c05  68 20 0d 4a 00                 push    0x4a0d20                               ; "m10"
00420c0a  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c0e  e8 42 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c13  e9 c3 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c18  68 1c 0d 4a 00                 push    0x4a0d1c                               ; "m11"
00420c1d  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c21  e8 2f ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c26  e9 b0 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c2b  68 18 0d 4a 00                 push    0x4a0d18                               ; "m12"
00420c30  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c34  e8 1c ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c39  e9 9d 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c3e  68 14 0d 4a 00                 push    0x4a0d14                               ; "m13"
00420c43  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c47  e8 09 ee 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c4c  e9 8a 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c51  68 10 0d 4a 00                 push    0x4a0d10                               ; "m14"
00420c56  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c5a  e8 f6 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c5f  e9 77 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c64  68 0c 0d 4a 00                 push    0x4a0d0c                               ; "m15"
00420c69  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c6d  e8 e3 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c72  e9 64 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c77  68 08 0d 4a 00                 push    0x4a0d08                               ; "m16"
00420c7c  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c80  e8 d0 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c85  e9 51 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c8a  68 04 0d 4a 00                 push    0x4a0d04                               ; "m17"
00420c8f  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420c93  e8 bd ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420c98  e9 3e 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420c9d  68 00 0d 4a 00                 push    0x4a0d00                               ; "m18"
00420ca2  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420ca6  e8 aa ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420cab  e9 2b 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420cb0  68 fc 0c 4a 00                 push    0x4a0cfc                               ; "m19"
00420cb5  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420cb9  e8 97 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420cbe  e9 18 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420cc3  68 f8 0c 4a 00                 push    0x4a0cf8                               ; "m20"
00420cc8  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420ccc  e8 84 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420cd1  e9 05 01 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420cd6  68 f4 0c 4a 00                 push    0x4a0cf4                               ; "m21"
00420cdb  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420cdf  e8 71 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420ce4  e9 f2 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420ce9  68 f0 0c 4a 00                 push    0x4a0cf0                               ; "m22"
00420cee  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420cf2  e8 5e ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420cf7  e9 df 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420cfc  68 ec 0c 4a 00                 push    0x4a0cec                               ; "m23"
00420d01  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d05  e8 4b ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d0a  e9 cc 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420d0f  68 e8 0c 4a 00                 push    0x4a0ce8                               ; "m24"
00420d14  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d18  e8 38 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d1d  e9 b9 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420d22  68 e4 0c 4a 00                 push    0x4a0ce4                               ; "m25"
00420d27  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d2b  e8 25 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d30  e9 a6 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420d35  68 e0 0c 4a 00                 push    0x4a0ce0                               ; "m26"
00420d3a  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d3e  e8 12 ed 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d43  e9 93 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420d48  68 dc 0c 4a 00                 push    0x4a0cdc                               ; "m27"
00420d4d  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d51  e8 ff ec 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d56  e9 80 00 00 00                 jmp     0x420ddb                               ; -> sub_00420ddb
00420d5b  68 d8 0c 4a 00                 push    0x4a0cd8                               ; "m28"
00420d60  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d64  e8 ec ec 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d69  eb 70                          jmp     0x420ddb                               ; -> sub_00420ddb
00420d6b  68 d4 0c 4a 00                 push    0x4a0cd4                               ; "m29"
00420d70  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d74  e8 dc ec 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d79  eb 60                          jmp     0x420ddb                               ; -> sub_00420ddb
00420d7b  68 d0 0c 4a 00                 push    0x4a0cd0                               ; "m30"
00420d80  8d 4c 24 08                    lea     ecx, [esp + 8]                      
00420d84  e8 cc ec 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420d89  eb 50                          jmp     0x420ddb                               ; -> sub_00420ddb
00420d8b  89 4c 24 24                    mov     dword ptr [esp + 0x24], ecx         
00420d8f  50                             push    eax                                 
00420d90  8d 44 24 28                    lea     eax, [esp + 0x28]                   
00420d94  68 a0 0c 4a 00                 push    0x4a0ca0                               ; "Wrong level to load. Unable to open level %d"
00420d99  50                             push    eax                                 
00420d9a  c6 44 24 24 02                 mov     byte ptr [esp + 0x24], 2            
00420d9f  e8 0e d3 05 00                 call    0x47e0b2                               ; -> sub_0047e0b2
00420da4  83 c4 08                       add     esp, 8                              
00420da7  8d 54 24 28                    lea     edx, [esp + 0x28]                   
00420dab  8b cc                          mov     ecx, esp                            
00420dad  89 64 24 10                    mov     dword ptr [esp + 0x10], esp         
00420db1  52                             push    edx                                 
00420db2  e8 d6 e8 05 00                 call    0x47f68d                               ; -> sub_0047f68d
00420db7  e8 94 4e ff ff                 call    0x415c50                               ; -> sub_00415c50
00420dbc  83 c4 04                       add     esp, 4                              
00420dbf  8d 4c 24 04                    lea     ecx, [esp + 4]                      
00420dc3  68 44 0d 4a 00                 push    0x4a0d44                               ; "m01"
00420dc8  e8 88 ec 05 00                 call    0x47fa55                               ; -> sub_0047fa55
00420dcd  8d 4c 24 24                    lea     ecx, [esp + 0x24]                   
00420dd1  c6 44 24 18 01                 mov     byte ptr [esp + 0x18], 1            
00420dd6  e8 3d eb 05 00                 call    0x47f918                               ; -> sub_0047f918
00420ddb  8b 74 24 20                    mov     esi, dword ptr [esp + 0x20]         
00420ddf  8d 44 24 04                    lea     eax, [esp + 4]                      
00420de3  50                             push    eax                                 
00420de4  8b ce                          mov     ecx, esi                            
00420de6  e8 a2 e8 05 00                 call    0x47f68d                               ; -> sub_0047f68d
00420deb  c7 44 24 08 01 00 00 00        mov     dword ptr [esp + 8], 1              
00420df3  8d 4c 24 04                    lea     ecx, [esp + 4]                      
00420df7  c6 44 24 18 00                 mov     byte ptr [esp + 0x18], 0            
