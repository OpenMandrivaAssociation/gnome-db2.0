%define pkgname	libgnomedb
%define	major	4
%define name	gnome-db2.0
%define oname gnome-db
%define api 3.0
%define libname	%mklibname %{oname}%{api}_ %major 
%define gdaver 2.99.6

Summary:	GNOME DB
Name:		%name
Version: 2.99.6
Release: %mkrel 1
License:	GPL/LGPL
Group: 		Databases
URL:		http://www.gnome-db.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	gda2.0-devel >= %gdaver
BuildRequires:	scrollkeeper
BuildRequires:	gtk-doc
BuildRequires:	libglade2.0-devel
BuildRequires:	gtksourceview-devel
BuildRequires:  evolution-data-server-devel
BuildRequires:	glade3-devel >= 3.1.5
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

%description -n %{libname}
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.


%package -n %{libname}-devel
Summary:	GNOME DB Development
Group: 		Development/Databases
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires(post):		scrollkeeper
Requires(postun):		scrollkeeper

%description -n %{libname}-devel
Gnome DB is a frontend to the GDA architecture, being developed as part
of the GNOME project. It adds, to the already powerful GDA architecture,
a nice GUI front end for users, as well as a whole set of software
components intended to be reused in other unrelated applications.

This package contains libraries, header files and tools to let
you develop GNOME-DB applications.


%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

# menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_bindir}/gnome-database-properties-3.0" \
 icon="gnome-db2.png" \
 needs="x11" section="More Applications/Databases" \
 title="GNOME Database configuration" \
 longtitle="Configure your database environment" \
 startup_notify="true" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="AdvancedSettings" \
  --add-category="X-MandrivaLinux-MoreApplications-Databases" \
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

%post
%{update_menus}
%post_install_gconf_schemas libgnomedb-3.0

%preun
%preun_uninstall_gconf_schemas libgnomedb-3.0

%postun
%{clean_menus}

%post -n %{libname}-devel
%update_scrollkeeper

%postun -n %{libname}-devel
%clean_scrollkeeper

%post -n %{libname} -p /sbin/ldconfig
							  
%postun -n %{libname} -p /sbin/ldconfig
							  
%files -f %{pkgname}-%api.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS
%_sysconfdir/gconf/schemas/libgnomedb-3.0.schemas
%{_bindir}/*
%{_datadir}/pixmaps/*
%_libdir/glade3/modules/libgladegnomedb.so
%_datadir/glade3/
%dir %_datadir/gnome-db/
%_datadir/gnome-db/*.xml
%_datadir/gnome-db/*.glade
%_datadir/applications/database-properties-3.0.desktop
%{_libdir}/libglade/2.0/*
%dir %{_libdir}/libgnomedb/
%{_libdir}/libgnomedb/plugins/
%{_menudir}/*
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/libgnomedb*-%{api}.so.%{major}*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/gnome-db/demo
