Summary:                A friendly interactive shell
Name:                   fish
Version:                1.21.5
Release:                %mkrel 1
License:                GPL
Group:                  Shells
URL:                    http://roo.no-ip.org/fish/
Source0:                http://roo.no-ip.org/%{name}/files/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:          doxygen ncurses-devel X11-devel
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

%build
%configure 
%make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
 
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
%doc user_doc/html/* ChangeLog 
%_mandir/man1/*
%_bindir/*
%_datadir/%name
%config(noreplace) %_sysconfdir/fish
%config(noreplace) %_sysconfdir/fish_inputrc
%config(noreplace) %_sysconfdir/fish.d
