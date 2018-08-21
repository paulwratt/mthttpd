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