# TODO:
# - rename to exo.spec (like tar name)
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		xfce_version	4.6.0
#
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl.UTF-8):	Biblioteka rozszerzeń do Xfce opracowana przez os-cillation
Name:		libexo
Version:	0.3.100
Release:	1
License:	GPL v2
Group:		X11/Libraries
Source0:	http://www.xfce.org/archive/xfce-%{xfce_version}/src/exo-%{version}.tar.bz2
# Source0-md5:	ebded97ff55f43cd0fe6b16242992ecf
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.10.6
BuildRequires:	gtk-doc >= 1.7
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

%description devel
Header files for libexo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libexo.

%package static
Summary:	Static libexo library
Summary(pl.UTF-8):	Statyczna biblioteka libexo
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

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
%setup -q -n exo-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--enable-hal \
	--enable-gtk-doc \
	--enable-notifications \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static} \
	--enable-python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_datadir}/locale/pt{_PT,}
mv $RPM_BUILD_ROOT%{_datadir}/locale/nb{_NO,}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/exo-0.3/*.{la,a}

%py_postclean

%find_lang %{name}-0.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n xfce-preferred-applications
%update_icon_cache hicolor

%postun	-n xfce-preferred-applications
%update_icon_cache hicolor

%files -f %{name}-0.3.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
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
%{_datadir}/xfce4/doc/C/*
%lang(es) %{_datadir}/xfce4/doc/es/*
%lang(fr) %{_datadir}/xfce4/doc/fr/*
%lang(id) %{_datadir}/xfce4/doc/id/*
%lang(ja) %{_datadir}/xfce4/doc/ja/*
%lang(pt_BR) %{_datadir}/xfce4/doc/pt_BR/*
%lang(tr) %{_datadir}/xfce4/doc/tr/*
%dir %{_datadir}/xfce4/helpers
%{_datadir}/xfce4/helpers/*.desktop
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/preferences-desktop-default-applications.png
%{_iconsdir}/hicolor/*/apps/applications-internet.png
%{_iconsdir}/hicolor/*/apps/applications-other.png
%{_mandir}/man1/*.1*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/exo

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
