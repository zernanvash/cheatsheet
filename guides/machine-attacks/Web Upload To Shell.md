# Web Upload To Shell

Use when a web application accepts uploaded files or has a CMS/plugin upload feature.

## Signals

- Upload form, avatar upload, document import, media manager, CMS admin panel.
- Server stack suggests executable extension: PHP, ASPX, JSP, CGI.
- Uploaded file is reachable over HTTP.

## Main Path

1. Identify allowed extensions and content checks.
2. Upload a harmless proof file first.
3. Determine storage path and execution behavior.
4. Use a stack-matched lab shell only when executable upload is confirmed.

```bash
ffuf -u http://target/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -e .php,.txt,.bak,.zip
curl -i -F 'file=@proof.txt' http://target/upload
```

## Options To Try

- Extension bypasses: `.phtml`, `.php5`, double extension, case changes, trailing dot where applicable.
- Content-type bypass: set MIME to image type while preserving executable extension.
- Image processing path: test metadata processors such as ExifTool/ImageMagick only in lab scope.
- If execution fails but read works, use upload for LFI log/source chaining.
- If admin access is required, hunt default creds or config leaks first.

## Study Examples

- Cajac and 0xb0b web challenge indexes include many web-first rooms where upload, CMS CVE, or source leak becomes the foothold.
