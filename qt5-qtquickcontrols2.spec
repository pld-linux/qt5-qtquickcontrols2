#
# Conditional build:
%bcond_without	doc	# Documentation
%bcond_without	qm	# QM translations

%define		orgname		qtquickcontrols2
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Quick Controls2 modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls2
Name:		qt5-%{orgname}
Version:	5.12.1
Release:	1
License:	LGPL v3 or GPL v2 or commercial
Group:		X11/Libraries
Source0:	http://download.qt.io/official_releases/qt/5.12/%{version}/submodules/%{orgname}-everywhere-src-%{version}.tar.xz
# Source0-md5:	85c27b5cefe8abf0e7389e9f132189f5
Source1:	http://download.qt.io/official_releases/qt/5.12/%{version}/submodules/qttranslations-everywhere-src-%{version}.tar.xz
# Source1-md5:	045ad1eda4d3a272b24b6c60a06b313f
URL:		http://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= %{qttools_ver}}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Quick Controls2, Dialogs modules.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera moduły Qt5 Quick Controls2, Dialogs.

%package -n Qt5Quick-controls2
Summary:	The Qt5 Quick Controls2 modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls2
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
Obsoletes:	qt5-qtquickcontrols2

%description -n Qt5Quick-controls2
Qt5 Quick Controls, Dialogs modules.

This package provides a set of widgets/controls that can be used to
build complete interfaces in Qt5 Quick (v2).

%description -n Qt5Quick-controls2 -l pl.UTF-8
Moduły Qt5 Quick Controls, Dialogs.

Ten pakiet dostarcza zestaw widgetów/kontrolek, które można
wykorzystywać do tworzenia kompletnych interfejsów przy użyciu Qt5
Quick (v2).

%package -n Qt5Quick-controls2-devel
Summary:	Qt5 Quick controls2 library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Quick controls2 - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}
Requires:	Qt5Quick-controls2 = %{version}-%{release}

%description -n Qt5Quick-controls2-devel
Qt5 Quick controls2 library - development files.

%description -n Qt5Quick-controls2-devel -l pl.UTF-8
Biblioteka Qt5 Quick controls2 - pliki programistyczne.

%package doc
Summary:	Qt5 Quick Controls2 documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls2 w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 Quick Controls2 documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls2 w formacie HTML.

%package doc-qch
Summary:	Qt5 Quick Controls2 documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 Quick Controls2 documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls2 w formacie QCH.

%package examples
Summary:	Examples for Qt5 Quick Controls2
Summary(pl.UTF-8):	Przykłady do Qt5 Quick controls2
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Examples for Qt5 Quick Controls2.

%description examples -l pl.UTF-8
Przykłady do Qt5 Quick controls2.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}

%build
qmake-qt5
%{__make}
%{?with_doc:%{__make} docs}

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
qmake-qt5
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtquickcontrols
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt,qtbase,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols,qtserialport,qtscript,qtwebengine,qtwebsockets,qtxmlpatterns}_*.qm
%endif

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_localedir}/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtquickcontrols2.lang
%if %{with qm}
find_qt5_qm qtquickcontrols2 >> qtquickcontrols2.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -n Qt5Quick-controls2 -f qtquickcontrols2.lang
%defattr(644,root,root,755)
%doc dist/changes-*
%ghost %{_libdir}/libQt5QuickControls2.so.5
%{_libdir}/libQt5QuickControls2.so.5.*
%ghost %{_libdir}/libQt5QuickTemplates2.so.5
%{_libdir}/libQt5QuickTemplates2.so.5.*
%{_libdir}/qt5/qml/Qt/labs
%{_libdir}/qt5/qml/QtQuick/Controls.2
%{_libdir}/qt5/qml/QtQuick/Templates.2

%files -n Qt5Quick-controls2-devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtQuickControls2
%{_includedir}/qt5/QtQuickTemplates2
%{_libdir}/cmake/Qt5QuickControls2
%{_libdir}/libQt5QuickControls2.la
%{_libdir}/libQt5QuickControls2.prl
%{_libdir}/libQt5QuickControls2.so
%{_libdir}/libQt5QuickTemplates2.la
%{_libdir}/libQt5QuickTemplates2.prl
%{_libdir}/libQt5QuickTemplates2.so
%{_pkgconfigdir}/Qt5QuickControls2.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_quickcontrols2.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_quickcontrols2_private.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_quicktemplates2_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtlabscalendar
%{_docdir}/qt5-doc/qtlabsplatform
%{_docdir}/qt5-doc/qtquickcontrols

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtlabscalendar.qch
%{_docdir}/qt5-doc/qtlabsplatform.qch
%{_docdir}/qt5-doc/qtquickcontrols.qch
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/qt5/quickcontrols2
