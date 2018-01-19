# mthttpd
modern version of thttpd v2.27 (Oct 2015) tiny/turbo/throttling HTTP server by Jef Poskanzer

for modern compilers, there is also a bug and securit fixed v2.25b (Dec 2003) thttpd on github maintained by Anthony G. Basile blueness@gentoo.org https://github.com/blueness/sthttpd

# differences
mthttpd comes with at _php.cgi_ script and an example _thttpd_ configuration file that will quickly and simply allow ANY vesion of PHP to be run in its CGI form using CGI path overloading. It will also work with any _thttpd_ server version, including "premium thttpd" (not tested). Some PHP applications may break, usually due to assumptions made about environment variables and there contents being made available to PHP.

I have a file manager application originally developed with PHP v4, using (standard) PHP SAPI modules for Apache, it runs 100% fine using CGI path overloading (which can also be done with Apache too).

A benificial side affect of this is that multile scripts can run multiple PHP versions, as well any other command line interpreter that outputs to STDOUT.

To assist in Apache migration and general PHP development, _mthttpd_ now directly outputs the PHP specific **SCRIPT_FILENAME** environment variable, along with the Apache variables **DOCUMENT_ROOT** and **REDIRECT_STATUS**. It also sets the internal default web sever user group to **www-data**.

Those environment variables are constructed in the _php.cgi_ script, however they will allow _mthttpd_ to run executable **.php** scripts using the _binfmt_misc_ method directly.

# more on standards
As I understand it the main resason **SCRIPT_FILENAME** is not included in _thttpd_ was because it was not part of the offical CGI standards. However with **SCRIPT_NAME** how does one know where the web server root is if **DOCUMENT_ROOT** is not supplied. After testing with _php.cgi_ the following assertions can be made:

* **SCRIPT_FILENAME** is not the same as **SCRIPT_NAME**
* **PHP_SELF** does _NOT_ refer to **SCRIPT_NAME**
* **PATH_TRANSLATED** is _NOT_ present without CGI path overloading
* **PATH_TRANSLATED** is the only variable to pass the _FULL_ path through the webserver to the intended script
* **DOCUMENT_ROOT** is required otherwise the webserver root must be hardcoded somewhere else
* **DOCUMENT_ROOT** + **SCRIPT_NAME** = **SCRIPT_FILENAME**

The above assertions are (mostly) not true in PHP SAPI modules. In a more traditional sense binary programs were never _ment_ to set environment variables. The Unix philosophy would dictate a specific shell environment would set the variables, and a binary would just update them when that environment was passed along. This was fine for production environments, owever, especially in "modern" times, the same can not be said for development environments.

# other thttpd goodies
It is possible to for a single instance to spawn seperate instances for a given _hostname_, however this requires a CGI with access to the system, and webserver users being OS users. OS users would also allow for other services to be easily secured (like ftp, git, etc).

This allows a _login.cgi_ to spawn a new _thttpd_ as a different user, however it does require a different port (not 80) on multi-homed IP hostnames. Xinix OS is an example of this (2017). This allows _thttp_ to support "sandboxed" script execution, which is great for developers.

# security
_thttp_ relies almost exclusively on filesystem rights. However by default it list files and folders beginning with"." (dot), which on most filesystems, are normally hidden (without the need for special attributes. This will be the next addition I make, a config option to see dot files, see to not view them by default. That will hugely improve _default_ _security_ in a production environment, where it is sadly a requirement nowadays.

CGI path overloading is not a new thing, not is it insecure in most instances, except posibbly where the target CGI is the actual scripting engine binary. Even then it is not _insecure_. There are still web applications and web games being developed that still use CGI path overloading as a default (and secure) script security solution.

With _mthttpd_ not showing dot files, in **chroot** mode, you will be able to securely hide binaries while still being able to provide secure public **/cgi-bin/** paths. This also allows _thttpd_ folder password system to become more secure.

A quote for the PHP Manual:

> If your web server does not allow you to do redirects, or the server does not have a way to communicate to the PHP binary that the request is a safely redirected request, you can specify the option --enable-force-cgi-redirect to the configure script. You still have to make sure your PHP scripts do not rely on one or another way of calling the script, neither by directly http://my.host/cgi-bin/php/dir/script.php nor by redirection http://my.host/dir/script.php.

Cheers

paulwratt@github
