AC_INIT(dots, 0.0.1, eitan@ascender.com)
AM_INIT_AUTOMAKE
AM_MAINTAINER_MODE
GNOME_DOC_INIT

dnl == check for python ==
AM_PATH_PYTHON(2.4)

dnl == Check for liblouis and liblouisxml
PKG_CHECK_MODULES(LIBLOUIS, [liblouis >= 1.6.2 liblouisxml >= 1.9.1])

dnl Find tables dir
TABLES_DIR=`pkg-config --variable=tablesdir liblouis`
AC_SUBST(TABLES_DIR)

dnl == check for xml2brl ==
AC_PATH_PROG(XML2BRL, xml2brl)
test -z "$XML2BRL" && AC_MSG_ERROR([
You need xml2brl which is bundled with liblouisxml.
])
AC_SUBST(XML2BRL)

dnl == check for xml2brl ==
AC_PATH_PROG(ANTIWORD, antiword)
test -z "$ANTIWORD" && AC_MSG_ERROR([
You need antiword for MS Word document support.
])
AC_SUBST(ANTIWORD)

dnl == i18n ==
#GETTEXT_PACKAGE=dots
#AC_SUBST(GETTEXT_PACKAGE)
#AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
#AM_GLIB_GNU_GETTEXT

dnl == intltool check ==
#IT_PROG_INTLTOOL([0.35.0])

dnl == generate makefiles ==
AC_OUTPUT([
Makefile
bin/Makefile
bin/dots
dots/Makefile
dots/host_settings.py
data/Makefile
])
