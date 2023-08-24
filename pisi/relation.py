# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 - 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pisi
import pisi.version
import pisi.db
import pisi.pxml.autoxml as autoxml


class Relation(metaclass=autoxml.autoxml):
    s_Package = [autoxml.String, autoxml.MANDATORY]
    a_version = [autoxml.String, autoxml.OPTIONAL]
    a_versionFrom = [autoxml.String, autoxml.OPTIONAL]
    a_versionTo = [autoxml.String, autoxml.OPTIONAL]
    a_release = [autoxml.String, autoxml.OPTIONAL]
    a_releaseFrom = [autoxml.String, autoxml.OPTIONAL]
    a_releaseTo = [autoxml.String, autoxml.OPTIONAL]

    def satisfies_relation(self, version, release):
        if self.version and version != self.version:
            return False
        else:
            v = pisi.version.make_version(version)

            if self.versionFrom and v < pisi.version.make_version(self.versionFrom):
                return False

            if self.versionTo and v > pisi.version.make_version(self.versionTo):
                return False

        if self.release and release != self.release:
            return False
        else:
            r = int(release)

            if self.releaseFrom and r < int(self.releaseFrom):
                return False

            if self.releaseTo and r > int(self.releaseTo):
                return False

        return True


def installed_package_satisfies(relation):
    installdb = pisi.db.installdb.InstallDB()
    pkg_name = relation.package
    if hasattr(relation, "type") and relation.type == "pkgconfig":
        pkg = installdb.get_package_by_pkgconfig(pkg_name)
        if pkg:
            return relation.satisfies_relation(pkg.version, pkg.release)
        else:
            return False
    elif hasattr(relation, "type") and relation.type == "pkgconfig32":
        pkg = installdb.get_package_by_pkgconfig32(pkg_name)
        if pkg:
            return relation.satisfies_relation(pkg.version, pkg.release)
        else:
            return False
    if not installdb.has_package(pkg_name):
        return False
    else:
        pkg = installdb.get_package(pkg_name)
        return relation.satisfies_relation(pkg.version, pkg.release)
