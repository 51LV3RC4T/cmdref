
---
Description :
     Change file owner

Parameters : #username #file

```cmd
chown {{username}} {{file}}
```

```example
chown root sensitive.txt
```

Tags :  #linux #chown #permissions #fundamentals

---

Description :
     Change file group

Parameters : #groupname #file

```cmd
chgrp {{groupname}} {{file}}
```

```example
chgrp users notes.txt
```

Tags :  #linux #chgrp #permissions #fundamentals

---

Description :
     Change owner and group together

Parameters : #username #groupname #file

```cmd
chown {{username}}:{{groupname}} {{file}}
```

```example
chown www-data:www-data index.php
```

Tags :  #linux #chown #permissions #fundamentals

---

Description :
     Change mode (recursive)

Parameters : #file

```cmd
chmod -R u+rwx {{file}}
```

```example
chmod -R u+rwx /tmp/scripts
```

Tags :  #linux #chmod #permissions #fundamentals

---

Description :
     Add execute bit for user

Parameters : #file

```cmd
chmod u+x {{file}}
```

```example
chmod u+x exploit.sh
```

Tags :  #linux #chmod #permissions #fundamentals

---

Description :
     Edit sudoers safely (use visudo)

Parameters :

```cmd
visudo
```

```example
visudo
```

Tags :  #linux #sudo #fundamentals

---

Description :
     List sudo privileges for current user

Parameters :

```cmd
sudo -l
```

```example
sudo -l
```

Tags :  #linux #sudo #privesc #fundamentals

---

Description :
     Run shell as another user with sudo

Parameters : #username

```cmd
sudo -u {{username}} /bin/bash
```

```example
sudo -u root /bin/bash
```

Tags :  #linux #sudo #privesc #fundamentals

---

Description :
     Journal logs for a systemd unit

Parameters : #servicename

```cmd
journalctl -u {{servicename}} -n 100 --no-pager
```

```example
journalctl -u ssh -n 100 --no-pager
```

Tags :  #linux #journalctl #logs #fundamentals

---

Description :
     Journal logs reverse chronological

Parameters :

```cmd
journalctl -r -n 50 --no-pager
```

```example
journalctl -r -n 50 --no-pager
```

Tags :  #linux #journalctl #logs #fundamentals

---

Description :
     Follow service logs live

Parameters : #servicename

```cmd
journalctl -u {{servicename}} -f
```

```example
journalctl -u nginx -f
```

Tags :  #linux #journalctl #logs #fundamentals

---

Description :
     Start systemd service

Parameters : #servicename

```cmd
systemctl start {{servicename}}
```

```example
systemctl start apache2
```

Tags :  #linux #systemctl #fundamentals

---

Description :
     Service status

Parameters : #servicename

```cmd
systemctl status {{servicename}}
```

```example
systemctl status ssh
```

Tags :  #linux #systemctl #fundamentals

---

Description :
     Show user and group IDs

Parameters : #username

```cmd
id {{username}}
```

```example
id www-data
```

Tags :  #linux #id #fundamentals

---

Description :
     Last logins

Parameters :

```cmd
last -a | head -n 20
```

```example
last -a | head -n 20
```

Tags :  #linux #last #fundamentals

---

Description :
     Users with login shell

Parameters :

```cmd
grep -v "/nologin\|/false" /etc/passwd
```

```example
grep -v "/nologin\|/false" /etc/passwd
```

Tags :  #linux #passwd #enum #fundamentals

---
