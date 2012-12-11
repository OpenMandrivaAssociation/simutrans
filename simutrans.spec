%define	majver		111
%define	minver		3
%define	minminver	1

Name:		simutrans
Version:	0.%{majver}.%{minver}.%{minminver}
Release:	1
Summary:	Transport and Economic Simulation Game
License:	Artistic
Group:		Games/Strategy
Url:		http://www.simutrans.com/
Source:		%{name}-src-%{majver}-%{minver}-%{minminver}.zip
Source1:	config.default
Source2:	simutrans.run
Source3:	simutrans.desktop
Source4:	simutrans.png
Source5:	simutrans_langtabs-99-17.tar.bz2
Patch0:		simutrans-no-x86-specifics-0.111.2.2.patch
Patch1:		simutrans-0.111.2.2-homepath.patch
Requires:	simutrans-pak >= 0.%{majver}
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	bzip2-devel
BuildRequires:	zlib-devel

%description
Simutrans is a freeware transportation simulator that runs under
Windows, Linux, and a few other operating systems (Apple Macintosh
with Intel processors, BEOS). It's similar to Transport Tycoon,
Transport Tycoon Deluxe and Transport Giant.

You take on the role of operating a transportation company, and your
goal is to get goods of various kinds, as well as passengers and mail,
from one place to the next.

Don't be fooled by the tile-based graphics - this is a very complex
game, and it is constantly evolving, with new features being added. It
is a living game, and consistently being made better and better.

%prep
%setup -q -c -a 5
find . -type f -exec chmod 644 {} \;
%patch1 -p1 -b .homepath
%ifarch x86_64
%patch0 -p1
%endif

%build
cp -pr %{SOURCE1} .
%make

%install
mkdir -p %{buildroot}%{_libexecdir}/simutrans
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_datadir}/applications

install -m 0755 build/default/sim %{buildroot}%{_libexecdir}/simutrans/simutrans.bin
cp -pr simutrans/{config,font,music,text} %{buildroot}%{_libexecdir}/simutrans/

sed -e 's,@LIBEXECDIR@,%{_libexecdir},g' %{SOURCE2} > %{buildroot}%{_bindir}/simutrans
chmod 0755 %{buildroot}%{_bindir}/simutrans
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/

%files
%doc simutrans/*.txt
%{_bindir}/*
%{_libexecdir}/simutrans
%{_iconsdir}/*
%{_datadir}/applications/*.desktop



%changelog
* Mon Apr 16 2012 Andrey Bondrov <abondrov@mandriva.org> 0.111.2.2-1
+ Revision: 791350
- Re-diff no-x86-specifics patch
- New version 0.111.2.2

* Fri Dec 09 2011 Andrey Bondrov <abondrov@mandriva.org> 0.111.0-2
+ Revision: 739531
- Add patch1 to fix game config dir in user home

* Fri Dec 09 2011 Andrey Bondrov <abondrov@mandriva.org> 0.111.0-1
+ Revision: 739527
- imported package simutrans

