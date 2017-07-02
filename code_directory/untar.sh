#!/bin/sh

for directory in */ ; do
    for file in */$directory/*.tar.gz ; do
        tar -zxf $file;
    done
done