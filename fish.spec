%define _empty_manifest_terminate_build 0
# building with tests enabled
%bcond_without tests

Summary:	A friendly interactive shell
Name:		fish
Version:	4.2.1
Release:	1
License:	GPLv2 and BSD and ISC and LGPLv2+ and MIT
Group:		Shells
URL:		https://github.com/fish-shell/fish-shell/
Source0:	https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
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
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	rust-packaging
%if %{with tests}
BuildRequires:	python%{pyver}dist(pexpect)
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
# tab completion wants man-db
Recommends:	man-db
Recommends:	man-pages
Recommends:	groff-base

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

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
# NOTE release of fish (> 4.2.1).
# in 4.2.1 the new man.fish test is flaky, the `man fish` pages all display normally
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
	-DBUILD_DOCS=ON \
	-Dextra_completionsdir=%{_datadir}/%{name}/vendor_completions.d \
	-Dextra_functionsdir=%{_datadir}/%{name}/vendor_functions.d \
	-Dextra_confdir=%{_datadir}/%{name}/vendor_conf.d \
	-G Ninja
%ninja_build -C build

%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%install
%ninja_install -C build -v

# Install docs from tarball root
cp -a README.rst %{buildroot}%{_docdir}
cp -a CONTRIBUTING.rst %{buildroot}%{_docdir}

%if %{with tests}
%check
export CI=1
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
%defattr(-,root,root,-)
%license COPYING
%license LICENSES.dependencies
%{_mandir}/man1/fish*.1*
%{_bindir}/fish*
%config(noreplace) %{_sysconfdir}/fish/
%{_datadir}/fish/
%{_datadir}/pkgconfig/fish.pc
%{_docdir}


%changelog
* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 1.23.1-2mdv2011.0
+ Revision: 635425
- do not build bundled xsel

* Mon Mar 08 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.23.1-1mdv2011.0
+ Revision: 515786
- fix file list
- use configure2_5x
- update to 1.23.1

* Fri Feb 19 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.23.0-3mdv2010.1
+ Revision: 507983
- fix URL, SOURCE, Licence

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 1.23.0-2mdv2010.0
+ Revision: 437549
- rebuild

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 1.23.0-1mdv2009.1
+ Revision: 324643
- New upstream release

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.22.3-1mdv2008.1
+ Revision: 136415
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - do not package big ChangeLog

* Thu May 03 2007 Michael Scherer <misc@mandriva.org> 1.22.3-1mdv2008.0
+ Revision: 20938
- update to 1.22.3
- Import fish

* Sun Apr 30 2006 Michael Scherer <misc@mandriva.org> 1.21.5-1mdk
- New release 1.21.5

* Mon Apr 10 2006 Michael Scherer <misc@mandriva.org> 1.21.3-1mdk
- New release 1.21.3

* Mon Feb 27 2006 Michael Scherer <misc@mandriva.org> 1.21.1-1mdk
- New release 1.21.1

* Tue Jan 31 2006 Michael Scherer <misc@mandriva.org> 1.20.1-1mdk
- New release 1.20.1

* Tue Jan 17 2006 Michael Scherer <misc@mandriva.org> 1.19.0-1mdk
- New release 1.19.0

* Tue Dec 20 2005 Michael Scherer <misc@mandriva.org> 1.18.2-1mdk
- first mandriva package, upon rgs request ( happy christmas to you ),
  based on Axel Liljencrantz <axel@liljencrantz.se> spec.
