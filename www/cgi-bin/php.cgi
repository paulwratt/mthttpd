#!/bin/sh
# "special" cgi->php redirect for thttpd & php5-cgi
# eg. http:/localhost/cgi-bin/php.cgi/test/index.php
#  ==  php5-cgi /home/sysop/devel/www/test/index.php

#export PHP_FCGI_CHILDREN=1
#export PHP_FCGI_MAX_REQUESTS=200

if [ "$PHP_AUTH_USER" = "" ]; then
  export PHP_AUTH_USER="minda"  ## FIXME:
fi
if [ "$PHP_AUTH_PW" = "" ]; then
  export PHP_AUTH_PW="admin"    ## FIXME:
fi

export DOCUMENT_ROOT=/home/sysop/devel/www
if [ "$PATH_TRANSLATED" = "" ]; then
  export PATH_TRANSLATED=${DOCUMENT_ROOT}/index.php
fi
export SCRIPT_FILENAME=${PATH_TRANSLATED}

EXT=${PATH_TRANSLATED#"${PATH_TRANSLATED%????}"}
if [ ! "$EXT" = ".php" ]; then
  printf "Content-Type: "
  file -b -i ${PATH_TRANSLATED}
  echo
  cat ${PATH_TRANSLATED}
else
  exec /usr/bin/php-cgi
fi
