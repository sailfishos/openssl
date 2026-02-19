%bcond_with checks

%define ssletcdir %{_sysconfdir}/pki/tls
%define sover 3
%define _rname openssl

Name:           openssl
Version:        3.5.5
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
# Note: changes to apps/openssl.cnf are disabled because
#       SFOS doesn't yet support crypto policies.
Patch0004:      0004-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch

BuildRequires:  pkgconfig
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(bigint)
BuildRequires:  perl(lib)
BuildRequires:  perl(Time::Piece)
BuildRequires:  pkgconfig(zlib)

%if %{with checks}
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
%endif

Requires:       openssl-libs = %{version}-%{release}
Provides:       ssl

%description
OpenSSL is a software library to be used in applications that need to
secure communications over computer networks against eavesdropping or
need to ascertain the identity of the party at the other end.
OpenSSL contains an implementation of the SSL and TLS protocols.

%package libs
Summary:        Secure Sockets and Transport Layer Security
Requires:       ca-certificates
Requires(post): diffutils
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

# 30-test_aesgcm.t test fails for aarch64 in QEMU
# https://github.com/openssl/openssl/issues/17900
%ifarch aarch64
rm -vf test/recipes/30-test_aesgcm.t
%endif

%global openssl_configure ./Configure \\\
    no-mdc2 no-ec2m no-sm2 no-sm4 no-docs \\\
    enable-rfc3779 enable-camellia enable-seed \\\
    enable-ktls \\\
    zlib \\\
%%ifarch x86_64 aarch64 ppc64le \
    enable-ec_nistp_64_gcc_128 \\\
%%endif \
    --prefix=%%{_prefix} \\\
    --libdir=%%{_lib} \\\
    --openssldir=%%{ssletcdir} \\\
    %%{optflags} \\\
    -Wa,--noexecstack \\\
    -Wl,-z,relro,-z,now \\\
    -fno-common \\\
    -DTERMIOS \\\
    -DPURIFY \\\
    -D_GNU_SOURCE \\\
    -DOPENSSL_NO_BUF_FREELISTS \\\
    $(getconf LFS_CFLAGS) \\\
    -Wall \\\
    --with-rand-seed=getrandom \\\
    %%{nil}

   # --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
   # # FIXME requires crypto-policies which isn't packaged now

%if %{with checks}
# Save the build environment for %%check
(
  echo "export LANG='${LANG}'"
  echo "export LD_AS_NEEDED='${LD_AS_NEEDED}'"
  echo "export CFLAGS='${CFLAGS}'"
  echo "export CXXFLAGS='${CXXFLAGS}'"
  echo "export FFLAGS='${FFLAGS}'"
) > "${RPM_BUILD_DIR}/.env"
%endif

%openssl_configure

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

[ -f "${RPM_BUILD_DIR}/.env" ] && source "${RPM_BUILD_DIR}/.env"

%openssl_configure

make build_programs_nodep build_modules_nodep link-utils %{?_smp_mflags}
# We should use LD_LIBRARY_PATH here (and below) instead of LD_PRELOAD,
# but it doesn't currently work right with Scratchbox2. JB#63879
# LD_LIBRARY_PATH="$PWD" make test %%{?_smp_mflags}
LD_PRELOAD="$PWD/libssl.so.3:$PWD/libcrypto.so.3" make run_tests %{?_smp_mflags}

# show ciphers
gcc -o showciphers %{optflags} -I%{buildroot}%{_includedir} %{SOURCE5} -L%{buildroot}%{_libdir} -lssl -lcrypto
# LD_LIBRARY_PATH=%%{buildroot}%%{_libdir} ./showciphers
LD_PRELOAD="%{buildroot}%{_libdir}/libssl.so.3:%{buildroot}%{_libdir}/libcrypto.so.3" ./showciphers
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
rm -f %{buildroot}%{_libdir}/*.a

# Remove the cnf.dist
rm -f %{buildroot}%{ssletcdir}/openssl.cnf.dist
rm -f %{buildroot}%{ssletcdir}/ct_log_list.cnf.dist

# Make a copy of the default openssl.cnf file
cp %{buildroot}%{ssletcdir}/openssl.cnf %{buildroot}%{ssletcdir}/openssl-orig.cnf

ln -sf ./%{_rname} %{buildroot}/%{_includedir}/ssl

# Remove unused perl scripts
rm -r %{buildroot}/%{ssletcdir}/misc
rm %{buildroot}%{_bindir}/c_rehash

%post libs -p /bin/sh
/sbin/ldconfig
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

%postun libs -p /sbin/ldconfig

%files
%license LICENSE.txt
%doc NEWS.md README.md
%{_bindir}/%{_rname}

%files libs
%license LICENSE.txt
%dir %{ssletcdir}
%config %{ssletcdir}/openssl-orig.cnf
%config (noreplace) %{ssletcdir}/openssl.cnf
%config (noreplace) %{ssletcdir}/ct_log_list.cnf
%attr(700,root,root) %{ssletcdir}/private
%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{sover}
%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{sover}
%{_libdir}/engines-%{sover}
%dir %{_libdir}/ossl-modules
%{_libdir}/ossl-modules/legacy.so

%files devel
%doc CONTRIBUTING.md HACKING.md AUTHORS.md ACKNOWLEDGEMENTS.md
%{_includedir}/%{_rname}/
%{_includedir}/ssl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_libdir}/cmake
%{_libdir}/cmake/OpenSSL
