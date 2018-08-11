Summary: Modified Throttleable lightweight httpd server with PHP SAPI
Name: mthttpd
Version: 2.27b0
Release: 1
Group: Networking
URL: http://paulwratt.gothub.io/mthttpd/
Source0: http://paulwratt.gothub.io/mthttpd/mthttpd-%{PACKAGE_VERSION}.tar.gz
Copyright: distributable (BSD)
BuildRoot: /tmp/mthttpd-root

%description
mthttpd is a modified thttpd v2.27 (+= v2.29) with PHP SAPI extensions.
thttpd is a very compact no-frills httpd serving daemon that can handle
very high loads.  While lacking many of the advanced features of
Apachee, thttpd operates without forking and is extremely efficient in
memory use.  Basic support for cgi scripts, authentication, and ssi is
provided for.  Advanced features include the ability to throttle traffic.

%prep
%setup

./configure --prefix=/usr

%build
make \
	WEBDIR=/home/httpd/html \
	BINDIR=/usr/sbin prefix=/usr \
	CGIBINDIR=/home/httpd/cgi-bin \
        WEBGROUP=www-data

%install

mkdir -p $RPM_BUILD_ROOT/home/httpd/{cgi-bin,logs}
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/usr/man/man{1,8}
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install  contrib/redhat-rpm/mthttpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/mthttpd
install  contrib/redhat-rpm/mthttpd.conf $RPM_BUILD_ROOT/etc/
make -i prefix=$RPM_BUILD_ROOT/usr install

%pre

grep '^httpd:' /etc/passwd >/dev/null || \
	/usr/sbin/adduser -r httpd

%post
/sbin/chkconfig --add mthttpd

%preun
/sbin/chkconfig --del mthttpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,bin,bin)
%doc [A-Z]*
%attr(2755, httpd, httpd) /usr/sbin/makeweb
/usr/sbin/htpasswd
/usr/sbin/syslogtocern
/usr/sbin/mthttpd
%attr(-, httpd, httpd) /home/httpd
%attr(0755, root, root) /etc/rc.d/init.d/mthttpd
%config /etc/mthttpd.conf
%doc /usr/man/man*/*

%changelog

* Mon May 26 2018 Paul Wratt <paul.wratt@gmail.com>
  - Updated to v2.27b0

* Mon Dec 29 2003 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.26

* Sat Dec 20 2003 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.25b

* Mon Oct 27 2003 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.25

* Sat Sep 13 2003 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.24

* Sat May 25 2002 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.23

* Mon Jul 09 2001 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.22

* Thu Apr 26 2001 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.21c

* Mon Apr 23 2001 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.21b

* Mon Oct 02 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.21

* Wed Sep 13 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.20

* Mon Sep 11 2000 Bennett Todd <bet@rahul.net>
  - added thttpd.conf, took config info out of init script
  - switched to logging in /var/log, used pidfile

* Thu Jun 15 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.19

* Thu May 18 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.18

* Fri Mar 17 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.17

* Mon Feb 28 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.16

* Thu Feb 03 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.15

* Thu Jan 21 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.14

* Thu Jan  6 2000 Jef Poskanzer <jef@mail.acme.com>
  - Updated to 2.13

* Mon Jan  3 2000 Bennett Todd <bet@rahul.net>
  - updated to 2.12, tweaked to move thttpd.init into tarball

* Mon Dec 13 1999 Bennett Todd <bet@mordor.net>
  - Updated to 2.09

* Fri Dec 10 1999 Bennett Todd <bet@mordor.net>
  - Updated to 2.08

* Wed Nov 24 1999 Bennett Todd <bet@mordor.net>
  - updated to 2.06, parameterized Version string in source url
  - changed to use "make install", simplified %files list

* Wed Nov 10 1999 Bennett Todd <bet@mordor.net>
  - Version 2.05, reset release to 1
  - dropped bugfix patch since Jef included that
  - streamlined install

* Sun Jul 25 1999 Bennett Todd <bet@mordor.net>
  - Release 4, added mime type swf

* Mon May  3 1999 Bennett Todd <bet@mordor.net>
  - Release 2, added patch to set cgi-timelimit up to 10 minutes
    fm default 30 seconds

* Wed Feb 10 1999 Bennett Todd <bet@mordor.net>
  - based on 2.00-2, bumped to 2.04, reset release back to 1
  - fixed a couple of broken entries in %install to reference $RPM_BUILD_ROOT
  - simplified %files to populate /usr/doc/... with just [A-Z]* (TODO had gone
    away, this simplification makes it liklier to be trivially portable to
    future releases).
  - added %doc tags for the man pages

