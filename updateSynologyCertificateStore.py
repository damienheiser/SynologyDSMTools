#!/bin/python
# Run with this bash script, change your CERT_DNS
#CERT_DOMAIN=domain.com
#CERT_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
#CERT_FOLDER="/usr/syno/etc/certificate/_archive/$CERT_ID"
#CERT_DNS="dns_namecom"
#mkdir $CERT_FOLDER
#
#/usr/local/share/acme.sh/acme.sh  --force --issue -d "$CERT_DOMAIN" --dns "$CERT_DNS" \
#    --cert-file "$CERT_FOLDER/cert.pem" \
#    --key-file "$CERT_FOLDER/privkey.pem" \
#    --fullchain-file "$CERT_FOLDER/fullchain.pem" \
#    --capath "$CERT_FOLDER/chain.pem" \
#    --reloadcmd "/bin/python /root/updateSynologyCertificateStore.py -d $CERT_ID -u $CERT_DOMAIN" \
#    --dnssleep 120
#
import json
import sys
import getopt
import subprocess

_synologyCertficateStoreLocation = '/usr/syno/etc/certificate/_archive/'

try:
    opts, remain = getopt.getopt(sys.argv[1:],"hd:u:",["help","directory=","url="])
except getopt.GetoptError:
    print 'updateSynologyCertificateStore.py -d <certParentDirectory> -u <certURL>'
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print 'updateSynologyCertificateStore.py -d <certParentDirectory> -u <certURL>\n'
        print 'example: updateSynologyCertficiateStore.py -d jD8wiw -u mydomain.dom'
        print 'Where jD8wiw is the certificate diretory located in /usr/syno/etc/certificate/_archive/'
        sys.exit(2)
    elif opt in ("-d", "--directory"):
        inputDirectory = arg
    elif opt in ("-u", "--url"):
        inputURL = arg

newCertJSON = {
        inputDirectory : {
            "desc" : inputURL,
            "services" : []
        }
}

try:
    with open(_synologyCertficateStoreLocation + 'INFO') as json_file:
        data = json.load(json_file)

except:
    print 'Unable to open Synology Certificate Store at ' + _synologyCertficateStoreLocation
    sys.exit(3)

# Create a backup of this file before directory added
with open(_synologyCertficateStoreLocation + 'INFO_backup_' + inputDirectory, 'w') as outfile:
    json.dump(data, outfile)

data.update (newCertJSON)

# Overwrite
with open(_synologyCertficateStoreLocation + 'INFO', 'w') as outfile:
    json.dump(data, outfile)

# change to subprocess.run in python 3?
# Restart nginx.  New certificate shows up in DSM
subprocess.call(["/usr/syno/sbin/synoservicectl", "--reload", "nginx"])
