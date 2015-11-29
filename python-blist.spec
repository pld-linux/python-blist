#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	blist
Summary:	The blist is a drop-in replacement for the Python list that provides better performance when modifying large lists
Summary(pl.UTF-8):	Blist jest zamiennikiem dla Pythonowych list który jest szybszy przy modifikacjach dużych list
Name:		python-%{module}
Version:	1.3.6
Release:	5
License:	BSD
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/b/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a538f1a24b9191e3c40252e9397408a9
URL:		http://stutzbachenterprises.com/blist/
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:		python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The blist is a drop-in replacement for the Python list that provides better performance when modifying large lists. 
The blist package also provides sortedlist, sortedset, weaksortedlist, weaksortedset, sorteddict, and btuple types

%description -l pl.UTF-8
Blist jest zamiennikiem dla Pythonowych list który jest szybszy przy modifikacjach dużych list.
Pakiet blist udostępnia też typy: sortedlist, sortedset, weaksortedlist, weaksortedset, sorteddict, and btuple.

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:		python3-modules

%description -n python3-%{module}
The blist is a drop-in replacement for the Python list that provides better performance when modifying large lists

%description -n python3-%{module} -l pl.UTF-8
Blist jest zamiennikiem dla Pythonowych list który jest szybszy przy modifikacjach dużych list.
Pakiet blist udostępnia też typy: sortedlist, sortedset, weaksortedlist, weaksortedset, sorteddict, and btuple.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_blist.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/_blist.cpython-*.so
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
