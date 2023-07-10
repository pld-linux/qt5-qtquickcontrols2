#
# Conditional build:
%bcond_without	doc	# Documentation
%bcond_without	qm	# QM translations

%define		orgname		qtquickcontrols2
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	5.12.3-2
%define		qttools_ver		%{version}
Summary:	The Qt5 Quick Controls2 modules
Summary(pl.UTF-8):	Moduły Qt5 Quick Controls2
Name:		qt5-%{orgname}
Version:	5.15.10
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	3d9fd23d30203792a8af0314e8ca5348
Source1:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qttranslations-everywhere-opensource-src-%{version}.tar.xz
# Source1-md5:	f421a46bfd3cbbdf0a3fa701d3ccbedf
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
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
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
Requires(post,postun):	/sbin/ldconfig
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}

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
BuildArch:	noarch

%description doc
Qt5 Quick Controls2 documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Quick Controls2 w formacie HTML.

%package doc-qch
Summary:	Qt5 Quick Controls2 documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Quick Controls w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

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
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
%{qmake_qt5}
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

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

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

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/quickcontrols2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Quick-controls2 -p /sbin/ldconfig
%postun	-n Qt5Quick-controls2 -p /sbin/ldconfig

%files -n Qt5Quick-controls2 -f qtquickcontrols2.lang
%defattr(644,root,root,755)
%doc dist/changes-*
# R: Core Gui Qml Quick QuickTemplates2
%attr(755,root,root) %{_libdir}/libQt5QuickControls2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5QuickControls2.so.5
# R: Core Gui Qml QmlModels Quick
%attr(755,root,root) %{_libdir}/libQt5QuickTemplates2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5QuickTemplates2.so.5
%dir %{_libdir}/qt5/qml/Qt/labs/calendar
# R: Core Gui Qml Quick QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/Qt/labs/calendar/libqtlabscalendarplugin.so
%{_libdir}/qt5/qml/Qt/labs/calendar/plugins.qmltypes
%{_libdir}/qt5/qml/Qt/labs/calendar/qmldir
%{_libdir}/qt5/qml/Qt/labs/calendar/*.qml
%{_libdir}/qt5/qml/Qt/labs/calendar/*.qmlc
%dir %{_libdir}/qt5/qml/Qt/labs/platform
# R: Core Gui Qml Quick QuickTemplates2 Widgets
%attr(755,root,root) %{_libdir}/qt5/qml/Qt/labs/platform/libqtlabsplatformplugin.so
%{_libdir}/qt5/qml/Qt/labs/platform/plugins.qmltypes
%{_libdir}/qt5/qml/Qt/labs/platform/qmldir
%dir %{_libdir}/qt5/qml/QtQuick/Controls.2
# R: Core Gui Qml Quick QuickControls2 QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Controls.2/libqtquickcontrols2plugin.so
%{_libdir}/qt5/qml/QtQuick/Controls.2/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Controls.2/qmldir
%{_libdir}/qt5/qml/QtQuick/Controls.2/*.qml
%{_libdir}/qt5/qml/QtQuick/Controls.2/designer
%dir %{_libdir}/qt5/qml/QtQuick/Controls.2/Fusion
# R: Core Gui Qml Quick QuickControls2 QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Controls.2/Fusion/libqtquickcontrols2fusionstyleplugin.so
%{_libdir}/qt5/qml/QtQuick/Controls.2/Fusion/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Controls.2/Fusion/qmldir
%{_libdir}/qt5/qml/QtQuick/Controls.2/Fusion/*.qml
%dir %{_libdir}/qt5/qml/QtQuick/Controls.2/Imagine
# R: Core Gui Qml Quick QuickControls2 QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Controls.2/Imagine/libqtquickcontrols2imaginestyleplugin.so
%{_libdir}/qt5/qml/QtQuick/Controls.2/Imagine/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Controls.2/Imagine/qmldir
%{_libdir}/qt5/qml/QtQuick/Controls.2/Imagine/*.qml
%dir %{_libdir}/qt5/qml/QtQuick/Controls.2/Material
# R: Core Gui Qml Quick QuickControls2 QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Controls.2/Material/libqqc2materialstyleplugin.so
%{_libdir}/qt5/qml/QtQuick/Controls.2/Material/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Controls.2/Material/qmldir
%{_libdir}/qt5/qml/QtQuick/Controls.2/Material/*.qml
%dir %{_libdir}/qt5/qml/QtQuick/Controls.2/Universal
# R: Core Gui Qml Quick QuickControls2 QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Controls.2/Universal/libqtquickcontrols2universalstyleplugin.so
%{_libdir}/qt5/qml/QtQuick/Controls.2/Universal/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Controls.2/Universal/qmldir
%{_libdir}/qt5/qml/QtQuick/Controls.2/Universal/*.qml
%dir %{_libdir}/qt5/qml/QtQuick/Templates.2
# R: Core Gui Qml Quick QuickTemplates2
%attr(755,root,root) %{_libdir}/qt5/qml/QtQuick/Templates.2/libqtquicktemplates2plugin.so
%{_libdir}/qt5/qml/QtQuick/Templates.2/plugins.qmltypes
%{_libdir}/qt5/qml/QtQuick/Templates.2/qmldir

%files -n Qt5Quick-controls2-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5QuickControls2.so
%{_libdir}/libQt5QuickControls2.prl
%attr(755,root,root) %{_libdir}/libQt5QuickTemplates2.so
%{_libdir}/libQt5QuickTemplates2.prl
%{_includedir}/qt5/QtQuickControls2
%{_includedir}/qt5/QtQuickTemplates2
%{_pkgconfigdir}/Qt5QuickControls2.pc
%{_pkgconfigdir}/Qt5QuickTemplates2.pc
%{_libdir}/cmake/Qt5QuickControls2
%{_libdir}/cmake/Qt5QuickTemplates2
%{_libdir}/qt5/mkspecs/modules/qt_lib_quickcontrols2.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_quickcontrols2_private.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_quicktemplates2.pri
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

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
