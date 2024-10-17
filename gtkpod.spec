%define build_plf	0

%if "%{?distro_section}" == "tainted"
%define build_plf	1
%endif

%define major     1
%define libname   %mklibname %{name} %{major}
%define libnameatomic   %mklibname atomicparsley %{major}
%define develname %mklibname %{name} -d
%define develnameatomic %mklibname atomicparsley -d

Name:		gtkpod
Summary:	GTK interface to iPod
Version:	2.1.2
Release:	1
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%version.tar.gz
Patch2:		gtkpod-2.1.0-pref.patch
URL:		https://gtkpod.sourceforge.net/
License:	GPLv2+
Group:		Communications
BuildRequires:	libid3tag-devel
BuildRequires:	libmp4v2-devel
BuildRequires:	libgpod-devel >= 0.7.0
BuildRequires:	libvorbis-devel
BuildRequires:	libflac-devel
BuildRequires:	glib2-devel >= 2.15
BuildRequires:	gtk+3-devel
BuildRequires:	libcurl-devel
BuildRequires:	flex
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	desktop-file-utils
BuildRequires:	anjuta-devel
BuildRequires:	gdl-devel
BuildRequires:	webkitgtk3-devel
BuildRequires:	gstreamer0.10-devel

%if %{build_plf}
BuildRequires:	libfaad2-devel
Requires:	faad2
%endif

Suggests:	%mklibname mp4v2_ 1

%description
gtkpod is a platform independent GUI for Apple's iPod using GTK2. It allows
you to upload songs and playlists to your iPod. It supports ID3 tag editing,
multiple charsets for ID3 tags, detects duplicate songs, allows offline
modification of the database with later synchronisation, and more.

gtkpod allows you to
    * Read your existing iTunesDB (i.e. import the existing contents of
      your iPod).
    * Add mp3 files to the iPod. You can choose the charset the ID3 tags
      are encoded in from within gtkpod. The default is the charset
      currently used by your locale setting.
    * When adding songs, gtkpod detects duplicates (opt).
    * Remove songs from the iPod.
    * Create and modify playlists.
    * Modify ID3 tags -- changes are also updated in the original file (opt)
    * Write the updated iTunesDB and added songs to your iPod.
    * Work offline and synchronize your new playlists / songs with the iPod
      at a later time.
%if %{build_plf}
This package is in "Tainted" as it requires package from "Tainted".
%endif

%package -n %{libname}
Summary:	Library package for %{name}
Group:		Communications

%description -n %{libname}
Library package for %{name}.


%package -n %{libnameatomic}
Summary:	Library package for %{name}
Group:		Communications

%description -n %{libnameatomic}
Library package for %{name}.


%package -n %{develnameatomic}
Summary:	Development files for %{name}
Group:		Communications
Provides:	gtkpod-atomic-devel
Requires:	%{libname} = %{version}-%{release}

%description -n %{develnameatomic}
Development files for %{name}, you need this package if you want to compile
applications against %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Communications
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files for %{name}, you need this package if you want to compile
applications against %{name}.

%prep
%setup -q
%patch2 -p1 -b .pref
sed -i -e '/^dist_profiles_DATA/s:=.*:=:' plugins/sjcd/data/Makefile.in || die

%build
autoreconf -vfi
export GST_INSPECT=true
%configure2_5x \
%if !%{build_plf}
	--without-faad \
%endif
	--disable-static
%make LIBS="$LIBS -lm"

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

desktop-file-install --vendor="" \
  --add-mime-type="x-content/audio-player" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# don't ship .la
find %{buildroot} -name '*.la' | xargs rm -f

%files -f %{name}.lang
%doc README AUTHORS ChangeLog
%{_datadir}/glib-2.0/schemas/*.xml
%{_bindir}/%{name}
%{_libdir}/%{name}/*.plugin
%{_libdir}/%{name}/*.so
%{_datadir}/%{name}
%{_datadir}/applications/gtkpod.desktop
%{_datadir}/icons/hicolor/*/apps/gtkpod.*
%{_mandir}/man1/gtkpod.1*

%files -n %{libname}
%{_libdir}/libgtkpod.so.%{major}*

%files -n %{libnameatomic}
%{_libdir}/libatomicparsley.so.0*

%files -n %{develname}
%{_includedir}/gtkpod/
%{_libdir}/libgtkpod.so
%{_libdir}/pkgconfig/*.pc

%files -n %{develnameatomic}
%{_libdir}/libatomicparsley.so
