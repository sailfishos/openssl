%define soversion 1.1

Summary: Compatibility version of the OpenSSL library
Name: openssl1.1
Version: 1.1.1w
Release: 1

Source: %{name}-%{version}.tar.gz
Source1: hobble-openssl
Source12: ec_curve.c
Source13: ectest.c
# Build changes
Patch1: openssl-1.1.1-build.patch
Patch2: openssl-1.1.1-defaults.patch
Patch3: openssl-1.1.1-no-html.patch
Patch4: openssl-1.1.1-man-rename.patch
# Functionality changes
Patch31: openssl-1.1.1-conf-paths.patch
Patch32: openssl-1.1.1-version-add-engines.patch
Patch33: openssl-1.1.1-apps-dgst.patch
Patch36: openssl-1.1.1-no-brainpool.patch
Patch37: openssl-1.1.1-ec-curves.patch
Patch38: openssl-1.1.1-no-weak-verify.patch
Patch40: openssl-1.1.1-disable-ssl3.patch
Patch41: openssl-1.1.1-system-cipherlist.patch
Patch42: openssl-1.1.1-fips.patch
Patch44: openssl-1.1.1-version-override.patch
Patch45: openssl-1.1.1-weak-ciphers.patch
Patch46: openssl-1.1.1-seclevel.patch
Patch47: 0001-ts-Use-SHA256-instead-of-SHA1-and-SHA512-instead-MD5.patch
Patch48: openssl-1.1.1-fips-post-rand.patch
Patch49: openssl-1.1.1-evp-kdf.patch
Patch50: openssl-1.1.1-ssh-kdf.patch
Patch51: openssl-1.1.1-intel-cet.patch
Patch60: openssl-1.1.1-krb5-kdf.patch
Patch61: openssl-1.1.1-edk2-build.patch
Patch62: openssl-1.1.1-fips-curves.patch
Patch65: openssl-1.1.1-fips-drbg-selftest.patch
Patch66: openssl-1.1.1-fips-dh.patch
Patch67: openssl-1.1.1-kdf-selftest.patch
Patch69: openssl-1.1.1-alpn-cb.patch
Patch70: openssl-1.1.1-rewire-fips-drbg.patch
# Backported fixes including security fixes
Patch52: openssl-1.1.1-s390x-update.patch
Patch53: openssl-1.1.1-fips-crng-test.patch
Patch55: openssl-1.1.1-aes-asm-aesv8-armx.pl-20-improvement-on-ThunderX2.patch
Patch56: openssl-1.1.1-s390x-ecc.patch
Patch57: openssl-1_1-Optimize-RSA-armv8.patch
Patch58: openssl-1_1-Optimize-AES-GCM-uarchs.patch
Patch59: openssl-1_1-Optimize-AES-XTS-aarch64.patch

License: OpenSSL
URL: http://www.openssl.org/
BuildRequires: make
BuildRequires: gcc 
BuildRequires: coreutils, perl, sed, zlib-devel
BuildRequires: lksctp-tools-devel
# /usr/bin/cmp
BuildRequires: diffutils
# /usr/bin/rename
BuildRequires: util-linux

Conflicts: openssl-libs < 3

%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
from the 1.1.1 version and is provided for compatibility with previous
releases.

%package devel
Summary: Files for development of applications which will use OpenSSL
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: pkgconfig
# The devel subpackage intentionally conflicts with main openssl-devel
# as simultaneous use of both openssl package cannot be encouraged.
# Making the packages non-conflicting would also require further
# changes in the dependent packages.
Conflicts: openssl-devel

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.


%prep
%setup -q -n %{name}-%{version}/openssl

sh %{SOURCE1} > /dev/null

cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/

%patch1 -p1 -b .build   %{?_rawbuild}
%patch2 -p1 -b .defaults
%patch3 -p1 -b .no-html  %{?_rawbuild}
%patch4 -p1 -b .man-rename

%patch31 -p1 -b .conf-paths
%patch32 -p1 -b .version-add-engines
%patch33 -p1 -b .dgst
%patch36 -p1 -b .no-brainpool
%patch37 -p1 -b .curves
%patch38 -p1 -b .no-weak-verify
%patch40 -p1 -b .disable-ssl3
%patch41 -p1 -b .system-cipherlist
%patch42 -p1 -b .fips
%patch44 -p1 -b .version-override
%patch45 -p1 -b .weak-ciphers
%patch46 -p1 -b .seclevel
%patch47 -p1 -b .ts-sha256-default
%patch48 -p1 -b .fips-post-rand
%patch49 -p1 -b .evp-kdf
%patch50 -p1 -b .ssh-kdf
%patch51 -p1 -b .intel-cet
%patch52 -p1 -b .s390x-update
%patch53 -p1 -b .crng-test
%patch55 -p1 -b .arm-update
%patch56 -p1 -b .s390x-ecc
%patch57 -p1 -b .opt-rsa
%patch58 -p1 -b .opt-aes-gcm
%patch59 -p1 -b .opt-aem-xts
%patch60 -p1 -b .krb5-kdf
%patch61 -p1 -b .edk2-build
%patch62 -p1 -b .fips-curves
%patch65 -p1 -b .drbg-selftest
%patch66 -p1 -b .fips-dh
%patch67 -p1 -b .kdf-selftest
%patch69 -p1 -b .alpn-cb
%patch70 -p1 -b .rewire-fips-drbg

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

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
export CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"
export CPPFLAGS="$CPPFLAGS -D_FILE_OFFSET_BITS=64"
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	zlib enable-camellia enable-seed enable-rfc3779 \
	enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
	enable-weak-ssl-ciphers \
	no-mdc2 no-ec2m no-sm2 no-sm4 \
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'

%make_build

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done


%define __provides_exclude_from %{_libdir}/engines-%{soversion}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl}
# We don't need to install docs now because we don't package it.
%{__make} DESTDIR=%{?buildroot} INSTALL="%{__install} -p" install_dev install_engines
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
	chmod 755 ${lib}
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

# Delete static library
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a || :

# Next step of gradual disablement of SSL3.
# Make SSL3 disappear to newly built dependencies.
sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\
#ifndef OPENSSL_NO_SSL3\
# define OPENSSL_NO_SSL3\
#endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libcrypto.so.%{version}
%{_libdir}/libssl.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{soversion}
%{_libdir}/engines-%{soversion}

%files devel
%{_prefix}/include/openssl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
