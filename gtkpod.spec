%define name	gtkpod
%define version 1.0.0
%define git 0
%if %git
%define release %mkrel -c %git 1
%else
%define release %mkrel 1
%endif

Name: 	 	%{name}
Summary: 	GTK interface to iPod
Version: 	%{version}
Release: 	%{release}
%if %git
Source0:       %{name}-%{git}.tar.xz
%else
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%version.tar.gz
%endif
Patch1: gtkpod-cover.patch
#gw change default mount point in the sync scripts. This isn't strictly
#nessessary as all scripts support a command line option -i mountpoint
Patch3: gtkpod-mountpoint.patch
Patch4: gtkpod-tomboy-notes-path.patch
Patch5: gtkpod-fix-quoting-in-sync-scripts.patch
URL:		http://gtkpod.sourceforge.net/
License:	GPLv2+
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libid3tag-devel
BuildRequires:	libmp4v2-devel
BuildRequires:	libgpod-devel >= 0.7.0
BuildRequires:	libvorbis-devel
BuildRequires:	libflac-devel
BuildRequires:	glib2-devel >= 2.15
BuildRequires:	gtk2-devel libglade2.0-devel
BuildRequires:	libcurl-devel
BuildRequires:	flex
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Suggests: %mklibname mp4v2_ 1

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

%prep
%if %git
%setup -q -n %name
./autogen.sh -V
%else
%setup -q -n %name-%version
%endif
%patch1 -p1 -b .cover
%patch3 -p1 -b .mountpoint
%patch4 -p0
%patch5 -p1
chmod 644 README ChangeLog COPYING AUTHORS

%build
%configure2_5x
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%find_lang %{name}

%if %_lib != lib
perl -pi -e "s!%_prefix/lib!%_libdir!g" %buildroot%_datadir/%name/scripts/sync-evolution.sh
%endif

desktop-file-install --vendor="" \
  --add-mime-type="x-content/audio-player" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*



%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%update_desktop_database
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%clean_desktop_database
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/gtkpod.desktop
%_datadir/icons/hicolor/*/apps/gtkpod.*
%_mandir/man1/gtkpod.1*
