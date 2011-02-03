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
