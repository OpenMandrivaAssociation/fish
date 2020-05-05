%define debug_package %{nil}

Summary:                A friendly interactive shell
Name:                   fish
Version:               	3.1.2
Release:                1
License:                GPLv2 and BSD and ISC and LGPLv2+ and MIT
Group:                  Shells
URL:			https://github.com/fish-shell/fish-shell/
Source0:                https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  	cmake
BuildRequires:  	gettext
BuildRequires:  	doxygen
BuildRequires:  	pkgconfig(ncurses)
BuildRequires:  	pkgconfig(libpcre2-8)
BuildRequires:  	pkgconfig(python)

# tab completion wants man-db
Recommends:     	man-db
Recommends:     	man-pages
Recommends:     	groff-base

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

%prep
%setup -q

%build
export CC=gcc
export CXX=g++
cmake -E env CXXFLAGS="-Wno-narrowing" cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%make_build

%install
%make_install

# Install docs from tarball root
cp -a README.md %{buildroot}%{_docdir}
cp -a CONTRIBUTING.md %{buildroot}%{_docdir}


%find_lang %{name}

%post
/usr/share/rpm-helper/add-shell %name $1 %{_bindir}/fish

%postun
/usr/share/rpm-helper/del-shell %name $1 %{_bindir}/fish

%files -f %{name}.lang
%defattr(-,root,root,-)
%license COPYING
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
