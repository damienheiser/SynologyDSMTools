# SynologyDSMTools
Various scripts and tools I use for administration of Synology DSM systems
## updateSynologyCertificateStore.py
Acme.sh is great and all for getting those certificates and installing them into the proper places for DSM to use.  But DSM doesn't recognize those new certificates. :(

Call this during the reload command of acme.sh to add the certificates to be available within DSM. Example is in issueNewCertificate.bash

Enjoy

## issueNewCertificate.bash
Simple reusable bash script that asks for the domain in a prompt, then calls Acme.sh and updateSynologyCertificateStore.py

- To use call ./issueNewCertificate.bash (after you chmod +x of course)
