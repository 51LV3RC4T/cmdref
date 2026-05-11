<!-- cmdref DB — Network Scanning
     Each entry lives between two --- lines.
     Use the workflow template for new entries.
-->

# Network Scanning

---

Description :
    Aggressive Nmap scan — OS detection, version detection, scripts, traceroute

Parameters : #cmd_ref_target #cmd_ref_param_file

```cmd
nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
```

```example
nmap -A 10.10.10.10 -oN output.txt
```

Tags : #nmap #scan #recon #linux

---

Description :
    Aggressive Nmap scan with T4 timing (faster, less stealthy)

Parameters : #cmd_ref_target #cmd_ref_param_file

```cmd
nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}} -T4
```

```example
nmap -A 10.10.10.10 -oN output.txt -T4
```

Tags : #nmap #scan #recon #linux

---

Description :
    Full port scan — all 65535 TCP ports

Parameters : #cmd_ref_target #cmd_ref_param_file

```cmd
nmap -p- {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
```

```example
nmap -p- 10.10.10.10 -oN full-ports.txt
```

Tags : #nmap #scan #full #linux

---

Description :
    Nmap UDP scan on common UDP ports

Parameters : #cmd_ref_target #cmd_ref_param_file

```cmd
nmap -sU --top-ports 200 {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
```

```example
nmap -sU --top-ports 200 10.10.10.10 -oN udp-scan.txt
```

Tags : #nmap #scan #udp #linux

---

Description :
    Ping sweep of an entire subnet

Parameters : #cmd_ref_target

```cmd
nmap -sn {{cmd_ref_target}}
```

```example
nmap -sn 10.10.10.0/24
```

Tags : #nmap #discovery #linux

---

Description :
    Gobuster directory brute-force against a web server

Parameters : #cmd_ref_url #cmd_ref_param_file_users #cmd_ref_param_file

```cmd
gobuster dir -u {{cmd_ref_url}} -w {{cmd_ref_param_file_users}} -o {{cmd_ref_param_file}}
```

```example
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -o dirs.txt
```

Tags : #gobuster #web #directory #linux

---

Description :
    Netcat reverse shell listener

Parameters : #cmd_ref_attacker_port

```cmd
nc -lvnp {{cmd_ref_attacker_port}}
```

```example
nc -lvnp 9999
```

Tags : #netcat #shell #listener #linux

---

Description :
    Nikto web server vulnerability scanner

Parameters : #cmd_ref_url #cmd_ref_param_file

```cmd
nikto -h {{cmd_ref_url}} -o {{cmd_ref_param_file}}
```

```example
nikto -h http://10.10.10.10 -o nikto-output.txt
```

Tags : #nikto #web #scan #linux

---

Description :
    SMB enumeration with enum4linux

Parameters : #cmd_ref_target

```cmd
enum4linux -a {{cmd_ref_target}}
```

```example
enum4linux -a 10.10.10.10
```

Tags : #enum4linux #smb #recon #linux

---

Description :
    Hydra SSH brute-force attack

Parameters : #cmd_ref_target #cmd_ref_param_file_users #cmd_ref_param_file_pass

```cmd
hydra -L {{cmd_ref_param_file_users}} -P {{cmd_ref_param_file_pass}} ssh://{{cmd_ref_target}}
```

```example
hydra -L users.txt -P rockyou.txt ssh://10.10.10.10
```

Tags : #hydra #bruteforce #ssh #linux

---

Description :
    CrackMapExec SMB login check with credentials

Parameters : #cmd_ref_target #cmd_ref_param_file_users #cmd_ref_param_file_pass

```cmd
crackmapexec smb {{cmd_ref_target}} -u {{cmd_ref_param_file_users}} -p {{cmd_ref_param_file_pass}}
```

```example
crackmapexec smb 10.10.10.10 -u users.txt -p passwords.txt
```

Tags : #crackmapexec #smb #linux

---

Description :
    WinPEAS — Windows privilege escalation enumeration (Windows target)

Parameters : #cmd_ref_param_file

```cmd
.\winPEASx64.exe > {{cmd_ref_param_file}}
```

```example
.\winPEASx64.exe > winpeas_out.txt
```

Tags : #winpeas #privesc #windows

---
