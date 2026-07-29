Challenge_URL: https://crackmes.one/crackme/697f761b32fcb81e1bd005c6

Quite a Simple Crackme Solution  
Author: killswitcher 
Introduction 
The challenge is relatively easy, as many clues are in the description. However, I had 
problems running the original file because I didn't have the version the file required: 
“./c++crackme: /lib/x86_64-linux-gnu/libstdc++.so.6: version `GLIBCXX_3.4.32' not found 
(required by ./c++crackme)” 
 
Solution 
Well, before opening the file in decompilers/debuggers, I always try to see the file's behavior 
first, but as explained above, it didn't work. I had to use Ghidra to decompile it:  
 
 
  
 
 
 
 
 
Next, I analyzed it in the compiler and suspected a sequence of characters that didn't 
contain letters; I suspected it was the password to solve the challenge: 
 
 
Finally, I analyzed the source code, put it together in a file called simplecrack.cpp, compiled 
it, ran it, pasted the password, and this was the result: 
