; function start found at 00437065
00437065  89 64 24 34                    mov     dword ptr [esp + 0x34], esp         
00437069  68 04 0c 4a 00                 push    0x4a0c04                               ; "sprites2\menu\lands_buttons"
0043706e  e8 13 59 04 00                 call    0x47c986                               ; -> sub_0047c986
00437073  e8 e8 62 01 00                 call    0x44d360                               ; -> sub_0044d360
00437078  83 c4 10                       add     esp, 0x10                           
0043707b  e8 50 ce fe ff                 call    0x423ed0                               ; -> sub_00423ed0
00437080  50                             push    eax                                 
00437081  8b ce                          mov     ecx, esi                            
00437083  e8 c8 00 00 00                 call    0x437150                               ; -> sub_00437150
00437088  8b 0d f8 79 71 00              mov     ecx, dword ptr [0x7179f8]           
0043708e  8d 54 24 10                    lea     edx, [esp + 0x10]                   
00437092  8d 44 24 14                    lea     eax, [esp + 0x14]                   
00437096  52                             push    edx                                 
00437097  50                             push    eax                                 
00437098  51                             push    ecx                                 
00437099  e8 92 ef 01 00                 call    0x456030                               ; -> sub_00456030
0043709e  8b 6c 24 30                    mov     ebp, dword ptr [esp + 0x30]         
004370a2  83 c4 0c                       add     esp, 0xc                            
004370a5  89 1d ac 7f 72 00              mov     dword ptr [0x727fac], ebx           
004370ab  89 1d b0 7f 72 00              mov     dword ptr [0x727fb0], ebx           
004370b1  bf 01 00 00 00                 mov     edi, 1                              
004370b6  be 28 72 72 00                 mov     esi, 0x727228                       
004370bb  8a 87 c8 71 72 00              mov     al, byte ptr [edi + 0x7271c8]       
004370c1  3a c3                          cmp     al, bl                              
004370c3  74 0a                          je      0x4370cf                               ; -> sub_004370cf
004370c5  76 0d                          jbe     0x4370d4                               ; -> sub_004370d4
004370c7  3c 02                          cmp     al, 2                               
004370c9  77 09                          ja      0x4370d4                               ; -> sub_004370d4
004370cb  33 ed                          xor     ebp, ebp                            
004370cd  eb 05                          jmp     0x4370d4                               ; -> sub_004370d4
004370cf  bd 01 00 00 00                 mov     ebp, 1                              
004370d4  8b 54 24 10                    mov     edx, dword ptr [esp + 0x10]         
004370d8  8b 44 24 14                    mov     eax, dword ptr [esp + 0x14]         
004370dc  52                             push    edx                                 
004370dd  50                             push    eax                                 
004370de  8d 44 6d 00                    lea     eax, [ebp + ebp*2]                  
004370e2  8d 0c 80                       lea     ecx, [eax + eax*4]                  
004370e5  8d 14 4f                       lea     edx, [edi + ecx*2]                  
004370e8  8b 04 95 9c 72 72 00           mov     eax, dword ptr [edx*4 + 0x72729c]   
004370ef  50                             push    eax                                 
004370f0  53                             push    ebx                                 
004370f1  68 f0 00 00 00                 push    0xf0                                
004370f6  68 40 01 00 00                 push    0x140                               
004370fb  e8 70 66 01 00                 call    0x44d770                               ; -> sub_0044d770
00437100  8b 4c 24 28                    mov     ecx, dword ptr [esp + 0x28]         
00437104  8b 54 24 2c                    mov     edx, dword ptr [esp + 0x2c]         
00437108  8b 06                          mov     eax, dword ptr [esi]                
0043710a  51                             push    ecx                                 
0043710b  52                             push    edx                                 
0043710c  50                             push    eax                                 
0043710d  53                             push    ebx                                 
0043710e  68 f0 00 00 00                 push    0xf0                                
00437113  68 40 01 00 00                 push    0x140                               
00437118  e8 53 66 01 00                 call    0x44d770                               ; -> sub_0044d770
0043711d  83 c4 30                       add     esp, 0x30                           
00437120  83 c6 04                       add     esi, 4                              
00437123  47                             inc     edi                                 
00437124  81 fe 7c 72 72 00              cmp     esi, 0x72727c                       
0043712a  7e 8f                          jle     0x4370bb                               ; -> sub_004370bb
0043712c  8b 0d f8 79 71 00              mov     ecx, dword ptr [0x7179f8]           
00437132  51                             push    ecx                                 
00437133  e8 88 ef 01 00                 call    0x4560c0                               ; -> sub_004560c0
00437138  83 c4 04                       add     esp, 4                              
0043713b  b0 01                          mov     al, 1                               
0043713d  5f                             pop     edi                                 
0043713e  5e                             pop     esi                                 
0043713f  5d                             pop     ebp                                 
00437140  5b                             pop     ebx                                 
00437141  83 c4 10                       add     esp, 0x10                           
00437144  c2 04 00                       ret     4                                   
00437147  90                             nop                                         
00437148  90                             nop                                         
00437149  90                             nop                                         
0043714a  90                             nop                                         
0043714b  90                             nop                                         
0043714c  90                             nop                                         
0043714d  90                             nop                                         
0043714e  90                             nop                                         
0043714f  90                             nop                                         
00437150  53                             push    ebx                                 
00437151  8b 5c 24 08                    mov     ebx, dword ptr [esp + 8]            
00437155  55                             push    ebp                                 
00437156  56                             push    esi                                 
00437157  8a 83 c8 71 72 00              mov     al, byte ptr [ebx + 0x7271c8]       
0043715d  57                             push    edi                                 
0043715e  84 c0                          test    al, al                              
00437160  8b f1                          mov     esi, ecx                            
00437162  0f 84 46 02 00 00              je      0x4373ae                               ; -> sub_004373ae
00437168  8d 43 ff                       lea     eax, [ebx - 1]                      
0043716b  83 f8 15                       cmp     eax, 0x15                           
0043716e  0f 87 3a 02 00 00              ja      0x4373ae                               ; -> sub_004373ae
00437174  33 c9                          xor     ecx, ecx                            
00437176  8a 88 c8 75 43 00              mov     cl, byte ptr [eax + 0x4375c8]       
0043717c  ff 24 8d 98 75 43 00           jmp     dword ptr [ecx*4 + 0x437598]        
00437183  68 c4 18 4a 00                 push    0x4a18c4                               ; "领土 : 01   难度等级 : 2 / 10"
00437188  8d 4e 08                       lea     ecx, [esi + 8]                      
0043718b  e8 c5 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437190  68 b4 18 4a 00                 push    0x4a18b4                               ; "基地代号: X8A3"
00437195  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437198  e8 b8 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043719d  8d 7e 10                       lea     edi, [esi + 0x10]                   
004371a0  68 c8 17 4a 00                 push    0x4a17c8                            
004371a5  8b cf                          mov     ecx, edi                            
004371a7  e8 a9 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004371ac  68 94 17 4a 00                 push    0x4a1794                               ; "任务：收集1000点研究指数，升级工厂，消灭敌人总部。"
004371b1  e9 26 02 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
004371b6  68 74 17 4a 00                 push    0x4a1774                               ; "领土 : 02   难度等级 : 3 / 10"
004371bb  8d 4e 08                       lea     ecx, [esi + 8]                      
004371be  e8 92 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004371c3  68 64 17 4a 00                 push    0x4a1764                               ; "基地代号: E1B2"
004371c8  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
004371cb  e8 85 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004371d0  8d 7e 10                       lea     edi, [esi + 0x10]                   
004371d3  68 a8 16 4a 00                 push    0x4a16a8                               ; "我们得到消息雷曼先生藏在此区域的某个地方。因此，为完成此项任务，我们打算准备一队重型机器人，来破坏敌方所有的抵抗力量和建筑。需要特别注意，在此任务中没有援军，并且敌人的作战力量优于我方。"
004371d8  8b cf                          mov     ecx, edi                            
004371da  e8 76 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004371df  68 68 16 4a 00                 push    0x4a1668                               ; "任务：用少量的重型战斗机器人消灭敌方所有的作战单位和建筑。"
004371e4  e9 f3 01 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
004371e9  68 48 16 4a 00                 push    0x4a1648                               ; "领土 : 03   难度等级 : 3 / 10"
004371ee  8d 4e 08                       lea     ecx, [esi + 8]                      
004371f1  e8 5f 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004371f6  68 38 16 4a 00                 push    0x4a1638                               ; "基地代号: B2E8"
004371fb  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
004371fe  e8 52 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437203  8d 7e 10                       lea     edi, [esi + 0x10]                   
00437206  68 c0 15 4a 00                 push    0x4a15c0                               ; "这次任务是保护罗根炸弹通过这个地区，你只有几个作战单位随行。特别要注意敌人的空中力量会毫不留情的破坏你的护航行动的。"
0043720b  8b cf                          mov     ecx, edi                            
0043720d  e8 43 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437212  68 98 15 4a 00                 push    0x4a1598                               ; "任务：抵制敌人的进攻，完成护航任务。"
00437217  e9 c0 01 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
0043721c  68 78 15 4a 00                 push    0x4a1578                               ; "领土 : 04   难度等级 : 4 / 10"
00437221  8d 4e 08                       lea     ecx, [esi + 8]                      
00437224  e8 2c 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437229  68 68 15 4a 00                 push    0x4a1568                               ; "基地代号: P4C7"
0043722e  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437231  e8 1f 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437236  8d 7e 10                       lea     edi, [esi + 0x10]                   
00437239  68 c8 14 4a 00                 push    0x4a14c8                               ; "在这个任务中，敌人的基地有很强的防御系统。你的工厂能生产破坏性极强的罗根炸弹，再借助3个飞碟的帮助，将有效破坏敌人的防御系统。你必须尽快，在35分钟内完成任务。"
0043723e  8b cf                          mov     ecx, edi                            
00437240  e8 10 58 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437245  68 94 14 4a 00                 push    0x4a1494                               ; "任务：在35分钟之内，破坏敌人的防御系统和建筑。 "
0043724a  e9 8d 01 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
0043724f  68 74 14 4a 00                 push    0x4a1474                               ; "领土 : 05   难度等级 : 5 / 10"
00437254  8d 4e 08                       lea     ecx, [esi + 8]                      
00437257  e8 f9 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043725c  68 64 14 4a 00                 push    0x4a1464                               ; "基地代号: W3C9"
00437261  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437264  e8 ec 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437269  8d 7e 10                       lea     edi, [esi + 0x10]                   
0043726c  68 80 13 4a 00                 push    0x4a1380                            
00437271  8b cf                          mov     ecx, edi                            
00437273  e8 dd 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437278  68 40 13 4a 00                 push    0x4a1340                               ; "任务：尽量多的控制金矿，坚持用炮塔保护我们的基地35分钟。"
0043727d  e9 5a 01 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
00437282  68 20 13 4a 00                 push    0x4a1320                               ; "领土 : 06   难度等级 : 6 / 10"
00437287  8d 4e 08                       lea     ecx, [esi + 8]                      
0043728a  e8 c6 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043728f  68 10 13 4a 00                 push    0x4a1310                               ; "基地代号: B7D4"
00437294  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437297  e8 b9 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043729c  8d 7e 10                       lea     edi, [esi + 0x10]                   
0043729f  68 68 12 4a 00                 push    0x4a1268                               ; "首先尽量多的控制金矿，你需要足够的资源保护基地30分钟。如果你能坚持到这一刻的话，就会获得支援，从而消灭敌方的总部。援军还包括金钱，所有这些援助将帮助你成功的完成任务。"
004372a4  8b cf                          mov     ecx, edi                            
004372a6  e8 aa 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004372ab  68 28 12 4a 00                 push    0x4a1228                               ; "任务：保护基地30分钟，一旦援军到达，迅速破坏敌方的总部。"
004372b0  e9 27 01 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
004372b5  68 08 12 4a 00                 push    0x4a1208                               ; "领土 : 07   难度等级 : 6 / 10"
004372ba  8d 4e 08                       lea     ecx, [esi + 8]                      
004372bd  e8 93 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004372c2  68 f8 11 4a 00                 push    0x4a11f8                               ; "基地代号: K0D7"
004372c7  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
004372ca  e8 86 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004372cf  8d 7e 10                       lea     edi, [esi + 0x10]                   
004372d2  68 80 11 4a 00                 push    0x4a1180                               ; "这次的任务比较困难，因为敌方拥有大量的空中力量。我们的空中力量不占优势。但是，我们可以巧妙的调集炮塔资源，打击敌人。 "
004372d7  8b cf                          mov     ecx, edi                            
004372d9  e8 77 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004372de  68 5c 11 4a 00                 push    0x4a115c                               ; "任务：消灭敌人，占领他们的基地。"
004372e3  e9 f4 00 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
004372e8  68 3c 11 4a 00                 push    0x4a113c                               ; "领土 : 08   难度等级 : 5 z 10"
004372ed  8d 4e 08                       lea     ecx, [esi + 8]                      
004372f0  e8 60 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004372f5  68 2c 11 4a 00                 push    0x4a112c                               ; "基地代号: H2E6"
004372fa  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
004372fd  e8 53 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437302  8d 7e 10                       lea     edi, [esi + 0x10]                   
00437305  68 70 10 4a 00                 push    0x4a1070                               ; "这块地方叫做黄金谷，有着丰富的黄金和矿物储量。我们的陆地力量目前正在此地区运转，所以我们不能依靠他们的帮助打击敌人。然而在这个任务中，你有大量的炮塔，可以利用他们有步骤的破坏敌人的总部。"
0043730a  8b cf                          mov     ecx, edi                            
0043730c  e8 44 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437311  68 40 10 4a 00                 push    0x4a1040                               ; "任务：用尽所有的金钱修建炮塔，消灭敌方的总部。"
00437316  e9 c1 00 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
0043731b  68 20 10 4a 00                 push    0x4a1020                               ; "领土 : 09   难度等级 : 8 / 10"
00437320  8d 4e 08                       lea     ecx, [esi + 8]                      
00437323  e8 2d 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437328  68 10 10 4a 00                 push    0x4a1010                               ; "基地代号: N3F3"
0043732d  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437330  e8 20 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437335  8d 7e 10                       lea     edi, [esi + 0x10]                   
00437338  68 80 0f 4a 00                 push    0x4a0f80                               ; "你的战役进行得非常精彩，胜利在望了。雷曼先生将自己的残余势力撤回了基地，你只有很短的时间消灭他的四个总部。呵呵，说起来容易，相信你一定能成功。"
0043733d  8b cf                          mov     ecx, edi                            
0043733f  e8 11 57 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437344  68 58 0f 4a 00                 push    0x4a0f58                               ; "任务：在40分钟之内消灭敌人的4个总部。"
00437349  e9 8e 00 00 00                 jmp     0x4373dc                               ; -> sub_004373dc
0043734e  68 38 0f 4a 00                 push    0x4a0f38                               ; "领土 : 10   难度等级 : 9 / 10"
00437353  8d 4e 08                       lea     ecx, [esi + 8]                      
00437356  e8 fa 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043735b  68 28 0f 4a 00                 push    0x4a0f28                               ; "基地代号: A6H2"
00437360  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437363  e8 ed 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437368  8d 7e 10                       lea     edi, [esi + 0x10]                   
0043736b  68 78 0e 4a 00                 push    0x4a0e78                               ; "在此任务中，敌方总部隐蔽在一个小岛上，你必须抵御敌人的进攻，直到积蓄足够的空中力量，消灭岛上的敌人总部。并且，调集力量在岛上南部的太阳能收集器，以利于更好的面对敌人的进攻。"
00437370  8b cf                          mov     ecx, edi                            
00437372  e8 de 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437377  68 48 0e 4a 00                 push    0x4a0e48                               ; "任务：积蓄空中力量，破坏敌人在岛上的总部。"
0043737c  eb 5e                          jmp     0x4373dc                               ; -> sub_004373dc
0043737e  68 28 0e 4a 00                 push    0x4a0e28                               ; "领土 : 11   难度等级 : 7 / 10"
00437383  8d 4e 08                       lea     ecx, [esi + 8]                      
00437386  e8 ca 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
0043738b  68 18 0e 4a 00                 push    0x4a0e18                               ; "基地代号: M7J1"
00437390  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00437393  e8 bd 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
00437398  8d 7e 10                       lea     edi, [esi + 0x10]                   
0043739b  68 20 0d 4a 00                 push    0x4a0d20                            
004373a0  8b cf                          mov     ecx, edi                            
004373a2  e8 ae 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004373a7  68 f0 0c 4a 00                 push    0x4a0cf0                               ; "任务：不要让罗曼先生逃走，不惜一切代价消灭他！"
004373ac  eb 2e                          jmp     0x4373dc                               ; -> sub_004373dc
004373ae  8d 4e 08                       lea     ecx, [esi + 8]                      
004373b1  68 e4 0c 4a 00                 push    0x4a0ce4                               ; "没有资料"
004373b6  e8 9a 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004373bb  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
004373be  68 e4 64 4a 00                 push    0x4a64e4                            
004373c3  e8 8d 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004373c8  8d 7e 10                       lea     edi, [esi + 0x10]                   
004373cb  68 e4 64 4a 00                 push    0x4a64e4                            
004373d0  8b cf                          mov     ecx, edi                            
004373d2  e8 7e 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004373d7  68 e4 64 4a 00                 push    0x4a64e4                            
004373dc  8d 6e 14                       lea     ebp, [esi + 0x14]                   
004373df  8b cd                          mov     ecx, ebp                            
004373e1  e8 6f 56 04 00                 call    0x47ca55                               ; -> sub_0047ca55
004373e6  8b 04 9d 24 72 72 00           mov     eax, dword ptr [ebx*4 + 0x727224]   
004373ed  85 c0                          test    eax, eax                            
004373ef  75 04                          jne     0x4373f5                               ; -> sub_004373f5
004373f1  33 c9                          xor     ecx, ecx                            
004373f3  eb 04                          jmp     0x4373f9                               ; -> sub_004373f9
004373f5  66 8b 48 04                    mov     cx, word ptr [eax + 4]              
004373f9  a1 c8 cc 49 00                 mov     eax, dword ptr [0x49ccc8]           
004373fe  99                             cdq                                         
004373ff  2b c2                          sub     eax, edx                            
00437401  0f bf d1                       movsx   edx, cx                             
00437404  d1 f8                          sar     eax, 1                              
00437406  2b c2                          sub     eax, edx                            
00437408  83 c0 03                       add     eax, 3                              
0043740b  89 86 44 03 00 00              mov     dword ptr [esi + 0x344], eax        
00437411  8b 04 9d 24 72 72 00           mov     eax, dword ptr [ebx*4 + 0x727224]   
00437418  33 db                          xor     ebx, ebx                            
0043741a  3b c3                          cmp     eax, ebx                            
0043741c  75 04                          jne     0x437422                               ; -> sub_00437422
0043741e  33 c9                          xor     ecx, ecx                            
00437420  eb 04                          jmp     0x437426                               ; -> sub_00437426
00437422  66 8b 48 06                    mov     cx, word ptr [eax + 6]              
00437426  a1 cc cc 49 00                 mov     eax, dword ptr [0x49cccc]           
0043742b  c7 86 4c 03 00 00 5d 00 00 00  mov     dword ptr [esi + 0x34c], 0x5d       
00437435  99                             cdq                                         
00437436  2b c2                          sub     eax, edx                            
00437438  c7 86 50 03 00 00 98 00 00 00  mov     dword ptr [esi + 0x350], 0x98       
00437442  0f bf c9                       movsx   ecx, cx                             
00437445  d1 f8                          sar     eax, 1                              
00437447  2b c1                          sub     eax, ecx                            
00437449  8d 8e e0 00 00 00              lea     ecx, [esi + 0xe0]                   
0043744f  83 c0 02                       add     eax, 2                              
00437452  c7 86 54 03 00 00 17 02 00 00  mov     dword ptr [esi + 0x354], 0x217      
0043745c  89 86 48 03 00 00              mov     dword ptr [esi + 0x348], eax        
00437462  c7 86 58 03 00 00 88 01 00 00  mov     dword ptr [esi + 0x358], 0x188      
0043746c  8b c1                          mov     eax, ecx                            
0043746e  ba 32 00 00 00                 mov     edx, 0x32                           
00437473  89 98 38 ff ff ff              mov     dword ptr [eax - 0xc8], ebx         
00437479  89 18                          mov     dword ptr [eax], ebx                
0043747b  89 98 c8 00 00 00              mov     dword ptr [eax + 0xc8], ebx         
00437481  89 98 90 01 00 00              mov     dword ptr [eax + 0x190], ebx        
00437487  83 c0 04                       add     eax, 4                              
0043748a  4a                             dec     edx                                 
0043748b  75 e6                          jne     0x437473                               ; -> sub_00437473
0043748d  8b 96 54 03 00 00              mov     edx, dword ptr [esi + 0x354]        
00437493  8b 86 4c 03 00 00              mov     eax, dword ptr [esi + 0x34c]        
00437499  2b d0                          sub     edx, eax                            
0043749b  8d 46 18                       lea     eax, [esi + 0x18]                   
0043749e  83 ea 32                       sub     edx, 0x32                           
004374a1  52                             push    edx                                 
004374a2  51                             push    ecx                                 
004374a3  50                             push    eax                                 
004374a4  51                             push    ecx                                 
004374a5  8b cc                          mov     ecx, esp                            
004374a7  89 64 24 24                    mov     dword ptr [esp + 0x24], esp         
004374ab  57                             push    edi                                 
004374ac  e8 dc 51 04 00                 call    0x47c68d                               ; -> sub_0047c68d
004374b1  e8 9a 1a 00 00                 call    0x438f50                               ; -> sub_00438f50
004374b6  8b 8e 54 03 00 00              mov     ecx, dword ptr [esi + 0x354]        
004374bc  8b 96 4c 03 00 00              mov     edx, dword ptr [esi + 0x34c]        
004374c2  2b ca                          sub     ecx, edx                            
004374c4  83 c4 10                       add     esp, 0x10                           
004374c7  83 e9 32                       sub     ecx, 0x32                           
004374ca  8d be 70 02 00 00              lea     edi, [esi + 0x270]                  
004374d0  51                             push    ecx                                 
004374d1  8d 96 a8 01 00 00              lea     edx, [esi + 0x1a8]                  
004374d7  57                             push    edi                                 
004374d8  52                             push    edx                                 
004374d9  51                             push    ecx                                 
004374da  8b cc                          mov     ecx, esp                            
004374dc  89 64 24 24                    mov     dword ptr [esp + 0x24], esp         
004374e0  55                             push    ebp                                 
004374e1  e8 a7 51 04 00                 call    0x47c68d                               ; -> sub_0047c68d
004374e6  e8 65 1a 00 00                 call    0x438f50                               ; -> sub_00438f50
004374eb  83 c4 10                       add     esp, 0x10                           
004374ee  33 c0                          xor     eax, eax                            
004374f0  39 1f                          cmp     dword ptr [edi], ebx                
004374f2  74 06                          je      0x4374fa                               ; -> sub_004374fa
004374f4  40                             inc     eax                                 
004374f5  83 c7 04                       add     edi, 4                              
004374f8  eb f6                          jmp     0x4374f0                               ; -> sub_004374f0
004374fa  8b 8e 4c 03 00 00              mov     ecx, dword ptr [esi + 0x34c]        
