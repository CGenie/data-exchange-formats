#!/bin/bash

C_OUTPUT_DIR=c-codec

python -m asn1ate.pyasn1gen weapons.asn | tee weapons.py

rm -Rf $C_OUTPUT_DIR
mkdir $C_OUTPUT_DIR
#$HOME/git-work/github/ASN.1/asn1scc/Asn1f2/bin/Debug/Asn1f2.exe -c weapons.asn -o $C_OUTPUT_DIR
$HOME/git-work/github/ASN.1/asn1c/asn1c/asn1c -fnative-types weapons.asn
mv *.c $C_OUTPUT_DIR
mv *.h $C_OUTPUT_DIR
mv Makefile.am.sample $C_OUTPUT_DIR
rm $C_OUTPUT_DIR/converter-sample.c
mv $C_OUTPUT_DIR/test-client.c ./
