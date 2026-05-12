
---
Description :
     Print current working directory

Parameters :

```cmd
pwd
```

```example
pwd
```

Tags :  #linux #basic #fundamentals

---

Description :
     List directory contents (long, all, human sizes)

Parameters : #directory

```cmd
ls -la {{directory}}
```

```example
ls -la /home
```

Tags :  #linux #basic #ls #fundamentals

---

Description :
     Change working directory

Parameters : #directory

```cmd
cd {{directory}}
```

```example
cd /tmp
```

Tags :  #linux #basic #fundamentals

---

Description :
     Create directory (parents)

Parameters : #directory

```cmd
mkdir -p {{directory}}
```

```example
mkdir -p /tmp/work
```

Tags :  #linux #mkdir #fundamentals

---

Description :
     Copy file or directory recursively

Parameters : #file #directory

```cmd
cp -r {{file}} {{directory}}
```

```example
cp -r ./notes /tmp/backup
```

Tags :  #linux #cp #fundamentals

---

Description :
     Move or rename path

Parameters : #file #directory

```cmd
mv {{file}} {{directory}}
```

```example
mv old.txt /tmp/new.txt
```

Tags :  #linux #mv #fundamentals

---

Description :
     Remove file (force)

Parameters : #file

```cmd
rm -f {{file}}
```

```example
rm -f ./junk.txt
```

Tags :  #linux #rm #fundamentals

---

Description :
     Remove directory recursively

Parameters : #directory

```cmd
rm -rf {{directory}}
```

```example
rm -rf /tmp/work
```

Tags :  #linux #rm #fundamentals

---

Description :
     Display file contents

Parameters : #file

```cmd
cat {{file}}
```

```example
cat /etc/passwd
```

Tags :  #linux #cat #fundamentals

---

Description :
     First lines of a file

Parameters : #file

```cmd
head -n 50 {{file}}
```

```example
head -n 50 /var/log/auth.log
```

Tags :  #linux #head #fundamentals

---

Description :
     Last lines of a file (follow with -f)

Parameters : #file

```cmd
tail -n 50 {{file}}
```

```example
tail -n 50 /var/log/syslog
```

Tags :  #linux #tail #fundamentals

---

Description :
     Search lines matching pattern in file

Parameters : #file

```cmd
grep -n "root" {{file}}
```

```example
grep -n "root" /etc/passwd
```

Tags :  #linux #grep #fundamentals

---

Description :
     Recursive search in directory for pattern

Parameters : #directory

```cmd
grep -Rni "password" {{directory}} 2>/dev/null
```

```example
grep -Rni "password" /var/www 2>/dev/null
```

Tags :  #linux #grep #fundamentals

---

Description :
     Find files by name under path

Parameters : #directory #file

```cmd
find {{directory}} -name "{{file}}" 2>/dev/null
```

```example
find / -name "*.conf" 2>/dev/null
```

Tags :  #linux #find #fundamentals

---

Description :
     Find files with SUID bit set

Parameters :

```cmd
find / -perm -4000 -type f 2>/dev/null
```

```example
find / -perm -4000 -type f 2>/dev/null
```

Tags :  #linux #find #suid #privesc #fundamentals

---

Description :
     Locate binary in PATH

Parameters : #binary

```cmd
which {{binary}}
```

```example
which python3
```

Tags :  #linux #which #fundamentals

---

Description :
     Resolve command type (alias, builtin, file)

Parameters : #binary

```cmd
type {{binary}}
```

```example
type ls
```

Tags :  #linux #type #fundamentals

---

Description :
     Download URL to file with curl

Parameters : #url #file

```cmd
curl -sSL "{{url}}" -o {{file}}
```

```example
curl -sSL "https://example.com/l.txt" -o l.txt
```

Tags :  #linux #curl #fundamentals

---

Description :
     Fetch URL (silent, show headers)

Parameters : #url

```cmd
curl -sI "{{url}}"
```

```example
curl -sI "http://10.10.10.10/"
```

Tags :  #linux #curl #fundamentals

---

Description :
     Download file with wget

Parameters : #url

```cmd
wget "{{url}}"
```

```example
wget "http://{{target-ip}}/backup.zip"
```

Tags :  #linux #wget #fundamentals

---

Description :
     Show disk usage of path

Parameters : #directory

```cmd
du -sh {{directory}}
```

```example
du -sh /var/log
```

Tags :  #linux #du #fundamentals

---

Description :
     Create nested path and file (heredoc)

Parameters : #directory #file

```cmd
mkdir -p {{directory}} && echo "content" > {{directory}}/{{file}}
```

```example
mkdir -p /tmp/x && echo "test" > /tmp/x/note.txt
```

Tags :  #linux #fundamentals

---
