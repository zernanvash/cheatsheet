# CryMore Writeup

I first ran the program and observed that it attempted to connect to
127.0.0.1 on port 44333. If the connection failed, the program printed
that the malware executed.

After analyzing the binary in Ghidra, I saw that if the connection
succeeds, the program sends an HTTP GET request to /neutralize and waits
for a response. It then checks whether the received data contains the
string "200 OK".

To neutralize the malware, I started a local listener on port 44333 that
returned an HTTP 200 OK response and closed the connection. This caused
the program to take the success path and print the neutralization
message.