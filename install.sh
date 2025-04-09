#!/bin/sh -e

pip install -r requirements.txt

python -c 'import stanza; stanza.download("cu")'

