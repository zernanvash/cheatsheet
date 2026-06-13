# Linux Text Processing Cheat Sheet

Command-line utilities for filtering, cutting, replacing, and processing text data during recon, local enumeration, log analysis, or CTF challenges.

## grep (Global Regular Expression Print)

Search text for patterns.

- `grep "pattern" file.txt` - search for a string in a file
- `grep -i "pattern" file.txt` - case-insensitive search
- `grep -r "pattern" /path/to/dir` - recursive search in a directory
- `grep -rnE "pass|secret|token" /var/www/html` - recursive, regex, print line numbers
- `grep -v "pattern" file.txt` - invert match (print lines NOT containing the pattern)
- `grep -oP '\[\D*?\]' file.txt` - extract only the matching part using Perl-compatible regex (PCRE)
- `grep -A 2 -B 1 "pattern" file.txt` - print 2 lines after (A) and 1 line before (B) the match
- `grep -w "pattern" file.txt` - match whole words only

## cut

Extract sections from each line of files.

- `cut -d ':' -f 1 /etc/passwd` - cut by delimiter `:` and select the first field (usernames)
- `cut -d ' ' -f 2,4 file.txt` - cut by space and select fields 2 and 4
- `cut -c 1-10 file.txt` - extract character positions 1 to 10 from each line
- `cut -c 5- file.txt` - extract from character position 5 to the end of the line

## awk

Versatile pattern scanning and processing language.

- `awk '{print $1}' file.txt` - print the first field of each line (default delimiter is whitespace)
- `awk -F: '{print $1, $3}' /etc/passwd` - set delimiter to `:` and print fields 1 and 3
- `awk -F: '$3 == 0 {print $1}' /etc/passwd` - print usernames with UID 0 (root equivalent)
- `awk -F: '$3 >= 1000 {print $1}' /etc/passwd` - print non-system user accounts
- `awk '/pattern/ {print $2}' file.txt` - find lines matching "pattern" and print the second field

## sed (Stream Editor)

Filter and transform text.

- `sed 's/old/new/' file.txt` - replace the first occurrence of "old" with "new" in each line
- `sed 's/old/new/g' file.txt` - replace all occurrences of "old" with "new" in each line (global)
- `sed -i 's/foo/bar/g' file.txt` - edit the file in-place (dangerous, keeps no backup)
- `sed -n '5,10p' file.txt` - print only lines 5 through 10
- `sed '/pattern/d' file.txt` - delete all lines matching "pattern"

## tr (Translate)

Translate, squeeze, or delete characters.

- `cat file.txt | tr 'a-z' 'A-Z'` - convert lowercase to uppercase
- `cat file.txt | tr -d '[]'` - delete specific characters (e.g., square brackets)
- `cat file.txt | tr -d '\r'` - strip Windows carriage returns (convert CRLF to LF)
- `cat file.txt | tr -s ' '` - squeeze multiple consecutive spaces into a single space
- `echo "ROT13" | tr 'A-Za-z' 'N-ZA-Mn-za-m'` - ROT13 decode/encode

## sort and uniq

Sort lines of text and remove duplicates.

- `sort file.txt` - sort lines alphabetically
- `sort -n file.txt` - sort lines numerically
- `sort -u file.txt` - sort and remove duplicates
- `sort file.txt | uniq` - remove adjacent duplicate lines (requires input to be sorted)
- `sort file.txt | uniq -c` - count occurrences of each line
- `sort file.txt | uniq -c | sort -nr` - count occurrences and sort numerically descending (find most frequent entries)
- `sort file.txt | uniq -u` - print only unique lines (lines that do not have duplicates)

## wc (Word Count)

Print newline, word, and byte counts.

- `wc -l file.txt` - count lines in a file
- `wc -w file.txt` - count words
- `wc -m file.txt` - count characters
- `wc -c file.txt` - count bytes

## tee

Read from standard input and write to standard output and files.

- `command | tee output.txt` - save output to a file while also displaying it on screen
- `command | tee -a output.txt` - append output to a file instead of overwriting it

## xargs

Build and execute command lines from standard input.

- `cat ips.txt | xargs -I {} nmap -p 80 {}` - pass each line of `ips.txt` as an argument to `nmap`
- `find /var/www -name "*.bak" | xargs rm` - find backup files and delete them

## Head and Tail

Output the first or last part of files.

- `head -n 10 file.txt` - view the first 10 lines
- `tail -n 10 file.txt` - view the last 10 lines
- `tail -f /var/log/apache2/access.log` - follow/monitor a log file in real-time

## Demonstrations & Real-World Use Cases

Here are practical combinations commonly used in CTFs and security assessments.

### 1. Extracting Active Users and Shells from `/etc/passwd`
Filter out system accounts (UID < 1000) and service shells, showing only true login users.

```bash
# Output format: username -> shell
awk -F: '$3 >= 1000 && $7 !~ /nologin|false/ {print $1 " -> " $7}' /etc/passwd
```
*Demonstration Input:*
```text
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
jake:x:1001:1001::/home/jake:/bin/bash
alice:x:1002:1002::/home/alice:/bin/sh
```
*Demonstration Output:*
```text
jake -> /bin/bash
alice -> /bin/sh
```

### 2. Parsing Nmap Grepable Output (`-oG`) for Open Ports
Find all IP addresses that have port `80` (HTTP) open from an Nmap scan.

```bash
# Grep for lines containing '/open/tcp//http/' and print the IP address (2nd field)
grep '/open/tcp//http/' nmap.gnmap | awk '{print $2}'
```
*Demonstration Input:*
```text
Host: 10.10.10.5 ()    Ports: 22/open/tcp//ssh/, 80/open/tcp//http/
Host: 10.10.10.12 ()   Ports: 22/open/tcp//ssh/, 443/open/tcp//https/
Host: 10.10.10.45 ()   Ports: 80/open/tcp//http/, 8080/open/tcp//http-proxy/
```
*Demonstration Output:*
```text
10.10.10.5
10.10.10.45
```

### 3. Extracting Top Most Frequent IP Addresses from Web Access Logs
Quickly identify scanning activity or high-traffic hosts from an Apache access log.

```bash
# Extract the first column (IP), count duplicates, sort numerically descending, and take top 5
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 5
```
*Demonstration Input:*
```text
192.168.1.50 - - [11/Jun/2026] "GET /index.php" 200 450
10.0.0.12 - - [11/Jun/2026] "GET /admin" 404 220
192.168.1.50 - - [11/Jun/2026] "GET /login" 200 310
192.168.1.50 - - [11/Jun/2026] "POST /login" 302 0
10.0.0.12 - - [11/Jun/2026] "GET /favicon.ico" 200 120
192.168.1.100 - - [11/Jun/2026] "GET /" 200 1500
```
*Demonstration Output:*
```text
      3 192.168.1.50
      2 10.0.0.12
      1 192.168.1.100
```

### 4. Cleaning Up Web Directory Traversal Wordlist
Remove comments, empty lines, and normalize Windows directory paths to Linux format for a tool.

```bash
# Remove empty lines, comments starting with #, and replace backslashes with forward slashes
grep -vE '^\s*(#|$)' paths.txt | tr '\\' '/' | sort -u
```
*Demonstration Input:*
```text
# Common backups
\var\www\backup.zip

\var\www\html\config.php
# Obsolete paths
\opt\old\
```
*Demonstration Output:*
```text
/opt/old/
/var/www/backup.zip
/var/www/html/config.php
```
