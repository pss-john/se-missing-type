# vim: sw=4:ts=4:et


%define relabel_files() \
restorecon -R /opt/gateway; \
restorecon -R /opt/gateway/*/gateway; \
restorecon -R /var/log/gateway; \
restorecon -R /etc/gateway; \

%define selinux_policyver 34.1.43-1

Name:   gateway_selinux
Version:	1.0
Release:	1%{?dist}
Summary:	SELinux policy module for gateway

Group:	System Environment/Base		
License:	GPLv2+	
# This is an example. You will need to change it.
URL:		http://HOSTNAME
Source0:	gateway.pp
Source1:	gateway.if
Source2:	gateway_selinux.8


Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the  SELinux policy security module for gateway.

%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/
install -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/gateway_selinux.8
install -d %{buildroot}/etc/selinux/targeted/contexts/users/


%post
semodule -n -i %{_datadir}/selinux/packages/gateway.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    %relabel_files

fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    semodule -n -r gateway
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       %relabel_files

    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/gateway.pp
%{_datadir}/selinux/devel/include/contrib/gateway.if
%{_mandir}/man8/gateway_selinux.8.*


%changelog
* Wed Feb 15 2023 YOUR NAME <YOUR@EMAILADDRESS> 1.0
- Initial version

