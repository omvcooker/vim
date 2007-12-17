# Notes / Warning :
# - this package is not prefixable
# - to update official patches, aka SOURCE4, see README.mdk in SOURCE4
# - as long as missing buildrequires is not identified, it must be manually built to get GUI

%define url ftp://ftp.vim.org/pub/vim/unix/
%define official_ptchlvl 87

%define perl_version %(rpm -q --qf '%%{epoch}:%%{version}' perl)

# Should we build X11 gui
%define buildgui 1

%{?_with_gui:%global buildgui 1}
%{?_without_gui:%global buildgui 0}

%define title       VI editor
%define longtitle   All-purpose text editor

Name:           vim
Version:        7.1
Release:        %mkrel 10
Summary:        VIsual editor iMproved
Url:            http://www.vim.org/
License:        Charityware
Group:          Editors
Source0:        %{url}/%name-%version.tar.bz2
Source2:        %{url}/extra/%name-%version-lang.tar.bz2
# read README.mdk in this tarball prior updating official patches:
Source4:        vim-%version.%{official_ptchlvl}-patches.tar.bz2
# http://vim.sourceforge.net/scripts/script.php?script_id=98
Source5:        vim-spec-3.0.bz2
Source6:        http://trific.ath.cx/Ftp/vim/syntax/dhcpd.vim
# from apparmor-utils package
Source7:        apparmor.vim
# MDK patches
Patch0:         vim-7.1-vimrc_nosetmouse.patch
Patch2:         vim-5.6a-paths.patch
Patch3:         vim-6.4-rpm-spec-syntax.patch
Patch8:         vim-6.0af-man-path.patch
Patch10:        xxd-locale.patch
Patch11:        vim-6.2-gcc31.patch
Patch20:        vimrc_hebrew.patch
Patch22:        vim-6.1-fix-xterms-comments.patch
Patch23:        vim-6.3-remove-docs.patch
Patch24:        vim-6.1-outline-mode.patch 
Patch25:        vim-6.1-xterm-s-insert.patch 
Patch26:        vim-7.0-changelog-mode.patch
Patch27:        vim-6.1-rpm42.patch
Patch28:        vim-6.4-po-mode.patch
Patch29:        vim-7.0-po-buildfix.patch
Patch30:        vim-7.0-add-dhcpd-syntax.patch
Patch31:	vim70-CVE-2007-2438.patch
Patch32:	vim-7.1-lzma-support.patch
Patch33:	vim-7.0-fortify_warnings-1.patch
BuildRequires:  python-devel
BuildRequires:  perl-devel
BuildRequires:  termcap-devel
BuildRequires:  acl-devel
%if %buildgui
BuildRequires:  libgnomeui2-devel
BuildRequires:  libxt-devel
BuildRequires:  tcl
BuildRequires:  tcl-devel
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.

%package common
Summary:    The common files needed by any version of the VIM editor
Group:      Editors
Requires:   perl = %perl_version
Requires(pre):      coreutils 
Requires(post):     coreutils 
Requires(preun):    coreutils 
Requires(postun):   coreutils 
Conflicts:  man-pages-fr < 1.68.0-2mdk
Conflicts:  man-pages-it < 0.3.4-2mdk
Conflicts:  man-pages-pl <= 0.4-10mdk

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.

%package minimal
Summary:    A minimal version of the VIM editor
Group:      Editors
Provides:   vim
Requires(post):     update-alternatives
Requires(postun):   update-alternatives

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-minimal package
includes a minimal version of VIM, which is installed into /bin/vi for use
when only the root partition is present.

%package enhanced
Summary:    A version of the VIM editor which includes recent enhancements
Group:      Editors
Requires:   vim-common >= %version
Obsoletes:  vim-color
Provides:   vim
Provides:   vim-color
Requires(post):     update-alternatives
Requires(postun):   update-alternatives

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-enhanced package
contains a version of VIM with extra, recently introduced features like
Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the VIM
editor which includes recently added enhancements like interpreters for the
Python and Perl scripting languages.  You'll also need to install the
vim-common package.

%if %buildgui
%package X11
Summary:    The VIM version of the vi editor for the X Window System
Group:      Editors
Provides:   vim
Requires:   vim-common >= %version
Requires(post):     desktop-file-utils
Requires(postun):   desktop-file-utils

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. VIM-X11 is a version of the
VIM editor which will run within the X Window System.  If you install this
package, you can run VIM as an X application with a full GUI interface and
mouse support.

Install the vim-X11 package if you'd like to try out a version of vi with
graphics and mouse capabilities.  You'll also need to install the
vim-common package.
%endif

%define localedir %{buildroot}%{_datadir}/locale/

%prep
%setup -q -b 2 -n vim71 -a4
# spec plugin
rm -f runtime/doc/pi_spec.txt
rm -f runtime/ftpplugin/spec.vim
tar xfj %SOURCE5 -C runtime
cp -a %SOURCE6 runtime/syntax/
cp -a %SOURCE7 runtime/syntax/
#official patches
for i in vim-%version.%{official_ptchlvl}-patches/%{version}*; do
    patch -p0 -s < $i
done

#mdk patches
%patch0 -p1 -b .vimrc_nosetmouse
%patch2 -p1
%patch3 -p0 -b .spec
%patch8 -p1 -b .manpath
%patch10 -p1 -b .xxdloc
%patch11 -p1 -b .gcc31
%patch20 -p1 -b .warly
%patch22 -p0
%patch23 -p0 -b .doc
%patch24 -p0
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p0
%patch30 -p0
%patch32 -p1 -b .lzma_support
%patch33 -p1 -b .fortify_overflow

perl -pi -e 's|SYS_VIMRC_FILE "\$VIM/vimrc"|SYS_VIMRC_FILE "%_sysconfdir/vim/vimrc"|' src/os_unix.h
perl -pi -e 's|SYS_GVIMRC_FILE "\$VIM/gvimrc"|SYS_GVIMRC_FILE "%_sysconfdir/vim/gvimrc"|' src/os_unix.h
# disable command echo
for i in runtime/{gvimrc_example.vim,vimrc_example.vim}; do
    perl -pi -e 's!^set showcmd!set noshowcmd!' $i
done
perl -pi -e 's|\Qsvn-commit.*.tmp\E|svn-commit*.tmp|'       ./runtime/filetype.vim

%build

%if %buildgui
# First build: gvim
LOCALEDIR=%localedir CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%_prefix \
--enable-pythoninterp \
--enable-perlinterp \
--enable-rubyinterp \
--enable-tclinterp \
--with-features=huge \
--enable-acl --with-x=yes --enable-gui=gnome2 --exec-prefix=%_prefix/X11R6 \
--enable-gtk2-check \
--enable-multibyte --enable-xim --enable-fontset --mandir=%_mandir \
--libdir=%_libdir --with-compiledby="%packager"
 
echo "#define MAX_FEAT 1" >> src/config.h
echo "#define FEAT_GUI" >> src/config.h
# workaround buggy build system:
perl -pi -e 's!/usr/include long!/usr/include !' src/auto/config.mk

%make
mv src/vim src/gvim
make -C src clean
%endif

# Second build: vim-enhanced
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"  ./configure --prefix=%_prefix \
--enable-acl --enable-pythoninterp --enable-perlinterp --with-features=huge \
--libdir=%_libdir --with-compiledby="%packager" \
--with-x=no --enable-gui=no --exec-prefix=%_prefix

%make
mv src/vim src/vim-enhanced
make -C src/ clean

# Third build: vim-minimal
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./configure  --prefix=%_prefix \
--with-features=tiny --disable-tclinterp --disable-cscope --disable-multibyte \
--disable-hangulinput --disable-xim --disable-fontset --disable-gui \
--disable-acl --disable-pythoninterp --disable-perlinterp \
--libdir=%_libdir --with-compiledby="%packager" \
--with-x=no --enable-gui=no --exec-prefix=%_prefix --with-tlib=termcap --disable-gpm

%make
cp src/vim src/vim-minimal
%make -C src

cp -al runtime/doc doc
# apply os_doc.diff
pushd doc
rm -f *.1
rm -f os_{390,dos,msdos,risc,win32,amiga,mac,os2,beos,mint,qnx,vms}.txt
rm -f gui_{w16,w32}.txt
rm -f vim2html.pl Makefile *awk
popd

# britton support
ln -s tutor.fr runtime/tutor/tutor.br
ln -s menu_fr_fr.iso_8859-15.vim runtime/lang/menu_br

%install
rm -fr %{buildroot}

[ ! -e mandrake ] && mv vim-%version.%{official_ptchlvl}-patches mandrake

perl -pi -e 's!LOCALEDIR=\$\(DEST_LANG\)!LOCALEDIR=\$(DESTDIR)\$\(prefix\)/share/locale!g' src/Makefile

mkdir -p %{buildroot}{/bin,%_bindir,%_datadir/{vim,locale},%_mandir/man1,%localedir}
%makeinstall_std VIMRTDIR=""


make -C src installmacros prefix=%{buildroot}%_prefix VIMRTDIR=""

%if %buildgui
mkdir -p %{buildroot}%_bindir
install -s -m 755 src/gvim %{buildroot}%_bindir
%endif

install -s -m 755 src/vim-enhanced %{buildroot}%_bindir
install -s -m 755 src/vim-minimal %{buildroot}/bin/vim-minimal

cd %{buildroot}
rm -f ./bin/rvim
for i in ex vimdiff; do
    ln -sf vim-enhanced ./usr/bin/$i
done
rm -f ./usr/man/man1/rvim.*
%if %buildgui
ln -sf gvim ./usr/bin/gvimdiff
ln -sf gvim ./usr/bin/vimx
%endif
cd -

# installing man pages
for i in %{buildroot}%_mandir/man1/{vi,rvi}; do
    cp %{buildroot}%_mandir/man1/vim.1 $i.1
done

%if %buildgui
cp %{buildroot}%_mandir/man1/vim.1 %{buildroot}%_mandir/man1/gvim.1
%endif

ln -sf vimrc_example.vim %{buildroot}/usr/share/vim/vimrc

cd %{buildroot}/%_prefix/share/vim/tools
# i need to make a choice :(.
rm -f vim132
perl -p -i -e 's|#!/usr/bin/nawk|#!/usr/bin/gawk|' mve.awk
perl -p -i -e 's|#!/usr/local/bin/perl|#!/usr/bin/perl|' *.pl
perl -p -i -e 's|#!/usr/gnu/bin/perl|#!/usr/bin/perl|' *
cd -
 
# Be short-circuit aware :
ln -f runtime/macros/README.txt README_macros.txt
ln -f runtime/tools/README.txt README_tools.txt
perl -p -i -e "s|#!/usr/local/bin/perl|#!/usr/bin/perl|" runtime/doc/*.pl

# installing the menu icons & entry
%if %buildgui
mkdir -p %{buildroot}{%_miconsdir,%_liconsdir,%_menudir}
cp runtime/vim16x16.png %{buildroot}%_miconsdir/gvim.png
cp runtime/vim32x32.png %{buildroot}%_iconsdir/gvim.png
cp runtime/vim48x48.png %{buildroot}%_liconsdir/gvim.png

# menu entry
install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}-X11.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/gvim -f
Icon=gvim
Terminal=false
Type=Application
StartupNotify=false
Categories=Gtk;X-MandrivaLinux-MoreApplications-Editors;TextEditor;
MimeType=text/plain
EOF

# gvim and fontset (from Pablo) 2001/03/19
echo 'set guifontset=-*-fixed-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-m-*-*-*,*' > %{buildroot}%{_datadir}/vim/gvimrc
%endif

# fix the paths in the man pages
for i in %{buildroot}/usr/share/man/man1/*.1; do
    perl -p -i -e "s|%{buildroot}||" $i
done

# prevent including twice the doc
rm -fr %{buildroot}/usr/share/vim/doc
ln -sf ../../../%_defaultdocdir/%name-common/doc %{buildroot}/usr/share/vim/doc

# symlink locales in right place so that %find_land put needed %lang:
# see %pre common why this is needed
pushd %{buildroot}/%_datadir/vim/lang
    ln -s ../../locale/* .
popd

%{find_lang} %name

find %{buildroot}%_datadir/vim/ -name "tutor.*" | egrep -v 'tutor(|\.vim)$' |
 sed -e "s^%{buildroot}^^" -e 's!^\(.*tutor.\)\(..\)!%lang(\2) \1\2!g' >> %name.lang

find %{buildroot}%_datadir/vim/ -name "menu*" |
 sed -e "s^%{buildroot}^^" -e 's!^\(.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
  -e 's!^\(.*menu\)\(_chinese\)!%lang(zh) \1\2!g' \
  -e 's!^\(.*menu\)\(_czech_\)!%lang(cs) \1\2!g' \
  -e 's!^\(.*menu\)\(_french\)!%lang(fr) \1\2!g' \
  -e 's!^\(.*menu\)\(_german\)!%lang(de) \1\2!g' \
  -e 's!^\(.*menu\)\(_japanes\)!%lang(ja) \1\2!g' \
  -e 's!^\(.*menu\)\(_polish\)!%lang(pl) \1\2!g' \
  -e 's!^\(.*menu\)\(_slovak\)!%lang(sk) \1\2!g' \
  -e 's!^\(.*menu\)\(_spanis\)!%lang(es) \1\2!g' \
  >> %name.lang
rm -f %{buildroot}%_bindir/vim

mkdir -p %{buildroot}/%_sysconfdir/vim/
MESSAGE='"Place your systemwide modification here.\n"%_datadir/vim/ files will be overwritten on update\n'
echo -e "$MESSAGE\nsource %_datadir/vim/vimrc" > %{buildroot}/%_sysconfdir/vim/vimrc
%if %buildgui
echo -e "$MESSAGE\nsource %_datadir/vim/gvimrc" > %{buildroot}/%_sysconfdir/vim/gvimrc
%endif

%pre common
# This is needed since locales have been moved to /usr/share/locale
# thus enabling us to install only requested locales
# the problem is that vim look for anything in %_datadir/vim/lang
# So we've to symlink locales there
# But to prevent update faillure, we must first be sure a link
# creation won't fail because old directory is still there
if test -d %_datadir/vim/lang -a ! -L %_datadir/vim/lang
then rm -fr %_datadir/vim/lang
else rm -f %_datadir/vim/lang
fi

%post minimal
update-alternatives --install /usr/bin/vi uvi /bin/vim-minimal 10
update-alternatives --install /bin/vi     vi  /bin/vim-minimal 10
update-alternatives --install /bin/vim    vim /bin/vim-minimal 10
for i in view ex rvi rview rvim; do
    update-alternatives --install /bin/$i $i /bin/vi 10 || :
done
:

%postun minimal
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-minimal
update-alternatives --remove vi  /bin/vim-minimal
update-alternatives --remove vim /bin/vim-minimal

for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done

:

%triggerpostun -n vim-minimal -- vim-minimal < 6.1-22mdk
for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done

:


%post enhanced
update-alternatives --install /usr/bin/vi uvi /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vi  vi     /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vim vim    /usr/bin/vim-enhanced 20
:

%postun enhanced
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-enhanced
update-alternatives --remove vi  /usr/bin/vim-enhanced
update-alternatives --remove vim /usr/bin/vim-enhanced
:
%if %buildgui
# menu stuff
%post X11
%{update_menus}
%{update_desktop_database}

%postun X11
%{clean_menus}
%{clean_desktop_database}
%endif

%clean
rm -rf %{buildroot}

%files common -f vim.lang
%defattr(-,root,root)
%doc README*.txt runtime/termcap
%doc --parents mandrake/README*
%doc doc
%_datadir/vim/doc


%dir %_datadir/vim/
%_datadir/vim/[^g]*
%_datadir/vim/gvimrc_example.vim
%_mandir/man1/vim.1*
%_mandir/man1/ex.1*
%_mandir/man1/vi.1*
%_mandir/man1/view.1*
%_mandir/man1/rvi.1*
%_mandir/man1/rview.1*
%_mandir/man1/vimdiff.1*
%_mandir/man1/vimtutor.1*
%_mandir/man1/rvim.1*
%_mandir/*/man*/*
%lang(fr) %_mandir/fr*/man*/*
%lang(it) %_mandir/it*/man*/*
%lang(pl) %_mandir/pl*/man*/*
%lang(ru) %_mandir/ru*/man*/*
%exclude %_mandir/man1/evim.1*
%exclude %_bindir/rview
%exclude %_bindir/rvim
%exclude %_bindir/view
%_bindir/vimtutor
%_bindir/xxd
%_mandir/man1/xxd.1*
%_sysconfdir/vim/
%config(noreplace) %_sysconfdir/vim/*

%files minimal
%defattr(-,root,root)
%doc README*.txt
/bin/vim-minimal

%files enhanced
%defattr(-,root,root)
%doc README*.txt
%_bindir/ex
%_bindir/vimdiff
%_bindir/vim-enhanced

%if %buildgui
%files X11
%defattr(-,root,root)
%doc README*.txt
%_bindir/gvim
%_bindir/gvimdiff
%_bindir/vimx
%_mandir/man1/gvim.1*
%_iconsdir/gvim.png
%_miconsdir/gvim.png
%_liconsdir/gvim.png
%_datadir/applications/mandriva-%{name}-X11.desktop
%_datadir/vim/gvimrc
%endif


