#!/bin/bash
# Acme.sh and your credentials are expected entered by now
# Set CERT_DNS to your preferred DNS 
echo Synology Acme.sh Lets Encrypt! Certificate Generator!\n
echo Please enter domain name. 
read CERT_DOMAIN

# Generate a random 6 character directory
#export CERT_FOLDER_NAME "$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)"
CERT_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
CERT_FOLDER="/usr/syno/etc/certificate/_archive/$CERT_ID"
CERT_DNS="dns_namecom"
mkdir $CERT_FOLDER

/usr/local/share/acme.sh/acme.sh  --force --issue -d "$CERT_DOMAIN" --dns "$CERT_DNS" \
    --cert-file "$CERT_FOLDER/cert.pem" \
    --key-file "$CERT_FOLDER/privkey.pem" \
    --fullchain-file "$CERT_FOLDER/fullchain.pem" \
    --capath "$CERT_FOLDER/chain.pem" \
    --reloadcmd "/bin/python /root/updateSynologyCertificateStore.py -d $CERT_ID -u $CERT_DOMAIN" \
    --dnssleep 120
