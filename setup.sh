#!/bin/bash
set -x

ver='v0.1.0'
cd server
rm -f ./fcct-*

# Download fcct binary and detached signature
curl -O -L "https://github.com/coreos/fcct/releases/download/${ver}/fcct-x86_64-unknown-linux-gnu"
curl -O -L "https://github.com/coreos/fcct/releases/download/${ver}/fcct-x86_64-unknown-linux-gnu.asc"

# Download Coreos Application Signing Key and import it
curl -O -L http://coreos.com/dist/pubkeys/app-signing-pubkey.gpg
gpg --import app-signing-pubkey.gpg

# Verify the downloaded binary
gpg --verify fcct-x86_64-unknown-linux-gnu.asc fcct-x86_64-unknown-linux-gnu

chmod +x fcct-x86_64-unknown-linux-gnu
cd ..

echo "Finish setup"