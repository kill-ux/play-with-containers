#!/bin/bash

wget https://releases.hashicorp.com/vagrant/2.4.9/vagrant_2.4.9_linux_amd64.zip

unzip vagrant_2.4.9_linux_amd64.zip -d ~/.local/bin 

rm vagrant_2.4.9_linux_amd64.zip

echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.zshrc
export PATH=$HOME/.local/bin:$PATH

echo "source ~/.zshrc"