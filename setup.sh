#!/bin/sh

echo "Creating local directory for site-packages..."
mkdir $HOME/local
mkdir $HOME/local/lib
mkdir $HOME/local/lib/python2.6
mkdir $HOME/local/lib/python2.6/site-packages

echo "Exporting local site-packages environment variable..."
export PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python2.6/site-packages

echo "Installing prerequisites..."
echo "python-bitstring"
easy_install --prefix="$HOME/local" bitstring
