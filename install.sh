#!/bin/sh -e

pip install -r requirements.txt

python -m nltk.downloader wordnet
