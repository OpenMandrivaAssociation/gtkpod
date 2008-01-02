%define name	gtkpod
%define version 0.99.12
%define release %mkrel 1

%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Name: 	 	%{name}
Summary: 	GTK interface to iPod
Version: 	%{version}
Release: 	%{release}

Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.gz
Patch1: gtkpod-0.99.8-cover.patch
#gw change default mount point in the sync scripts. This isn't strictly
#nessessary as all scripts support a command line option -i mountpoint
Patch3: gtkpod-mountpoint.patch
URL:		http://gtkpod.sourceforge.net/
License:	GPL
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libid3tag-devel
BuildRequires:	libgpod-devel >= 0.6.0
BuildRequires:	libvorbis-devel
BuildRequires:	libflac-devel
BuildRequires:	gtk2-devel libglade2.0-devel
BuildRequires:	libcurl-devel
BuildRequires:	libhal-devel
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libgnomecanvas2-devel
BuildRequires:	flex
%if %build_plf
BuildRequires:	libmp4v2-devel
%endif

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

%if %build_plf
This package is in PLF as it may violate some MP4 patents.
%endif

%prep
%setup -q
%patch1 -p1 -b .cover
%patch3 -p1 -b .mountpoint
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_icon_cache hicolor
		
%postun
%clean_menus
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/gtkpod.desktop
%_datadir/icons/hicolor/*/apps/gtkpod.*

