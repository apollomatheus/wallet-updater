#!/bin/sh
version=$1
link=$2
daemon=$3

mkdir update$version
echo "Updating to version $version"
wget $link -q -P update$version
cd update$version
tar -xf *.tar.gz
cp ./*/* /usr/local/ -a 
# ./autogen.sh
# ./configure --with-gui=no --disable-tests --disable-gui-tests
# make
# make install
# echo "Starting client back"
/usr/local/bin/$daemon
