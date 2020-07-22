#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_with	static_libs	# don't build static library

%define		xfce_version	4.12.0
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl.UTF-8):	Biblioteka rozszerzeń do Xfce opracowana przez os-cillation
Name:		exo
Version:	0.12.11
Release:	1
License:	GPL v2
Group:		X11/Libraries
Source0:	http://archive.xfce.org/src/xfce/exo/0.12/%{name}-%{version}.tar.bz2
# Source0-md5:	efeb039d64b3257e39a1a38e75eb19b1
Patch0:		mate-terminal.patch
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	gtk+3-devel
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	gtk-doc-automake
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	perl-URI
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	xfce4-dev-tools >= 4.10.0
Requires:	glib2 >= 1:2.27.0
Requires:	xfce4-dirs >= 4.6
Provides:	libexo
Obsoletes:	libexo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension library to Xfce developed by os-cillation.

%description -l pl.UTF-8
Biblioteka rozszerzeń do Xfce opracowana przez os-cillation.

%package -n xfce-preferred-applications
Summary:	The Xfce Preferred Applications framework
Summary(pl.UTF-8):	Struktura Preferowanych Aplikacji Xfce
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme

%description -n xfce-preferred-applications
The Xfce Preferred Applications framework.

%description -n xfce-preferred-applications -l pl.UTF-8
Struktura Preferowanych Aplikacji Xfce.

%package apidocs
Summary:	libexo API documentation
Summary(pl.UTF-8):	Dokumentacja API libexo
Group:		Documentation
Requires:	gtk-doc-common
Provides:	libexo-apidocs
Obsoletes:	libexo-apidocs
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
libexo API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libexo.

%package devel
Summary:	Header files for libexo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libexo
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.14.0
Requires:	gtk+3-devel
Requires:	libxfce4util-devel >= %{xfce_version}
Provides:	libexo-devel
Obsoletes:	libexo-devel

%description devel
Header files for libexo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libexo.

%package static
Summary:	Static libexo library
Summary(pl.UTF-8):	Statyczna biblioteka libexo
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	libexo-static
Obsoletes:	libexo-static

%description static
Static libexo library.

%description static -l pl.UTF-8
Statyczna biblioteka libexo.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/' configure.ac
%{__sed} -i -e '1s,/usr/bin/env perl,%{__perl},' exo-helper/helpers/exo-compose-mail

mkdir -p m4

%build
%{?with_apidocs:%{__gtkdocize}}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# already exists as ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

# unknown / unsupported
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{hy_AM,ie}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}/exo}

%find_lang exo-1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	-n xfce-preferred-applications
%update_icon_cache hicolor

%postun	-n xfce-preferred-applications
%update_icon_cache hicolor

%files -f exo-1.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_libdir}/libexo-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-1.so.0
%attr(755,root,root) %{_libdir}/libexo-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-2.so.0
%{_pixmapsdir}/exo

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/exo-desktop-item-edit
%attr(755,root,root) %{_bindir}/exo-open
%attr(755,root,root) %{_bindir}/exo-preferred-applications
%dir %{_libdir}/xfce4/exo
%attr(755,root,root) %{_libdir}/xfce4/exo/exo-compose-mail
%dir %{_libdir}/xfce4/exo-2
%attr(755,root,root) %{_libdir}/xfce4/exo-2/exo-helper-2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/xfce4/*.rc
%dir %{_datadir}/xfce4/helpers
%{_datadir}/xfce4/helpers/*.desktop
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/preferences-desktop-default-applications.png
%{_mandir}/man1/*.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/exo-1
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/exo-csource
%attr(755,root,root) %{_libdir}/libexo-1.so
%attr(755,root,root) %{_libdir}/libexo-2.so
%{_includedir}/exo-1
%{_includedir}/exo-2
%{_pkgconfigdir}/exo-1.pc
%{_pkgconfigdir}/exo-2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexo-1.a
%{_libdir}/libexo-2.a
%endif
