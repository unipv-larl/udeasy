#!/bin/bash

if [ $# -eq 0 ]
then
  echo "Error: at least one argument expected
  Usage: bash build_deb.sh VERSION [REVISION]"
  exit 1
elif [ $# -eq 1 ]
then
  revision="1"
else
  revision=$2
fi

version=$1

year=$(date +"%Y")

cd ./python_scripts

# build with pyinstaller
pyinstaller --distpath ../ubuntu64/dist --workpath ../ubuntu64/build -n udeasy -w -F home.py

# cd to the dist directory
echo "creating the directory for udeasy v$version..."
cd ../ubuntu64/dist

# create version directory
version_dir="udeasy_$version-"$revision"_amd64"
mkdir $version_dir

# create DEBIAN dir and usr
mkdir $version_dir/DEBIAN
mkdir $version_dir/usr

# create control and copyright in DEBIAN
echo "Package: udeasy
Version: $version
Architecture: amd64
Maintainer: Luca Brigada Villa <luca.brigadavilla@unibg.it>
Homepage: https://unipv-larl.github.io/udeasy/
Description: A tool for querying CoNNL-U files
 udeasy is an application written in Python 3 whose main goal is to allow the user to easily query a treebank and extract patterns from a treebank in CoNLL-U format." > $version_dir/DEBIAN/control

echo "Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: udeasy
Source: https://unipv-larl.github.io/udeasy/download.html

Files: *
Copyright: $year Luca Brigada Villa <luca.brigadavilla@unibg.it>
License: CC-BY-NC-SA 4.0
 The full text of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License
 can be found in the file \`/usr/share/doc/udeasy_$version/license\'." > $version_dir/DEBIAN/copyright

# create bin and share in usr
mkdir $version_dir/usr/bin
mkdir $version_dir/usr/share

# copy executable in bin
cp udeasy $version_dir/usr/bin/udeasy

# create applications and doc in share
mkdir $version_dir/usr/share/applications
mkdir $version_dir/usr/share/doc

# create desktop file and copy icon in applications
cp image.png $version_dir/usr/share/applications/udeasy.png
echo "[Desktop Entry]
Encoding=UTF-8
Version=$version
Type=Application
Terminal=false
Exec=/usr/bin/udeasy
Name=udeasy
Icon=/usr/share/applications/udeasy.png" > $version_dir/usr/share/applications/udeasy.desktop

# write copyright in doc
echo "Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: udeasy
Source: https://unipv-larl.github.io/udeasy/download.html

Files: *
Copyright: $year Luca Brigada Villa <luca.brigadavilla@unibg.it>
License: CC-BY-NC-SA 4.0
 The full text of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License
 can be found in the file \`/usr/share/doc/udeasy_$version/license\'." > $version_dir/usr/share/doc/copyright

# write license in doc
wget -O $version_dir/usr/share/doc/license https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.txt

echo "building deb package..."
# build deb file
dpkg-deb --build --root-owner-group udeasy_$version-"$revision"_amd64

echo "Done."
