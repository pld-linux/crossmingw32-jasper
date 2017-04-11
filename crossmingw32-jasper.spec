Summary:	JasPer library for images manipulation - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka JasPer do obróbki obrazów - wersja skrośna dla MinGW32
Name:		crossmingw32-jasper
Version:	2.0.12
Release:	1
License:	BSD-like
Group:		Development/Libraries
#Source0Download: http://www.ece.uvic.ca/~frodo/jasper/#download
Source0:	http://www.ece.uvic.ca/~frodo/jasper/software/jasper-%{version}.tar.gz
# Source0-md5:	b839a8bf418a64aa2d06413b23dd5ab3
Patch0:		jasper-nodocs.patch
URL:		http://www.ece.uvic.ca/~frodo/jasper/
BuildRequires:	cmake >= 2.8.11
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libjpeg
Requires:	crossmingw32-libjpeg
Obsoletes:	crossmingw32-jasper-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

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
%patch0 -p1

%build
# there is upstream directory named "build", use different name
install -d builddir
cd builddir
# note: build/jasper.pc.in expects CMAKE_INSTALL_INCLUDEDIR and CMAKE_INSTALL_LIBDIR relative to CMAKE_INSTALL_PREFIX
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib \
	-DCMAKE_SYSTEM_NAME=Windows \
	-DJAS_ENABLE_AUTOMATIC_DEPENDENCIES=FALSE \
	-DJAS_ENABLE_OPENGL=FALSE \
	-DJPEG_INCLUDE_DIR:PATH=%{_includedir} \
	-DJPEG_LIBRARY=%{_libdir}/libjpeg.dll.a

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.exe \
	$RPM_BUILD_ROOT%{_mandir}/man1/*.1
%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/{README,*.pdf,html}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README doc/jasper.pdf doc/jpeg2000.pdf
%{_libdir}/libjasper.dll.a
%{_includedir}/jasper
%{_pkgconfigdir}/jasper.pc

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libjasper.dll
