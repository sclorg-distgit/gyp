%{?scl:%scl_package gyp}
%{!?scl:%global pkg_name %{name}}
%global		revision	0bb6747
%{expand:	%%global	archivename	gyp-%{version}%{?revision:-git%{revision}}}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%if 0%{?rhel} == 5
%global __python2 /usr/bin/python26
%global __os_install_post %__multiple_python_os_install_post
%endif
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:		%{?scl_prefix}gyp
Version:	0.1
Release:	0.20%{?revision:.%{revision}git}%{?dist}
Summary:	Generate Your Projects

Group:		Development/Tools
License:	BSD
URL:		http://code.google.com/p/gyp/
# No released tarball avaiable. so the tarball was generated
# from svn as following:
#
# 1. svn co http://gyp.googlecode.com/svn/trunk gyp
# 2. cd gyp
# 3. version=$(grep version= setup.py|cut -d\' -f2)
# 4. revision=$(git log --oneline|head -1|cut -d' ' -f1)
# 5. tar -a --exclude-vcs -cf /tmp/gyp-$version-git$revision.tar.bz2 *
Source0:	%{archivename}.tar.bz2
Patch0:		gyp-rpmoptflags.patch

%if 0%{?rhel} && 0%{?rhel} == 5
BuildRequires:	python26-devel
%else
BuildRequires:	python2-devel
%endif
BuildRequires:	python-setuptools
Requires:	python-setuptools
BuildArch:	noarch
BuildRequires:	python2-devel
BuildArch:	noarch

%{?scl:BuildRequires: %{scl}-runtime}
%{?scl:Requires: %{scl}-runtime}
%{?scl:Obsoletes: nodejs010-gyp}

%description
GYP is a tool to generates native Visual Studio, Xcode and SCons
and/or make build files from a platform-independent input format.

Its syntax is a universal cross-platform build representation
that still allows sufficient per-platform flexibility to accommodate
irreconcilable differences.

%prep
%setup -q -c -n %{archivename}
%patch0 -p1 -b .0-rpmoptflags
for i in $(find pylib -name '*.py'); do
	sed -e '\,#![ \t]*/.*python,{d}' $i > $i.new && touch -r $i $i.new && mv $i.new $i
done

%build
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}


%install
rm -rf $RPM_BUILD_ROOT

%{?scl:scl enable %{scl} "}
%{__python} setup.py install --root $RPM_BUILD_ROOT --skip-build \
    --prefix %{_prefix}
%{?scl:"}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{_bindir}/gyp
%{?scl:%_scl_root}%{python_sitelib}/*

%changelog
* Wed Jul 22 2015 Tomas Hrcka <thrcka@redhat.com> - 0.1-0.20.0bb6747git
- Rebase to latest upstream

* Fri May  1 2015 Akira TAGOH <tagoh@redhat.com> - 0.1-0.17.0bb6747git
- Rebase to 0bb6747.
- Add R: python-setuptools (#1217358)

* Mon Mar  2 2015 Akira TAGOH <tagoh@redhat.com> - 0.1-0.16.2037svn
- Rebase to r2037.

* Wed Jun 25 2014 Akira TAGOH <tagoh@redhat.com> - 0.1-0.15.1617svn
- Update rpm macros to the latest guidelines.
- Build against python26 for EPEL5.

- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Tomas Hrcka <thrcka@redhat.com> - 0.1-0.12.1617svn
- Obsolete nodejs010-gyp

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.11.1617svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Akira TAGOH <tagoh@redhat.com> - 0.1-0.10.1617svn
- Rebase to r1617

* Mon Apr 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.1-0.9.1010svn
- Add SCL runtime to Requires as well

* Mon Apr 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.1-0.8.1010svn
- Add conditional BR on SCL runtime

* Fri Apr 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.1-0.7.1010svn
- Add support for software collections

* Tue Feb 12 2013 Akira TAGOH <tagoh@redhat.com> - 0.1-0.9.1569svn
- Rebase to r1569 (#908983)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.8.1010svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.7.1010svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Akira TAGOH <tagoh@redhat.com> - 0.1-0.6.1010svn
- Rebase to r1010.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.5.840svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.4.840svn
- Rebase to r840.
- generate Makefile with RPM_OPT_FLAGS in CCFLAGS.

* Fri Aug  6 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.3.839svn
- Drop the unnecessary macro.

* Thu Aug  5 2010 Akira TAGOH <tagoh@redhat.com. - 0.1-0.2.839svn
- Update the spec file according to the suggestion in rhbz#621242.

* Wed Aug  4 2010 Akira TAGOH <tagoh@redhat.com> - 0.1-0.1.839svn
- Initial packaging.

