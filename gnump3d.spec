Name:		        gnump3d
Version:	        3.0
Release:	        12
License:	        GPL
Group:		        System/Servers
Summary:	        Streaming server for MP3's
URL:		        http://www.gnu.org/software/gnump3d/
Source0:	        http://savannah.gnu.org/download/gnump3d/%{name}-%{version}.tar.bz2
Source1:	        gnump3d.service
Patch0:             gnump3d-3.0-use-constant-libdir.patch
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
%patch0 -p 1 

chmod 644 lib/gnump3d/mp4info.pm

%install

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/gnump3d.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/*.types %{buildroot}%{_sysconfdir}/%{name}

install -d %{buildroot}%{_bindir}
install -m 755 bin/gnump3d2 %{buildroot}%{_bindir}/gnump3d
install -m 755 bin/gnump3d-top %{buildroot}%{_bindir}
install -m 755 bin/gnump3d-index %{buildroot}%{_bindir}

install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d-top.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d-index.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d.1 %{buildroot}%{_mandir}/man1
install -m 644 man/gnump3d.conf.1 %{buildroot}%{_mandir}/man1

install -d -m 755 %{buildroot}%{_datadir}/%{name}/themes
cp -R templates/* %{buildroot}%{_datadir}/%{name}/themes

install -d -m 755 %{buildroot}%{_datadir}/%{name}/lib
cp -R lib/* %{buildroot}%{_datadir}/%{name}/lib

install -d -m 755 %{buildroot}%{_unitdir}
install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} <<EOF
/var/log/gnump3d/access.log {
    missingok
    notifempty
    nocompress
    postrotate
    /bin/kill -HUP `cat /var/run/gnump3d.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
EOF

install -d -m 755 %{buildroot}/var/log/gnump3d
install -d -m 755 %{buildroot}/var/cache/gnump3d
install -d -m 755 %{buildroot}/var/cache/gnump3d/serving

# fix locations...
perl -pi \
	-e 's|^theme_directory = .*|theme_directory = %{_datadir}/%{name}/themes|;' \
	-e 's|^plugin_directory = .*|plugin_directory = %{_datadir}/%{name}/lib/gnump3d/plugins|;' \
	-e 's|nobody|gnump3d|;' \
	%{buildroot}%{_sysconfdir}/%{name}/gnump3d.conf

%pre
%_pre_useradd gnump3d /var/cache/gnump3d /bin/false

%post
%systemd_post %{name}.service

if [ $1 = 1 ]; then
  # create various files
  %create_ghostfile /var/cache/gnump3d/song.tags gnump3d gnump3d 640
  %create_ghostfile /var/log/gnump3d/access.log gnump3d gnump3d 640
  %create_ghostfile /var/log/gnump3d/error.log gnump3d gnump3d 640
fi

%preun
%systemd_preun %{name}.service

%postun
%_postun_userdel gnump3d
%systemd_postun_with_restart %{name}.service

%clean

%files
%doc AUTHORS DOWNSAMPLING README SUPPORT COPYING INSTALL TODO ChangeLog
%dir %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_unitdir}/gnump3d*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/gnump3d
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/log/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d/serving
