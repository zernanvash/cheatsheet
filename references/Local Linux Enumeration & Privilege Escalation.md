## Quick SUID Check

Use this during Linux privilege escalation to list files with the SUID bit set:

```bash
find / -perm -4000 -type f 2>/dev/null
```

<b>Kernel, Operating System &amp; Device Information:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>uname -a</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Print all available system information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>uname -r</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Kernel release</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>uname -n</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">System hostname</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>hostname</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>uname -m</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Linux kernel architecture (32 or 64 bit)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /proc/version</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Kernel information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/*-release</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Distribution information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/issue</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /proc/cpuinfo</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">CPU information</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>df -a</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">File system information</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Users &amp; Groups:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/passwd</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all users on the system</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/group</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all groups on the system</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/shadow</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Show user hashes – <span style="color: #ff0000;">Privileged command</span></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>grep -v -E "^#" /etc/passwd | awk -F: '$3 == 0 { print $1}'</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all super user accounts</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>finger</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Users currently logged in</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>pinky</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>users</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>who -a</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>w</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Who is currently logged in and what they’re doing</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>last</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Listing of last logged on users</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>lastlog</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Information on when all users last logged in</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>lastlog –u %username%</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Information on when the specified user last logged in</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span id="more-1721"></span></p>
<p><span style="font-family: Arial, sans-serif;"><b>User &amp; Privilege Information:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>whoami</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Current username</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>id</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Current user information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/sudoers</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Who’s allowed to do what as root – <span style="color: #ff0000;">Privileged command</span></span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>sudo -l</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Can the current user perform anything as root</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Environmental Information:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>env</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Display environmental variables</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>set</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>echo $PATH</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Path information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>history</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Displays command history of current user</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>pwd</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Print working directory, i.e. ‘where am I’</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/profile</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Display default system variables</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Interesting Files:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -perm -4000 -type f 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find SUID files</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -uid 0 -perm -4000 -type f 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find SUID files owned by root</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -perm -2000 -type f 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find files with GUID bit set</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -perm -2 -type f 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find world-writable files</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -perm -2 -type d 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find word-writable directories </span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find /home –name *.rhosts -print 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find rhost config files</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -ahlR /root/</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">See if you can access other user directories to find interesting files&nbsp;&nbsp;–&nbsp;<span style="color: #ff0000;">Privileged command</span></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat ~/.bash_history</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Show the current users’ command history</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -la ~/.*_history</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Show the current users’ various history files</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -la ~/.ssh/ </code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Check for interesting ssh files in the current users’ directory</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -la /usr/sbin/in.*</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Check Configuration of inetd services</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>grep -l -i pass /var/log/*.log 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Check log files for keywords (‘pass’ in this example) and show positive matches</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find /var/log -type f -exec ls -la {} \; 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List files in specified directory (/var/log)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find /var/log -name *.log -type f -exec ls -la {} \; 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List .log files in specified directory (/var/log)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find /etc/ -maxdepth 1 -name *.conf -type f -exec ls -la {} \; 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List .conf files in /etc (recursive 1 level)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -la /etc/*.conf</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="24" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -maxdepth 4 -name *.conf -type f -exec grep -Hn password {} \; 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Find .conf files (recursive 4 levels) and output line number where the word password is located</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>lsof -i -n</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List open files (output will depend on account privileges)</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Service Information:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ps aux | grep root</code></span></td>
<td width="54%">View services running as root</td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/inetd.conf</code></span></td>
<td width="54%">List services managed by inetd</td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/xinetd.conf</code></span></td>
<td width="54%">As above for xinetd</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Jobs/Tasks:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>crontab -l -u %username%</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Display scheduled jobs for the specified user –&nbsp;<span style="color: #ff0000;">Privileged command</span></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -la /etc/cron*</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Scheduled jobs overview (hourly, daily, monthly etc)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ls -aRl /etc/cron* | awk '$1 ~ /w.$/' 2&gt;/dev/null</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">What can ‘others’ write in /etc/cron* directories</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>top</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List of current tasks</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Networking, Routing &amp; Communications:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>/sbin/ifconfig -a</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all network interfaces</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/network/interfaces</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>arp -a</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Display ARP communications</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>route</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Display route information</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/resolv.conf</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Show configured DNS sever addresses</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>netstat -antp</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all TCP sockets and related PIDs (-p&nbsp;<span style="color: #ff0000;">Privileged command</span>)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>netstat -anup</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List all UDP sockets and related PIDs&nbsp;(-p&nbsp;<span style="color: #ff0000;">Privileged command</span>)</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>iptables -L</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List rules&nbsp;–&nbsp;<span style="color: #ff0000;">Privileged command</span></span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>cat /etc/services</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">View port numbers/services mappings</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Programs Installed:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Result</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>dpkg -l</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed packages (Debian)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>rpm -qa</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed packages (Red Hat)</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>sudo -V</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Sudo version – does an exploit exist?</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>httpd -v</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Apache version</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>apache2 -v</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>apache2ctl (or apachectl) -M</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">List loaded Apache modules</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>mysql --version</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed MYSQL version details</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>perl -v</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed Perl version details</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>java -version</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed Java version details</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>python --version</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed Python version details</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>ruby -v</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Installed Ruby version details</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -name %program_name% 2&gt;/dev/null</code>&nbsp;(i.e. nc, netcat, wget, nmap etc)</span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Locate ‘useful’ programs (netcat, wget etc)</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>which %program_name%</code> (i.e. nc, netcat, wget, nmap etc)</span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">As above</span></td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><span style="font-family: Arial, sans-serif;"><b>Common Shell Escape Sequences:</b></span></p>
<table border="1" cellpadding="10" cellspacing="0" width="100%">
<colgroup>
<col width="117">
<col width="139"> </colgroup>
<tbody>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><b>Command</b></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;"><b>Program(s)</b></span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>:!bash</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">vi, vim</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>:set shell=/bin/bash</code></span><span style="font-family: Arial, sans-serif;"><code>:shell</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">vi, vim</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>!bash</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">man,&nbsp;</span><span style="font-family: Arial, sans-serif;">more,&nbsp;</span><span style="font-family: Arial, sans-serif;">less</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>find / -exec /usr/bin/awk 'BEGIN {system("/bin/bash")}' \; </code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">find</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>awk 'BEGIN {system("/bin/bash")}'</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">awk</span></td>
</tr>
<tr valign="TOP">
<td height="1" width="46%"><span style="font-family: Arial, sans-serif;"><code>--interactive</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">nmap</span></td>
</tr>
<tr valign="TOP">
<td width="46%"><span style="font-family: Arial, sans-serif;"><code>perl -e 'exec "/bin/bash";'</code></span></td>
<td width="54%"><span style="font-family: Arial, sans-serif;">Perl</span>
