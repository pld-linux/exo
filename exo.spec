#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_pre		beta2
%define		xfce_version	4.3.90.2
#
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl):	Biblioteka rozszerzeñ do Xfce opracowana przez os-cillation
Name:		libexo
Version:	0.3.1.8
Release:	0.%{_pre}.2
License:	GPL v2
Group:		Libraries
Source0:	http://www.xfce.org/archive/xfce-%{xfce_version}/src/exo-%{version}%{_pre}.tar.bz2
# Source0-md5:	b8465faab19e233d5edda12bdd4940b4
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.10.1
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libtool
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2:2.9.3
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	rpm-pythonprov
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
BuildRequires:	xfce-mcs-manager-devel >= %{xfce_version}
BuildRequires:	xorg-lib-libXt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension library to Xfce developed by os-cillation.

%description -l pl
Biblioteka rozszerzeñ do Xfce opracowana przez os-cillation.

%package -n xfce-preferred-applications
Summary:	The Xfce Preferred Applications framework
Summary(pl):	Struktura Preferowanych Aplikacji Xfce
Group:		Applications
Requires(post,postun):	gtk+2 >= 2:2.10.0
Requires:	xfce-mcs-plugins >= %{xfce_version}

%description -n xfce-preferred-applications
The Xfce Preferred Applications framework.

%description -n xfce-preferred-applications -l pl
Struktura Preferowanych Aplikacji Xfce.

%package devel
Summary:	Header files for libexo library
Summary(pl):	Pliki nag³ówkowe biblioteki libexo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libxfce4util-devel >= %{xfce_version}

%description devel
Header files for libexo library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libexo.

%package static
Summary:	Static libexo library
Summary(pl):	Statyczna biblioteka libexo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libexo library.

%description static -l pl
Statyczna biblioteka libexo.

%package -n python-exo
Summary:	Python binding for libexo library
Summary(pl):	Wi±zania Pythona do biblioteki libexo
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-exo
Python binding for libexo library.

%description -n python-exo -l pl
Wi±zania Pythona do biblioteki libexo.

%package -n python-exo-devel
Summary:	Development files for libexo Python bindings
Summary(pl):	Pliki programistyczne wi±zañ Pythona do libexo
Group:		Libraries/Python
Requires:	python-exo = %{version}-%{release}

%description -n python-exo-devel
Development files for libexo Python bindings.

%description -n python-exo-devel -l pl
Pliki programistyczne wi±zañ Pythona do libexo.

%prep
%setup -q -n exo-%{version}%{_pre}

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static} \
	--enable-xfce-mcs-manager
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/xfce4/mcs-plugins/*.{la,a}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/exo-0.3/*.{la,a}

%py_postclean

%find_lang %{name}-0.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n xfce-preferred-applications
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%postun	-n xfce-preferred-applications
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%files -f %{name}-0.3.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/exo-compose-mail-0.3
%attr(755,root,root) %{_libdir}/exo-helper-0.3
%attr(755,root,root) %{_libdir}/xfce4/mcs-plugins/exo-preferred-applications-settings.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/xfce4/*.rc
%{_datadir}/xfce4/doc/C
%lang(ja) %{_datadir}/xfce4/doc/ja
%dir %{_datadir}/xfce4/helpers
%{_datadir}/xfce4/helpers/*.desktop
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/preferences-desktop-default-applications.png
%{_iconsdir}/hicolor/*/apps/applications-internet.png
%{_iconsdir}/hicolor/*/apps/applications-other.png
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/exo-0.3
%{_pkgconfigdir}/*.pc
# not present in beta ?
#%{_gtkdocdir}/exo

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
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
