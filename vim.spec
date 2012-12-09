# Notes / Warning :
# - this package is not prefixable
# - to update official patches, aka SOURCE4, see README.upstream_patches in SOURCE4

%define url ftp://ftp.vim.org/pub/vim/unix/
%define official_ptchlvl 646
%define rversion	7.3

# Should we build X11 gui
%bcond_without gui
%bcond_with	python3

%define	title		VI editor
%define longtitle	All-purpose text editor

Name:		vim
Version:	%{rversion}.%{official_ptchlvl}
Release:	2
Summary:	VIsual editor iMproved
Url:		http://www.vim.org/
License:	Charityware
Group:		Editors
Source0:	%{url}/%{name}-%{rversion}.tar.bz2
# read README.mdv prior updating official patches:
Source3:	README.mdv
Source4:	vim-%{rversion}-patches.tar.xz
# http://vim.sourceforge.net/scripts/script.php?script_id=98
Source5:	vim-spec-3.0.bz2
Source6:	http://trific.ath.cx/Ftp/vim/syntax/dhcpd.vim
# from apparmor-utils package
Source7:	apparmor.vim
Source8:	cfengine.vim
Source9:	nagios.vim
# MDK patches
Patch0:		vim-7.2-vimrc_nosetmouse.patch
Patch2:		vim-5.6a-paths.patch
Patch3:		vim-7.3.478-rpm-spec-syntax.patch
Patch8:		vim-6.0af-man-path.patch
Patch10:	xxd-locale.patch
Patch20:	vimrc_hebrew.patch
Patch22:	vim-6.1-fix-xterms-comments.patch
Patch23:	vim-6.3-remove-docs.patch
Patch24:	vim-6.1-outline-mode.patch
Patch25:	vim-6.1-xterm-s-insert.patch
Patch26:	vim-7.0-changelog-mode.patch
Patch27:	vim-6.1-rpm42.patch
Patch28:	vim-7.3-po-mode.patch
Patch30:	vim-7.3.478-add-dhcpd-syntax.patch
Patch33:	vim-7.1.314-CVE-2009-0316-debian.patch
# (proyvind): adds various new keywords from C++11 standard to C++ syntax highlighting
Patch34:	vim-7.3.372-add-new-cpp11-keywords-to-cpp-syntax.patch
# (proyvind): fix path to locale files
Patch35:	vim-7.3.372-use-proper-localedir.patch
Patch36:	vim-7.3.372-add-missing-functions-for-ruby-dlopen.patch
Patch37:	vim-7.3.381-always-install-icons.patch
Patch38:	vim-7.3.478-dont-check-for-xsetlocale.patch

# Fedora patches
Patch100:	vim-7.0-fortify_warnings-1.patch
Patch101:	vim-7.3-fstabsyntax.patch

BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(python)
%if %{with python3}
BuildRequires:	pkgconfig(python3)
%endif
BuildRequires:	perl-devel
BuildRequires:	acl-devel
%if %{with gui}
BuildRequires:	pkgconfig(libgnomeui-2.0) pkgconfig(ncurses)
BuildRequires:	pkgconfig(xt)
BuildRequires:	tcl
BuildRequires:	tcl-devel
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-common package
contains files which every VIM binary will need in order to run.

%package	common
Summary:	The common files needed by any version of the VIM editor
Group:		Editors
Conflicts:	man-pages-fr < 1.68.0-2mdk
Conflicts:	man-pages-it < 0.3.4-2mdk
Conflicts:	man-pages-pl <= 0.4-10mdk
Conflicts:	git-core < 1:1.6.0.1-2mdv
Requires:   update-alternatives

%description	common
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-common package
contains files which every VIM binary will need in order to run.

%package	minimal
Summary:	A minimal version of the VIM editor
Group:		Editors
Provides:	vim
Requires:	update-alternatives

%description	minimal
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-minimal package
includes a minimal version of VIM, which is installed into /bin/vi for use
when only the root partition is present.

%package	enhanced
Summary:	A version of the VIM editor which includes recent enhancements
Group:		Editors
Requires:	vim-common >= %{EVRD}
Obsoletes:	vim-color
Provides:	vim
Provides:	vim-color

%description	enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-enhanced package
contains a version of VIM with extra, recently introduced features like
Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the VIM
editor which includes recently added enhancements like interpreters for the
Python and Perl scripting languages. You'll also need to install the
vim-common package.

%if %{with gui}
%package	X11
Summary:	The VIM version of the vi editor for the X Window System
Group:		Editors
Provides:	vim
Requires:	vim-common >= %{EVRD}

%description	X11
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. VIM-X11 is a version of the
VIM editor which will run within the X Window System. If you install this
package, you can run VIM as an X application with a full GUI interface and
mouse support.

Install the vim-X11 package if you'd like to try out a version of vi with
graphics and mouse capabilities. You'll also need to install the
vim-common package.
%endif

%prep
%setup -q -n vim73 -a4
# spec plugin
rm -f runtime/doc/pi_spec.txt
rm -f runtime/ftpplugin/spec.vim
tar xfj %{SOURCE5} -C runtime
cp -a %{SOURCE6} runtime/syntax/
cp -a %{SOURCE7} runtime/syntax/
cp -a %{SOURCE8} runtime/syntax/
cp -a %{SOURCE9} runtime/syntax/
#pushd vim-%{rversion}-patches
#md5sum -c MD5SUMS
#popd
#official patches
for i in `seq -f '%03g' 1 %{official_ptchlvl}`; do
	p=vim-%{rversion}-patches/%{rversion}.$i
	cmd="patch -p0 %{_default_patch_flags} -i $p"
	echo $cmd
	$cmd || { echo $p; exit 1; }
done

#mdk patches
%patch0 -p1 -b .vimrc_nosetmouse
%patch2 -p1
%patch3 -p1 -b .spec~
%patch8 -p1 -b .manpath
%patch10 -p1 -b .xxdloc
%patch20 -p1 -b .warly
%patch22 -p0
%patch23 -p0 -b .doc
%patch24 -p0
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p1
%patch30 -p1
%patch33 -p1 -b .security
%patch34 -p1 -b .cpp11~
%patch35 -p1 -b .localedir~
%patch36 -p1 -b .dlopen~
%patch37 -p1 -b .icons_install~
%patch38 -p1 -b .xsetlocale~

# Fedora patches
%patch100 -p1
%patch101 -p1

perl -pi -e 's|SYS_VIMRC_FILE "\$VIM/vimrc"|SYS_VIMRC_FILE "%{_sysconfdir}/vim/vimrc"|' src/os_unix.h
perl -pi -e 's|SYS_GVIMRC_FILE "\$VIM/gvimrc"|SYS_GVIMRC_FILE "%{_sysconfdir}/vim/gvimrc"|' src/os_unix.h
# disable command echo
for i in runtime/{gvimrc_example.vim,vimrc_example.vim}; do
	 perl -pi -e 's!^set showcmd!set noshowcmd!' $i
done
perl -pi -e 's|\Qsvn-commit.*.tmp\E|svn-commit*.tmp|' ./runtime/filetype.vim
cd src
autoconf

%build
%if %{with gui}
# First build: gvim
%configure2_5x \
	--disable-darwin \
	--disable-selinux \
	--disable-xsmp \
	--disable-xsmp-interact \
	--enable-luainterp=dynamic \
	--enable-mzschemeinterp=no \
	--enable-perlinterp=dynamic \
	--enable-pythoninterp=dynamic \
	--enable-python3interp=dynamic \
	--enable-tclinterp=dynamic \
	--enable-rubyinterp=dynamic \
	--disable-cscope \
	--disable-workshop \
	--enable-netbeans \
	--disable-sniff \
	--enable-multibyte \
	--disable-hangulinput \
	--enable-xim \
	--enable-fontset \
	--with-features=huge \
	--enable-gui=gnome2 \
	--with-tlib=ncurses \
	--enable-gtk2-check \
	--enable-gnome-check \
	--enable-acl \
	--enable-gpm \
	--disable-sysmouse \
	--enable-nls \
	--with-x=yes \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="%{packager}"

%make
mv src/vim src/gvim
make -C src clean
%endif

# Second build: vim-enhanced
%configure2_5x \
	--disable-selinux \
	--enable-acl \
	--enable-luainterp=dynamic \
	--enable-perlinterp=dynamic \
	--enable-pythoninterp=dynamic \
	--enable-python3interp=dynamic \
	--enable-tclinterp=dynamic \
	--enable-rubyinterp=dynamic \
	--with-features=huge \
	--with-x=no \
	--enable-gui=no \
	--with-tlib=ncurses \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="%{packager}"

%make
mv src/vim src/vim-enhanced
make -C src/ clean

# Third build: vim-minimal
%configure2_5x \
	--disable-selinux \
	--with-features=tiny \
	--disable-tclinterp \
	--disable-cscope \
	--enable-multibyte \
	--disable-hangulinput \
	--disable-xim \
	--disable-fontset \
	--disable-gui \
	--disable-acl \
	--disable-pythoninterp \
	--disable-perlinterp \
	--with-x=no \
	--enable-gui=no \
	--with-tlib=ncurses \
	--disable-gpm \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="%{packager}"

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
%makeinstall_std VIMRTDIR=""


make -C src installmacros prefix=%{buildroot}%{_prefix} VIMRTDIR=""

%if %{with gui}
install -m755 src/gvim -D %{buildroot}%{_bindir}/gvim
%endif

install -m755 src/vim-enhanced -D %{buildroot}%{_bindir}
install -m755 src/vim-minimal -D %{buildroot}/bin/vim-minimal

rm -f %{buildroot}%{_bindir}/{rview,rvim,view}
for i in ex vimdiff; do
  ln -sf vim-enhanced %{buildroot}%{_bindir}/$i
done
rm -f %{buildroot}%{_mandir}/man1/evim.*
%if %{with gui}
ln -sf gvim %{buildroot}%{_bindir}/gvimdiff
ln -sf gvim %{buildroot}%{_bindir}/vimx
%endif
rm -f %{buildroot}%{_datadir}/vim/*/cmake.vim

# installing man pages
for i in %{buildroot}%{_mandir}/man1/{vi,rvi}; do
  ln -s vim.1%{_extension} $i.1%{_extension}
done

%if %{with gui}
ln -s vim.1%{_extension} %{buildroot}%{_mandir}/man1/gvim.1%{_extension}
%endif

ln -sf vimrc_example.vim %{buildroot}%{_datadir}/vim/vimrc

# Be short-circuit aware :
ln -f runtime/macros/README.txt README_macros.txt
ln -f runtime/tools/README.txt README_tools.txt

# installing the menu icons & entry
%if %{with gui}
# menu entry
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-X11.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/gvim -f
Icon=gvim
Terminal=false
Type=Application
StartupNotify=false
Categories=Gtk;TextEditor;Utility;
MimeType=text/plain;
EOF

# gvim and fontset (from Pablo) 2001/03/19
echo 'set guifontset=-*-fixed-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-m-*-*-*,*' > %{buildroot}%{_datadir}/vim/gvimrc
%else
rm -rf %{buildroot}%{_iconsdir}
%endif

# prevent including twice the doc
rm -rf %{buildroot}%{_datadir}/vim/doc
ln -s %{_defaultdocdir}/%{name}-common/doc %{buildroot}%{_datadir}/vim/doc

%{find_lang} %{name} --with-man --all-name

find %{buildroot}%{_datadir}/vim/tutor -name "tutor.*" | grep -v -E 'tutor(|\.vim)$' |
 sed -e "s^%{buildroot}^^" -e 's!^\(.*tutor.\)\(..\)!%lang(\2) \1\2!g' >> %{name}.lang

find %{buildroot}%{_datadir}/vim/lang -name "menu*" |
 sed -e "s^%{buildroot}^^" \
  -e 's!^\(/.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
  -e 's!^\(/.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
  -e 's!^\(/.*menu\)\(_chinese\)!%lang(zh) \1\2!g' \
  -e 's!^\(/.*menu\)\(_czech_\)!%lang(cs) \1\2!g' \
  -e 's!^\(/.*menu\)\(_french\)!%lang(fr) \1\2!g' \
  -e 's!^\(/.*menu\)\(_german\)!%lang(de) \1\2!g' \
  -e 's!^\(/.*menu\)\(_japanes\)!%lang(ja) \1\2!g' \
  -e 's!^\(/.*menu\)\(_polish\)!%lang(pl) \1\2!g' \
  -e 's!^\(/.*menu\)\(_slovak\)!%lang(sk) \1\2!g' \
  -e 's!^\(/.*menu\)\(_spanis\)!%lang(es) \1\2!g' \
  -e 's!^\(/.*menu_\)\(..\)!%lang(\2) \1\2!g' \
  >> %{name}.lang
rm -f %{buildroot}%{_bindir}/vim

mkdir -p %{buildroot}%{_sysconfdir}/vim/
MESSAGE='"Place your systemwide modification here.\n"%{_datadir}/vim/ files will be overwritten on update\n'
echo -e "$MESSAGE\nsource %{_datadir}/vim/vimrc" > %{buildroot}%{_sysconfdir}/vim/vimrc
%if %{with gui}
echo -e "$MESSAGE\nsource %{_datadir}/vim/gvimrc" > %{buildroot}%{_sysconfdir}/vim/gvimrc
%endif

%post minimal
update-alternatives --install /bin/vi vi /bin/vim-minimal 10 \
    --slave /bin/view view /bin/vim-minimal \
    --slave /bin/ex ex /bin/vim-minimal \
    --slave /bin/rvi rvi /bin/vim-minimal \
    --slave /bin/rview rview /bin/vim-minimal
update-alternatives --install /bin/vim vim /bin/vim-minimal 10 \
    --slave /bin/rvim rvim /bin/vim-minimal

%postun minimal
[ $1 = 0 ] || exit 0
update-alternatives --remove vi /bin/vim-minimal
update-alternatives --remove vim /bin/vim-minimal

%triggerpostun minimal -- vim-minimal < 7.3
update-alternatives --remove uvi /bin/vim-minimal
for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done

%post enhanced
update-alternatives --install /bin/vi vi /usr/bin/vim-enhanced 20 \
    --slave /bin/view view /usr/bin/vim-enhanced \
    --slave /bin/ex ex /usr/bin/vim-enhanced \
    --slave /bin/rvi rvi /usr/bin/vim-enhanced \
    --slave /bin/rview rview /usr/bin/vim-enhanced
update-alternatives --install /bin/vim vim /usr/bin/vim-enhanced 20 \
    --slave /bin/rvim rvim /usr/bin/vim-enhanced

%postun enhanced
[ $1 = 0 ] || exit 0
update-alternatives --remove vi /usr/bin/vim-enhanced
update-alternatives --remove vim /usr/bin/vim-enhanced

%triggerpostun enhanced -- vim-enhanced < 7.3
update-alternatives --remove uvi /usr/bin/vim-enhanced

%files common -f vim.lang
%doc README*.txt runtime/termcap
#%doc --parents mandriva/README*
%doc doc

%dir %{_datadir}/vim/
%{_datadir}/vim/autoload
%{_datadir}/vim/colors
%{_datadir}/vim/compiler
%{_datadir}/vim/doc
%{_datadir}/vim/ftplugin
%{_datadir}/vim/indent
%{_datadir}/vim/keymap
%dir %{_datadir}/vim/lang
%{_datadir}/vim/lang/README.txt
%{_datadir}/vim/macros
%{_datadir}/vim/plugin
%{_datadir}/vim/print
%{_datadir}/vim/spell
%{_datadir}/vim/syntax
%{_datadir}/vim/tools
%dir %{_datadir}/vim/tutor
%{_datadir}/vim/tutor/*.txt
%{_datadir}/vim/tutor/tutor
%{_datadir}/vim/tutor/tutor.vim
%{_datadir}/vim/*.vim
%{_datadir}/vim/vimrc
%{_mandir}/man1/vim.1*
%{_mandir}/man1/ex.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%{_mandir}/man1/rvi.1*
%{_mandir}/man1/rview.1*
%{_mandir}/man1/vimdiff.1*
%{_mandir}/man1/vimtutor.1*
%{_mandir}/man1/rvim.1*
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/man1/xxd.1*
%dir %{_sysconfdir}/vim/
%config(noreplace) %{_sysconfdir}/vim/*

%files minimal
%doc README*.txt
/bin/vim-minimal

%files enhanced
%doc README*.txt
%{_bindir}/ex
%{_bindir}/vimdiff
%{_bindir}/vim-enhanced

%if %{with gui}
%files X11
%doc README*.txt
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/vimx
%{_mandir}/man1/gvim.1*
%{_iconsdir}/locolor/16x16/apps/gvim.png
%{_iconsdir}/locolor/32x32/apps/gvim.png
%{_iconsdir}/hicolor/48x48/apps/gvim.png
%{_datadir}/applications/mandriva-%{name}-X11.desktop
%{_datadir}/vim/gvimrc
%endif


%changelog
* Thu Aug 30 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.646-1
+ Revision: 816059
- Revert 7.3.640 patch to original format (because there is binary patch)
- 7.3.646

* Fri Aug 24 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.638-1
+ Revision: 815657
- 7.3.638

* Thu Aug 23 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.635-1
+ Revision: 815636
- 7.3.635

* Wed Aug 22 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.633-1
+ Revision: 815595
- 7.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.6337.3.633

* Thu Aug 16 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.632-1
+ Revision: 814932
- 7.3.632

* Tue Aug 14 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.629-1
+ Revision: 814767
- 7.3.629

* Mon Jul 30 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.618-1
+ Revision: 811398
- 7.3-618

* Thu Jul 26 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.615-1
+ Revision: 811118
- 7.3-615

* Fri Jul 20 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.608-1
+ Revision: 810347
- 7.3-608

* Thu Jul 19 2012 Lonyai Gergely <aleph@mandriva.org> 7.3.605-1
+ Revision: 810271
- 7.3-605

* Thu Mar 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.3.486-1
+ Revision: 788118
- fix messed up description
- update to latest patches
- add syntax highlightning for %%triggerposttransin & %%triggerposttransun
- fix deprecated-grep
- drop dead patch that disables forking
- update rpm syntax highlightning (P3)
- remove *ancient* check for _Xsetlocale() which for some reason tests positive
  and breaks gvim (P38)
- update to latest patch level
- verify md5sum of official patches

  + Lonyai Gergely <aleph@mandriva.org>
    - 7.3-434
    - 7.3-429

* Tue Jan 24 2012 Bogdano Arendartchuk <bogdano@mandriva.com> 7.3.381-2
+ Revision: 767988
- rebuld for newer perl

* Wed Dec 14 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.3.381-1
+ Revision: 741373
- make python3 a conditional, disabled by default untill available in main...
- make sure to disable selinux on both minimal & enhanced builds as well
- fix icons to be installed during 'make install' (P37)
- update patch level to 381
- make patch level patching a bit spiffier
- fix language files missing %%lang attribute
- fix install of locale files as well
- symlink man pages to vim.1 rather than making copies
- don't strip binaries when installing them
- use bcond for gui build conditional
- clean up and apply some cosmetics :)
- remove some dead hacks
- switch to use ncurses as terminal library for minimal package as well, it'll
  be pulled in by other packages anyways, so linking against termcap in stead
  won't save us anything
- enable multibyte support for minimal build
- change to --with-compiled-by="%%{vendor} %%{bugurl}" and add
--with-modified-by="%%{packager}"
- add missing functions for dlopen() of ruby interpreter (P36), and enable it
- add missing buildrequires for python3, enabling it's suppport as intended
- dynamically load interpreters (except for ruby, needs a couple of fixes)
- use %%configure2_5x macro
- fix localedir location properly in the source rather than working around it
  with dirty symlink hack (P35)
- fix duplicates in %%files
- no need to pass '-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64' manually anymore,
  configure script checks for necessity and takes care of passing it
- drop deprecated rpm stuff
- drop redundant dependency on perl-base
- drop useless version macros for perl, python & ruby
- update rpm spec syntax patch
- adds various new keywords from C++11 standard to C++ syntax highlighting (P34)
- remove obsolete scripts for no longer supported releases
- use pkgconfig(foo) buildrequires where available

* Mon Dec 12 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.372-1
+ Revision: 740589
- 7.3-372

* Thu Nov 17 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.353-1
+ Revision: 731486
- 7.3-353

* Mon Oct 17 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.338-1
+ Revision: 705051
- 7.3-338

* Thu Sep 22 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.322-1
+ Revision: 700889
- Drop the nofork patch in Cooker
- 7.3-322

* Mon Aug 22 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.285-1
+ Revision: 696077
- 7.3-285

* Thu Aug 18 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.284-1
+ Revision: 695137
- 7.3-284

* Wed Aug 17 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.281-1
+ Revision: 695015
- 7.3-281

* Fri Aug 12 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.280-1
+ Revision: 694146
- 7.3-280
- Add some missing vim patch

* Thu Jul 28 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.266-1
+ Revision: 692116
- 7.3-266

* Wed Jul 13 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.244-1
+ Revision: 689816
- 7.3-244

* Mon Jun 27 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.237-1
+ Revision: 687419
- 7.3-237
  Small changes in Makefile (bugfixes)
  Redownload the 7.3-* patches and use the rereleased patches.
  Drop the complemented doc/*.txt files.

* Mon Jun 20 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.230-1
+ Revision: 686110
- 7.3-230
  Official patch: the 223 patch is wrong. I dropped one comment line.
  nofork.patch rediffed

* Tue Jun 14 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.219-1
+ Revision: 684985
- Add lua dependency
- 7.3-219

* Fri Jun 03 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.206-1
+ Revision: 682633
- 7.3-206

* Wed May 25 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.201-1
+ Revision: 678988
- 7.3-201

* Mon May 16 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.189-1
+ Revision: 675004
- 7.3-189

* Tue Apr 05 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.154-1
+ Revision: 650605
- rediff xxd-locale.patch
- 7.3.154

* Wed Mar 30 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.146-1
+ Revision: 649049
- 7.3-146
  Remove some old patch

* Wed Mar 16 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.138-1
+ Revision: 645626
- 7.3-138

* Mon Feb 28 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.135-1
+ Revision: 640865
- 7.3.135

* Thu Feb 24 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.125-1
+ Revision: 639637
- 7.3.125
  "Recreate" the patch creator system
  Add the official patches to svn

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 7.3.107-2
+ Revision: 637130
- rebuild

* Tue Feb 01 2011 Lonyai Gergely <aleph@mandriva.org> 7.3.107-1
+ Revision: 634609
- 7.3.107

* Tue Jan 11 2011 Guillaume Rousse <guillomovitch@mandriva.org> 7.3.099-1
+ Revision: 630888
- update to patch level 099

* Sun Oct 31 2010 Ahmad Samir <ahmadsamir@mandriva.org> 7.3.003-3mdv2011.0
+ Revision: 590970
- manually delete unpackaged files due to change in %%exclude behaviour

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Tue Sep 07 2010 Ahmad Samir <ahmadsamir@mandriva.org> 7.3.003-2mdv2011.0
+ Revision: 576664
- rebuild for perl 5.12.2

* Thu Aug 26 2010 Thierry Vignaud <tv@mandriva.org> 7.3.003-1mdv2011.0
+ Revision: 573427
- bump to official patchlevel 003

* Fri Aug 20 2010 Guillaume Rousse <guillomovitch@mandriva.org> 7.3.0-1mdv2011.0
+ Revision: 571548
- fix alternative mess (#28869):
- drop uvi alternative, there isn't any such command
- ensure rvi, view, ex, ... are slaves from master vi alternative
- ensure rvim is slaves from master vim alternative
- rename README.mdk into README.mdv, and drop unrelated bash-completion content
- new version
- drop perl 5.10 syntax patch (uneeded anymore)
- rediff po-mode and fstabsyntax patches

  + Anssi Hannula <anssi@mandriva.org>
    - move dependency on perl-common from vim-common into vim-enhanced and
      vim-X11 as the dependency is in the binaries themselves (fixes vim
      startup during upgrade)

* Tue Jul 27 2010 Jérôme Quelin <jquelin@mandriva.org> 7.2.446-4mdv2011.0
+ Revision: 562081
- perl 5.12.1 rebuild

* Sun Jul 25 2010 Thierry Vignaud <tv@mandriva.org> 7.2.446-3mdv2011.0
+ Revision: 558321
- drop patch 32 (lzma support was merged upstream and this one was just breaking stuff)

* Thu Jul 22 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 7.2.446-2mdv2011.0
+ Revision: 556718
- Rebuild vim

* Tue Jul 20 2010 Thierry Vignaud <tv@mandriva.org> 7.2.446-1mdv2011.0
+ Revision: 556286
- bump to official patchlevel 446
- rediff a couple patches
- drop patch 102 (merged upstream)

* Tue Jul 20 2010 Jérôme Quelin <jquelin@mandriva.org> 7.2.284-6mdv2011.0
+ Revision: 555416
- rebuild for perl 5.12

* Wed Mar 31 2010 Funda Wang <fwang@mandriva.org> 7.2.284-5mdv2010.1
+ Revision: 530157
- fix desktop file

  + Jérôme Quelin <jquelin@mandriva.org>
    - rebuild for main/testing

* Thu Jan 07 2010 Anssi Hannula <anssi@mandriva.org> 7.2.284-3mdv2010.1
+ Revision: 487277
- add release on requires on vim-common in vim-enhanced and vim-X11, as
  the vim-enhanced and vim-X11 binaries contain a version-specific
  dependency on perl, which is pulled in by vim-common; thus it is
  required to have them in sync (fixes unavailable vim during upgrade)

  + Thierry Vignaud <tv@mandriva.org>
    - rename mandrake directory as mandriva (#25692)

* Tue Nov 10 2009 Michael Scherer <misc@mandriva.org> 7.2.284-2mdv2010.1
+ Revision: 463902
- add highlighting for Suggests: keyword

* Mon Nov 09 2009 Thierry Vignaud <tv@mandriva.org> 7.2.284-1mdv2010.1
+ Revision: 463787
- new release

* Fri Sep 18 2009 Thierry Vignaud <tv@mandriva.org> 7.2.259-1mdv2010.0
+ Revision: 444368
- bump to official patchlevel 259

* Tue Aug 25 2009 Michael Scherer <misc@mandriva.org> 7.2.245-3mdv2010.0
+ Revision: 420658
- rebuild for new perl

* Mon Aug 24 2009 Götz Waschk <waschk@mandriva.org> 7.2.245-2mdv2010.0
+ Revision: 420636
- perl rebuild

* Thu Aug 13 2009 Thierry Vignaud <tv@mandriva.org> 7.2.245-1mdv2010.0
+ Revision: 416035
- bump to official patchlevel 245

  + Michael Scherer <misc@mandriva.org>
    - add version of the GPL to the syntax highlighter for spec file

* Wed Jul 29 2009 Thierry Vignaud <tv@mandriva.org> 7.2.239-1mdv2010.0
+ Revision: 402932
- bump to official patchlevel 239

* Mon May 25 2009 Thierry Vignaud <tv@mandriva.org> 7.2.188-1mdv2010.0
+ Revision: 379502
- bump to official patchlevel 188

* Tue May 12 2009 Thierry Vignaud <tv@mandriva.org> 7.2.166-1mdv2010.0
+ Revision: 374905
- bump to official patchlevel 166

* Wed Mar 04 2009 Colin Guthrie <cguthrie@mandriva.org> 7.2.127-8mdv2009.1
+ Revision: 348709
- Do not fork gvim after initialising gtk (breaks lots of things) mdv#44925

* Wed Feb 25 2009 Thierry Vignaud <tv@mandriva.org> 7.2.127-7mdv2009.1
+ Revision: 344641
- patch 33: security fix for CVE-2009-0316 (#48045)
- bump to official patchlevel 127

* Mon Feb 16 2009 Thierry Vignaud <tv@mandriva.org> 7.2.108-6mdv2009.1
+ Revision: 340883
- bump to official patchlevel 108

* Mon Feb 02 2009 Jérôme Soyer <saispo@mandriva.org> 7.2.087-6mdv2009.1
+ Revision: 336345
- Revert to old patch from Fedora

* Sun Feb 01 2009 Jérôme Soyer <saispo@mandriva.org> 7.2.087-5mdv2009.1
+ Revision: 336102
- Really revert 087
- Revert to 87
- Bump Release
- Add python and ruby support for vim-enhanced

* Sun Feb 01 2009 Jérôme Soyer <saispo@mandriva.org> 7.2.087-4mdv2009.1
+ Revision: 336087
- Upgrade top 087 upstream patch
- Clean SPEC
- Fix lib64 for python interpreter

* Mon Jan 19 2009 Helio Chissini de Castro <helio@mandriva.com> 7.2.079-4mdv2009.1
+ Revision: 331250
- Cmake syntax files would be available by cmake own package. This solves current issue of not uptodate syntax new macro entries,
  as cmake is released more often than a vim release.

* Mon Jan 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 7.2.079-3mdv2009.1
+ Revision: 331225
- really add nagios syntax file

* Fri Jan 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 7.2.079-2mdv2009.1
+ Revision: 330280
- add nagios syntax file

* Wed Jan 07 2009 Thierry Vignaud <tv@mandriva.org> 7.2.079-1mdv2009.1
+ Revision: 326714
- bump to official patchlevel 079

* Wed Dec 24 2008 Michael Scherer <misc@mandriva.org> 7.2.069-11mdv2009.1
+ Revision: 318354
- rebuild for new python

* Tue Dec 16 2008 Thierry Vignaud <tv@mandriva.org> 7.2.069-10mdv2009.1
+ Revision: 314751
- fix build
- bump to official patchlevel 069
- rediff some patches due to stricter rpm-4.6rc3
- include official patchlevel in version instead of release

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 7.2-9.065mdv2009.1
+ Revision: 311037
- rebuild for new tcl

  + Thierry Vignaud <tv@mandriva.org>
    - source 3: restore README.mdk (explaining how to update to latest official
      patchlevel) from vim-7.0-14mdv2007.0.src.rpm since it disapeared between
      2007.0 & 2007.1

* Thu Dec 04 2008 Thierry Vignaud <tv@mandriva.org> 7.2-8.065mdv2009.1
+ Revision: 309911
- include official patchlevel in release number
- bump to official patchlevel 065

* Wed Sep 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 7.2-8mdv2009.0
+ Revision: 287822
- cfengine syntax file
- patch perl syntax file for 5.10 new keywords

* Wed Sep 17 2008 Thierry Vignaud <tv@mandriva.org> 7.2-7mdv2009.0
+ Revision: 285363
- bump to official patchlevel 018
- bump to official patchlevel 015

* Tue Sep 09 2008 Thierry Vignaud <tv@mandriva.org> 7.2-5mdv2009.0
+ Revision: 283113
- bump to official patchlevel 013
- fix unreadable files (#43598)

* Mon Sep 01 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.2-4mdv2009.0
+ Revision: 278469
- Restored/redid vimrc_nosetmouse patch for vim 7.2, it wasn't already
  applied.

* Fri Aug 29 2008 Pixel <pixel@mandriva.com> 7.2-3mdv2009.0
+ Revision: 277246
- really fix upgrading

* Thu Aug 28 2008 Thierry Vignaud <tv@mandriva.org> 7.2-2mdv2009.0
+ Revision: 276819
- fix upgrading

* Wed Aug 27 2008 Thierry Vignaud <tv@mandriva.org> 7.2-1mdv2009.0
+ Revision: 276566
- new release
- bump to official patchlevel 006
- drop patch 0 (merged upstream)
- rediff patch 28 & 32
- bump to official patchlevel 330

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 7.1-16mdv2009.0
+ Revision: 265771
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Jun 11 2008 Thierry Vignaud <tv@mandriva.org> 7.1-15mdv2009.0
+ Revision: 218083
- bump to official patchlevel 314
- bump to official patchlevel 264
- do not require the whole perl

* Thu Feb 07 2008 Thierry Vignaud <tv@mandriva.org> 7.1-14mdv2008.1
+ Revision: 163557
- make xxd working with files larger than 2GB on ia32 (#37332)
- add patch 34: match more keywords in fstab
- update to official patchlevel 244
- buildrequires ncurses-devel, thus using ncurses instead of termcap (#37529)

* Wed Jan 30 2008 Thierry Vignaud <tv@mandriva.org> 7.1-13mdv2008.1
+ Revision: 160321
- update to official patchlevel 242
- point the bogus patch on error

* Mon Jan 21 2008 Gustavo De Nardin <gustavodn@mandriva.com> 7.1-12mdv2008.1
+ Revision: 155887
- re-rebuild for perl-5.10.0 (unneeded, vim was just left half upgraded by urpmi)

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 7.1-11mdv2008.1
+ Revision: 151249
- rebuild for perl-5.10.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 7.1-10mdv2008.0
+ Revision: 82053
- rebuild for new soname of tcl

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Tue Aug 21 2007 Thierry Vignaud <tv@mandriva.org> 7.1-9mdv2008.0
+ Revision: 68592
- fix file conflict (#32651)
- kill file require on update-alternatives
- update to officiel patch level 87
- fix man pages extension

* Wed Aug 15 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.1-8mdv2008.0
+ Revision: 63544
- fix crash

* Sun Jul 15 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.1-7mdv2008.0
+ Revision: 52224
- fix problems reading compressed files caused by fortify patch (update P33, fixes #31908)
- update to patch level 028 (S4)

* Fri Jul 13 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.1-6mdv2008.0
+ Revision: 51790
- replace buffer overflow patch (P33) with better from LFS

* Thu Jul 12 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 7.1-5mdv2008.0
+ Revision: 51636
- fix buffer overflow that caused vim to be crashed with fortify (P33)
- do parallell build
- more lzma support added (P32)
- add some lzma support (P32, work in progress)

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 7.1-4mdv2008.0
+ Revision: 45094
- recognize %%serverbuild when syntax highlighting

  + Michael Scherer <misc@mandriva.org>
    - fix documentation

* Mon Jun 25 2007 Thierry Vignaud <tv@mandriva.org> 7.1-3mdv2008.0
+ Revision: 44064
- update to official patch 12

  + Andreas Hasenack <andreas@mandriva.com>
    - added apparmor syntax file

* Wed May 16 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 7.1-2mdv2008.0
+ Revision: 27371
- Added vimrc_nosetmouse patch, don't 'set mouse=a' by default, keep
  behaviour like old versions before 7.1, set mouse=a changes behavior
  of copy/paste with mouse on X.

* Tue May 15 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 7.1-1mdv2008.0
+ Revision: 26879
- New version

* Thu May 10 2007 Thierry Vignaud <tv@mandriva.org> 7.0-19mdv2008.0
+ Revision: 26129
- bump release

* Thu May 10 2007 Thierry Vignaud <tv@mandriva.org> 7.0-18mdv2008.0
+ Revision: 26112
- patch 31: security fix for CVE-2007-2438

* Thu Apr 19 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 7.0-17mdv2008.0
+ Revision: 14888
- Kill old debian style

