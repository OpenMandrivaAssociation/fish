Summary:                A friendly interactive shell
Name:                   fish
Version:                1.23.1
Release:                %mkrel 2
License:                GPLv2
Group:                  Shells
URL:                    https://sourceforge.net/projects/fish/
Source0:                https://sourceforge.net/projects/fish/%{name}-%{version}.tar.bz2
Patch0:                 fish-1.23.0-ARG_MAX.patch
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:          doxygen ncurses-devel
Requires(post):         rpm-helper
Requires(postun):       rpm-helper
# for some function in fish configfile, like max_width, etc
Requires:               bc

%description
fish is a shell geared towards interactive use. It's features are
focused on user friendlieness and discoverability. The language syntax
is simple but incompatible with other shell languages.

%prep
%setup -q
%patch0 -p1 -b .ARG_MAX

%build
%configure2_5x --without-xsel
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -Rf $RPM_BUILD_ROOT/usr/share/doc/fish/
%find_lang %{name}
%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/share/rpm-helper/add-shell %name $1 %_bindir/fish

%postun
/usr/share/rpm-helper/del-shell %name $1 %_bindir/fish

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc user_doc/html/*
%_mandir/man1/*
%_bindir/*
%_datadir/%name
%config(noreplace) %_sysconfdir/fish
%{_docdir}/*


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
