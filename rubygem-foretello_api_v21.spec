%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foretello_api_v21

%global foreman_dir /usr/share/foreman
%global foreman_bundlerd_dir %{foreman_dir}/bundler.d

%if !("%{?scl}" == "ruby193" || 0%{?rhel} > 6 || 0%{?fedora} > 16)
%global gem_dir /usr/lib/ruby/gems/1.8
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%endif

%if "%{?scl}" == "ruby193"
    %global scl_ruby /usr/bin/ruby193-ruby
    %global scl_rake /usr/bin/ruby193-rake
    ### TODO temp disabled for SCL
    %global nodoc 1
%else
    %global scl_ruby /usr/bin/ruby
    %global scl_rake /usr/bin/rake
%endif

Summary: Plugin for Foreman & Katello API v2.1, which is based on v2 controllers but uses the response format according to the jsonapi.org specification.
Name: %{?scl_prefix}rubygem-%{gem_name}

Version: 1.0.0
Release: 0%{?dist}
Group: Development/Ruby
License: Distributable
URL: https://github.com/fusor/foretello_api_v21
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

%if "%{?scl}" == "ruby193"
Requires: %{?scl_prefix}ruby-wrapper
BuildRequires: %{?scl_prefix}ruby-wrapper
%endif
%if "%{?scl}" == "ruby193" || 0%{?rhel} > 6 || 0%{?fedora} > 16
BuildRequires:  %{?scl_prefix}rubygems-devel
%endif

%if 0%{?fedora} > 19
Requires: %{?scl_prefix}ruby(release) = 2.0.0
BuildRequires: %{?scl_prefix}ruby(release) = 2.0.0
%else
%if "%{?scl}" == "ruby193" || 0%{?rhel} > 6 || 0%{?fedora} > 16
Requires: %{?scl_prefix}ruby(abi) = 1.9.1
BuildRequires: %{?scl_prefix}ruby(abi) = 1.9.1
%else
Requires: ruby(abi) = 1.8
BuildRequires: ruby(abi) = 1.8
%endif
%endif

Requires: foreman >= 1.7.0
BuildRequires: foreman >= 1.7.0
BuildRequires: foreman-assets >= 1.7.0
BuildRequires: foreman-plugin >= 1.7.0
BuildRequires: %{?scl_prefix}rubygem-active_model_serializers

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(foretello_api_v21) = %{version}

Requires: %{?scl_prefix}rubygem-active_model_serializers

%description
Fusor Plugin

%package doc
BuildArch:  noarch
Requires:   %{?scl_prefix}%{pkg_name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} --force %{SOURCE0}
%{?scl:"}

%build

%install

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file
%foreman_precompile_plugin

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{gem_instdir}/
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_dir}/%{gem_name}.rb
#%{foreman_assets_plugin}

%files doc
%{gem_dir}/doc/%{gem_name}-%{version}

%changelog
* Thu Apr 09 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-6
- add cpus to discovered host response (jmagen@redhat.com)
- review previous change to rename method (jmagen@redhat.com)
- Merge pull request #2 from fusor/rename (jmagen@redhat.com)
- change to rename method (jmagen@redhat.com)

* Tue Apr 07 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-5
- add PUT rename for discovered hosts (jmagen@redhat.com)

* Mon Mar 30 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-4
- remove cpus attribute from DiscoveredHostSerializer (jmagen@redhat.com)

* Mon Mar 30 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-3
- add discovered host controller and serializer (jmagen@redhat.com)

* Fri Mar 20 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-2
- new package built with tito

* Fri Mar 20 2015 John Matthews <jwmatthews@gmail.com> 0.0.1-1
- Initial spec creation
