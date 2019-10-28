#
# Conditional build:
%bcond_with	doc	# build doc (uses network)
%bcond_with	tests	# do perform tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	kombu
Summary:	Messaging library for Python
Name:		python-%{module}
Version:	4.2.1
Release:	2
License:	BSD-like
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/k/kombu/%{module}-%{version}.tar.gz
# Source0-md5:	15e43bdeacef6805a61e2cdee717f748
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
BuildRequires:	python-amqp
BuildRequires:	python-django
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mock
BuildRequires:	python3-nose
%endif
%if %{with doc}
BuildRequires:	python3-amqp
BuildRequires:	python3-django
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-3
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

%package -n python3-%{module}-apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description -n python3-%{module}-apidocs
API documentation for %{module}.

%description -n python3-%{module}-apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-2
rm -rf .build/html/_sources
mv .build .build2
cd ..
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-3/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-3
rm -rf .build/html/_sources
mv .build .build3
cd ..
%endif
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
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS TODO
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build2/html/*
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS Changelog FAQ LICENSE README.rst THANKS TODO
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-*.egg-info

%if %{with doc}
%files -n python3-%{module}-apidocs
%defattr(644,root,root,755)
%doc docs/.build3/html/*
%endif
%endif
