%define	majver		120
%define	minver		0
%define	minminver	1

Name:		simutrans
%if "%minminver" != ""
Version:	0.%{majver}.%{minver}.%{minminver}
Source0:	http://skylink.dl.sourceforge.net/project/simutrans/simutrans/%majver-%minver-%minminver/simutrans-src-%majver-%minver-%minminver.zip
Source9:	http://skylink.dl.sourceforge.net/project/simutrans/simutrans/%majver-%minver-%minminver/simulinux-x64-%majver-%minver-%minminver.zip
%else
Version:	0.%{majver}.%{minver}
Source0:	http://tenet.dl.sourceforge.net/project/simutrans/simutrans/%majver-%minver/simutrans-src-%majver-%minver.zip
Source9:	http://tenet.dl.sourceforge.net/project/simutrans/simutrans/%majver-%minver/simulinux-%majver-%minver.zip
%endif
Release:	2
Summary:	Transport and Economic Simulation Game
License:	Artistic
Group:		Games/Strategy
Url:		http://www.simutrans.com/
Source1:	config.default
Source2:	simutrans.run
Source3:	simutrans.desktop
Source4:	simutrans.png
Source5:	simutrans_langtabs-99-17.tar.bz2
Source100:	%name.rpmlintrc
Patch0:		simutrans-no-x86-specifics-0.111.2.2.patch
Patch1:		simutrans-0.111.2.2-homepath.patch
Patch2:		simutrans-0.120-opengl-compile.patch
Requires:	simutrans-pak >= 0.%{majver}
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	bzip2-devel
BuildRequires:	zlib-devel

%description
Simutrans is a free transportation simulator.

It is similar to Transport Tycoon, Transport Tycoon Deluxe
and Transport Giant.

You take on the role of operating a transportation company, and your
goal is to get goods of various kinds, as well as passengers and mail,
from one place to the next.

Don't be fooled by the tile-based graphics - this is a very complex
game, and it is constantly evolving, with new features being added. It
is a living game, and consistently being made better and better.

%prep
%setup -q -c -a 5
find . -type f -exec chmod 644 {} \;
%patch1 -p1 -b .homepath~
%ifarch x86_64
%patch0 -p1 -b .64~
%endif
%patch2 -p1 -b .glew~
unzip -o %SOURCE9

%build
cp -pr %{SOURCE1} .
%make
# Currently broken, but may be good in the future: BACKEND=opengl

%install
mkdir -p %{buildroot}%{_datadir}/simutrans
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_datadir}/applications

install -m 0755 build/default/sim %{buildroot}%{_bindir}/simutrans.bin
cp -pr simutrans/{config,font,music,script,text,themes} %{buildroot}%{_datadir}/simutrans/

sed -e 's,@DATADIR@,%{_datadir},g;s,@BINDIR@,%_bindir,g' %{SOURCE2} > %{buildroot}%{_bindir}/simutrans
chmod 0755 %{buildroot}%{_bindir}/simutrans
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/

%files
%doc simutrans/*.txt
%{_bindir}/*
%{_datadir}/simutrans
%{_iconsdir}/*
%{_datadir}/applications/*.desktop
