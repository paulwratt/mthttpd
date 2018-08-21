# Setting up a chroot jail

As mentioned in the sample installations article, running your web server in a chroot tree is very secure but inconvenient if you're using CGI. The only CGI programs you can run in such a setup are compiled statically-linked executables. If you want to write CGIs in, say, shell script, you will need a more complicated setup.

The basic idea of a chroot tree is you're reproducing a limited copy of the system-wide file tree. It includes only the files you need, nothing else. When the web server issues the chroot() system call, this sub-tree becomes the filesystem as far as that one process is concerned. It can't break out and get to the larger filesystem. Any child processes it spawns can't break out either. Obviously this adds a big layer of security. However, without access to things like shared libraries and interpreters, most programs can't run. So, to make a chroot tree in which you can run these programs, you have to put in some extra files.

Below is an `ls -lR` of the files needed for a FreeBSD-based chroot tree that allows shell script CGIs. This should be considered a starting point for your own chroot tree. If you're using another operating system, for instance Solaris, your tree will likely be very different. If you want to make one that allows perl, you'll have to add in all the perl files - the perl interpreter, libraries, perl files, include files, all sorts of stuff.

```
    total 15
    drwxr-xr-x  2 root  wheel  512 Nov 21 17:22 bin/
    drwxr-xr-x  2 root  wheel  512 Nov 21 18:17 dev/
    drwxr-xr-x  2 root  wheel  512 Nov 21 18:13 etc/
    drwxrwxrwt  2 root  wheel  512 Nov 21 17:11 tmp/
    drwxr-xr-x  7 root  wheel  512 Nov 21 18:06 usr/

    ./bin:
    total 1309
    -r-xr-xr-x  2 root  wheel   46600 May 17  1999 [*
    -r-xr-xr-x  1 root  wheel   55392 May 17  1999 cat*
    -r-xr-xr-x  1 root  wheel   58280 May 17  1999 chmod*
    -r-xr-xr-x  1 root  wheel   61184 May 17  1999 cp*
    -r-xr-xr-x  1 root  wheel  145784 May 17  1999 date*
    -r-xr-xr-x  1 root  wheel   41620 May 17  1999 echo*
    -r-xr-xr-x  1 root  wheel   84728 May 17  1999 expr*
    -r-xr-xr-x  1 root  wheel  155976 May 17  1999 mv*
    -r-xr-xr-x  1 root  wheel  158792 May 17  1999 rm*
    -r-xr-xr-x  1 root  wheel  321760 May 17  1999 sh*
    -r-xr-xr-x  1 root  wheel   42732 May 17  1999 sleep*
    -r-xr-xr-x  2 root  wheel   46600 May 17  1999 test*

    ./dev:
    total 0
    crw-rw-rw-  1 root  wheel    2,   2 Nov 21 17:12 null
    crw-rw-rw-  1 root  wheel   22,   2 Nov 21 18:17 stderr
    crw-rw-rw-  1 root  wheel   22,   0 Nov 21 18:17 stdin
    crw-rw-rw-  1 root  wheel   22,   1 Nov 21 18:17 stdout

    ./etc:
    total 2
    -r--r--r--  1 root  wheel  1000 Jul 21 15:50 localtime
    -rw-r--r--  1 root  wheel    38 Nov 12 18:42 resolv.conf

    ./usr:
    total 5
    drwxr-xr-x  2 root  wheel  512 Nov 21 18:21 bin/
    drwxr-xr-x  2 root  wheel  512 Nov 21 18:53 lib/
    drwxr-xr-x  2 root  wheel  512 Nov 21 18:06 libexec/
    drwxrwxrwt  2 root  wheel  512 Nov 21 17:11 tmp/

    ./usr/bin:
    total 747
    -r-xr-xr-x  1 root  wheel  119540 May 17  1999 awk*
    -r-xr-xr-x  3 root  wheel   38572 May 17  1999 egrep*
    -r-xr-xr-x  3 root  wheel   38572 May 17  1999 fgrep*
    -r-xr-xr-x  3 root  wheel   38572 May 17  1999 grep*
    -r-xr-xr-x  3 root  wheel   99448 May 17  1999 gunzip*
    -r-xr-xr-x  3 root  wheel   99448 May 17  1999 gzcat*
    -r-xr-xr-x  3 root  wheel   99448 May 17  1999 gzip*
    -r-xr-xr-x  1 root  wheel    4540 May 17  1999 head*
    -r-xr-xr-x  1 root  wheel    3356 May 17  1999 nice*
    -r-xr-xr-x  1 root  wheel   19300 May 17  1999 sed*
    -r-xr-xr-x  1 root  wheel   23940 May 17  1999 sort*
    -r-xr-xr-x  1 root  wheel    9976 May 17  1999 tail*
    -r-xr-xr-x  1 root  wheel    6388 May 17  1999 touch*
    -r-xr-xr-x  1 root  wheel    8636 May 17  1999 tr*
    -r-xr-xr-x  1 root  wheel    2356 May 17  1999 true*
    -r-xr-xr-x  1 root  wheel    5064 May 17  1999 uniq*
    -r-xr-xr-x  1 root  wheel    4384 May 17  1999 wc*

    ./usr/lib:
    total 2507
    -r--r--r--  1 root  wheel  1043748 Nov 21 18:52 libc.a
    lrwxrwxrwx  1 root  wheel        9 Nov 21 18:53 libc.so@ -> libc.so.3
    -r--r--r--  1 root  wheel   514015 May 17  1999 libc.so.3
    -r--r--r--  1 root  wheel    27066 May 17  1999 libgnuregex.a
    lrwxrwxrwx  1 root  wheel       16 Nov 21 18:53 libgnuregex.so@ -> libgnuregex.so.2
    -r--r--r--  1 root  wheel    27154 May 17  1999 libgnuregex.so.2
    -r--r--r--  1 root  wheel   262966 May 17  1999 libm.a
    lrwxrwxrwx  1 root  wheel        9 Nov 21 18:53 libm.so@ -> libm.so.2
    -r--r--r--  1 root  wheel   115780 May 17  1999 libm.so.2
    -r--r--r--  1 root  wheel    57612 May 17  1999 libz.a
    lrwxrwxrwx  1 root  wheel        9 Nov 21 18:53 libz.so@ -> libz.so.2
    -r--r--r--  1 root  wheel    51010 May 17  1999 libz.so.2

    ./usr/libexec:
    total 139
    -r-xr-xr-x  1 root  wheel  63652 May 17  1999 ld-elf.so.1*
    -r-xr-xr-x  1 root  wheel  77824 May 18  1999 ld.so*
```

A chroot setup like this is more secure than not doing chroot at all, but obviously less secure than the bare minimum static-binaries-only chroot jail. A poorly-written CGI shell script might allow an attacker to run arbitrary shell commands. Without chroot, this attacker would have access to the entire machine; with it, he or she is restricted to the chroot tree.

Also: it is actually possible to break out of chroot jail. A process running as root, either via a setuid program or some security hole, can change its own chroot tree to the next higher directory, repeating as necessary to get to the top of the filesystem. So, a chroot tree must be considered merely one aspect of a multi-layered defense-in-depth. If your chroot tree has enough tools in it for a cracker to gain root access, then it's no good; so you want to keep the contents to the minimum necessary. In particular, don't include any setuid-root executables!

One idea I haven't tried, which might give improved security while still allowing CGI access, is to use the _noexec_ filesystem mount option. This is a flag you can set on a disk partition that tells the system to not allow any programs to be run from that area. The idea is, you would create two partitions for your chroot tree, one with the noexec option and one without it. The noexec partition becomes the main chroot tree; the execs-allowed one gets mounted inside the other one, and is the only place that CGI programs are allowed. Then, after you have yourself all set up, you make the execs-allowed partition read-only. 