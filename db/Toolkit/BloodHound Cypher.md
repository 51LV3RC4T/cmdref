
---
Description :
     Cypher — users with SPN (Kerberoast candidates)

Parameters :

```cmd
MATCH (u:User {hasspn:true}) RETURN u.name, u.serviceprincipalnames
```

```example
MATCH (u:User {hasspn:true}) RETURN u.name, u.serviceprincipalnames
```

Tags :  #linux #bloodhound #cypher #ad #toolkit

---

Description :
     Cypher — AS-REP roastable (DontReqPreAuth)

Parameters :

```cmd
MATCH (u:User {dontreqpreauth: true}) RETURN u.name
```

```example
MATCH (u:User {dontreqpreauth: true}) RETURN u.name
```

Tags :  #linux #bloodhound #cypher #asreproast #toolkit

---

Description :
     Cypher — shortest paths from owned user to Domain Admins

Parameters : #username

```cmd
MATCH (o:User {name: $n}), (g:Group), p=shortestPath((o)-[*1..]->(g)) WHERE g.name CONTAINS 'DOMAIN ADMINS' RETURN p
```

```example
MATCH (o:User {name: 'USER@CORP.LOCAL'}), (g:Group), p=shortestPath((o)-[*1..]->(g)) WHERE g.objectid ENDS WITH '-512' RETURN p
```

Tags :  #linux #bloodhound #cypher #path #toolkit

---

Description :
     Cypher — computers where Domain Users has local admin (generic)

Parameters :

```cmd
MATCH (g:Group {name:'DOMAIN USERS@CORP.LOCAL'})-[:MemberOf*1..]->(mg:Group)-[:AdminTo]->(c:Computer) RETURN c.name
```

```example
MATCH (g:Group)-[:AdminTo]->(c:Computer) WHERE g.name =~ '(?i).*domain users.*' RETURN g.name, c.name LIMIT 50
```

Tags :  #linux #bloodhound #cypher #toolkit

---

Description :
     Cypher — unconstrained delegation computers

Parameters :

```cmd
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name
```

```example
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name
```

Tags :  #linux #bloodhound #cypher #delegation #toolkit

---

Description :
     Cypher — constrained delegation allowed targets

Parameters :

```cmd
MATCH (c:Computer)-[:AllowedToDelegate]->(t) RETURN c.name, labels(t), coalesce(t.name,t.objectid)
```

```example
MATCH (c:Computer)-[:AllowedToDelegate]->(t) RETURN c.name, t.name
```

Tags :  #linux #bloodhound #cypher #delegation #toolkit

---

Description :
     Cypher — RDP or HasSession edges to high-value targets

Parameters :

```cmd
MATCH (u:User)-[:CanRDP|MemberOf*1..]->(x) RETURN u.name, type(x), x.name LIMIT 100
```

```example
MATCH (u:User)-[r:CanRDP]->(c:Computer) RETURN u.name, c.name
```

Tags :  #linux #bloodhound #cypher #toolkit

---

Description :
     Cypher — owned objects marker query template (replace OWNED_USER)

Parameters :

```cmd
MATCH (o:User) WHERE o.name =~ '(?i).*OWNED.*' MATCH (o)-[r]->(n) RETURN type(r), n LIMIT 200
```

```example
MATCH (o:User) WHERE o.owned=true MATCH (o)-[r]->(n) RETURN type(r), labels(n), n.name LIMIT 200
```

Tags :  #linux #bloodhound #cypher #toolkit

---

Description :
     Cypher — DCSync principals (generic BloodHound 4.x style)

Parameters :

```cmd
MATCH (n) WHERE ANY(x IN n.highvalue WHERE x = true) MATCH p=(s)-[:MemberOf|GetChanges|GetChangesAll*1..]->(d:Domain) RETURN p LIMIT 25
```

```example
MATCH (g:Group) WHERE g.name CONTAINS 'EXCHANGE' MATCH (g)-[:MemberOf*..]->(x) RETURN g,x LIMIT 50
```

Tags :  #linux #bloodhound #cypher #dcsync #toolkit

---

Description :
     Cypher — GPOs linked to OU affecting computers

Parameters :

```cmd
MATCH (g:GPO)-[:GpLink]->(ou:OU) RETURN g.name, ou.name
```

```example
MATCH (g:GPO)-[:GpLink]->(ou:OU) RETURN g.name, ou.name
```

Tags :  #linux #bloodhound #cypher #gpo #toolkit

---
