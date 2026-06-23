# GetToKnow-v0.1 Writeup

Challenge_URL: https://crackmes.one/crackme/698c7dbfa15272fa37a80c73

1. Open exe file in IDA Pro in Graph mode. You will see four blocks. Take your look at the end of the first block and you will see, that after 
"jnz     short loc_7FF7287D14CB"(last command in this block) there are two blocks: one to "You did it" (good boy), second for "Try again" (bad boy). That's mean we need this block.
2. Then look to the command above and ther is "call strcmp". This command for the string compare. Set breake point here.
3. Run program, input something and then, before the command execute, take a look to registers. In rdx your input and in rax password for program.