Name:     slimbookrgbkeyboard
Version:  0.3.6
Release:  1%{?dist}
Summary:  Slimbook UI for ite-8291r3-ctl & clevo-xsm-wmi keyboard modules.
License:  GPLv3+
URL:      https://slimbook.es/en/tutoriales/aplicaciones-slimbook/501-en-slimbook-rgb-keyboard-3-0
Source0:  https://launchpad.net/~slimbook/+archive/ubuntu/slimbook/+sourcefiles/slimbookrgbkeyboard/%{version}/slimbookrgbkeyboard_%{version}.orig.tar.xz
BuildRequires:   gcc
BuildRequires:   make

%description
Slimbook UI for ite-8291r3-ctl & clevo-xsm-wmi keyboard modules.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files

%changelog

* Thu Jul 2 2021 slimbook <dev@slimbook.es> - 0.3.6-1
- Autostart solved issue
