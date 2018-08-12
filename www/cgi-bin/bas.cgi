#!/bin/sh
# "special" cgi->bas redirect for thttpd & bas ANSI BASIC Interpreter
# eg. http:/localhost/cgi-bin/php.cgi/test/index.bas
#  ==       bas /home/sysop/devel/www/test/index.bas

export DOCUMENT_ROOT=/home/sysop/devel/www
if [ "$PATH_TRANSLATED" = "" ]; then
  export PATH_TRANSLATED=${DOCUMENT_ROOT}/index.bas
fi
export SCRIPT_FILENAME=${PATH_TRANSLATED}

EXT=${PATH_TRANSLATED#"${PATH_TRANSLATED%????}"}
if [ ! "$EXT" = ".bas" ]; then
  printf "Content-Type: "
  file -b -i ${PATH_TRANSLATED}
  echo
  cat ${PATH_TRANSLATED}
else
  date=`date -u '+%a, %d %b %Y %H:%M:%S %Z'`
  cat << EOF
Content-type: text/html
Expires: $date

EOF
  exec /usr/bin/bas ${PATH_TRANSLATED}
fi
