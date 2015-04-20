#!/bin/bash

C_OUTPUT_DIR=c-codec

python -m asn1ate.pyasn1gen chatroom.asn | tee chatroom.py

rm -Rf $C_OUTPUT_DIR
mkdir $C_OUTPUT_DIR
$HOME/asn1c-bin/bin/asn1c -fnative-types chatroom.asn
mv *.c $C_OUTPUT_DIR
mv *.h $C_OUTPUT_DIR
mv Makefile.am.sample $C_OUTPUT_DIR
rm $C_OUTPUT_DIR/converter-sample.c
mv $C_OUTPUT_DIR/test-client.c ./
