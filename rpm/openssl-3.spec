#
# spec file for package openssl-3
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%bcond_with fips
# If enabled openssl-3 provides unversioned /bin/openssl
%bcond_with openssl_3_default

%define ssletcdir %{_sysconfdir}/ssl
%define sover 3
%define _rname openssl
%define man_suffix 3ssl
Name:           openssl-3
# Don't forget to update the version in the "openssl" meta-package!
Version:        3.2.0
Release:        0
Summary:        Secure Sockets and Transport Layer Security
License:        Apache-2.0
URL:            https://www.openssl.org/
Source:         %{name}-%{version}.tar.gz
# to get mtime of file:
Source1:        %{name}.changes
# https://www.openssl.org/about/
# http://pgp.mit.edu:11371/pks/lookup?op=get&search=0xA2D29B7BF295C759#/openssl.keyring
Source5:        showciphers.c
# PATCH-FIX-OPENSUSE: Do not install html docs as it takes ages
Patch1:         openssl-no-html-docs.patch
Patch2:         openssl-truststore.patch
Patch3:         openssl-pkgconfig.patch
Patch4:         openssl-DEFAULT_SUSE_cipher.patch
Patch5:         openssl-ppc64-config.patch
# Add crypto-policies support
Patch6:         openssl-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch
Patch7:         openssl-crypto-policies-support.patch
# PATCH-FIX-OPENSUSE: Revert of 0e55c3ab8d702ffc897c9beb51d19b14b789618
# Makefile: Call mknum.pl on 'make ordinals' only if needed
Patch8:         openssl-Revert-Makefile-Call-mknum.pl-on-make-ordinals-only-if.patch
# PATCH-FIX-FEDORA Add FIPS_mode compatibility macro and flag support
Patch9:         openssl-Add-FIPS_mode-compatibility-macro.patch
Patch10:        openssl-Add-Kernel-FIPS-mode-flag-support.patch
# PATCH-FIX-UPSTREAM Fix test/recipes/01-test_symbol_presence.t
Patch11:        openssl-Fix_test_symbol_presence.patch
# PATCH-FIX-UPSTREAM https://github.com/openssl/openssl/pull/22971
Patch12:        openssl-Enable-BTI-feature-for-md5-on-aarch64.patch
# PATCH-FIX-UPSTREAM: bsc#1218690 CVE-2023-6129 - POLY1305 MAC implementation corrupts vector registers on PowerPC
Patch13:        openssl-CVE-2023-6129.patch
# PATCH-FIX-FEDORA Load FIPS the provider and set FIPS properties implicitly
Patch14:        openssl-Force-FIPS.patch
# PATCH-FIX-FEDORA Embed the FIPS hmac
Patch15:        openssl-FIPS-embed-hmac.patch
# PATCH-FIX-UPSTREAM: bsc#1218810 CVE-2023-6237: Excessive time spent checking invalid RSA public keys
Patch16:        openssl-CVE-2023-6237.patch
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(zlib)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Module::Load::Conditional)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Pod::Html)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(bigint)
Requires:       libopenssl3 = %{version}-%{release}
Requires:       openssl
Provides:       ssl
# Needed for clean upgrade path, boo#1070003
Obsoletes:      openssl-1_0_0
# Needed for clean upgrade from former openssl-1_1_0, boo#1081335
Obsoletes:      openssl-1_1_0
%{?suse_build_hwcaps_libs}
%if 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150400
Requires:       crypto-policies
%endif

%description
OpenSSL is a software library to be used in applications that need to
secure communications over computer networks against eavesdropping or
need to ascertain the identity of the party at the other end.
OpenSSL contains an implementation of the SSL and TLS protocols.

%package -n libopenssl3
Summary:        Secure Sockets and Transport Layer Security
%if %{with fips}
BuildRequires:  fips-check
%endif
Recommends:     ca-certificates-mozilla
Conflicts:      %{name} < %{version}-%{release}
# Needed for clean upgrade from former openssl-1_1_0, boo#1081335
Obsoletes:      libopenssl1_1_0
%if 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150400
Requires:       crypto-policies
%endif
# Merge back the hmac files bsc#1185116
Provides:       libopenssl3-hmac = %{version}-%{release}
Obsoletes:      libopenssl3-hmac < %{version}-%{release}
# Needed for clean upgrade from former openssl-1_1_0, boo#1081335
Obsoletes:      libopenssl1_1_0-hmac
# Needed for clean upgrade from SLE-12 openssl-1_0_0, bsc#1158499
Obsoletes:      libopenssl-1_0_0-hmac

%description -n libopenssl3
OpenSSL is a software library to be used in applications that need to
secure communications over computer networks against eavesdropping or
need to ascertain the identity of the party at the other end.
OpenSSL contains an implementation of the SSL and TLS protocols.

%package -n libopenssl-3-devel
Summary:        Development files for OpenSSL
Requires:       libopenssl3 = %{version}
Requires:       pkgconfig(zlib)
Recommends:     %{name} = %{version}
Provides:       ssl-devel
Conflicts:      ssl-devel
# Needed for clean upgrade from former openssl-1_1_0, boo#1081335
Obsoletes:      libopenssl-1_1_0-devel
# Needed for clean upgrade from SLE-12 openssl-1_0_0, bsc#1158499
Obsoletes:      libopenssl-1_0_0-devel
Obsoletes:      openssl-devel < %{version}
Provides:       openssl-devel = %{version}
Provides:       pkgconfig(libcrypto) = %{version}
Provides:       pkgconfig(libopenssl) = %{version}
Provides:       pkgconfig(libssl) = %{version}
Provides:       pkgconfig(openssl) = %{version}

%description -n libopenssl-3-devel
This subpackage contains header files for developing applications
that want to make use of the OpenSSL C API.

%package doc
Summary:        Manpages and additional documentation for openssl
Conflicts:      libopenssl-3-devel < %{version}-%{release}
Conflicts:      openssl-doc
Provides:       openssl-doc = %{version}
Obsoletes:      openssl-doc < %{version}
BuildArch:      noarch

%description doc
This package contains optional documentation provided in addition to
this package's base documentation.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%ifarch armv5el armv5tel
export MACHINE=armv5el
%endif
%ifarch armv6l armv6hl
export MACHINE=armv6l
%endif

./Configure \
    no-mdc2 no-ec2m no-sm2 no-sm4 \
    enable-rfc3779 enable-camellia enable-seed \
%ifarch x86_64 aarch64 ppc64le
    enable-ec_nistp_64_gcc_128 \
%endif
%if %{with fips}
    enable-fips \
%endif
    enable-ktls \
    zlib \
    --prefix=%{_prefix} \
    --libdir=%{_lib} \
    --openssldir=%{ssletcdir} \
    %{optflags} \
    -Wa,--noexecstack \
    -Wl,-z,relro,-z,now \
    -fno-common \
    -DTERMIO \
    -DPURIFY \
    -D_GNU_SOURCE \
    -DOPENSSL_NO_BUF_FREELISTS \
    $(getconf LFS_CFLAGS) \
    -Wall \
    --with-rand-seed=getrandom \
    --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
    -DSUSE_OPENSSL_FIPS_VERSION=%{release}

# Show build configuration
perl configdata.pm --dump

# Do not run this in a production package the FIPS symbols must be patched-in
# util/mkdef.pl crypto update

%make_build depend
%make_build all

%check
# Relax the crypto-policies requirements for the regression tests
# Revert patch7 before running tests
patch -p1 -R < %{PATCH7}
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export MALLOC_CHECK_=3
export MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
# export HARNESS_VERBOSE=yes

# Run the tests in non FIPS mode
LD_LIBRARY_PATH="$PWD" make test -j16

%if %{with fips}
# Embed HMAC into fips provider for test run
OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < providers/fips.so > providers/fips.so.hmac
qobjcopy --update-section .rodata1=providers/fips.so.hmac providers/fips.so providers/fips.so.mac
mv providers/fips.so.mac providers/fips.so

# Run the tests also in FIPS mode
OPENSSL_FORCE_FIPS_MODE=1 LD_LIBRARY_PATH="$PWD" make test -j16 || :

# Add generation of HMAC checksum of the final stripped library
# We manually copy standard definition of __spec_install_post
# and add hmac calculation/embedding to fips.so
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    OPENSSL_CONF=/dev/null LD_LIBRARY_PATH=. apps/openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:f4556650ac31d35461610bac4ed81b1a181b2d8a43ea2854cbae22ca74560813 < $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so > $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
    objcopy --update-section .rodata1=$RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac \
    mv $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.mac $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so \
    rm $RPM_BUILD_ROOT%{_libdir}/ossl-modules/fips.so.hmac \
%{nil}

%endif

# show ciphers
gcc -o showciphers %{optflags} -I%{buildroot}%{_includedir} %{SOURCE5} -L%{buildroot}%{_libdir} -lssl -lcrypto
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./showciphers

%install
%make_install %{?_smp_mflags} MANSUFFIX=%{man_suffix}

rename so.%{sover} so.%{version} %{buildroot}%{_libdir}/*.so.%{sover}
for lib in %{buildroot}%{_libdir}/*.so.%{version} ; do
    chmod 755 ${lib}
    ln -sf $(basename ${lib}) %{buildroot}%{_libdir}/$(basename ${lib} .%{version})
    ln -sf $(basename ${lib}) %{buildroot}%{_libdir}/$(basename ${lib} .%{version}).%{sover}
done

# Remove static libraries
rm -f %{buildroot}%{_libdir}/lib*.a

# Remove the cnf.dist
rm -f %{buildroot}%{ssletcdir}/openssl.cnf.dist
rm -f %{buildroot}%{ssletcdir}/ct_log_list.cnf.dist

# Make a copy of the default openssl.cnf file
cp %{buildroot}%{ssletcdir}/openssl.cnf %{buildroot}%{ssletcdir}/openssl-orig.cnf

# Create openssl ca-certificates dir required by nodejs regression tests [bsc#1207484]
mkdir -p %{buildroot}%{_localstatedir}/lib/ca-certificates/openssl
install -d -m 555 %{buildroot}%{_localstatedir}/lib/ca-certificates/openssl

# Remove the fipsmodule.cnf because FIPS module is loaded automatically
rm -f %{buildroot}%{ssletcdir}/fipsmodule.cnf

ln -sf ./%{_rname} %{buildroot}/%{_includedir}/ssl
mkdir %{buildroot}/%{_datadir}/ssl
mv %{buildroot}/%{ssletcdir}/misc %{buildroot}/%{_datadir}/ssl/

# Avoid file conflicts with man pages from other packages
pushd %{buildroot}/%{_mandir}
find . -type f -exec chmod 644 {} +
mv man5/config.5%{man_suffix} man5/openssl.cnf.5
popd

# Do not install demo scripts executable under /usr/share/doc
find demos -type f -perm /111 -exec chmod 644 {} +

# Place showciphers.c for %%doc macro
cp %{SOURCE5} .

%if %{with fips}
# Compute the FIPS hmac using the brp-50-generate-fips-hmac script
export BRP_FIPSHMAC_FILES="%{buildroot}%{_libdir}/libssl.so.%{sover} %{buildroot}%{_libdir}/libcrypto.so.%{sover}"
%endif

# Rename the openssl CLI to openssl-1_1
mv %{buildroot}%{_bindir}/openssl %{buildroot}%{_bindir}/openssl-3
mv %{buildroot}%{_bindir}/c_rehash %{buildroot}%{_bindir}/c_rehash-3

# Install the openssl-3.cnf config file
mv %{buildroot}%{_sysconfdir}/ssl/openssl.cnf  %{buildroot}%{_sysconfdir}/ssl/openssl-3.cnf
# Unused depends on perl curl bindings which we don't have 
rm %{buildroot}%{_datadir}/ssl/misc/tsget.pl


%if %{with openssl_3_default}
ln -s openssl-%{_sonum} %{buildroot}%{_bindir}/openssl
ln -s openssl-%{_sonum}.cnf %{buildroot}%{_sysconfdir}/ssl/openssl.cnf
ln -s c_rehash-%{_sonum} %{buildroot}%{_bindir}/c_rehash
%endif

%post -p /bin/sh
if [ "$1" -gt 1 ] ; then
    # Check if the packaged default config file for openssl-3, called openssl.cnf,
    # is the original or if it has been modified and alert the user in that case
    # that a copy of the original file openssl-orig.cnf can be used if needed.
    cmp --silent %{ssletcdir}/openssl-3.cnf %{ssletcdir}/openssl-3-orig.cnf 2>/dev/null
    if [ "$?" -eq 1 ] ; then
        echo -e " The openssl-3 default config file openssl.cnf is different from" ;
        echo -e " the original one shipped by the package. A copy of the original" ;
        echo -e " file is packaged and named as openssl-orig.cnf if needed."
    fi
fi

%post -n libopenssl3 -p /sbin/ldconfig
%postun -n libopenssl3 -p /sbin/ldconfig

%files -n libopenssl3
%license LICENSE.txt
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{sover}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{sover}
%{_libdir}/engines-%{sover}
%dir %{_libdir}/ossl-modules
%{_libdir}/ossl-modules/legacy.so
%if %{with fips}
%{_libdir}/ossl-modules/fips.so
%{_libdir}/.libssl.so.%{sover}.hmac
%{_libdir}/.libcrypto.so.%{sover}.hmac
%endif

%files -n libopenssl-3-devel
%doc NOTES*.md CONTRIBUTING.md HACKING.md AUTHORS.md ACKNOWLEDGEMENTS.md
%{_includedir}/%{_rname}/
%{_includedir}/ssl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc README.md
%doc doc/html/* doc/HOWTO/* demos
%doc showciphers.c
%{_mandir}/man3/*

%files
%license LICENSE.txt
%doc CHANGES.md NEWS.md FAQ.md README.md
%dir %{ssletcdir}
%config %{ssletcdir}/openssl-orig.cnf
%config (noreplace) %{ssletcdir}/openssl-3.cnf
%config (noreplace) %{ssletcdir}/ct_log_list.cnf
%attr(700,root,root) %{ssletcdir}/private
%dir %{_datadir}/ssl
%{_datadir}/ssl/misc
%dir %{_localstatedir}/lib/ca-certificates/
%dir %{_localstatedir}/lib/ca-certificates/openssl
%{_bindir}/%{_rname}-3
%{_bindir}/c_rehash-3
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
