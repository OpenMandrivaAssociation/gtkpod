%define name	gtkpod
%define version 2.0.2
%define git 0
%if %git
%define release %mkrel -c %git 1
%else
%define release %mkrel 1
%endif

%define major 1
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name: 	 	%{name}
Summary: 	GTK interface to iPod
Version: 	%{version}
Release: 	%{release}
%if %git
Source0:       %{name}-%{git}.tar.xz
%else
Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%version.tar.gz
%endif
Patch0: gtkpod-2.0.0-gtk-deprecated.patch
Patch1: gtkpod-cover.patch
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
BuildRequires:	libanjuta-devel >= 2.30.0
BuildRequires:	libgdl-devel
BuildRequires:	libcurl-devel
BuildRequires:	webkitgtk-devel
BuildRequires:	libgstreamer-plugins-base-devel
BuildRequires:	flex
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Suggests: %mklibname mp4v2_ 1
Suggests: faad2

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

%package -n %libname
Group: System/Libraries
Summary: Shared library part of %nama

%description -n %libname
This is the shared library part of %{name}.

%package -n %develname
Group: Development/C
Summary: Development files for %name
Provides: %name-devel = %version-%release
Requires: %libname = %version-%release

%description -n %develname
This is the development part of %{name}.

%prep
%if %git
%setup -q -n %name
./autogen.sh -V
%else
%setup -q -n %name-%version
%endif
%patch0 -p1 -b .deprecated
%patch1 -p1 -b .cover
%patch4 -p0
%patch5 -p1
chmod 644 README ChangeLog COPYING AUTHORS
#patch0
autoconf

%build
#gw we suggest it, this trick is to make the m4a plugin build
ln -s /bin/true faad
export PATH=.:$PATH
%configure2_5x --disable-static
%make LDFLAGS=%ldflags
										
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

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/gtkpod.desktop
%_datadir/icons/hicolor/*/apps/gtkpod.*
%_mandir/man1/gtkpod.1*
%dir %_libdir/%name
%_libdir/%name/*.la
%_libdir/%name/*.so
%_libdir/%name/core_prefs.plugin
%_libdir/%name/cover_display.plugin
%_libdir/%name/coverweb.plugin
%_libdir/%name/details_editor.plugin
%_libdir/%name/exporter.plugin
%_libdir/%name/filetype_flac.plugin
%_libdir/%name/filetype_m4a.plugin
%_libdir/%name/filetype_mp3.plugin
%_libdir/%name/filetype_mp4.plugin
%_libdir/%name/filetype_ogg.plugin
%_libdir/%name/filetype_wav.plugin
%_libdir/%name/filetype_video.plugin
%_libdir/%name/info_display.plugin
%_libdir/%name/media_player.plugin
%_libdir/%name/mserv.plugin
%_libdir/%name/photo_editor.plugin
%_libdir/%name/playlist_display.plugin
%_libdir/%name/repository_editor.plugin
%_libdir/%name/sorttab_display.plugin
%_libdir/%name/track_display.plugin


%files -n %libname
%defattr(-,root,root)
%_libdir/libgtkpod.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/libgtkpod.so
%_libdir/libgtkpod.la
%_libdir/pkgconfig/libgtkpod-1.0.pc
%_includedir/gtkpod
