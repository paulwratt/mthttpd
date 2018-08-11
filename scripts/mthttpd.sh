#!/bin/sh
#
# mthttpd.sh - startup script for mthttpd on FreeBSD
#
# This goes in /usr/local/etc/rc.d and gets run at boot-time.
#
# Variables available:
#   mthttpd_enable='YES/NO'
#   mthttpd_program='path'
#   mthttpd_pidfile='path'
#   mthttpd_devfs='path'
#
# PROVIDE: mthttpd
# REQUIRE: LOGIN FILESYSTEMS
# KEYWORD: shutdown

. /etc/rc.subr

name='mthttpd'
rcvar='mthttpd_enable'

load_rc_config "$name"

# Defaults.
mthttpd_enable="${mthttpd_enable:-'NO'}"
mthttpd_program="${mthttpd_program:-'/usr/local/sbin/mthttpd'}"
mthttpd_pidfile="${mthttpd_pidfile:-'/var/run/mthttpd.pid'}"

mthttpd_precmd ()
    {
    if [ '' != "$mthttpd_devfs" ] ; then
	mount -t devfs devfs "$mthttpd_devfs"
	devfs -m "$mthttpd_devfs" rule -s 1 applyset
	devfs -m "$mthttpd_devfs" rule -s 2 applyset
    fi
    }

mthttpd_stop ()
    {
    kill -USR1 `cat "$pidfile"`
    }

command="$mthttpd_program"
pidfile="$mthttpd_pidfile"
start_precmd='mthttpd_precmd'
stop_cmd='mthttpd_stop'

run_rc_command "$1"
