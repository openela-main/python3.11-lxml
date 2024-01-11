%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

Name:           python%{python3_pkgversion}-lxml
Version:        4.9.2
Release:        3%{?dist}
Summary:        XML processing library combining libxml2/libxslt with the ElementTree API

# The lxml project is licensed under BSD-3-Clause
# Some code is derived from ElementTree and cElementTree
# thus using the MIT-CMU elementtree license
# .xsl schematron files are under the MIT license
License:        BSD and MIT
URL:            https://github.com/lxml/lxml
# We use the get-lxml-source.sh script to generate the tarball
# without the isoschematron submodule as it contains a problematic
# license.
# See: https://gitlab.com/fedora/legal/fedora-license-data/-/issues/154
Source0:         lxml-%{version}-no-isoschematron.tar.gz
Source1:         get-lxml-source.sh

BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-Cython

%global _description \
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It\
provides safe and convenient access to these libraries using the ElementTree It\
extends the ElementTree API significantly to offer support for XPath, RelaxNG,\
XML Schema, XSLT, C14N and much more.

%description %{_description}

%prep
%autosetup -n lxml-%{version} -p1

# Remove isoschematron module due to problematic license
sed -i "s/, 'lxml.isoschematron'//" setup.py
# Remove the doctests for it (the documentation is not shipped)
# The command [d]eletes all lines from the first pattern to the second
sed -Ei '/^Schematron$/,/^\(Pre-ISO-Schematron\)$/d' doc/validation.txt

# Remove pregenerated Cython C sources
# We need to do this after %%pyproject_buildrequires because setup.py errors
# without Cython and without the .c files.
find -type f -name '*.c' -print -delete >&2

%build
env WITH_CYTHON=true %py3_build

%install
%py3_install

%check
# The tests assume inplace build, so we copy the built library to source-dir.
# If not done that, Python can either import the tests or the extension modules, but not both.
cp -a build/lib.%{python3_platform}-*/* src/
# The options are: verbose, unit, functional
%{python3} test.py -vuf

%files -n python%{python3_pkgversion}-lxml
%license doc/licenses/BSD.txt doc/licenses/elementtree.txt
%doc README.rst
%{python3_sitearch}/lxml/
%{python3_sitearch}/lxml-*.egg-info/

%changelog
* Thu Feb 16 2023 Charalampos Stratakis <cstratak@redhat.com> - 4.9.2-3
- Remove the isoschematron submodule

* Fri Feb 10 2023 Charalampos Stratakis <cstratak@redhat.com> - 4.9.2-2
- Bump release

* Mon Nov 14 2022 Charalampos Stratakis <cstratak@redhat.com> - 4.9.2-1
- Initial package
- Fedora contributions by:
      Alexander Todorov <atodorov@redhat.com>
      Bill Nottingham <notting@fedoraproject.org>
      Charalampos Stratakis <cstratak@redhat.com>
      Dan Horák <dan@danny.cz>
      David Malcolm <dmalcolm@redhat.com>
      Dennis Gilmore <dennis@ausil.us>
      Fabio Alessandro Locati <fale@redhat.com>
      Igor Raits <ignatenkobrain@fedoraproject.org>
      Jason ティビツ <tibbs@fedoraproject.org>
      Jeffrey C. Ollie <jcollie@fedoraproject.org>
      Jesse Keating <jkeating@fedoraproject.org>
      Kevin Fenzi <kevin@scrye.com>
      Lumir Balhar <lbalhar@redhat.com>
      Mikolaj Izdebski <mizdebsk@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      Peter Robinson <pbrobinson@gmail.com>
      Robert Kuska <rkuska@redhat.com>
      Shahms King <shahms@fedoraproject.org>
      Slavek Kabrda <bkabrda@redhat.com>
      tomspur <tomspur@fedoraproject.org>
      Ville Skyttä <scop@fedoraproject.org>
