Summary:	Extension library to Xfce developed by os-cillation
Summary(pl):	Biblioteka rozszerzeñ do Xfce opracowana przez os-cillation
Name:		libexo
Version:	0.3.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://download.berlios.de/xfce-goodies/exo-%{version}.tar.bz2
# Source0-md5:	ffcd73ec6b34f19c81afdc3f1a97377b
URL:		http://www.os-cillation.com/
BuildRequires:	autoconf
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig
BuildRequires:	libxfcegui4-devel >= 4.1.90
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension library to Xfce developed by os-cillation.

%description -l pl
Biblioteka rozszerzeñ do Xfce opracowana przez os-cillation.

%package devel
Summary:	Header files for libexo library
Summary(pl):	Pliki nag³ówkowe biblioteki libexo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%prep
%setup -q -n exo-%{version}

%build
%{__autoconf}
%configure \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{py_sitescriptdir}/*.py
%{_datadir}/locale/*/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/exo-0.3
%{_datadir}/pygtk/2.0/defs/exo-0.3/*
%{py_sitedir}/exo-0.3/exo/*.py[co]
%{py_sitedir}/exo-0.3/*
%{py_sitescriptdir}/*.py[co]
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{py_sitedir}/exo-0.3/*.a
