#! /bin/bash -ex

# Download a release of lxml (if missing) and remove the isoschematron module from it

version=$1

if [ -z "${version}" ]; then
    echo "Usage: $0 VERSION" >& 2
    echo "" >& 2
    echo "example: $0 4.9.2" >& 2
    exit 1
fi

versionedname=lxml-${version}
orig_archive=${versionedname}.tar.gz
new_archive=${versionedname}-no-isoschematron.tar.gz

if [ ! -e ${orig_archive} ]; then
    wget -N https://files.pythonhosted.org/packages/source/l/lxml/${orig_archive}
fi

deleted_module=lxml-${version}/src/lxml/isoschematron/
deleted_test=lxml-${version}/src/lxml/tests/test_isoschematron.py

# tar --delete does not operate on compressed archives, so do
# gz decompression explicitly
gzip --decompress ${orig_archive}
tar -v --delete -f ${orig_archive//.gz} {$deleted_module,$deleted_test}
gzip -cf ${orig_archive//.gz} > ${new_archive}
