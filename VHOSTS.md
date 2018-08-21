# Setting up Virtual Hosting

 Now, what if you want to serve multiple domains? With HTTP/1.1 you can do "name based" virtual domains, which are very easy to set up. As of version 2.05 thttpd supports them.

### DNS.
    Name-based virtual hosts are set up via the domain name system. You make a CNAME record (which is basically an alias) for each virtual host pointing at the real host. A full explanation of DNS and BIND is way beyond the scope of this document, but if you just tell your local DNS person that you want to make some CNAMEs, they'll know what to do.
### Config file.
    All you have to do here is add the "vhost" option to your thttpd_config file.
### Data directory.
    The data dir for a vhost system is different. The top level directory should not contain any HTML stuff. Instead all it contains is subdirectories, one per virtual host. The directory's name is just the virtual hostname, or an IP number The HTML for each host goes in its subdirectory. The vhost directory for my own secondary web server looks like this:

```
        lrwxr-xr-x   1 root  www   13 Nov 15 11:32 192.100.66.6@ -> gate.acme.com
        lrwxr-xr-x   1 root  www   13 Nov 15 11:32 63.197.234.19@ -> gate.acme.com
        drwxrwxr-x   3 root  www  512 Nov 15 12:15 gate.acme.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.axilla.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:16 www.cloaca.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.foetid.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.lirpa.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.maxnix.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.phoon.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.setuid.com/
        drwxrwxr-x   2 root  www  512 Nov 15 12:04 www.tranya.com/
```

    The server's _real_ name is gate.acme.com, and I added symbolic links for its two IP numbers. In addition there are directories for all the virtual hosts I'm serving.

That ought to do it for name-based vhosting. 


# On IP aliasing:

If you want to do multi-homing but your OS's ifconfig program doesn't have the alias command, you may still be able to get it to work.

If you're running Solaris 2.3 or later, it's just a matter of a different user-interface on the ifconfig program. The Solaris equivalent of the example in the thttpd man page would be:

```
        ifconfig le0 www.acme.com
        ifconfig le0:0 www.acme.com
        ifconfig le0:1 www.joe.acme.com up
        ifconfig le0:2 www.jane.acme.com up
```

Not so hard. Still, it would be nice if Sun got with the program and supported the alias command. Maybe some day.

If you're running IRIX, you can use the PPP driver to add IP aliases. This is complicated but does not require kernel hacking. First you start up PPP commands for the aliased addresses. Sticking once again with the example in the man page:

```
        /usr/etc/ppp -r 192.100.66.200 &
        /usr/etc/ppp -r 192.100.66.201 &
```

These commands will complain that they can't find the address - that's ok, you just need them to start. In fact if you like, you can kill them after they complain. Next you point the aliased addresses at the real one, using `ifconfig`:

```
        ifconfig ppp0 192.100.66.200 192.100.66.10
        ifconfig ppp0 192.100.66.201 192.100.66.10
```

Next you have to tell ARP that all the IP addresses go to the same ethernet address. You will need the ethernet address for you system, which you can get from the `netstat -ia` command - it's the bunch of hex digits separated by colons.

```
        arp -s 192.100.66.10 08:00:20:09:0e:86 pub
        arp -s 192.100.66.200 08:00:20:09:0e:86 pub
        arp -s 192.100.66.201 08:00:20:09:0e:86 pub
```

Finally, you have to add routes from the new PPP interfaces to localhost:

```
        route add 192.100.66.200 localhost 1
        route add 192.100.66.201 localhost 1
```

If you're running SunOS 4.1.x, fetch this tar file: ftp://ftp.cerf.net/pub/vendor/peggy/vif.tar.gz It contains some netnews articles with instructions and source code for adding a "virtual interface" device to the kernel. Installing this stuff is not trivial. There's also supposedly a way to use a PPP driver under SunOS, as with IRIX above, but I haven't found details on this yet.

If you're running Linux, here's a pointer to some kernel patches to add ip aliasing: ftp://ftp.mindspring.com/users/rsanders/ipalias/ I'm not sure what version of Linux this is for. Recent/future versions of Linux may come with aliasing already installed, so check your ifconfig man page before you start hacking. 