%define	majver	111
%define	minver	0

Name:		simutrans
Version:	0.%{majver}.%{minver}
Release:	%mkrel 1
Summary:	Transport and Economic Simulation Game
License:	Artistic
Group:		Games/Strategy
Url:		http://www.simutrans.com/
Source:		%{name}-src-%{majver}-%{minver}.zip
Source1:	config.default
Source2:	simutrans.run
Source3:	simutrans.desktop
Source4:	simutrans.png
Source5:	simutrans_langtabs-99-17.tar.bz2
Patch:		simutrans-no-x86-specifics.patch
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
%ifnarch %{ix86}
%patch -p1
%endif
cp -pr %{SOURCE1} .

%build
%make

%install
%__rm -rf %{buildroot}
%__mkdir_p %{buildroot}%{_libexecdir}/simutrans
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_iconsdir}
%__mkdir_p %{buildroot}%{_datadir}/applications

install -m 0755 build/default/sim %{buildroot}%{_libexecdir}/simutrans/simutrans.bin
cp -pr simutrans/{config,font,music,text} %{buildroot}%{_libexecdir}/simutrans/

sed -e 's,@LIBEXECDIR@,%{_libexecdir},g' %{SOURCE2} > %{buildroot}%{_bindir}/simutrans
chmod 0755 %{buildroot}%{_bindir}/simutrans
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/

%clean
%__rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc simutrans/*.txt
%{_bindir}/*
%{_libexecdir}/simutrans
%{_iconsdir}/*
%{_datadir}/applications/*.desktop
