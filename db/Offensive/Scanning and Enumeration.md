
---
Description :
     Nmap default scripts and service version on single host

Parameters : #target-ip

```cmd
nmap -sC -sV {{target-ip}}
```

```example
nmap -sC -sV 10.10.10.10
```

Tags :  #linux #nmap #oscp #pen-200 #enum

---

Description :
     Nmap all TCP ports (top ports aggressive timing)

Parameters : #target-ip

```cmd
nmap -p- -T4 -sC -sV {{target-ip}}
```

```example
nmap -p- -T4 -sC -sV 10.10.10.10
```

Tags :  #linux #nmap #oscp #pen-200

---

Description :
     Nmap UDP top ports (slow)

Parameters : #target-ip

```cmd
nmap -sU --top-ports 50 {{target-ip}}
```

```example
nmap -sU --top-ports 50 10.10.10.10
```

Tags :  #linux #nmap #oscp #pen-200

---

Description :
     Nmap safe script scan for vulnerabilities

Parameters : #target-ip

```cmd
nmap --script vuln {{target-ip}}
```

```example
nmap --script vuln 10.10.10.10
```

Tags :  #linux #nmap #oscp #pen-200

---

Description :
     Nmap SMB scripts against host

Parameters : #target-ip

```cmd
nmap -p 445 --script smb-enum-shares,smb-enum-users {{target-ip}}
```

```example
nmap -p 445 --script smb-enum-shares,smb-enum-users 10.10.10.10
```

Tags :  #linux #nmap #smb #oscp #pen-200

---

Description :
     Host discovery ping sweep on subnet (edit CIDR for your lab)

Parameters :

```cmd
nmap -sn 10.10.10.0/24
```

```example
nmap -sn 10.10.10.0/24
```

Tags :  #linux #nmap #ping #oscp #pen-200

---

Description :
     Dig ANY query

Parameters : #domain

```cmd
dig ANY {{domain}} @8.8.8.8
```

```example
dig ANY example.com @8.8.8.8
```

Tags :  #linux #dig #dns #oscp #pen-200

---

Description :
     SNMP one-liner walk (public string)

Parameters : #target-ip

```cmd
snmpwalk -v 2c -c public {{target-ip}}
```

```example
snmpwalk -v 2c -c public 10.10.10.10
```

Tags :  #linux #snmp #oscp #pen-200

---

Description :
     Netcat port banner grab

Parameters : #target-ip #target-port

```cmd
nc -nv {{target-ip}} {{target-port}}
```

```example
nc -nv 10.10.10.10 80
```

Tags :  #linux #nc #oscp #pen-200

---
