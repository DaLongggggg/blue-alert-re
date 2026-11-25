00438b90  53                             push    ebx                                 
00438b91  8b 5c 24 08                    mov     ebx, dword ptr [esp + 8]            
00438b95  55                             push    ebp                                 
00438b96  56                             push    esi                                 
00438b97  8a 83 dc ad 72 00              mov     al, byte ptr [ebx + 0x72addc]       
00438b9d  57                             push    edi                                 
00438b9e  84 c0                          test    al, al                              
00438ba0  8b f1                          mov     esi, ecx                            
00438ba2  0f 84 b1 04 00 00              je      0x439059                               ; -> sub_00439059
00438ba8  8d 43 ff                       lea     eax, [ebx - 1]                      
00438bab  83 f8 15                       cmp     eax, 0x15                           
00438bae  0f 87 a5 04 00 00              ja      0x439059                               ; -> sub_00439059
00438bb4  ff 24 85 44 92 43 00           jmp     dword ptr [eax*4 + 0x439244]        
00438bbb  68 dc 54 4a 00                 push    0x4a54dc                               ; "领土: 01   难度等级: 1"
00438bc0  8d 4e 08                       lea     ecx, [esi + 8]                      
00438bc3  e8 8d 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438bc8  68 bc 54 4a 00                 push    0x4a54bc                               ; "基地代号: X8A   战场：加拿大"
00438bcd  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438bd0  e8 80 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438bd5  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438bd8  68 94 53 4a 00                 push    0x4a5394                            
00438bdd  8b cf                          mov     ecx, edi                            
00438bdf  e8 71 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438be4  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438be7  68 38 53 4a 00                 push    0x4a5338                               ; "任务：增加你的陆地作战单位的技术水平，并得到空中力量的援助。用它们去摧毁岛上敌人的总部。"
00438bec  e9 99 04 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438bf1  68 20 53 4a 00                 push    0x4a5320                               ; "领土: 02   难度等级: 2"
00438bf6  8d 4e 08                       lea     ecx, [esi + 8]                      
00438bf9  e8 57 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438bfe  68 00 53 4a 00                 push    0x4a5300                               ; "基地代号: E1B   战场：摩洛哥"
00438c03  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438c06  e8 4a 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c0b  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438c0e  68 5c 52 4a 00                 push    0x4a525c                               ; "我们的运兵飞船被击落了！他们担负着运送一个小分队占领摩洛哥的任务。因此，你就必须承担起占领摩洛哥基地的任务。使用飞碟，逐步占领敌人的建筑，最后，摧毁敌人的总部。"
00438c13  8b cf                          mov     ecx, edi                            
00438c15  e8 3b 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c1a  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438c1d  68 28 52 4a 00                 push    0x4a5228                               ; "任务：占领敌人的建筑，聚集重兵力摧毁敌人的总部。"
00438c22  e9 63 04 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438c27  68 10 52 4a 00                 push    0x4a5210                               ; "领土: 09   难度等级: 5"
00438c2c  8d 4e 08                       lea     ecx, [esi + 8]                      
00438c2f  e8 21 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c34  68 f0 51 4a 00                 push    0x4a51f0                               ; "基地代号: B2E   战场：斯洛伐克"
00438c39  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438c3c  e8 14 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c41  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438c44  68 80 51 4a 00                 push    0x4a5180                               ; "在这次任务中你必须把罗根炸弹（共4个）护送到我方的总部。你可以随意调动我方的超级机器人。要非常提防敌方的空袭。"
00438c49  8b cf                          mov     ecx, edi                            
00438c4b  e8 05 6e 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c50  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438c53  68 4c 51 4a 00                 push    0x4a514c                               ; "任务：保护好罗根炸弹，并把它们护送到我方的总部。"
00438c58  e9 2d 04 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438c5d  68 34 51 4a 00                 push    0x4a5134                               ; "领土: 04   难度等级: 3"
00438c62  8d 4e 08                       lea     ecx, [esi + 8]                      
00438c65  e8 eb 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c6a  68 14 51 4a 00                 push    0x4a5114                               ; "基地代号: P4C   战场：德克萨斯"
00438c6f  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438c72  e8 de 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c77  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438c7a  68 a4 50 4a 00                 push    0x4a50a4                               ; "你首先要夺取一个重要的能量资源――太阳能搜集器，把敌人赶出德克萨斯基地。然后占领所有的建筑,并干掉所有的敌人。"
00438c7f  8b cf                          mov     ecx, edi                            
00438c81  e8 cf 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438c86  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438c89  68 74 50 4a 00                 push    0x4a5074                               ; "任务：摧毁敌人的所有作战单位，并控制整个基地。"
00438c8e  e9 f7 03 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438c93  68 5c 50 4a 00                 push    0x4a505c                               ; "领土: 05   难度等级: 6"
00438c98  8d 4e 08                       lea     ecx, [esi + 8]                      
00438c9b  e8 b5 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ca0  68 40 50 4a 00                 push    0x4a5040                               ; "基地代号: C9F   战场：中国"
00438ca5  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438ca8  e8 a8 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438cad  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438cb0  68 38 4f 4a 00                 push    0x4a4f38                            
00438cb5  8b cf                          mov     ecx, edi                            
00438cb7  e8 99 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438cbc  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438cbf  68 f0 4e 4a 00                 push    0x4a4ef0                               ; "任务：你的任务是消灭企图控制这个地区的每一个敌人，并占领敌人的建筑。"
00438cc4  e9 c1 03 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438cc9  68 d8 4e 4a 00                 push    0x4a4ed8                               ; "领土: 06   难度等级: 3"
00438cce  8d 4e 08                       lea     ecx, [esi + 8]                      
00438cd1  e8 7f 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438cd6  68 bc 4e 4a 00                 push    0x4a4ebc                               ; "基地代号: W3C   战场：俄国"
00438cdb  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438cde  e8 72 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ce3  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438ce6  68 0c 4e 4a 00                 push    0x4a4e0c                               ; "敌人占领了所有飞机生产基地。它们位于西伯利亚沿海。你的任务是把它们全部消灭，最后，再摧毁敌人的总部。小心！敌人的空中力量非常强大！领土西北角的太阳能搜集器能够帮助你取得胜利。"
00438ceb  8b cf                          mov     ecx, edi                            
00438ced  e8 63 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438cf2  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438cf5  68 dc 4d 4a 00                 push    0x4a4ddc                               ; "任务：夺取敌人的飞机生产基地，摧毁敌人的总部。"
00438cfa  e9 8b 03 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438cff  68 c4 4d 4a 00                 push    0x4a4dc4                               ; "领土: 07   难度等级: 4"
00438d04  8d 4e 08                       lea     ecx, [esi + 8]                      
00438d07  e8 49 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d0c  68 a8 4d 4a 00                 push    0x4a4da8                               ; "基地代号: B7D   战场：苏丹"
00438d11  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438d14  e8 3c 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d19  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438d1c  68 c4 4c 4a 00                 push    0x4a4cc4                            
00438d21  8b cf                          mov     ecx, edi                            
00438d23  e8 2d 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d28  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438d2b  68 7c 4c 4a 00                 push    0x4a4c7c                               ; "任务：坚守阵地20分钟，然后，用飞碟去占领敌人的建筑，摧毁敌人的总部。"
00438d30  e9 55 03 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438d35  68 64 4c 4a 00                 push    0x4a4c64                               ; "领土: 13   难度等级: 9"
00438d3a  8d 4e 08                       lea     ecx, [esi + 8]                      
00438d3d  e8 13 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d42  68 48 4c 4a 00                 push    0x4a4c48                               ; "基地代号: D5I   战场：荷兰"
00438d47  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438d4a  e8 06 6d 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d4f  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438d52  68 98 4b 4a 00                 push    0x4a4b98                               ; "敌人控制了这里的大部分地区。首先，你必须护送好罗根炸弹，稍后，我们会需要它们的。用超级机器人和重型空中单位完成这个任务。当把罗根炸弹护送到目的地后，集中所有兵力一举歼灭敌人。"
00438d57  8b cf                          mov     ecx, edi                            
00438d59  e8 f7 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d5e  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438d61  68 70 4b 4a 00                 push    0x4a4b70                               ; "任务：保护好罗根炸弹，摧毁敌人的总部。"
00438d66  e9 1f 03 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438d6b  68 58 4b 4a 00                 push    0x4a4b58                               ; "领土: 03   难度等级: 2"
00438d70  8d 4e 08                       lea     ecx, [esi + 8]                      
00438d73  e8 dd 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d78  68 3c 4b 4a 00                 push    0x4a4b3c                               ; "基地代号: F1B   战场：挪威"
00438d7d  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438d80  e8 d0 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d85  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438d88  68 78 4a 4a 00                 push    0x4a4a78                               ; "在这项任务中你有几个地面作战单位和四个带原子能弹头的罗根炸弹。用它们去清除敌人的防线和炮塔。然后用地面单位去占领敌人的建筑。记住，阿锡莱利大炮最利于击中远距离的目标。最后，你必须摧毁敌人的总部。"
00438d8d  8b cf                          mov     ecx, edi                            
00438d8f  e8 c1 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438d94  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438d97  68 60 4a 4a 00                 push    0x4a4a60                               ; "任务：摧毁敌人的总部。"
00438d9c  e9 e9 02 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438da1  68 48 4a 4a 00                 push    0x4a4a48                               ; "领土: 10   难度等级: 5"
00438da6  8d 4e 08                       lea     ecx, [esi + 8]                      
00438da9  e8 a7 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438dae  68 28 4a 4a 00                 push    0x4a4a28                               ; "基地代号: L4E   战场：澳大利亚"
00438db3  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438db6  e8 9a 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438dbb  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438dbe  68 4c 49 4a 00                 push    0x4a494c                            
00438dc3  8b cf                          mov     ecx, edi                            
00438dc5  e8 8b 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438dca  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438dcd  68 14 49 4a 00                 push    0x4a4914                               ; "任务：用你的空中力量除去敌人的防御，摧毁他们的总部。"
00438dd2  e9 b3 02 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438dd7  68 fc 48 4a 00                 push    0x4a48fc                               ; "领土: 11   难度等级: 4"
00438ddc  8d 4e 08                       lea     ecx, [esi + 8]                      
00438ddf  e8 71 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438de4  68 e0 48 4a 00                 push    0x4a48e0                               ; "基地代号: K0D   战场：希腊"
00438de9  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438dec  e8 64 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438df1  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438df4  68 20 48 4a 00                 push    0x4a4820                               ; "到现在为止，我们已经取得了欧洲战争的胜利,是收复南部的时候了。我们处于敌人的强大防御工事之下。我们的陆地作战单位还没有到达，并且你手中只有几个炮塔。用炮塔占领附近敌人的设施，摧毁敌人的总部。"
00438df9  8b cf                          mov     ecx, edi                            
00438dfb  e8 55 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e00  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438e03  68 ec 47 4a 00                 push    0x4a47ec                               ; "任务：用炮塔逐步占领敌人的建筑，并摧毁敌人的总部。"
00438e08  e9 7d 02 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438e0d  68 d4 47 4a 00                 push    0x4a47d4                               ; "领土: 12   难度等级: 5"
00438e12  8d 4e 08                       lea     ecx, [esi + 8]                      
00438e15  e8 3b 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e1a  68 b8 47 4a 00                 push    0x4a47b8                               ; "基地代号: H2E   战场：巴西"
00438e1f  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438e22  e8 2e 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e27  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438e2a  68 a0 46 4a 00                 push    0x4a46a0                            
00438e2f  8b cf                          mov     ecx, edi                            
00438e31  e8 1f 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e36  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438e39  68 58 46 4a 00                 push    0x4a4658                               ; "任务：占领地图东部的建筑，坚守阵地直到援军到达。然后，摧毁敌人的总部。"
00438e3e  e9 47 02 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438e43  68 40 46 4a 00                 push    0x4a4640                               ; "领土: 08   难度等级: 4"
00438e48  8d 4e 08                       lea     ecx, [esi + 8]                      
00438e4b  e8 05 6c 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e50  68 20 46 4a 00                 push    0x4a4620                               ; "基地代号: X8D   战场：加拿大"
00438e55  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438e58  e8 f8 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e5d  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438e60  68 94 45 4a 00                 push    0x4a4594                               ; "基地的南部控制在我们的手中，但是，其北部却掌握在敌人的手中。你的任务是夺回失去的领土。要注意！敌人控制着罗根炮弹工厂，所以你必须非常小心。"
00438e65  8b cf                          mov     ecx, edi                            
00438e67  e8 e9 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e6c  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438e6f  68 6c 45 4a 00                 push    0x4a456c                               ; "任务：摧毁敌人所有的作战单位和设施。"
00438e74  e9 11 02 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438e79  68 58 45 4a 00                 push    0x4a4558                               ; "领土: 14   难度: 6"
00438e7e  8d 4e 08                       lea     ecx, [esi + 8]                      
00438e81  e8 cf 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e86  68 38 45 4a 00                 push    0x4a4538                               ; "基地代号: U6F   战场:委内瑞拉"
00438e8b  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438e8e  e8 c2 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438e93  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438e96  68 94 44 4a 00                 push    0x4a4494                               ; "敌人在这个地区的陆地作战单位非常多。首先，你要掌握许多金矿和飞机生产基地。然后，用战斗机摧毁敌人的高射炮，这样，你就能安全地用运兵飞船把坦克运送到敌人的领土上了。"
00438e9b  8b cf                          mov     ecx, edi                            
00438e9d  e8 b3 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ea2  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438ea5  68 58 44 4a 00                 push    0x4a4458                               ; "任务：用运兵飞船把我方的陆地作战单位运送到敌人的领土上。"
00438eaa  e9 db 01 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438eaf  68 40 44 4a 00                 push    0x4a4440                               ; "领土: 15   难度等级: 6"
00438eb4  8d 4e 08                       lea     ecx, [esi + 8]                      
00438eb7  e8 99 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ebc  68 24 44 4a 00                 push    0x4a4424                               ; "基地代号: N3F   战场：埃及"
00438ec1  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438ec4  e8 8c 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ec9  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438ecc  68 a8 43 4a 00                 push    0x4a43a8                               ; "敌人的援军就要到达我方埃及西部的基地了。在他们到达之前，占领这个基地。你仅仅有30分钟的时间。充分利用空中力量完成这次任务。"
00438ed1  8b cf                          mov     ecx, edi                            
00438ed3  e8 7d 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ed8  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438edb  68 80 43 4a 00                 push    0x4a4380                               ; "任务：用30分钟的时间占领敌人的基地。"
00438ee0  e9 a5 01 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438ee5  68 68 43 4a 00                 push    0x4a4368                               ; "领土: 16   难度等级: 7"
00438eea  8d 4e 08                       lea     ecx, [esi + 8]                      
00438eed  e8 63 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438ef2  68 44 43 4a 00                 push    0x4a4344                               ; "基地代号: J9G   战场：阿拉斯加州"
00438ef7  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438efa  e8 56 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438eff  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438f02  68 b0 42 4a 00                 push    0x4a42b0                               ; "这个地区有着丰富的金矿资源。你的第一个目的是要控制所有的金矿。然后，在敌人建筑的旁边建造炮塔，从而摧毁它们。注意！你仅有40分钟的时间完成这项任务！"
00438f07  8b cf                          mov     ecx, edi                            
00438f09  e8 47 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f0e  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438f11  68 5c 42 4a 00                 push    0x4a425c                               ; "任务：利用炮塔和作战单位摧毁敌人所有的军事力量，占领整个基地。你仅有40分钟的时间！"
00438f16  e9 6f 01 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438f1b  68 48 42 4a 00                 push    0x4a4248                               ; "领土: 17   难度: 7"
00438f20  8d 4e 08                       lea     ecx, [esi + 8]                      
00438f23  e8 2d 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f28  68 2c 42 4a 00                 push    0x4a422c                               ; "基地代号: R4G   战场：南韩"
00438f2d  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438f30  e8 20 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f35  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438f38  68 30 41 4a 00                 push    0x4a4130                            
00438f3d  8b cf                          mov     ecx, edi                            
00438f3f  e8 11 6b 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f44  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438f47  68 e4 40 4a 00                 push    0x4a40e4                               ; "任务：你必须坚守30分钟。当援军到达后，立即升级你的工厂，并摧毁敌人的总部。"
00438f4c  e9 39 01 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438f51  68 cc 40 4a 00                 push    0x4a40cc                               ; "领土: 18   难度等级: 7"
00438f56  8d 4e 08                       lea     ecx, [esi + 8]                      
00438f59  e8 f7 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f5e  68 b0 40 4a 00                 push    0x4a40b0                               ; "基地代号: Y1G   战场：日本"
00438f63  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438f66  e8 ea 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f6b  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438f6e  68 24 40 4a 00                 push    0x4a4024                               ; "注意！这个地区的敌人十分强大。他们有许多炮塔和空中作战单位。必须有一队重型陆地作战单位才能击败它。单独的作战单位是无法攻破敌人的防御的。"
00438f73  8b cf                          mov     ecx, edi                            
00438f75  e8 db 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f7a  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438f7d  68 f4 3f 4a 00                 push    0x4a3ff4                               ; "任务：用大量的重型陆地作战单位击败敌人的防御。"
00438f82  e9 03 01 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438f87  68 e0 3f 4a 00                 push    0x4a3fe0                               ; "领土: 19   难度: 8"
00438f8c  8d 4e 08                       lea     ecx, [esi + 8]                      
00438f8f  e8 c1 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438f94  68 c4 3f 4a 00                 push    0x4a3fc4                               ; "基地代号: E0H   战场:智利"
00438f99  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438f9c  e8 b4 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438fa1  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438fa4  68 28 3f 4a 00                 push    0x4a3f28                               ; "这是一次特殊的任务，敌人有两个总部。一个在岛上，你需要大量的空中作战单位攻下它。要快，使敌人没有喘息的机会，他们就来不及升级工厂并制造出更强大的武器了。"
00438fa9  8b cf                          mov     ecx, edi                            
00438fab  e8 a5 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438fb0  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438fb3  68 0c 3f 4a 00                 push    0x4a3f0c                               ; "任务：尽快摧毁敌人的总部。"
00438fb8  e9 cd 00 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438fbd  68 f4 3e 4a 00                 push    0x4a3ef4                               ; "领土: 20   难度等级: 8"
00438fc2  8d 4e 08                       lea     ecx, [esi + 8]                      
00438fc5  e8 8b 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438fca  68 d8 3e 4a 00                 push    0x4a3ed8                               ; "基地代号: A6H   战场: 俄国"
00438fcf  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00438fd2  e8 7e 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438fd7  8d 7e 10                       lea     edi, [esi + 0x10]                   
00438fda  68 5c 3e 4a 00                 push    0x4a3e5c                               ; "首先你要尽量多占领飞机生产基地，控制好形势，这样，利用空中力量占领位于西北部的太阳能搜集器。最后，升级你的单位，消灭敌人。"
00438fdf  8b cf                          mov     ecx, edi                            
00438fe1  e8 6f 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00438fe6  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00438fe9  68 10 3e 4a 00                 push    0x4a3e10                               ; "任务：用空中力量占领太阳能搜集器，升级你的作战单位，摧毁敌人所有的总部。"
00438fee  e9 97 00 00 00                 jmp     0x43908a                               ; -> sub_0043908a
00438ff3  68 f8 3d 4a 00                 push    0x4a3df8                               ; "领土: 21   难度等级: 9"
00438ff8  8d 4e 08                       lea     ecx, [esi + 8]                      
00438ffb  e8 55 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439000  68 d4 3d 4a 00                 push    0x4a3dd4                               ; "基地代号: Q2I   战场: 南非共和国"
00439005  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
00439008  e8 48 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
0043900d  8d 7e 10                       lea     edi, [esi + 0x10]                   
00439010  68 1c 3d 4a 00                 push    0x4a3d1c                               ; "我们的战役已接近了尾声。你的下一个任务是在南非。迅速占领太阳能搜集器，要不惜任何代价。这个建筑对于你非常重要，因为，你要击败敌人只能靠重型作战单位。在这次任务中，你可以利用两个飞碟。"
00439015  8b cf                          mov     ecx, edi                            
00439017  e8 39 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
0043901c  8d 6e 14                       lea     ebp, [esi + 0x14]                   
0043901f  68 e0 3c 4a 00                 push    0x4a3ce0                               ; "任务：摧毁敌人所有的建筑和作战单位。你仅有50分钟的时间。"
00439024  eb 64                          jmp     0x43908a                               ; -> sub_0043908a
00439026  68 c8 3c 4a 00                 push    0x4a3cc8                               ; "领土: 22   难度等级: 9"
0043902b  8d 4e 08                       lea     ecx, [esi + 8]                      
0043902e  e8 22 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439033  68 ac 3c 4a 00                 push    0x4a3cac                               ; "基地代号: M7J   战场: 伊朗"
00439038  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
0043903b  e8 15 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439040  8d 7e 10                       lea     edi, [esi + 0x10]                   
00439043  68 f4 3b 4a 00                 push    0x4a3bf4                               ; "这是最后的一次任务。敌人聚集了他的所有残余兵力保护他们的老家“超级防线”。消灭所有敌人，占领敌人的每一个建筑。这是唯一能击败超级防线的方法，这样才能制止地球的混乱，把人类解救出来。"
00439048  8b cf                          mov     ecx, edi                            
0043904a  e8 06 6a 04 00                 call    0x47fa55                               ; -> sub_0047fa55
0043904f  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00439052  68 c4 3b 4a 00                 push    0x4a3bc4                               ; "任务：摧毁敌人的残余兵力，战胜“超级防线”。"
00439057  eb 31                          jmp     0x43908a                               ; -> sub_0043908a
00439059  68 b8 3b 4a 00                 push    0x4a3bb8                               ; "没有资料"
0043905e  8d 4e 08                       lea     ecx, [esi + 8]                      
00439061  e8 ef 69 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439066  68 14 a1 4a 00                 push    0x4aa114                            
0043906b  8d 4e 0c                       lea     ecx, [esi + 0xc]                    
0043906e  e8 e2 69 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439073  8d 7e 10                       lea     edi, [esi + 0x10]                   
00439076  68 14 a1 4a 00                 push    0x4aa114                            
0043907b  8b cf                          mov     ecx, edi                            
0043907d  e8 d3 69 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439082  8d 6e 14                       lea     ebp, [esi + 0x14]                   
00439085  68 14 a1 4a 00                 push    0x4aa114                            
0043908a  8b cd                          mov     ecx, ebp                            
0043908c  e8 c4 69 04 00                 call    0x47fa55                               ; -> sub_0047fa55
00439091  8b 04 9d 34 ae 72 00           mov     eax, dword ptr [ebx*4 + 0x72ae34]   
00439098  85 c0                          test    eax, eax                            
0043909a  75 04                          jne     0x4390a0                               ; -> sub_004390a0
0043909c  33 c9                          xor     ecx, ecx                            
0043909e  eb 04                          jmp     0x4390a4                               ; -> sub_004390a4
004390a0  66 8b 48 04                    mov     cx, word ptr [eax + 4]              
004390a4  a1 d4 fb 49 00                 mov     eax, dword ptr [0x49fbd4]           
004390a9  99                             cdq                                         
004390aa  2b c2                          sub     eax, edx                            
004390ac  0f bf c9                       movsx   ecx, cx                             
004390af  d1 f8                          sar     eax, 1                              
004390b1  2b c1                          sub     eax, ecx                            
004390b3  83 c0 03                       add     eax, 3                              
004390b6  89 86 44 03 00 00              mov     dword ptr [esi + 0x344], eax        
004390bc  8b 04 9d 34 ae 72 00           mov     eax, dword ptr [ebx*4 + 0x72ae34]   
004390c3  33 db                          xor     ebx, ebx                            
004390c5  3b c3                          cmp     eax, ebx                            
004390c7  75 04                          jne     0x4390cd                               ; -> sub_004390cd
004390c9  33 c9                          xor     ecx, ecx                            
004390cb  eb 04                          jmp     0x4390d1                               ; -> sub_004390d1
004390cd  66 8b 48 06                    mov     cx, word ptr [eax + 6]              
004390d1  a1 d8 fb 49 00                 mov     eax, dword ptr [0x49fbd8]           
004390d6  c7 86 4c 03 00 00 5d 00 00 00  mov     dword ptr [esi + 0x34c], 0x5d       
004390e0  99                             cdq                                         
004390e1  2b c2                          sub     eax, edx                            
004390e3  c7 86 50 03 00 00 98 00 00 00  mov     dword ptr [esi + 0x350], 0x98       
004390ed  0f bf d1                       movsx   edx, cx                             
004390f0  d1 f8                          sar     eax, 1                              
004390f2  2b c2                          sub     eax, edx                            
004390f4  8d 8e e0 00 00 00              lea     ecx, [esi + 0xe0]                   
004390fa  83 c0 02                       add     eax, 2                              
004390fd  c7 86 54 03 00 00 17 02 00 00  mov     dword ptr [esi + 0x354], 0x217      
00439107  89 86 48 03 00 00              mov     dword ptr [esi + 0x348], eax        
0043910d  c7 86 58 03 00 00 88 01 00 00  mov     dword ptr [esi + 0x358], 0x188      
00439117  8b c1                          mov     eax, ecx                            
00439119  ba 32 00 00 00                 mov     edx, 0x32                           
0043911e  89 98 38 ff ff ff              mov     dword ptr [eax - 0xc8], ebx         
00439124  89 18                          mov     dword ptr [eax], ebx                
00439126  89 98 c8 00 00 00              mov     dword ptr [eax + 0xc8], ebx         
0043912c  89 98 90 01 00 00              mov     dword ptr [eax + 0x190], ebx        
00439132  83 c0 04                       add     eax, 4                              
00439135  4a                             dec     edx                                 
00439136  75 e6                          jne     0x43911e                               ; -> sub_0043911e
00439138  8b 86 54 03 00 00              mov     eax, dword ptr [esi + 0x354]        
0043913e  8b 96 4c 03 00 00              mov     edx, dword ptr [esi + 0x34c]        
00439144  2b c2                          sub     eax, edx                            
00439146  83 e8 32                       sub     eax, 0x32                           
00439149  50                             push    eax                                 
0043914a  51                             push    ecx                                 
0043914b  8d 4e 18                       lea     ecx, [esi + 0x18]                   
0043914e  51                             push    ecx                                 
0043914f  51                             push    ecx                                 
00439150  8b cc                          mov     ecx, esp                            
00439152  89 64 24 24                    mov     dword ptr [esp + 0x24], esp         
00439156  57                             push    edi                                 
00439157  e8 31 65 04 00                 call    0x47f68d                               ; -> sub_0047f68d
0043915c  e8 4f 1b 00 00                 call    0x43acb0                               ; -> sub_0043acb0
00439161  8b 96 54 03 00 00              mov     edx, dword ptr [esi + 0x354]        
00439167  8b 8e 4c 03 00 00              mov     ecx, dword ptr [esi + 0x34c]        
0043916d  2b d1                          sub     edx, ecx                            
0043916f  83 c4 10                       add     esp, 0x10                           
00439172  83 ea 32                       sub     edx, 0x32                           
00439175  8d be 70 02 00 00              lea     edi, [esi + 0x270]                  
0043917b  52                             push    edx                                 
0043917c  8d 86 a8 01 00 00              lea     eax, [esi + 0x1a8]                  
00439182  57                             push    edi                                 
00439183  50                             push    eax                                 
00439184  51                             push    ecx                                 
00439185  8b cc                          mov     ecx, esp                            
00439187  89 64 24 24                    mov     dword ptr [esp + 0x24], esp         
0043918b  55                             push    ebp                                 
0043918c  e8 fc 64 04 00                 call    0x47f68d                               ; -> sub_0047f68d
00439191  e8 1a 1b 00 00                 call    0x43acb0                               ; -> sub_0043acb0
00439196  83 c4 10                       add     esp, 0x10                           
00439199  33 c0                          xor     eax, eax                            
0043919b  39 1f                          cmp     dword ptr [edi], ebx                
0043919d  74 06                          je      0x4391a5                               ; -> sub_004391a5
0043919f  40                             inc     eax                                 
004391a0  83 c7 04                       add     edi, 4                              
004391a3  eb f6                          jmp     0x43919b                               ; -> sub_0043919b
004391a5  8b 96 4c 03 00 00              mov     edx, dword ptr [esi + 0x34c]        
004391ab  8d 9e 64 03 00 00              lea     ebx, [esi + 0x364]                  
004391b1  8b cb                          mov     ecx, ebx                            
004391b3  8d 7c 80 05                    lea     edi, [eax + eax*4 + 5]              
004391b7  8b 86 50 03 00 00              mov     eax, dword ptr [esi + 0x350]        
004391bd  89 11                          mov     dword ptr [ecx], edx                
004391bf  8b 96 54 03 00 00              mov     edx, dword ptr [esi + 0x354]        
004391c5  c1 e7 02                       shl     edi, 2                              
004391c8  89 41 04                       mov     dword ptr [ecx + 4], eax            
004391cb  8b 86 58 03 00 00              mov     eax, dword ptr [esi + 0x358]        
004391d1  89 51 08                       mov     dword ptr [ecx + 8], edx            
004391d4  89 41 0c                       mov     dword ptr [ecx + 0xc], eax          
004391d7  e8 24 ba fe ff                 call    0x424c00                               ; -> sub_00424c00
004391dc  83 f8 03                       cmp     eax, 3                              
004391df  75 0f                          jne     0x4391f0                               ; -> sub_004391f0
004391e1  b9 c4 01 00 00                 mov     ecx, 0x1c4                          
004391e6  2b cf                          sub     ecx, edi                            
004391e8  89 8e 58 03 00 00              mov     dword ptr [esi + 0x358], ecx        
004391ee  eb 0d                          jmp     0x4391fd                               ; -> sub_004391fd
004391f0  ba b5 01 00 00                 mov     edx, 0x1b5                          
004391f5  2b d7                          sub     edx, edi                            
004391f7  89 96 58 03 00 00              mov     dword ptr [esi + 0x358], edx        
004391fd  8b 86 6c 03 00 00              mov     eax, dword ptr [esi + 0x36c]        
00439203  8b 13                          mov     edx, dword ptr [ebx]                
00439205  03 c2                          add     eax, edx                            
00439207  b9 d3 01 00 00                 mov     ecx, 0x1d3                          
0043920c  99                             cdq                                         
0043920d  2b c2                          sub     eax, edx                            
0043920f  2b cf                          sub     ecx, edi                            
00439211  d1 f8                          sar     eax, 1                              
00439213  89 86 5c 03 00 00              mov     dword ptr [esi + 0x35c], eax        
00439219  8d 81 d3 01 00 00              lea     eax, [ecx + 0x1d3]                  
0043921f  99                             cdq                                         
00439220  2b c2                          sub     eax, edx                            
00439222  89 8e 68 03 00 00              mov     dword ptr [esi + 0x368], ecx        
00439228  d1 f8                          sar     eax, 1                              
0043922a  c7 86 70 03 00 00 d3 01 00 00  mov     dword ptr [esi + 0x370], 0x1d3      
00439234  89 86 60 03 00 00              mov     dword ptr [esi + 0x360], eax        
0043923a  5f                             pop     edi                                 
0043923b  5e                             pop     esi                                 
0043923c  5d                             pop     ebp                                 
0043923d  5b                             pop     ebx                                 
