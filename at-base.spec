#
# spec file for package at-base
#
# Copyright (c) 2020 SUSE Software Solutions GmbH Nuernberg, Germany
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Name:           at-base
Version:        0.1
Release:        0
Summary:        AwayTeam VPN Server
License:        GPLv3+
URL:            https://github.com/AwayTeam-VPN/at-base
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  systemd-rpm-macros
Requires:       python3 python3-flask strongswan firewalld
BuildArch:      noarch

%description
AwayTeam VPN Server with dynamic firewall and IPSec

%prep

%build

%check

%install
#install -D -m 644 %{SOURCE0} %{buildroot}%{_unitdir}/at-base.service

%pre
%service_add_pre at-base.service

%post
%service_add_post at-base.service

%preun
%service_del_preun at-base.service

%files
%doc README
%license COPYING
%config(noreplace) %{_sysconfdir}/at-base/at-base.conf
%{_unitdir}/at-base.service

%changelog

