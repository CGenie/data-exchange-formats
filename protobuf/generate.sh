#!/bin/bash

SRC_DIR=.
DST_DIR=compiled

rm -Rf $DST_DIR
mkdir $DST_DIR
touch $DST_DIR/__init__.py

protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/chatroom.proto
