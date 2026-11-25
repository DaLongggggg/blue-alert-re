; function start found at 0042f523
0042f523  89 64 24 18                    mov     dword ptr [esp + 0x18], esp         
0042f527  68 08 23 4a 00                 push    0x4a2308                               ; "data\nonexisting.wav"
0042f52c  e8 55 04 05 00                 call    0x47f986                               ; -> sub_0047f986
0042f531  b9 60 6a 71 00                 mov     ecx, 0x716a60                       
0042f536  e8 b5 62 fd ff                 call    0x4057f0                               ; -> sub_004057f0
0042f53b  68 cc 22 4a 00                 push    0x4a22cc                               ; "i 欢迎你来到蓝色警戒教练课堂。请点击右边的箭头继续课程。"
0042f540  b9 84 7b 72 00                 mov     ecx, 0x727b84                       
0042f545  89 3d 34 b8 71 00              mov     dword ptr [0x71b834], edi           
0042f54b  89 3d 30 b8 71 00              mov     dword ptr [0x71b830], edi           
0042f551  89 3d 2c b8 71 00              mov     dword ptr [0x71b82c], edi           
0042f557  89 3d 28 b8 71 00              mov     dword ptr [0x71b828], edi           
0042f55d  e8 f3 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f562  68 ac 22 4a 00                 push    0x4a22ac                               ; "! 点击右边的箭头环视整个地图。"
0042f567  b9 88 7b 72 00                 mov     ecx, 0x727b88                       
0042f56c  e8 e4 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f571  68 88 22 4a 00                 push    0x4a2288                               ; "! 你也可以用方向键环视整个地图。"
0042f576  b9 8c 7b 72 00                 mov     ecx, 0x727b8c                       
0042f57b  e8 d5 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f580  68 78 22 4a 00                 push    0x4a2278                               ; "i 课程A: 飞碟。"
0042f585  b9 90 7b 72 00                 mov     ecx, 0x727b90                       
0042f58a  e8 c6 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f58f  68 44 22 4a 00                 push    0x4a2244                               ; "! 这是你的飞碟。选择它，然后点击目的地来移动飞碟。"
0042f594  b9 94 7b 72 00                 mov     ecx, 0x727b94                       
0042f599  e8 b7 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f59e  68 f8 21 4a 00                 push    0x4a21f8                               ; "i 飞碟是最重要的作战单位。它有三个基本特征。可以用它来占领，升级，修理。"
0042f5a3  b9 98 7b 72 00                 mov     ecx, 0x727b98                       
0042f5a8  e8 a8 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5ad  68 c0 21 4a 00                 push    0x4a21c0                               ; "! 现在试着占领这个轻型工厂。选择飞碟，然后点击工厂。"
0042f5b2  b9 9c 7b 72 00                 mov     ecx, 0x727b9c                       
0042f5b7  e8 99 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5bc  68 64 21 4a 00                 push    0x4a2164                               ; "! 这个轻型工厂会制造出陆地作战单位。它们的制造是自动的，不用花费任何东西。请等到进度条满。"
0042f5c1  b9 a0 7b 72 00                 mov     ecx, 0x727ba0                       
0042f5c6  e8 8a 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5cb  68 ec 20 4a 00                 push    0x4a20ec                               ; "i 同时，为了制造出更多的作战单位，你也可以用飞碟升级工厂。绿色箭头的显示表示可以升级工厂了。现在，升级这个轻型工厂。"
0042f5d0  b9 a4 7b 72 00                 mov     ecx, 0x727ba4                       
0042f5d5  e8 7b 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5da  68 98 20 4a 00                 push    0x4a2098                               ; "! 飞碟也可以修理被破坏的建筑。（请按鼠标右键切换修理和升级模式，修理这个建筑。）"
0042f5df  b9 a8 7b 72 00                 mov     ecx, 0x727ba8                       
0042f5e4  e8 6c 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5e9  68 88 20 4a 00                 push    0x4a2088                               ; "i 课程B:炮塔。"
0042f5ee  b9 ac 7b 72 00                 mov     ecx, 0x727bac                       
0042f5f3  e8 5d 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f5f8  68 20 20 4a 00                 push    0x4a2020                               ; "i 这是你的金矿。你可以用制造的金钱来生产保护建筑的炮塔。你也可以升级这个建筑。它会加速你的金钱的流入。"
0042f5fd  b9 b0 7b 72 00                 mov     ecx, 0x727bb0                       
0042f602  e8 4e 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f607  68 90 1f 4a 00                 push    0x4a1f90                               ; "! 现在，你有足够的钱建造你的第一个炮塔了。当敌人在炮塔射程内时，炮塔会自动向敌人射击。点击炮塔图标，把它放在建筑的附近，毁掉敌人的作战单位。"
0042f60c  b9 b4 7b 72 00                 mov     ecx, 0x727bb4                       
0042f611  e8 3f 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f616  68 7c 1f 4a 00                 push    0x4a1f7c                               ; "i 课程C:空中力量."
0042f61b  b9 b8 7b 72 00                 mov     ecx, 0x727bb8                       
0042f620  e8 30 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f625  68 34 1f 4a 00                 push    0x4a1f34                               ; "! 这是空中单位生产基地。你可以使用它生产出空中力量。请等到进度条满。"
0042f62a  b9 bc 7b 72 00                 mov     ecx, 0x727bbc                       
0042f62f  e8 21 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f634  68 24 1f 4a 00                 push    0x4a1f24                               ; "! 点击图标。"
0042f639  b9 c0 7b 72 00                 mov     ecx, 0x727bc0                       
0042f63e  e8 12 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f643  68 e4 1e 4a 00                 push    0x4a1ee4                               ; "! 用它去轰炸敌人的作战单位。只用几次，你就会把敌人全部消灭。"
0042f648  b9 c4 7b 72 00                 mov     ecx, 0x727bc4                       
0042f64d  e8 03 04 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f652  68 d0 1e 4a 00                 push    0x4a1ed0                               ; "i 课程D:技术水平。"
0042f657  b9 c8 7b 72 00                 mov     ecx, 0x727bc8                       
0042f65c  e8 f4 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f661  68 60 1e 4a 00                 push    0x4a1e60                               ; "i 这是你的轻型工厂。它能制造轻型作战单位。它也可以制造更强的中型作战单位，但它需要研究指数来提高它的技术水平。"
0042f666  b9 cc 7b 72 00                 mov     ecx, 0x727bcc                       
0042f66b  e8 e5 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f670  68 0c 1e 4a 00                 push    0x4a1e0c                               ; "! 现在你拥有了400研究指数。要获得更多的研究指数，你必须占领位于下方的太阳能搜集器。"
0042f675  b9 d0 7b 72 00                 mov     ecx, 0x727bd0                       
0042f67a  e8 d6 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f67f  68 88 1d 4a 00                 push    0x4a1d88                               ; "! 现在，选择轻型工厂，注意屏幕右边的作战单位图标。当你有500分的时候，就可以升级你的工厂了。技术水平图标会显示在作战单位图标的旁边。"
0042f684  b9 d4 7b 72 00                 mov     ecx, 0x727bd4                       
0042f689  e8 c7 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f68e  68 50 1d 4a 00                 push    0x4a1d50                               ; "! 现在，点击技术水平图标，一种新的武器会自动开始制造。"
0042f693  b9 d8 7b 72 00                 mov     ecx, 0x727bd8                       
0042f698  e8 b8 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f69d  68 38 1d 4a 00                 push    0x4a1d38                               ; "i 课程E:最后的任务。"
0042f6a2  b9 dc 7b 72 00                 mov     ecx, 0x727bdc                       
0042f6a7  e8 a9 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f6ac  68 10 1d 4a 00                 push    0x4a1d10                               ; "! 这是你的总部。任务是毁掉敌人的基地。"
0042f6b1  b9 e0 7b 72 00                 mov     ecx, 0x727be0                       
0042f6b6  e8 9a 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f6bb  68 a4 1c 4a 00                 push    0x4a1ca4                               ; "! 哦，一些建筑有卫星保护系统。所以你应该用陆地作战单位攻击这些建筑。占领这些工厂，然后，毁掉敌人的基地。"
0042f6c0  b9 e4 7b 72 00                 mov     ecx, 0x727be4                       
0042f6c5  e8 8b 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f6ca  68 80 1c 4a 00                 push    0x4a1c80                               ; "! 很好！你成功地掌握了全部课程。"
0042f6cf  b9 e8 7b 72 00                 mov     ecx, 0x727be8                       
0042f6d4  e8 7c 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f6d9  68 7c 1c 4a 00                 push    0x4a1c7c                               ; "_  "
0042f6de  b9 ec 7b 72 00                 mov     ecx, 0x727bec                       
0042f6e3  e8 6d 03 05 00                 call    0x47fa55                               ; -> sub_0047fa55
0042f6e8  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f6ee  6a 13                          push    0x13                                
0042f6f0  8b c1                          mov     eax, ecx                            
0042f6f2  55                             push    ebp                                 
0042f6f3  c1 e0 05                       shl     eax, 5                              
0042f6f6  03 c1                          add     eax, ecx                            
0042f6f8  6a ed                          push    -0x13                               
0042f6fa  6a eb                          push    -0x15                               
0042f6fc  c6 05 2c 7c 72 00 00           mov     byte ptr [0x727c2c], 0              
0042f703  8d 04 40                       lea     eax, [eax + eax*2]                  
0042f706  8d 0c 81                       lea     ecx, [ecx + eax*4]                  
0042f709  8d 0c cd 34 96 6b 00           lea     ecx, [ecx*8 + 0x6b9634]             
0042f710  e8 3b b4 01 00                 call    0x44ab50                               ; -> sub_0044ab50
0042f715  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f71b  6a d3                          push    -0x2d                               
0042f71d  8b c1                          mov     eax, ecx                            
0042f71f  68 2d 01 00 00                 push    0x12d                               
0042f724  c1 e0 05                       shl     eax, 5                              
0042f727  03 c1                          add     eax, ecx                            
0042f729  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f72c  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f72f  8d 0c c5 34 96 6b 00           lea     ecx, [eax*8 + 0x6b9634]             
0042f736  e8 f5 b2 01 00                 call    0x44aa30                               ; -> sub_0044aa30
0042f73b  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f741  57                             push    edi                                 
0042f742  8b c1                          mov     eax, ecx                            
0042f744  57                             push    edi                                 
0042f745  c1 e0 05                       shl     eax, 5                              
0042f748  03 c1                          add     eax, ecx                            
0042f74a  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f74d  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f750  8d 04 c5 34 96 6b 00           lea     eax, [eax*8 + 0x6b9634]             
0042f757  c6 40 5d 01                    mov     byte ptr [eax + 0x5d], 1            
0042f75b  8b 0d 80 1b 61 00              mov     ecx, dword ptr [0x611b80]           
0042f761  51                             push    ecx                                 
0042f762  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f768  8b c1                          mov     eax, ecx                            
0042f76a  c1 e0 05                       shl     eax, 5                              
0042f76d  03 c1                          add     eax, ecx                            
0042f76f  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f772  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f775  8d 0c c5 34 96 6b 00           lea     ecx, [eax*8 + 0x6b9634]             
0042f77c  e8 cf b2 01 00                 call    0x44aa50                               ; -> sub_0044aa50
0042f781  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f787  be 58 7b 72 00                 mov     esi, 0x727b58                       
0042f78c  8b c1                          mov     eax, ecx                            
0042f78e  c1 e0 05                       shl     eax, 5                              
0042f791  03 c1                          add     eax, ecx                            
0042f793  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f796  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f799  8d 04 c5 34 96 6b 00           lea     eax, [eax*8 + 0x6b9634]             
0042f7a0  c7 40 58 21 00 00 00           mov     dword ptr [eax + 0x58], 0x21        
0042f7a7  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f7ad  8b c1                          mov     eax, ecx                            
0042f7af  c1 e0 05                       shl     eax, 5                              
0042f7b2  03 c1                          add     eax, ecx                            
0042f7b4  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f7b7  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f7ba  c6 04 c5 94 96 6b 00 00        mov     byte ptr [eax*8 + 0x6b9694], 0      
0042f7c2  8b ce                          mov     ecx, esi                            
0042f7c4  e8 da 00 05 00                 call    0x47f8a3                               ; -> sub_0047f8a3
0042f7c9  83 c6 04                       add     esi, 4                              
0042f7cc  81 fe 80 7b 72 00              cmp     esi, 0x727b80                       
0042f7d2  7c ee                          jl      0x42f7c2                               ; -> sub_0042f7c2
0042f7d4  a1 b8 6d 71 00                 mov     eax, dword ptr [0x716db8]           
0042f7d9  3b c7                          cmp     eax, edi                            
0042f7db  0f 8e 5c 01 00 00              jle     0x42f93d                               ; -> sub_0042f93d
0042f7e1  8b 0d 34 b8 71 00              mov     ecx, dword ptr [0x71b834]           
0042f7e7  8b 35 30 b8 71 00              mov     esi, dword ptr [0x71b830]           
0042f7ed  8b 15 28 b8 71 00              mov     edx, dword ptr [0x71b828]           
0042f7f3  8b d8                          mov     ebx, eax                            
0042f7f5  a1 2c b8 71 00                 mov     eax, dword ptr [0x71b82c]           
0042f7fa  4e                             dec     esi                                 
0042f7fb  79 0d                          jns     0x42f80a                               ; -> sub_0042f80a
0042f7fd  41                             inc     ecx                                 
0042f7fe  be 05 00 00 00                 mov     esi, 5                              
0042f803  83 f9 10                       cmp     ecx, 0x10                           
0042f806  7c 02                          jl      0x42f80a                               ; -> sub_0042f80a
0042f808  33 c9                          xor     ecx, ecx                            
0042f80a  4a                             dec     edx                                 
0042f80b  79 0d                          jns     0x42f81a                               ; -> sub_0042f81a
0042f80d  40                             inc     eax                                 
0042f80e  ba 03 00 00 00                 mov     edx, 3                              
0042f813  83 f8 10                       cmp     eax, 0x10                           
0042f816  7c 02                          jl      0x42f81a                               ; -> sub_0042f81a
0042f818  33 c0                          xor     eax, eax                            
0042f81a  4b                             dec     ebx                                 
0042f81b  75 dd                          jne     0x42f7fa                               ; -> sub_0042f7fa
0042f81d  a3 2c b8 71 00                 mov     dword ptr [0x71b82c], eax           
0042f822  89 15 28 b8 71 00              mov     dword ptr [0x71b828], edx           
0042f828  89 0d 34 b8 71 00              mov     dword ptr [0x71b834], ecx           
0042f82e  89 35 30 b8 71 00              mov     dword ptr [0x71b830], esi           
0042f834  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f83a  be 7a 00 00 00                 mov     esi, 0x7a                           
0042f83f  8b d1                          mov     edx, ecx                            
0042f841  c1 e2 04                       shl     edx, 4                              
0042f844  03 d1                          add     edx, ecx                            
0042f846  8d 14 52                       lea     edx, [edx + edx*2]                  
0042f849  8d 14 51                       lea     edx, [ecx + edx*2]                  
0042f84c  39 34 d5 50 b5 70 00           cmp     dword ptr [edx*8 + 0x70b550], esi   
0042f853  74 07                          je      0x42f85c                               ; -> sub_0042f85c
0042f855  33 c0                          xor     eax, eax                            
0042f857  a3 2c b8 71 00                 mov     dword ptr [0x71b82c], eax           
0042f85c  8b 14 85 80 1b 61 00           mov     edx, dword ptr [eax*4 + 0x611b80]   
0042f863  8b c1                          mov     eax, ecx                            
0042f865  c1 e0 05                       shl     eax, 5                              
0042f868  03 c1                          add     eax, ecx                            
0042f86a  8d 04 40                       lea     eax, [eax + eax*2]                  
0042f86d  8d 0c 81                       lea     ecx, [ecx + eax*4]                  
0042f870  8d 04 cd 34 96 6b 00           lea     eax, [ecx*8 + 0x6b9634]             
0042f877  89 50 2c                       mov     dword ptr [eax + 0x2c], edx         
0042f87a  a1 b0 b5 71 00                 mov     eax, dword ptr [0x71b5b0]           
0042f87f  8b c8                          mov     ecx, eax                            
0042f881  c1 e1 05                       shl     ecx, 5                              
0042f884  03 c8                          add     ecx, eax                            
0042f886  8d 14 49                       lea     edx, [ecx + ecx*2]                  
0042f889  8d 0c 90                       lea     ecx, [eax + edx*4]                  
0042f88c  c1 e1 03                       shl     ecx, 3                              
0042f88f  80 b9 94 96 6b 00 01           cmp     byte ptr [ecx + 0x6b9694], 1        
0042f896  75 6f                          jne     0x42f907                               ; -> sub_0042f907
0042f898  8d 89 34 96 6b 00              lea     ecx, [ecx + 0x6b9634]               
0042f89e  e8 9d b5 01 00                 call    0x44ae40                               ; -> sub_0044ae40
0042f8a3  8b 0d b0 b5 71 00              mov     ecx, dword ptr [0x71b5b0]           
0042f8a9  8b c1                          mov     eax, ecx                            
0042f8ab  c1 e0 04                       shl     eax, 4                              
0042f8ae  03 c1                          add     eax, ecx                            
0042f8b0  8d 04 40                       lea     eax, [eax + eax*2]                  
0042f8b3  8d 04 41                       lea     eax, [ecx + eax*2]                  
0042f8b6  c1 e0 03                       shl     eax, 3                              
0042f8b9  39 b0 50 b5 70 00              cmp     dword ptr [eax + 0x70b550], esi     
0042f8bf  0f 85 08 0f 00 00              jne     0x4307cd                               ; -> sub_004307cd
0042f8c5  80 b8 f3 b3 70 00 01           cmp     byte ptr [eax + 0x70b3f3], 1        
0042f8cc  0f 85 fb 0e 00 00              jne     0x4307cd                               ; -> sub_004307cd
0042f8d2  8b c1                          mov     eax, ecx                            
0042f8d4  6a 05                          push    5                                   
0042f8d6  c1 e0 05                       shl     eax, 5                              
0042f8d9  03 c1                          add     eax, ecx                            
0042f8db  8d 14 40                       lea     edx, [eax + eax*2]                  
0042f8de  8d 04 91                       lea     eax, [ecx + edx*4]                  
0042f8e1  8d 0c c5 34 96 6b 00           lea     ecx, [eax*8 + 0x6b9634]             
0042f8e8  e8 23 b1 01 00                 call    0x44aa10                               ; -> sub_0044aa10
0042f8ed  a1 b0 b5 71 00                 mov     eax, dword ptr [0x71b5b0]           
0042f8f2  8b c8                          mov     ecx, eax                            
0042f8f4  c1 e1 05                       shl     ecx, 5                              
0042f8f7  03 c8                          add     ecx, eax                            
0042f8f9  8d 0c 49                       lea     ecx, [ecx + ecx*2]                  
0042f8fc  8d 14 88                       lea     edx, [eax + ecx*4]                  
