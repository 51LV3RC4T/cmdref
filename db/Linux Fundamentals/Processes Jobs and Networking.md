
---
Description :
     List processes (full format)

Parameters :

```cmd
ps aux
```

```example
ps aux
```

Tags :  #linux #ps #fundamentals

---

Description :
     Process tree

Parameters :

```cmd
ps auxf
```

```example
ps auxf
```

Tags :  #linux #ps #fundamentals

---

Description :
     Interactive process viewer

Parameters :

```cmd
top
```

```example
top
```

Tags :  #linux #top #fundamentals

---

Description :
     Send graceful TERM to PID

Parameters : #pid

```cmd
kill -TERM {{pid}}
```

```example
kill -TERM 1234
```

Tags :  #linux #kill #fundamentals

---

Description :
     Force kill PID

Parameters : #pid

```cmd
kill -KILL {{pid}}
```

```example
kill -KILL 1234
```

Tags :  #linux #kill #fundamentals

---

Description :
     List background jobs in current shell

Parameters :

```cmd
jobs -l
```

```example
jobs -l
```

Tags :  #linux #jobs #fundamentals

---

Description :
     Bring background job to foreground

Parameters :

```cmd
fg
```

```example
fg
```

Tags :  #linux #jobs #fundamentals

---

Description :
     Listening TCP/UDP sockets with process info

Parameters :

```cmd
ss -tulpn
```

```example
ss -tulpn
```

Tags :  #linux #ss #network #fundamentals

---

Description :
     Legacy listening ports listing

Parameters :

```cmd
netstat -tulpn
```

```example
netstat -tulpn
```

Tags :  #linux #netstat #network #fundamentals

---

Description :
     Ping host a few times

Parameters : #target-ip

```cmd
ping -c 4 {{target-ip}}
```

```example
ping -c 4 10.10.10.10
```

Tags :  #linux #ping #network #fundamentals

---

Description :
     Trace route to host

Parameters : #target-ip

```cmd
traceroute {{target-ip}}
```

```example
traceroute 10.10.10.10
```

Tags :  #linux #traceroute #network #fundamentals

---

Description :
     DNS lookup (short)

Parameters : #domain

```cmd
host {{domain}}
```

```example
host example.com
```

Tags :  #linux #host #dns #fundamentals

---

Description :
     Open TCP connection test with bash

Parameters : #target-ip #target-port

```cmd
timeout 2 bash -c "echo >/dev/tcp/{{target-ip}}/{{target-port}}" && echo open || echo closed
```

```example
timeout 2 bash -c "echo >/dev/tcp/10.10.10.10/445" && echo open || echo closed
```

Tags :  #linux #bash #network #fundamentals

---
