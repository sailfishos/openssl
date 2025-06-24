%bcond_with checks

%define ssletcdir %{_sysconfdir}/pki/tls
%define sover 3
%define _rname openssl

Name:           openssl
Version:        3.2.4
Release:        0
Summary:        Secure Sockets and Transport Layer Security
License:        ASL 2.0
URL:            https://github.com/sailfishos/openssl/
Source:         %{name}-%{version}.tar.gz
# https://www.openssl.org/about/
# http://pgp.mit.edu:11371/pks/lookup?op=get&search=0xA2D29B7BF295C759#/openssl.keyring
Source5:        showciphers.c
Patch0001:      0001-Remove-build-date-for-reproducibility.patch
Patch0002:      0002-Implicitly-load-OpenSSL-configuration.patch
Patch0003:      0003-Set-a-sane-default-cipher-list-for-applications.patch
Patch0004:      0004-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch
# FIXME: Enable add crypto-policies once we have done it
# Patch0005:      0005-Add-default-section-to-load-crypto-policies-configur.patch
BuildRequires:  pkgconfig
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(bigint)
BuildRequires:  perl(lib)
BuildRequires:  pkgconfig(zlib)
%if %{with checks}
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
%endif
Requires:       openssl-libs = %{version}-%{release}
Provides:       ssl
# Requires:       crypto-policies

%description
OpenSSL is a software library to be used in applications that need to
secure communications over computer networks against eavesdropping or
need to ascertain the identity of the party at the other end.
OpenSSL contains an implementation of the SSL and TLS protocols.

%package libs
Summary:        Secure Sockets and Transport Layer Security
Requires:       ca-certificates
Conflicts:      %{name} < %{version}-%{release}
# Requires:       crypto-policies
# Require previous compatibility version so rpm does not break during update
Requires:       openssl1.1

%description libs
OpenSSL is a software library to be used in applications that need to
secure communications over computer networks against eavesdropping or
need to ascertain the identity of the party at the other end.
OpenSSL contains an implementation of the SSL and TLS protocols.

%package devel
Summary:        Development files for OpenSSL
Requires:       openssl-libs = %{version}
Requires:       pkgconfig(zlib)
Recommends:     %{name} = %{version}

%description devel
This subpackage contains header files for developing applications
that want to make use of the OpenSSL C API.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build

./Configure \
    no-mdc2 no-ec2m no-sm2 no-sm4 no-docs \
    enable-rfc3779 enable-camellia enable-seed \
%ifarch x86_64 aarch64 ppc64le
    enable-ec_nistp_64_gcc_128 \
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
    %{nil}
   # --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
   # # FIXME requires crypto-policies which isn't packaged now

# Show build configuration
perl configdata.pm --dump

# Do not run this in a production package the FIPS symbols must be patched-in
# util/mkdef.pl crypto update

%make_build depend
%make_build all

%check
%if %{with checks}
# Relax the crypto-policies requirements for the regression tests
# Revert patch4 before running tests
patch -p1 -R < %{PATCH4}
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export MALLOC_CHECK_=3
export MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
# export HARNESS_VERBOSE=yes

LD_LIBRARY_PATH="$PWD" make test -j16

# show ciphers
gcc -o showciphers %{optflags} -I%{buildroot}%{_includedir} %{SOURCE5} -L%{buildroot}%{_libdir} -lssl -lcrypto
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./showciphers
%endif

%install
%make_install %{?_smp_mflags}

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

ln -sf ./%{_rname} %{buildroot}/%{_includedir}/ssl

# Remove unused perl scripts
rm -r %{buildroot}/%{ssletcdir}/misc
rm %{buildroot}%{_bindir}/c_rehash

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

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc NEWS.md README.md
%dir %{ssletcdir}
%config %{ssletcdir}/openssl-orig.cnf
%config (noreplace) %{ssletcdir}/openssl.cnf
%config (noreplace) %{ssletcdir}/ct_log_list.cnf
%attr(700,root,root) %{ssletcdir}/private
%{_bindir}/%{_rname}

%files libs
%license LICENSE.txt
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{sover}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{sover}
%{_libdir}/engines-%{sover}
%dir %{_libdir}/ossl-modules
%{_libdir}/ossl-modules/legacy.so

%files devel
%doc NOTES*.md CONTRIBUTING.md HACKING.md AUTHORS.md ACKNOWLEDGEMENTS.md
%{_includedir}/%{_rname}/
%{_includedir}/ssl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
