
---
Description :
     Gobuster directory brute force

Parameters : #url #file

```cmd
gobuster dir -u "{{url}}" -w {{file}} -t 50
```

```example
gobuster dir -u "http://10.10.10.10/" -w /usr/share/wordlists/dirb/common.txt -t 50
```

Tags :  #linux #gobuster #web #oscp #pen-200

---

Description :
     Gobuster with extension list

Parameters : #url #file

```cmd
gobuster dir -u "{{url}}" -w {{file}} -x php,txt,bak,html -t 40
```

```example
gobuster dir -u "http://10.10.10.10/" -w /usr/share/wordlists/dirb/common.txt -x php,txt,bak -t 40
```

Tags :  #linux #gobuster #web #oscp #pen-200

---

Description :
     FFUF quick directory fuzz

Parameters : #url #file

```cmd
ffuf -u "{{url}}/FUZZ" -w {{file}} -mc 200,204,301,302,307,401,403
```

```example
ffuf -u "http://10.10.10.10/FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 200,204,301,302,307,401,403
```

Tags :  #linux #ffuf #web #oscp #pen-200

---

Description :
     Nikto web scanner

Parameters : #url

```cmd
nikto -h "{{url}}"
```

```example
nikto -h "http://10.10.10.10"
```

Tags :  #linux #nikto #web #oscp #pen-200

---

Description :
     WhatWeb fingerprint

Parameters : #url

```cmd
whatweb -a 3 "{{url}}"
```

```example
whatweb -a 3 "http://10.10.10.10"
```

Tags :  #linux #whatweb #web #oscp #pen-200

---

Description :
     Curl follow redirects show response

Parameters : #url

```cmd
curl -sL "{{url}}" | head -n 80
```

```example
curl -sL "http://10.10.10.10/login.php" | head -n 80
```

Tags :  #linux #curl #web #oscp #pen-200

---

Description :
     Wfuzz single parameter test

Parameters : #url #file

```cmd
wfuzz -c -z file,{{file}} --hc 404 "{{url}}?id=FUZZ"
```

```example
wfuzz -c -z file,/usr/share/wordlists/wfuzz/general/common.txt --hc 404 "http://10.10.10.10/?id=FUZZ"
```

Tags :  #linux #wfuzz #web #oscp #pen-200

---

Description :
     SQLMap basic GET test

Parameters : #url

```cmd
sqlmap -u "{{url}}" --batch --risk 1 --level 1
```

```example
sqlmap -u "http://10.10.10.10/item.php?id=1" --batch --risk 1 --level 1
```

Tags :  #linux #sqlmap #web #oscp #pen-200

---
