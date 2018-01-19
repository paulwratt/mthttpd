#!/bin/sh
export DOCUMENT_ROOT=/home/sysop/devel/www
export SCRIPT_FILENAME=${DOCUMENT_ROOT}${SCRIPT_NAME}
exec /usr/bin/php-cgi

