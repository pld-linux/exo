#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_pre	beta1
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl):	Biblioteka rozszerzeñ do Xfce opracowana przez os-cillation
Name:		libexo
Version:	0.3.1.6
Release:	0.%{_pre}.1
License:	GPL v2
Group:		Libraries
Source0:	http://download.berlios.de/xfce-goodies/exo-%{version}%{_pre}.tar.bz2
# Source0-md5:	27428c5462837162ccda6ae1d2626627
URL:		http://www.os-cillation.com/
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.6.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libxfce4util-devel >= 4.2.2
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-pygtk-devel >= 2:2.4.0
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xfce-mcs-manager
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

%description -n xfce-preferred-applications
The Xfce Preferred Applications framework.

%description -n xfce-preferred-applications -l pl
Struktura Preferowanych Aplikacji Xfce.

%package devel
Summary:	Header files for libexo library
Summary(pl):	Pliki nag³ówkowe biblioteki libexo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libxfce4util-devel >= 4.2.2

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
%configure \
	--with-html-dir=%{_gtkdocdir} \
	%{!?with_static_libs:--disable-static} \
	--enable-xfce-mcs-manager
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitedir}/exo-0.3/*.{la,a}

%py_postclean

%find_lang %{name}-0.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-0.3.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/exo-helper-0.3
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/xfce4/*.rc
%{_datadir}/xfce4/doc/C
%dir %{_datadir}/xfce4/helpers
%{_datadir}/xfce4/helpers/*.desktop
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/preferences-desktop-default-applications.png
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
