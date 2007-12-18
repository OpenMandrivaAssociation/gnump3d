%define name	gnump3d
%define version	2.9.9.9
%define release %mkrel 2

Name:		        %{name}
Version:	        %{version}
Release:	        %{release}
License:	        GPL
Group:		        System/Servers
Summary:	        GNUMP3d is a streaming server for MP3's
URL:		        http://www.gnu.org/software/gnump3d/
Source0:	        http://savannah.gnu.org/download/gnump3d/%{name}-%{version}.tar.bz2
Source1:	        gnump3d.init.bz2
Source2:	        gnump3d.logrotate.bz2
Requires(post):     rpm-helper
Requires(preun):    rpm-helper
Requires(pre):      rpm-helper
Requires(preun):    rpm-helper
BuildArch:	        noarch

%description
GNUMP3d is a streaming server for MP3's, OGG vorbis, and other
streamable audio files, it is designed to be: 
 
* Small, stable, self-contained, and secure.
* Simple to install, configure, and use.
* Portable across different varieties of Unix.

%prep
%setup -q
bzcat %{SOURCE1} > %{name}.init
bzcat %{SOURCE2} > %{name}.logrotate

# fix locations...
perl -pi \
	-e 's|PLUGINDIR|%{perl_vendorlib}|;' \
	-e 's|nobody|gnump3d|;' \
	etc/gnump3d.conf

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/gnump3d.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/*.types %{buildroot}%{_sysconfdir}/%{name}

install -d %{buildroot}%{_bindir}
install -m 755 bin/gnump3d2 %{buildroot}%{_bindir}/gnump3d
install -m 755 bin/gnump3d-top %{buildroot}%{_bindir}
install -m 755 bin/gnump3d-index %{buildroot}%{_bindir}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -R templates/* %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d-top.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d-index.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d.conf.1 %{buildroot}%{_mandir}/man1

install -d -m 755 %{buildroot}%{perl_vendorlib}/%{name}
install -d -m 755 %{buildroot}%{perl_vendorlib}/%{name}/plugins
install -d -m 755 %{buildroot}%{perl_vendorlib}/%{name}/lang
install -m 644 lib/gnump3d/*.pm %{buildroot}%{perl_vendorlib}/%{name}
install -m 644 lib/gnump3d/plugins/*.pm %{buildroot}%{perl_vendorlib}/%{name}/plugins
install -m 644 lib/gnump3d/lang/*.pm %{buildroot}%{perl_vendorlib}/%{name}/lang

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{name}.init %{buildroot}%{_initrddir}/%{name}

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d -m 755 %{buildroot}/var/log/gnump3d
install -d -m 755 %{buildroot}/var/cache/gnump3d
install -d -m 755 %{buildroot}/var/cache/gnump3d/serving

%pre
%_pre_useradd gnump3d /var/cache/gnump3d /bin/false

%post
%_post_service gnump3d

if [ $1 = 1 ]; then
  # create various files
  %create_ghostfile /var/cache/gnump3d/song.tags gnump3d gnump3d 640
  %create_ghostfile /var/log/gnump3d/access.log gnump3d gnump3d 640
  %create_ghostfile /var/log/gnump3d/error.log gnump3d gnump3d 640
fi

%preun
%_preun_service gnump3d

%postun
%_postun_userdel gnump3d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS DOWNSAMPLING README SUPPORT COPYING INSTALL TODO ChangeLog
%dir %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_initrddir}/gnump3d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/gnump3d
%{_bindir}/*
%{perl_vendorlib}/%{name}
%{_mandir}/man1/*
%{_datadir}/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/log/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d/serving


