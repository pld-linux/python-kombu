#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do perform tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	kombu
Summary:	Messaging library for Python
Name:		python-%{module}
Version:	3.0.29
Release:	2
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/k/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	892bf89ee247c0d16d2bdd63f1ddf4c5
Patch0:		unittest2.patch
URL:		http://pypi.python.org/pypi/kombu
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	python-django
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mock
BuildRequires:	python3-nose
%endif
%endif
Requires:	python-amqp >= 1.4.7
Requires:	python-anyjson >= 0.3.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQ protocol, and
also provide proven and tested solutions to common messaging problems.

%package -n python3-%{module}
Summary:	Messaging library for Python
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQ protocol, and
also provide proven and tested solutions to common messaging problems.

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

%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html
rm -rf .build/html/_sources
cd ..
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
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

%files
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS TODO
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-*.egg-info

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS TODO
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build/html/*
%endif
