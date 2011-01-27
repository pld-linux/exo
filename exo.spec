#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
%define		xfce_version	4.8.0
#
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl.UTF-8):	Biblioteka rozszerzeń do Xfce opracowana przez os-cillation
Name:		exo
Version:	0.6.0
Release:	1
License:	GPL v2
Group:		X11/Libraries
Source0:	http://archive.xfce.org/xfce/4.8/src/%{name}-%{version}.tar.bz2
# Source0-md5:	ac9deafdf9de426d8a03855ac549f424
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	gtk-doc-automake
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	perl-URI
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2:2.10.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	xfce4-dev-tools >= 4.8.0
Requires(post,postun):	glib2 >= 1:2.26.0
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
	--enable-notifications \
	--enable-python \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/exo-*/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{tl_PH,ur_PK}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}/exo}

%py_postclean

%find_lang exo-1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules
exit 0

%postun
/sbin/ldconfig
umask 022
%{_bindir}/gio-querymodules %{_libdir}/gio/modules
exit 0

%post	-n xfce-preferred-applications
%update_icon_cache hicolor

%postun	-n xfce-preferred-applications
%update_icon_cache hicolor

%files -f exo-1.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_libdir}/libexo-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-1.so.0
%attr(755,root,root) %{_libdir}/gio/modules/libexo-module-1.so
%{_pixmapsdir}/exo-1

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/xfce4/exo-1
%attr(755,root,root) %{_libdir}/xfce4/exo-1/exo-compose-mail-1
%attr(755,root,root) %{_libdir}/xfce4/exo-1/exo-helper-1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/xfce4/*.rc
%dir %{_datadir}/doc/exo
%dir %{_datadir}/doc/exo/html
%{_datadir}/doc/exo/html/exo-preferred-applications.css
%{_datadir}/doc/exo/html/C
%lang(bn) %{_datadir}/doc/exo/html/bn
%lang(ca) %{_datadir}/doc/exo/html/ca
%lang(da) %{_datadir}/doc/exo/html/da
%lang(de) %{_datadir}/doc/exo/html/de
%lang(el) %{_datadir}/doc/exo/html/el
%lang(es) %{_datadir}/doc/exo/html/es
%lang(fr) %{_datadir}/doc/exo/html/fr
%lang(gl) %{_datadir}/doc/exo/html/gl
%lang(id) %{_datadir}/doc/exo/html/id
%lang(it) %{_datadir}/doc/exo/html/it
%lang(ja) %{_datadir}/doc/exo/html/ja
%lang(pt) %{_datadir}/doc/exo/html/pt
%lang(pt_BR) %{_datadir}/doc/exo/html/pt_BR
%lang(ru) %{_datadir}/doc/exo/html/ru
%lang(sv) %{_datadir}/doc/exo/html/sv
%lang(tr) %{_datadir}/doc/exo/html/tr
%lang(ug) %{_datadir}/doc/exo/html/ug
%lang(zh_CN) %{_datadir}/doc/exo/html/zh_CN
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
%{_gtkdocdir}/exo-1
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexo-1.so
%{_libdir}/libexo-1.la
%{_includedir}/exo-1
%{_pkgconfigdir}/exo-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexo-1.a
%endif

%files -n python-exo
%defattr(644,root,root,755)
%dir %{py_sitedir}/exo-0.6
%attr(755,root,root) %{py_sitedir}/exo-0.6/_exo.so
%dir %{py_sitedir}/exo-0.6/exo
%{py_sitedir}/exo-0.6/exo/*.py[co]
%{py_sitescriptdir}/*.py[co]

%files -n python-exo-devel
%defattr(644,root,root,755)
%{_datadir}/pygtk/2.0/defs/exo-0.6
