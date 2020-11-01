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

Used `ls` command to look for the flag in the current folder:
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

Listed files in the current folder:
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

`ls` showed current directory had a lot of folders:

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
