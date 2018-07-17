# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
%define soversion 10

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}
Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.0.2m
# Do not forget to bump SHLIB_VERSION on version upgrades
Release: 2%{?dist}
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: %{name}-%{version}.tar.gz
Source1: hobble-openssl
Source2: Makefile.certificate
Source5: README.legacy-settings
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source8: openssl-thread-test.c
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source11: README.FIPS
Source12: ec_curve.c
Source13: ectest.c
# Build changes
Patch1: openssl-1.0.2e-rpmbuild.patch
Patch2: openssl-1.0.2a-defaults.patch
Patch4: openssl-1.0.2i-enginesdir.patch
Patch5: openssl-1.0.2a-no-rpath.patch
Patch6: openssl-1.0.2a-test-use-localhost.patch
Patch7: openssl-1.0.0-timezone.patch
Patch8: openssl-1.0.1c-perlfind.patch
Patch9: openssl-1.0.1c-aliasing.patch
# Bug fixes
Patch23: openssl-1.0.2c-default-paths.patch
Patch24: openssl-1.0.2a-issuer-hash.patch
# Functionality changes
Patch33: openssl-1.0.0-beta4-ca-dir.patch
Patch34: openssl-1.0.2a-x509.patch
Patch35: openssl-1.0.2a-version-add-engines.patch
Patch39: openssl-1.0.2a-ipv6-apps.patch
Patch40: openssl-1.0.2m-fips.patch
Patch43: openssl-1.0.2m-krb5keytab.patch
Patch45: openssl-1.0.2a-env-zlib.patch
Patch47: openssl-1.0.2a-readme-warning.patch
Patch49: openssl-1.0.1i-algo-doc.patch
Patch50: openssl-1.0.2a-dtls1-abi.patch
Patch51: openssl-1.0.2a-version.patch
Patch56: openssl-1.0.2a-rsa-x931.patch
Patch58: openssl-1.0.2a-fips-md5-allow.patch
Patch60: openssl-1.0.2a-apps-dgst.patch
Patch63: openssl-1.0.2a-xmpp-starttls.patch
Patch65: openssl-1.0.2i-chil-fixes.patch
Patch66: openssl-1.0.2h-pkgconfig.patch
Patch68: openssl-1.0.2m-secure-getenv.patch
Patch70: openssl-1.0.2a-fips-ec.patch
Patch71: openssl-1.0.2m-manfix.patch
Patch72: openssl-1.0.2a-fips-ctor.patch
Patch73: openssl-1.0.2c-ecc-suiteb.patch
Patch74: openssl-1.0.2j-deprecate-algos.patch
Patch75: openssl-1.0.2a-compat-symbols.patch
Patch76: openssl-1.0.2j-new-fips-reqs.patch
Patch77: openssl-1.0.2j-downgrade-strength.patch
Patch78: openssl-1.0.2k-cc-reqs.patch
Patch90: openssl-1.0.2i-enc-fail.patch
Patch92: openssl-1.0.2a-system-cipherlist.patch
Patch93: openssl-1.0.2g-disable-sslv2v3.patch
Patch94: openssl-1.0.2d-secp256k1.patch
Patch95: openssl-1.0.2e-remove-nistp224.patch
Patch96: openssl-1.0.2e-speed-doc.patch
Patch99: openssl-1.0.2k-fips-randlock.patch
# Backported fixes including security fixes
Patch80: openssl-1.0.2e-wrap-pad.patch
Patch81: openssl-1.0.2a-padlock64.patch
Patch82: openssl-1.0.2m-trusted-first-doc.patch
# Mer patches
Patch202: openssl-1.0.2d-remove-date-string.patch
Patch204: openssl-1.0.2d-armtick.patch

License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRequires: coreutils, perl, sed, zlib-devel
# /usr/bin/cmp
BuildRequires: diffutils
# /usr/bin/rename
BuildRequires: util-linux
Requires: coreutils, make
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Requires: ca-certificates >= 2008-5
# Needed obsoletes due to the base/lib subpackage split
Obsoletes: openssl < 1.0.1b

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name}%{?_isa} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n %{name}-%{version}/%{name}

# The hobble_openssl is called here as we're building from git and don't
# need a hobbled tarball to distribute.
bash %{SOURCE1}

cp %{SOURCE12} %{SOURCE13} crypto/ec/

%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .defaults
%patch4 -p1 -b .enginesdir %{?_rawbuild}
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .perlfind %{?_rawbuild}
%patch9 -p1 -b .aliasing

%patch23 -p1 -b .default-paths
%patch24 -p1 -b .issuer-hash

%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch39 -p1 -b .ipv6-apps
%patch40 -p1 -b .fips
%patch43 -p1 -b .krb5keytab
%patch45 -p1 -b .env-zlib
%patch47 -p1 -b .warning
%patch49 -p1 -b .algo-doc
%patch50 -p1 -b .dtls1-abi
%patch51 -p1 -b .version
%patch56 -p1 -b .x931
%patch58 -p1 -b .md5-allow
%patch60 -p1 -b .dgst
%patch63 -p1 -b .starttls
%patch65 -p1 -b .chil
%patch66 -p1 -b .pkgconfig
%patch68 -p1 -b .secure-getenv
%patch70 -p1 -b .fips-ec
%patch71 -p1 -b .manfix
%patch72 -p1 -b .fips-ctor
%patch73 -p1 -b .suiteb
%patch74 -p1 -b .deprecate-algos
%patch75 -p1 -b .compat
%patch76 -p1 -b .fips-reqs
%patch77 -p1 -b .strength
%patch78 -p1 -b .cc-reqs
%patch90 -p1 -b .enc-fail
%patch92 -p1 -b .system
%patch93 -p1 -b .v2v3
%patch94 -p1 -b .secp256k1
%patch95 -p1 -b .nistp224
%patch96 -p1 -b .speed-doc
%patch99 -p1 -b .randlock

%patch80 -p1 -b .wrap
%patch81 -p1 -b .padlock64
%patch82 -p1 -b .trusted-first

%patch202 -p1 -b .date
%patch204 -p1 -b .armtick

sed -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux-generic64
%endif

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=/usr --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
	enable-cms enable-md2 no-mdc2 no-rc5 no-ec2m no-gost no-srp \
       --enginesdir=%{_libdir}/openssl/engines \
       shared  ${sslarch} %{?!nofips:fips}

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
make depend
make all

# Generate hashes for the included certs.
make rehash

# Overwrite FIPS README and copy README.legacy-settings
cp -f %{SOURCE5} %{SOURCE11} .

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

%check
# Verify that what was compiled actually works.

# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
make -C test apps tests
%{__cc} -o openssl-thread-test \
	-I./include \
	$RPM_OPT_FLAGS \
	%{SOURCE8} \
	-L. \
	-lssl -lcrypto \
	-lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT/%{_lib}/libcrypto.so.%{version} >$RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT/%{_lib}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT%{_libdir}/openssl
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man/* $RPM_BUILD_ROOT%{_mandir}/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/man
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} $RPM_BUILD_ROOT/%{_lib}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done
for lib in $RPM_BUILD_ROOT/%{_lib}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f ../../%{_lib}/`basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT/%{_lib}/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs/renew-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{_includedir}/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Remove man pages
rm -rf $RPM_BUILD_ROOT%{_mandir}

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc
mv CA.sh CA
popd

mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir -m700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl.cnf

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
cat $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h >> \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h
%endif

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FAQ LICENSE CHANGES NEWS INSTALL README
%doc doc/c-indentation.el doc/openssl.txt
# these files got remove - xfade
# %doc doc/openssl_button.html doc/openssl_button.gif
%doc doc/ssleay.txt
%doc README.FIPS
%{_sysconfdir}/pki/tls/certs/make-dummy-cert
%{_sysconfdir}/pki/tls/certs/renew-dummy-cert
%{_sysconfdir}/pki/tls/certs/Makefile
%{_sysconfdir}/pki/tls/misc/CA
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts
%{_sysconfdir}/pki/tls/misc/c_*
%attr(0755,root,root) %{_bindir}/openssl

%files libs
%defattr(-,root,root)
%doc LICENSE
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) /%{_lib}/libcrypto.so.%{version}
%attr(0755,root,root) /%{_lib}/libcrypto.so.%{soversion}
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
%attr(0644,root,root) /%{_lib}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac
%attr(0755,root,root) %{_libdir}/openssl

%files devel
%defattr(-,root,root)
%doc doc/c-indentation.el doc/openssl.txt CHANGES
%{_prefix}/include/openssl
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/*.a

%files perl
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/c_rehash
%{_sysconfdir}/pki/tls/misc/*.pl
%{_sysconfdir}/pki/tls/misc/tsget

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

