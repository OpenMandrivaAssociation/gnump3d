%define name	gnump3d
%define version	3.0
%define release %mkrel 8

Name:		        %{name}
Version:	        %{version}
Release:	        %{release}
License:	        GPL
Group:		        System/Servers
Summary:	        Streaming server for MP3's
URL:		        http://www.gnu.org/software/gnump3d/
Source0:	        http://savannah.gnu.org/download/gnump3d/%{name}-%{version}.tar.bz2
Source1:	        gnump3d.init
Patch0:             gnump3d-3.0-use-constant-libdir.patch
Requires(post):     rpm-helper
Requires(preun):    rpm-helper
Requires(pre):      rpm-helper
Requires(preun):    rpm-helper
BuildArch:	        noarch
Buildroot:	        %{_tmppath}/%{name}-%{version}

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
rm -rf %{buildroot}

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

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

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
%{_mandir}/man1/*
%{_datadir}/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/log/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d
%dir %attr(-,gnump3d,gnump3d) /var/cache/gnump3d/serving




%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-8mdv2011.0
+ Revision: 610955
- rebuild

* Fri Feb 19 2010 Funda Wang <fwang@mandriva.org> 3.0-7mdv2010.1
+ Revision: 508344
- fix build

* Tue Nov 11 2008 Olivier Thauvin <nanardon@mandriva.org> 3.0-7mdv2009.1
+ Revision: 302255
- fix initscipt:
  * pid option does not exists
  * restart: do stop/start not start/stop

* Tue Sep 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-6mdv2009.0
+ Revision: 285138
- fix initscript and library search path in main programm

* Fri Sep 12 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-5mdv2009.0
+ Revision: 283947
- uncompress additional files
- use herein documents instead of additional source whenever possible
- LSB-compliant init script
- setup libs in a constant directory, to avoid breakage on each update

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 3.0-4mdv2009.0
+ Revision: 246497
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 3.0-2mdv2008.1
+ Revision: 170870
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Thu Jan 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.0-1mdv2008.1
+ Revision: 154207
- update to new version 3.0

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.9.9-2mdv2008.1
+ Revision: 132438
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Dec 14 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.9.9-1mdv2007.0
+ Revision: 96790
- new version

* Wed Nov 15 2006 Olivier Blin <oblin@mandriva.com> 2.9.9-2mdv2007.1
+ Revision: 84512
- add forgotten file.types by using a more general pattern
- Import gnump3d

* Wed Sep 06 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.9-1mdv2007.0
- New version 2.9.9

* Wed Aug 30 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.8-2mdv2007.0
- Rebuild

* Thu Nov 24 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.8-1mdk
- 2.9.8

* Tue Oct 18 2005 Olivier Thauvin <nanardon@mandriva.org> 2.9.5-1mdk
- 2.9.5

* Fri Jul 08 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.9.4-1mdk 
- new version

* Tue Jul 05 2005 Oden Eriksson <oeriksson@mandriva.com> 2.8-4mdk
- rebuild
- misc spec file fixes

* Thu May 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.8-3mdk
- fixed url (Eskild Hustvedt (Zero_Dogg) <eskild@mandrakehelp.com>)

* Wed May 19 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.8-2mdk
- remove mpg321 dependency
- create various files at install

* Wed May 19 2004 Guillaume Rousse <guillomovitch@mandrake.org> 2.8-1mdk
- new release
- spec cleanup

* Mon May 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-3mdk
- build release
- fix deps

