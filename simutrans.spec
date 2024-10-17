%define majver %(echo %{version} |cut -d. -f1)
%define minver %(echo %{version} |cut -d. -f2)
%define minminver %(echo %{version} |cut -d. -f3)
%define dashedver %(echo %{version} |sed -e 's,\\.,-,g')

Name:		simutrans
Version:	124.1
Source0:	http://tenet.dl.sourceforge.net/project/simutrans/simutrans/%{dashedver}/simutrans-src-%{dashedver}.zip
Source9:	http://tenet.dl.sourceforge.net/project/simutrans/simutrans/%{dashedver}/simulinux-x64-%{dashedver}.zip
Release:	1
Summary:	Transport and Economic Simulation Game
License:	Artistic
Group:		Games/Strategy
Url:		https://www.simutrans.com/
Source1:	config.default
Source2:	simutrans.run
Source3:	simutrans.desktop
Source4:	simutrans.png
Source100:	%name.rpmlintrc
Patch0:		simutrans-no-x86-specifics-0.111.2.2.patch
Patch1:		simutrans-0.111.2.2-homepath.patch
Requires:	simutrans-pak >= 0.%{majver}
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	bzip2-devel
BuildRequires:	zlib-devel
BuildRequires:	cmake ninja
Recommends:	timidity-patch-SGMPlusStein

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
%patch 1 -p1 -b .homepath~
%ifnarch %{ix86}
%patch 0 -p1 -b .64~
%endif
unzip -o %SOURCE9

%cmake \
	-DENABLE_WATERWAY_SIGNS:BOOL=ON \
	-DSIMUTRANS_INSTALL_PAK64:BOOL=ON \
	-G Ninja

%build
cp -pr %{SOURCE1} .
%ninja_build -C build

%install
mkdir -p %{buildroot}%{_datadir}/simutrans
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_datadir}/applications

install -m 0755 build/simutrans/simutrans %{buildroot}%{_bindir}/simutrans.bin
cp -pr simutrans/{config,font,music,script,text,themes} %{buildroot}%{_datadir}/simutrans/

sed -e 's,@DATADIR@,%{_datadir},g;s,@BINDIR@,%_bindir,g' %{SOURCE2} > %{buildroot}%{_bindir}/simutrans
chmod 0755 %{buildroot}%{_bindir}/simutrans
install -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE4} %{buildroot}%{_iconsdir}/

ln -s %{_datadir}/timidity/SGMPlusStein/SGM-V2.01-JN5.2PlusStein.sf2 %{buildroot}%{_datadir}/simutrans/music/

%files
%doc simutrans/*.txt
%{_bindir}/*
%{_datadir}/simutrans
%{_iconsdir}/*
%{_datadir}/applications/*.desktop
