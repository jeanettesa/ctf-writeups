# shebang0-5

## shebang0
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 125

### Problem description
Welcome to the Shebang Linux Series. Here you will be tested on your basic
command line knowledge! These challenges will be done through an ssh connection.
Also please do not try and mess up the challenges on purpose, and report any
problems you find to the challenge author. You can find the passwords at /etc/passwords.
The username is the challenge title, shebang0-5, and the password is the previous
challenges flag, but for the first challenge, its shebang0.

The first challenge is an introductory challenge. Connect to cyberyoddha.baycyber.net
on port 1337 to receive your flag!

### Solution
Connected via ssh using the following command:
```
$ ssh shebang0@cyberyoddha.baycyber.net -p 1337
shebang0@cyberyoddha.baycyber.net's password: # insert password shebang0
```

Used `ls` command to look for the flag in the current directory:
```
$ ls -al
total 12
dr-x------ 1 shebang0 root 4096 Oct 30 07:07 .
drwxr-xr-x 1 root     root 4096 Oct 30 07:07 ..
-rw-r--r-- 1 root     root   33 Oct  6 00:26 .flag.txt
```

There was file called `.flag.txt`.

Output the file contents using `cat`:
```
$ cat .flag.txt    
CYCTF{w3ll_1_gu3$$_b@sh_1s_e@zy}
```

Thus, the flag is `CYCTF{w3ll_1_gu3$$_b@sh_1s_e@zy}`.

## shebang1
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 125

### Problem description
This challenge is simple.

### Solution
Connected via ssh with user shebang1.

Listed files in the current directory:
```
$ ls
flag.txt
```

Tried to `cat` the flag:
```
$ cat flag.txt
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
(....)
```

File `flag.txt` contained a lot of information. The `wc` command suggested
it contained 9522 lines.

```
$ wc -l flag.txt
9522 flag.txt
```

So it seemed easier to search for the flag (special characters) using `grep`:
```
$ grep "{"
flag.txt:CYCTF{w3ll_1_gu3$$_y0u_kn0w_h0w_t0_gr3p}
```

So the flag for shebang1 is `CYCTF{w3ll_1_gu3$$_y0u_kn0w_h0w_t0_gr3p}`.

## shebang2
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 150

### Problem description
This is a bit harder.

### Solution
Connected via ssh with user shebang2.

`ls` showed current directory had a lot of directories:

```
$ ls -al
total 412
dr-x------ 1 shebang2 root 4096 Oct 31 01:01 .
drwxr-xr-x 1 root     root 4096 Oct 31 00:49 ..
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 1
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 10
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 100
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 11
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 12
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 13
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 14
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 15
drwxr-xr-x 2 root     root 4096 Oct 14 18:37 16
(...)
```

Recursive `ls` (with the `-R` argument) showed each directory had a lot of files:

```
$ ls -lR
(...)
./1:
total 400
-rw-r--r-- 1 root root 19 Oct 14 18:37 1
-rw-r--r-- 1 root root 19 Oct 14 18:37 10
-rw-r--r-- 1 root root 19 Oct 14 18:37 100
-rw-r--r-- 1 root root 19 Oct 14 18:37 11
-rw-r--r-- 1 root root 19 Oct 14 18:37 12
-rw-r--r-- 1 root root 19 Oct 14 18:37 13
-rw-r--r-- 1 root root 19 Oct 14 18:37 14
-rw-r--r-- 1 root root 19 Oct 14 18:37 15
-rw-r--r-- 1 root root 19 Oct 14 18:37 16
-rw-r--r-- 1 root root 19 Oct 14 18:37 17
(...)
```

Tried to `cat` the content of all files to look for patterns:

```
$ cat */*
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
This is not a flag
(...)
```

Then tried to `grep` (using `-rv` arguments) recursively for files not containing
the string: `This is not a flag`.

```
$ grep -rv "This is not a flag"
86/13:CYCTF{W0w_th@t$_@_l0t_0f_f1l3s}
```

Thus, the flag for shebang2 is: `CYCTF{W0w_th@t$_@_l0t_0f_f1l3s}`.

## shebang3
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 150

### Problem description
These files are the same...

### Solution
Connected via ssh as user shebang3.

Executing the `ls` command in the current directory showed two files:

```
$ ls
file.txt  file2.txt
```

The problem description gives a clue that we need to find differences between
the files.

In [stackoverflow](https://stackoverflow.com/questions/18204904/fast-way-of-finding-lines-in-one-file-that-are-not-in-another)
I found a solution to find lines in one file that are not in the other:

```
$ grep -F -x -v -f file.txt file2.txt
C
Y
C
T
F
{
S
P
T
T
H
F
F
}
(...)
```

The string looked promising, but submitting it showed it was not the entire
flag. So I tried to `grep` for all lines with exactly one character in `file.txt`:

```
$ grep "^.$" file2.txt
1
C
Y
C
T
F
{
S
P
O
T
_
T
H
3
_
D
1
F
F
}
(...)
```

Thus, the flag for shebang3 is: `CYCTF{SPOT_TH3_D1FF}`.

## shebang4
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 200

### Problem description
Since you have been doing so well, I thought I would make this an easy one.

### Solution
Connected via ssh as user shebang4.

Listing current directory contents showed the flag in a `png` file:

```
$ ls
flag.png
```

To make it easier to view the file, I disconnected from ssh and transferred
the image file to my own computer using `scp`:
```
$ scp -P1337 shebang4@cyberyoddha.baycyber.net:/home/shebang4/flag.png .
shebang4@cyberyoddha.baycyber.net's password:
flag.png
100%   12KB  62.4KB/s   00:00
```

Viewing the image showed the flag:

![flag4](./flag_shebang4.png)

So the flag for shebang4 is: `CYCTF{W3ll_1_gu3$$_th@t_w@s_actually_easy}`.

## shebang5
Author: stephencurry396 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Points: 250

### Problem description
there is a very bad file on this Server. can yoU fInD it.

### Concepts
* [setuid](https://en.wikipedia.org/wiki/Setuid)

### Solution
Connected via ssh as user shebang5.

Listing current directory contents showed only the empty file .hushlogin.

```
$ ls -al
total 12
dr-x------ 1 shebang5 root 4096 Oct 31 01:01 .
drwxr-xr-x 1 root     root 4096 Oct 31 00:49 ..
-rw-r--r-- 1 root     root    0 Oct 31 01:01 .hushlogin
```

Actually, the capitalization in the problem description (UID) suggests that
maybe we need to look for a file with the `SUID` permission set.

As stated in the wikipedia entry on [setuid](https://en.wikipedia.org/wiki/Setuid):

> The Unix access rights flags setuid and setgid (short for "set user ID" and
"set group ID") allow users to run an executable with the file system permissions
of the executable's owner or group respectively and to change behaviour in directories.
They are often used to allow users on a computer system to run programs with
temporarily elevated privileges in order to perform a specific task.

Used the `find` command to look for a file with such permissions:
```
$ find / -perm /u=s,g=s 2>/dev/null
/var/mail
/var/local
/var/cat
/usr/sbin/unix_chkpwd
/usr/sbin/pam_extrausers_chkpwd
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/wall
/usr/bin/chage
/usr/bin/chsh
(...)
```

The `/var/cat` file stood out, as `cat` is usually located in the `/usr/bin`
directory, without the `SUID` permission set.

Executing the file to check that it behaves as the regular `cat` program:
```
$ /var/cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
(...)
```

Examining the file attributes with `ls`, we can see that the owner of `/var/cat`
is `shebang6`:
```
$ ls -al /var/cat
---s--x--x 1 shebang6 root 16992 Oct 14 20:51 /var/cat
```

Now we can use the `find` command to look for files owned by `shebang6`:
```
$ find / -user shebang6 2>/dev/null
/var/cat
/etc/passwords/shebang6
```

The file `/etc/passwords/shebang6` looked promising, so tried to output its
content with `/var/cat`:

```
$ /var/cat /etc/passwords/shebang6
CYCTF{W3ll_1_gu3$$_SU1D_1$_e@$y_fl@g$}
```

Thus, the flag for shebang5 is `CYCTF{W3ll_1_gu3$$_SU1D_1$_e@$y_fl@g$}`.
