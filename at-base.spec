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
License:        GPL3
URL:            https://github.com/AwayTeam-VPN/at-base
Source0:        %{name}-%{version}.tar.xz
#BuildRequires:  python3
Requires:       python3 python3-flask strongswan firewalld
BuildArch:      noarch

%description
AwayTeam VPN Server with dynamic firewall and IPSec

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%python3_build

%check

%install

%files

%changelog

