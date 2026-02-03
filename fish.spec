%define _empty_manifest_terminate_build 0
# building with tests disabled for ABF as many are flaky, tests passing locally
%bcond tests 0

Summary:	A friendly interactive shell
Name:		fish
Version:	4.4.0
Release:	1
License:	GPLv2 and BSD and ISC and LGPLv2+ and MIT
Group:		Shells
URL:		https://github.com/fish-shell/fish-shell/
Source0:	https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	atomic-devel
BuildRequires:	cargo
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	gnupg
BuildRequires:	groff
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pexpect)
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	rust-packaging
%if %{with tests}
# tests/checks/jobs.fish requires bg and fg provided by bash/sh
# and tools from coreutils
BuildRequires:	bash
BuildRequires:	coreutils
# for tests/check/git.fish
BuildRequires:	git
# for tests/check/mux-multiline-prompt.fish also requires coreutils
BuildRequires:	grep
BuildRequires:	less
# for tests/checks/locale-numeric.fish
BuildRequires:	locales
BuildRequires:	locales-en
BuildRequires:	locales-fr
BuildRequires:	locales-extra-charsets
# tests/check/jobs.fish requires ps from procps-ng
BuildRequires:	procps-ng
BuildRequires:	tmux
%endif
# Needed to get terminfo
Requires:	ncurses
Requires:	gawk
Requires:	bc
Requires:	gzip

# tab completion wants man-db
Recommends:	man-db
Recommends:	man-pages
Recommends:	groff-base

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

%package devel
Summary:	Development files for the fish shell
Group:		Development/Libraries/C and C++

%description devel
This package contains development files for the fish shell.

%prep
%setup -q
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/fish-shell/rust-pcre2?tag=0.2.9-utf32"]
git = "https://github.com/fish-shell/rust-pcre2"
tag = "0.2.9-utf32"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

# make a build dir to build out of source
mkdir -p build/

# NOTE Remove flaky tests, these mostly run successfully in local builds but fail on
# NOTE the ABF, possibly due to the terminal emulation type used in our build
# NOTE environment.
# NOTE Upstream appear to be revising their testing set up to more universally
# NOTE support CI type environments, this may need a revisit for the next
# NOTE release of fish (> 4.3.1).
# in 4.3.1 the man.fish test is flaky, the `man fish` pages all display normally
# both in fish and bash shells in post install manual testing - disable this test by removing it.
rm -f tests/checks/man.fish

# Change the bundled scripts to invoke the python binary directly.
for f in $(find share/tools -type f -name '*.py'); do
    sed -i -e '1{s@^#!.*@#!%{__python3}@}' "$f"
done

%build
export CARGO_NET_OFFLINE=true
cmake -B ./build \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DWITH_MESSAGE_LOCALIZATION=ON \
	-DWITH_DOCS=ON \
	-Dextra_completionsdir=%{_datadir}/%{name}/vendor_completions.d \
	-Dextra_functionsdir=%{_datadir}/%{name}/vendor_functions.d \
	-Dextra_confdir=%{_datadir}/%{name}/vendor_conf.d \
	-G Ninja
%ninja_build -C build

%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%install
%ninja_install -C build

# Install docs from tarball root
cp -a README.rst %{buildroot}%{_docdir}/fish
cp -a CONTRIBUTING.rst %{buildroot}%{_docdir}/fish

# Remove build artifacts from buildroot
rm -fv %{buildroot}/%{_docdir}/fish/.buildinfo
rm -fv %{buildroot}/%{_datadir}/fish/completions/..fish

%if %{with tests}
%check
export CI=true
%ninja -C build fish_run_tests -v
%endif

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/fish" > %{_sysconfdir}/shells
    echo "/bin/fish" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/fish$" %{_sysconfdir}/shells || echo "%{_bindir}/fish" >> %{_sysconfdir}/shells
    grep -q "^/bin/fish$" %{_sysconfdir}/shells || echo "/bin/fish" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/fish$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/fish$!d' %{_sysconfdir}/shells
fi

%files
%license COPYING LICENSES.dependencies
%{_bindir}/fish*
%{_docdir}/fish/
%{_datadir}/fish/
%{_mandir}/man1/fish*.1*
%config(noreplace) %{_sysconfdir}/fish/

%files devel
%license COPYING
%{_datadir}/pkgconfig/fish.pc
