# ASCII_CRACK Writeup

Challenge_URL: https://crackmes.one/crackme/69a806c17b3cc38c80464e06

The program transforms the input string using a simple algorithm and then 
compares it with the hardcoded string "IYJ~U4cQ1Q[<mL[(U;`'Ynk/M-i".

The transformation of the input string consists of sequentially adding the 
counter value to each character. The counter starts at 6 and decreases by 1
each time. All calculations are performed modulo 256. 

To calculate the required string, it is necessary to perform the inverse 
operation on the hardcoded string (substract the counter value, starting at 6 
and decreasing by 1 for each character).

required string is CTF{S3cR3T_AsSc1_Fl4g}{@_@}

the code to get required string is here:

if __name__ == "__main__":
	basic_str =  "IYJ~U4cQ1Q[<mL[(U;`'Ynk/M-i"
	for count, item in enumerate(basic_str):
		cnt = 6-count
		print(chr((ord(item)-cnt)%256), end='')