# SMBClient Cheat Sheet

## Quick Use

- `smbclient -L //ip/` - list SMB shares
- `smbclient -L //ip/ -N` - list shares with no password
- `smbclient //ip/share` - connect to a share
- `smbclient //ip/share -N` - connect with no password
- `smbclient //ip/share -U username` - connect as a user
- `smbclient //ip/share -U 'domain\\username'` - connect with domain user

## Authentication

- `smbclient -L //ip/ -U username` - list shares as user
- `smbclient //ip/share -U username%password` - pass credentials inline
- `smbclient //ip/share -U username --pw-nt-hash hash` - authenticate with NT hash
- `smbclient //ip/share -k` - use Kerberos authentication
- `smbclient //ip/share -W DOMAIN -U username` - specify workgroup/domain

## Inside smbclient

- `help` - show available commands
- `ls` - list files
- `pwd` - show remote directory
- `cd folder` - change remote directory
- `lcd folder` - change local directory
- `get file` - download a file
- `mget *` - download multiple files
- `put file` - upload a file
- `mput *` - upload multiple files
- `mkdir folder` - create remote directory
- `rm file` - delete remote file
- `exit` - quit

## Downloading Files

- `smbclient //ip/share -N -c 'ls'` - run `ls` then exit
- `smbclient //ip/share -N -c 'get file.txt'` - download one file
- `smbclient //ip/share -N -c 'prompt off; mget *'` - download all files in current remote directory
- `smbclient //ip/share -N -c 'recurse on; prompt off; mget *'` - recursively download files

## Uploading Files

- `smbclient //ip/share -U username -c 'put shell.php'` - upload one file
- `smbclient //ip/share -U username -c 'mkdir test; cd test; put file.txt'` - create folder and upload
- `smbclient //ip/share -U username -c 'prompt off; mput *'` - upload all files in current local directory

## Useful Flags

- `-L` - list available shares
- `-N` - no password
- `-U user` - username
- `-W domain` - workgroup or domain
- `-I ip` - connect to specific IP when using a hostname
- `-p port` - specify SMB port
- `-m SMB3` - force SMB protocol version
- `-c 'command'` - run command non-interactively
- `-d 3` - increase debug level

## Common Enumeration Flow

- `smbclient -L //ip/ -N` - try anonymous share listing
- `smbclient -L //ip/ -U guest` - try guest login
- `smbclient //ip/share -N -c 'recurse on; ls'` - recursively list anonymous share
- `smbclient //ip/share -N -c 'recurse on; prompt off; mget *'` - download accessible files

## Troubleshooting

- `smbclient -L //ip/ -m SMB2` - force SMB2
- `smbclient -L //ip/ -m SMB3` - force SMB3
- `smbclient -L //ip/ -p 445` - connect on port 445
- `smbclient -L //ip/ -d 3` - show more debug output
