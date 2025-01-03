#
# Conditional build:
%bcond_without	apidocs		# gtk-doc documentation
%bcond_with	static_libs	# static libraries

%define		xfce_version	4.20.0
Summary:	Extension library to Xfce developed by os-cillation
Summary(pl.UTF-8):	Biblioteka rozszerzeń do Xfce opracowana przez os-cillation
Name:		exo
Version:	4.20.0
Release:	1
License:	GPL v2
Group:		X11/Libraries
Source0:	https://archive.xfce.org/src/xfce/exo/4.20/%{name}-%{version}.tar.bz2
# Source0-md5:	f059ec3d8686d4b322c42d19ebec0366
URL:		https://docs.xfce.org/xfce/exo/start
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.72.0
BuildRequires:	gtk+3-devel >= 3.24.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.20}
BuildRequires:	gtk-doc-automake >= 1.20
BuildRequires:	libtool >= 2:2.4
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	perl-URI
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.000
BuildRequires:	xfce4-dev-tools >= 4.20.0
Requires:	glib2 >= 1:2.72.0
Requires:	gtk+3 >= 3.24.0
Requires:	xfce4-dirs >= 4.6
Provides:	libexo
Obsoletes:	libexo < 0.3.101
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension library to Xfce developed by os-cillation.

%description -l pl.UTF-8
Biblioteka rozszerzeń do Xfce opracowana przez os-cillation.

%package -n xfce-preferred-applications
Summary:	The Xfce Preferred Applications framework
Summary(pl.UTF-8):	Struktura Preferowanych Aplikacji Xfce
Group:		X11/Applications
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	hicolor-icon-theme

%description -n xfce-preferred-applications
The Xfce Preferred Applications framework.

%description -n xfce-preferred-applications -l pl.UTF-8
Struktura Preferowanych Aplikacji Xfce.

%package devel
Summary:	Header files for libexo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libexo
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk+3-devel >= 3.24.0
Requires:	libxfce4util-devel >= %{xfce_version}
Provides:	libexo-devel
Obsoletes:	libexo-devel < 0.3.101

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
Obsoletes:	libexo-static < 0.3.101

%description static
Static libexo library.

%description static -l pl.UTF-8
Statyczna biblioteka libexo.

%package apidocs
Summary:	libexo API documentation
Summary(pl.UTF-8):	Dokumentacja API libexo
Group:		Documentation
Requires:	gtk-doc-common
Provides:	libexo-apidocs
Obsoletes:	libexo-apidocs < 0.3.101
BuildArch:	noarch

%description apidocs
libexo API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libexo.

%prep
%setup -q

mkdir -p m4

%build
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libexo*.la

# unify dir name
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fa_IR,fa}
# duplicates of hy,ur,az
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{az_AZ,hy_AM,ur_PK}
# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{hye,ie}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}/exo-2}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	-n xfce-preferred-applications
%update_icon_cache hicolor

%postun	-n xfce-preferred-applications
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS
%attr(755,root,root) %{_libdir}/libexo-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexo-2.so.0
%{_pixmapsdir}/exo

%files -n xfce-preferred-applications
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/exo-desktop-item-edit
%attr(755,root,root) %{_bindir}/exo-open
%{_mandir}/man1/exo-open.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexo-2.so
%{_includedir}/exo-2
%{_pkgconfigdir}/exo-2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexo-2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/exo-2
%endif
