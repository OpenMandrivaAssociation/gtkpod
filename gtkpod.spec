%define name	gtkpod
%define version 0.99.9
%define cvs 20070619
%define release %mkrel 0.%cvs.1

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

Source0:	http://prdownloads.sourceforge.net/gtkpod/%{name}-%{cvs}.tar.bz2
Patch: gtkpod-0.99.4-evopath.patch
Patch1: gtkpod-0.99.8-cover.patch
#gw change default mount point in the sync scripts. This isn't strictly
#nessessary as all scripts support a command line option -i mountpoint
Patch3: gtkpod-mountpoint.patch
URL:		http://gtkpod.sourceforge.net/
License:	GPL
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libid3tag-devel
BuildRequires:	libgpod-devel >= 0.4.3
BuildRequires:	libvorbis-devel
BuildRequires:	libflac-devel
BuildRequires:	gtk2-devel ImageMagick libglade2.0-devel
BuildRequires:	libcurl-devel
BuildRequires:	libhal-devel
BuildRequires:	libgnome-vfs2-devel
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
%setup -q -n %name
%patch0 -p1 -b .evo
%patch1 -p1 -b .cover
%patch3 -p1 -b .mountpoint
chmod 644 README ChangeLog COPYING AUTHORS
./autogen.sh

%build
%configure2_5x
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm %buildroot/%_datadir/%name/pixmaps/%name.glade*
ln -s %_datadir/gtkpod/gtkpod.glade %buildroot/%_datadir/gtkpod/pixmaps/gtkpod.glade
ln -s %_datadir/gtkpod/gtkpod.gladep %buildroot/%_datadir/gtkpod/pixmaps/gtkpod.gladep

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="GTKPod" longtitle="Interface to iPod" section="Multimedia/Sound" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=GTKPod
Comment=Interface to iPod
Exec=%{name}
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Sound;Audio;Player;
EOF


#icons
mkdir -p $RPM_BUILD_ROOT{%{_liconsdir},%{_miconsdir},%{_iconsdir}}
cp pixmaps/%{name}-icon-48x48.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -size 32x32 pixmaps/%{name}-icon-64x64.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -size 16x16 pixmaps/%{name}-icon-64x64.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-*
%{_menudir}/%{name}
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png


