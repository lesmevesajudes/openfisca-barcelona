#!/bin/sh

if [ -f setup.py ]; then
	pip install -e .
fi

grep "^PATHS_FROM_ECLIPSE_TO_PYTHON =" /usr/local/lib/python2.7/site-packages/pydevd_file_utils.py
if [ $? -ne 0 ]; then
	PARENT_PATH=${HOST_PATH%/*}
	sed -i "s@setup_client_server_paths(PATHS_FROM_ECLIPSE_TO_PYTHON)@PATHS_FROM_ECLIPSE_TO_PYTHON = [\(r'$PARENT_PATH',r'/usr/src/app'\)]\nsetup_client_server_paths(PATHS_FROM_ECLIPSE_TO_PYTHON)@" /usr/local/lib/python2.7/site-packages/pydevd_file_utils.py
fi

exec openfisca serve --country-package $COUNTRY_PACKAGE --bind 0.0.0.0:2000
