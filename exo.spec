#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
%define		xfce_version	4.6.2
#
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl.UTF-8):	Biblioteka rozszerzeń do Xfce opracowana przez os-cillation
Name:		exo
Version:	0.3.107
Release:	4
License:	GPL v2
Group:		X11/Libraries
Source0:	http://www.xfce.org/archive/xfce-%{xfce_version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	3a92cca0c99ee940db4410891c9e8498
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.10.6
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	gtk-doc-automake
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libtool
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	perl-URI
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2:2.10.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	xfce4-dev-tools >= 4.6.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
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
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name} = %{version}-%{release}

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

%description apidocs
libexo API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libexo.

%package devel
Summary:	Header files for libexo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libexo
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+2-devel >= 2:2.10.6
Requires:	hal-devel >= 0.5.7
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

%package -n python-exo
Summary:	Python binding for libexo library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libexo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-exo
Python binding for libexo library.

%description -n python-exo -l pl.UTF-8
Wiązania Pythona do biblioteki libexo.

%package -n python-exo-devel
Summary:	Development files for libexo Python bindings
Summary(pl.UTF-8):	Pliki programistyczne wiązań Pythona do libexo
Group:		Libraries/Python
Requires:	python-exo = %{version}-%{release}

%description -n python-exo-devel
Development files for libexo Python bindings.

%description -n python-exo-devel -l pl.UTF-8
Pliki programistyczne wiązań Pythona do libexo.

%prep
%setup -q

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
	--enable-hal \
	--enable-notifications \
	--enable-python \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitedir}/exo-0.3/*.{la,a}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}/exo}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/ur_PK

%py_postclean

%find_lang libexo-0.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n xfce-preferred-applications
%update_icon_cache hicolor

%postun	-n xfce-preferred-applications
%update_icon_cache hicolor

%files -f libexo-0.3.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libexo-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-0.3.so.0
%attr(755,root,root) %{_libdir}/libexo-hal-0.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-hal-0.3.so.0
%{_pixmapsdir}/exo-0.3

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/exo-compose-mail-0.3
%attr(755,root,root) %{_libdir}/exo-helper-0.3
%attr(755,root,root) %{_libdir}/exo-mount-notify-0.3
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/xfce4/*.rc
%{_datadir}/xfce4/doc/C/*.html
%{_datadir}/xfce4/doc/C/images/*.png
%lang(da) %{_datadir}/xfce4/doc/am/*.html
%lang(da) %{_datadir}/xfce4/doc/am/images/*.png
%lang(da) %{_datadir}/xfce4/doc/da/*.html
%lang(da) %{_datadir}/xfce4/doc/da/images/*.png
%lang(es) %{_datadir}/xfce4/doc/es/*.html
%lang(es) %{_datadir}/xfce4/doc/es/images/*.png
%lang(fr) %{_datadir}/xfce4/doc/fr/*.html
%lang(fr) %{_datadir}/xfce4/doc/fr/images/*.png
%lang(gl) %{_datadir}/xfce4/doc/gl/*.html
%lang(gl) %{_datadir}/xfce4/doc/gl/images/*.png
%lang(id) %{_datadir}/xfce4/doc/id/*.html
%lang(id) %{_datadir}/xfce4/doc/id/images/*.png
%lang(it) %{_datadir}/xfce4/doc/it/*.html
%lang(it) %{_datadir}/xfce4/doc/it/images/*.png
%lang(ja) %{_datadir}/xfce4/doc/ja/*.html
%lang(ja) %{_datadir}/xfce4/doc/ja/images/*.png
%lang(pt) %{_datadir}/xfce4/doc/pt/*.html
%lang(pt) %{_datadir}/xfce4/doc/pt/images/*.png
%lang(pt_BR) %{_datadir}/xfce4/doc/pt_BR/*.html
%lang(pt_BR) %{_datadir}/xfce4/doc/pt_BR/images/*.png
%lang(tr) %{_datadir}/xfce4/doc/tr/*.html
%lang(tr) %{_datadir}/xfce4/doc/tr/images/*.png
%lang(ug) %{_datadir}/xfce4/doc/ug/*.html
%lang(ug) %{_datadir}/xfce4/doc/ug/images/*.png
%dir %{_datadir}/xfce4/helpers
%{_datadir}/xfce4/helpers/*.desktop
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/preferences-desktop-default-applications.png
%{_iconsdir}/hicolor/*/apps/applications-internet.png
%{_iconsdir}/hicolor/*/apps/applications-other.png
%{_mandir}/man1/*.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/exo-0.3
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexo-0.3.so
%attr(755,root,root) %{_libdir}/libexo-hal-0.3.so
%{_libdir}/libexo-0.3.la
%{_libdir}/libexo-hal-0.3.la
%{_includedir}/exo-0.3
%{_pkgconfigdir}/exo-0.3.pc
%{_pkgconfigdir}/exo-hal-0.3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexo-0.3.a
%{_libdir}/libexo-hal-0.3.a
%endif

%files -n python-exo
%defattr(644,root,root,755)
%dir %{py_sitedir}/exo-0.3
%attr(755,root,root) %{py_sitedir}/exo-0.3/_exo.so
%dir %{py_sitedir}/exo-0.3/exo
%{py_sitedir}/exo-0.3/exo/*.py[co]
%{py_sitescriptdir}/*.py[co]

%files -n python-exo-devel
%defattr(644,root,root,755)
%{_datadir}/pygtk/2.0/defs/exo-0.3
