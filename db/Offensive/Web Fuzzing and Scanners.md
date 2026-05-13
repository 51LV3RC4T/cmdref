
---
Description :
     feroxbuster recursive directory brute force

Parameters : #url #file

```cmd
feroxbuster -u "{{url}}" -w {{file}} -t 50 -k -r
```

```example
feroxbuster -u "http://10.10.10.10/" -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 50 -k -r
```

Tags :  #linux #feroxbuster #web #offensive

---

Description :
     feroxbuster with extensions

Parameters : #url #file

```cmd
feroxbuster -u "{{url}}" -w {{file}} -x php,html,bak,txt -t 40
```

```example
feroxbuster -u "http://10.10.10.10/" -w /usr/share/wordlists/dirb/common.txt -x php,html,bak -t 40
```

Tags :  #linux #feroxbuster #web #offensive

---

Description :
     wpscan aggressive plugins/themes enumeration

Parameters : #url

```cmd
wpscan --url "{{url}}" --enumerate ap,at,tt,cb,dbe,u --plugins-detection aggressive
```

```example
wpscan --url "http://10.10.10.10/blog/" --enumerate ap,at,u --plugins-detection aggressive
```

Tags :  #linux #wpscan #wordpress #web #offensive

---

Description :
     wpscan with API token (faster vulnerability data)

Parameters : #url

```cmd
wpscan --url "{{url}}" --api-token "$WPSCAN_API_TOKEN"
```

```example
wpscan --url "http://10.10.10.10/" --api-token "$WPSCAN_API_TOKEN"
```

Tags :  #linux #wpscan #wordpress #web #offensive

---

Description :
     ffuf host header fuzz virtual hosts

Parameters : #url #file

```cmd
ffuf -u "{{url}}" -H "Host: FUZZ" -w {{file}} -mc 200,204,301,302,403
```

```example
ffuf -u "http://10.10.10.10/" -H "Host: FUZZ" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200,301,302,403
```

Tags :  #linux #ffuf #web #offensive

---

Description :
     ffuf POST body fuzz

Parameters : #url #file

```cmd
ffuf -u "{{url}}" -X POST -d "user=admin&pass=FUZZ" -w {{file}} -fr "Invalid"
```

```example
ffuf -u "http://10.10.10.10/login.php" -X POST -d "user=admin&pass=FUZZ" -w /usr/share/wordlists/rockyou.txt -fr "Invalid"
```

Tags :  #linux #ffuf #web #offensive

---

Description :
     ffuf rate limited polite scan

Parameters : #url #file

```cmd
ffuf -u "{{url}}/FUZZ" -w {{file}} -t 5 -p 0.1 -mc 200,301,302,403
```

```example
ffuf -u "http://10.10.10.10/FUZZ" -w common.txt -t 5 -p 0.1 -mc 200,301,302,403
```

Tags :  #linux #ffuf #web #offensive

---

Description :
     nuclei quick templates scan

Parameters : #url

```cmd
nuclei -u "{{url}}" -severity medium,high,critical -silent
```

```example
nuclei -u "http://10.10.10.10/" -severity medium,high,critical -silent
```

Tags :  #linux #nuclei #web #offensive

---

Description :
     katana crawl pass URLs to ffuf pipeline style

Parameters : #url

```cmd
katana -u "{{url}}" -silent | httpx -silent
```

```example
katana -u "http://10.10.10.10/" -silent | httpx -silent
```

Tags :  #linux #katana #httpx #web #offensive

---
