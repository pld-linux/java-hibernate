# TODO:
# - build from source, but FIRST finish maven
%include	/usr/lib/rpm/macros.java
%define		srcname		hibernate
Summary:	Relational Persistence for Java
Name:		java-hibernate
Version:	3.5.1
Release:	0.1
License:	LGPL
Group:		Libraries/Java
Source0:	https://sourceforge.net/projects/hibernate/files/hibernate3/3.5.1-Final/hibernate-distribution-%{version}-Final-dist.tar.gz
# Source0-md5:	407fdc684dc8c48e46bc2ce76a05a207
URL:		http://www.hibernate.org/
BuildRequires:	jar
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
Requires:	java-antlr
Requires:	java-cglib
Requires:	java-commons-collections
Requires:	java-dom4j
Requires:	java-javassist
Requires:	java-jta
Requires:	java-slf4j
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hibernate is a collection of related projects enabling developers to
utilize POJO-style domain models in their applications in ways
extending well beyond Object/Relational Mapping.

%package doc
Summary:	Manual for %{srcname}
Summary(fr.UTF-8):	Documentation pour %{srcname}
Summary(it.UTF-8):	Documentazione di %{srcname}
Summary(pl.UTF-8):	Podręcznik dla %{srcname}
Group:		Documentation

%description doc
Documentation for %{srcname}.

%description doc -l fr.UTF-8
Documentation pour %{srcname}.

%description doc -l it.UTF-8
Documentazione di %{srcname}.

%description doc -l pl.UTF-8
Dokumentacja do %{srcname}.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n hibernate-distribution-%{version}-Final

%build
# build source jar
jar cf %{srcname}.src.jar -C %{_datadir}/empty .
for I in $(ls -d project/*/src/main/java); do
	jar uf %{srcname}.src.jar -C $I .
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib

# jars
cp -a hibernate3.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/hibernate.jar

# install bundled version of libraries that are not available in PLD yet
cp -a lib/jpa/hibernate-jpa-2.0-api-1.0.0.Final.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/hibernate-jpa-2.0-api-1.0.0.Final.jar
cp -a lib/optional/c3p0/c3p0-0.9.1.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/c3p0-0.9.1.jar
cp -a lib/optional/proxool/proxool-0.8.3.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/proxool-0.8.3.jar
cp -a lib/optional/ehcache/ehcache-1.5.0.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/ehcache-1.5.0.jar
cp -a lib/optional/jbosscache/jbosscache-core-3.2.1.GA.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/jbosscache-core-3.2.1.GA.jar
cp -a lib/optional/infinispan/infinispan-core-4.0.0.FINAL.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/infinispan-core-4.0.0.FINAL.jar
cp -a lib/optional/oscache/oscache-2.1.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/oscache-2.1.jar
cp -a lib/optional/swarmcache/swarmcache-1.0RC2.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/swarmcache-1.0RC2.jar

# symlink required libs that are available in PLD
ln -s ${_javadir}/cglib.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/cglib.jar
ln -s ${_javadir}/javassist.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/javassist.jar
ln -s ${_javadir}/jta.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/jta.jar
ln -s ${_javadir}/antlr.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/antlr.jar
ln -s ${_javadir}/commons-collections.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/commons-collections.jar
ln -s ${_javadir}/dom4j.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/dom4j.jar
ln -s ${_javadir}/slf4j.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}/lib/slf4j.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a documentation/javadocs/ $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc changelog.txt
%{_javadir}/%{srcname}

%files doc
%defattr(644,root,root,755)
%lang(es)    %doc documentation/manual/es-ES
%lang(en)    %doc documentation/manual/en-US
%lang(de)    %doc documentation/manual/de-DE
%lang(fr)    %doc documentation/manual/fr-FR
%lang(ja)    %doc documentation/manual/ja-JP
%lang(pt_BR) %doc documentation/manual/pt-BR
%lang(zh_CN) %doc documentation/manual/zh-CN

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}

%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
