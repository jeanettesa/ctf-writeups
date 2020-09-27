# linux starter

## Problem description

Don't Try to break this jail

ssh wolfie@linuxstarter.darkarmy.xyz -p 8001 password : wolfie

## Solving the challenge

Connected to the server through ssh.

Found the OS: \
![](./os_scaled.png)

Checked current working directory: \
![](./pwd_scaled.png)


Since it is Ubuntu, thought I would first check .bashrc and .profile: \
*wolfie@9ad161dbc9ce:~$ cat .bashrc .profile*
```
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

(...)
```

Didn't find any configuration except the default, but the `HISTCONTROL` parameter made me
look for the flag using the history command: \
![](./history_scaled.png)

Turns out that `/home/wolfie/imp/flag.txt` has the flag: \
![](./flag_scaled.png)
