#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	kombu
Summary:	Messaging library for Python
Name:		python-%{module}
Version:	3.0.29
Release:	1
License:	BSD-like
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/k/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	892bf89ee247c0d16d2bdd63f1ddf4c5
URL:		http://pypi.python.org/pypi/kombu
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%if %{with python2}
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-modules
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
BuildRequires:	python3-unittest2
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

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html
rm -rf .build/html/_sources
cd ..
%endif
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
