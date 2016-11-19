# Execute with either sh or bash

PYTHONPATH=${PYTHONPATH}:${PWD}/src python src/update_site.py
exit $?

