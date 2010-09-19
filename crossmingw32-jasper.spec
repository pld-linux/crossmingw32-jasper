Summary:	JasPer library for images manipulation - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka JasPer do obróbki obrazów - wersja skrośna dla MinGW32
Name:		crossmingw32-jasper
Version:	1.900.1
Release:	2
License:	BSD-like
Group:		Development/Libraries
Source0:	http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
# Source0-md5:	a342b2b4495b3e1394e161eb5d85d754
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	crossmingw32-libjpeg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
JasPer is a collection of software (i.e., a library and application
programs) for the coding and manipulation of images. This software can
handle image data in a variety of formats. One such format supported
by JasPer is the JPEG-2000 code stream format defined in ISO/IEC
15444-1:2000 (but JasPer contains only partial implementation).

This package contains the cross version of library for Win32.

%description -l pl.UTF-8
JasPer to zestaw oprogramowania (biblioteka i aplikacje) do kodowania
i obróbki obrazków w różnych formatach. Jednym z nich jest JPEG-2000
zdefiniowany w ISO/IEC 15444-1:2000 (JasPer zawiera tylko częściową
implementację tego formatu).

Ten pakiet zawiera wersję skrośną biblioteki dla Win32.

%package static
Summary:	Static JasPer library (cross MinGW32 version)
Summary(pl.UTF-8):	Biblioteka statyczna JasPer (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static JasPer library (cross MinGW32 version).

%description static -l pl.UTF-8
Biblioteka statyczna JasPer (wersja skrośna MinGW32).

%package dll
Summary:	DLL JasPer library for Windows
Summary(pl.UTF-8):	Biblioteka DLL JasPer dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-libjpeg-dll
Requires:	wine

%description dll
DLL JasPer library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL JasPer dla Windows.

%prep
%setup -q -n jasper-%{version}

# don't build apps (and trmdemo uses sleep() not present in mingw32)
sed -i -e 's/^SUBDIRS =.*/SUBDIRS = libjasper/' src/Makefile.am
sed -i -e 's/^AM_DISABLE_SHARED/AC_LIBTOOL_WIN32_DLL/' configure.ac
sed -i -e 's/^libjasper_la_LDFLAGS = /&-no-undefined /' src/libjasper/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-opengl \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README doc/jasper.pdf doc/jpeg2000.pdf
%{_libdir}/libjasper.dll.a
%{_libdir}/libjasper.la
%{_includedir}/jasper

%files static
%defattr(644,root,root,755)
%{_libdir}/libjasper.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libjasper-*.dll
