#!/bin/bash

function generate {
    FILE=$1
    DST_DIR=$2
    SRC_DIR=$(dirname $FILE)

    rm -Rf $DST_DIR
    mkdir $DST_DIR
    touch $DST_DIR/__init__.py

    protoc -I=$SRC_DIR --python_out=$DST_DIR $FILE
}

generate ./chatroom.proto compiled
generate ./chatroom-2.proto compiled_v2
