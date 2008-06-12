%define pkgname	libgnomedb
%define	major	4
%define name	gnome-db2.0
%define oname gnome-db
%define api 3.0
%define libname	%mklibname %{oname}%{api}_ %major 
%define libnamedev %mklibname -d %{oname}%{api}
%define gdaver 3.1.2

Summary:	GNOME DB
Name:		%name
Version: 3.1.2
Release: %mkrel 3
License:	GPL/LGPL
Group: 		Databases
URL:		http://www.gnome-db.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# (fc) 3.1.2-3mdv fix underlinking
Patch0:		libgnomedb-3.1.2-fixunderlinking.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	gda2.0-devel >= %gdaver
BuildRequires:	scrollkeeper
BuildRequires:	gtk-doc
BuildRequires:	libglade2.0-devel
BuildRequires:	gtksourceview1-devel
BuildRequires:  evolution-data-server-devel
BuildRequires:	glade3-devel >= 3.1.5
BuildRequires:	libgoocanvas-devel >= 0.9
BuildRequires:	libgraphviz-devel
BuildRequires:	ImageMagick
BuildRequires:  perl-XML-Parser
BuildRequires:  desktop-file-utils
BuildRequires:  intltool

%description
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

This package contains the core components of GNOME-DB.

%package -n %{libname}
Summary:	GNOME DB libraries
Group: 		System/Libraries
Requires: %name >= %version

%description -n %{libname}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.


%package -n %{libnamedev}
Summary:	GNOME DB Development
Group: 		Development/Databases
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Obsoletes: %mklibname -d %{oname}%{api}_ %major
Requires(post):		scrollkeeper
Requires(postun):		scrollkeeper

%description -n %{libnamedev}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

This package contains libraries, header files and tools to let
you develop GNOME-DB applications.


%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .fixunderlinking

#needed by patch0
autoreconf

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

#replace icon with correct name
sed -i -e 's/^Icon=gnome-db$/Icon=gnome-db2/g' $RPM_BUILD_ROOT%{_datadir}/applications/database-properties-3.0.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="AdvancedSettings" \
  --add-category="GNOME" \
  --add-category="GTK" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


# icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}
install -D -m 644 gnome-db.png $RPM_BUILD_ROOT%{_liconsdir}/gnome-db2.png
convert -geometry 32x32 gnome-db.png $RPM_BUILD_ROOT%{_iconsdir}/gnome-db2.png
convert -geometry 16x16 gnome-db.png $RPM_BUILD_ROOT%{_miconsdir}/gnome-db2.png

%{find_lang} %{pkgname}-%api --with-gnome

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.{la,a} \
       $RPM_BUILD_ROOT%{_libdir}/glade3/modules/*a \
       $RPM_BUILD_ROOT%{_libdir}/libgnomedb/plugins/*a

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_menus}
%post_install_gconf_schemas libgnomedb-3.0
%endif

%preun
%preun_uninstall_gconf_schemas libgnomedb-3.0

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%if %mdkversion < 200900
%post -n %{libnamedev}
%update_scrollkeeper
%endif

%if %mdkversion < 200900
%postun -n %{libnamedev}
%clean_scrollkeeper
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
							  
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif
							  
%files -f %{pkgname}-%api.lang
%defattr(-, root, root)
%doc AUTHORS COPYING NEWS
%_sysconfdir/gconf/schemas/libgnomedb-3.0.schemas
%{_bindir}/*
%{_datadir}/pixmaps/*
%_libdir/glade3/modules/libgladegnomedb.so
%_datadir/glade3/
%dir %_datadir/gnome-db-%{api}/
%_datadir/gnome-db-%{api}/*.xml
%_datadir/gnome-db-%{api}/*.glade
%_datadir/applications/database-properties-3.0.desktop
%{_libdir}/libglade/2.0/*
%dir %{_libdir}/gnome-db-%{api}/
%{_libdir}/gnome-db-%{api}/plugins/
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgnomedb*-%{api}.so.%{major}*

%files -n %{libnamedev}
%defattr(-, root, root)
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/gnome-db-%{api}/demo
