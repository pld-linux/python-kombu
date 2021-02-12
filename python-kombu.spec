#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	kombu
Summary:	Messaging library for Python
Summary(pl.UTF-8):	Biblioteka komunikatów dla Pythona
Name:		python-%{module}
# keep 4.x here for python2 support
Version:	4.6.11
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/kombu/
Source0:	https://files.pythonhosted.org/packages/source/k/kombu/%{module}-%{version}.tar.gz
# Source0-md5:	759b31d97fc11c4cb16f6d293723e85e
URL:		https://pypi.org/project/kombu/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:20.6.7
%if %{with tests}
BuildRequires:	python-Pyro4
BuildRequires:	python-amqp >= 2.6.0
BuildRequires:	python-botocore
BuildRequires:	python-case >= 1.5.2
BuildRequires:	python-importlib_metadata >= 0.18
BuildRequires:	python-nose
BuildRequires:	python-pytest
BuildRequires:	python-pytz
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:20.6.7
%if %{with tests}
BuildRequires:	python3-Pyro4
BuildRequires:	python3-amqp >= 2.6.0
BuildRequires:	python3-amqp < 2.7
BuildRequires:	python3-botocore
BuildRequires:	python3-case >= 1.5.2
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.18
%endif
BuildRequires:	python3-nose
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-amqp
BuildRequires:	python-sphinx_celery
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQ protocol, and
also provide proven and tested solutions to common messaging problems.

%description -l pl.UTF-8
Celem Kombu jest jak największe ułatwienie wymiany komunikatów w
Pythonie poprzez dostarczenie idomatycznego, wysokopoziomowego
interfejsu do protokołu AMQ oraz sprawdzonych rozwiązań powszechnych
problemów związanych z komunikowaniem.

%package -n python3-%{module}
Summary:	Messaging library for Python
Summary(pl.UTF-8):	Biblioteka komunikatów dla Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQ protocol, and
also provide proven and tested solutions to common messaging problems.

%description -n python3-%{module} -l pl.UTF-8
Celem Kombu jest jak największe ułatwienie wymiany komunikatów w
Pythonie poprzez dostarczenie idomatycznego, wysokopoziomowego
interfejsu do protokołu AMQ oraz sprawdzonych rozwiązań powszechnych
problemów związanych z komunikowaniem.

%package apidocs
Summary:	API documentation for kombu module
Summary(pl.UTF-8):	Dokumentacja API modułu kombu
Group:		Documentation
Obsoletes:	python3-kombu-apidocs < 5

%description apidocs
API documentation for kombu module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu kombu.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python} -m pytest t/unit
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
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
%doc AUTHORS FAQ LICENSE README.rst THANKS TODO
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS FAQ LICENSE README.rst THANKS TODO
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,userguide,*.html,*.js}
%endif
