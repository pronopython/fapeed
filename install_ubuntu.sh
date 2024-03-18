#!/bin/bash
#
##############################################################################################
#
# Fapeed - Adult Slideshow App
#
# For updates see git-repo at
# https://github.com/pronopython/fapeed
#
##############################################################################################
#
# Copyright (C) PronoPython
#
# Contact me at pronopython@proton.me
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################################
#

INSTALLDIR=""

echo "Fapeed installer"
echo ""

if ! type "fapeed_printModuleDir" >/dev/null 2>&1; then
	echo "Installing Fapeed module via pip"
	pip install .
	echo ""
fi

INSTALLDIR="$(fapeed_printModuleDir)"

echo "Fapeed module installed in: ${INSTALLDIR}"
echo ""

echo "Creating start menu entry..."

DESKTOPFILE=~/.local/share/applications/Fapeed.desktop

touch $DESKTOPFILE

echo "[Desktop Entry]" > $DESKTOPFILE
echo "Name=Fapeed" >> $DESKTOPFILE
echo "Exec=fapeed" >> $DESKTOPFILE
echo "Terminal=false" >> $DESKTOPFILE
echo "Type=Application" >> $DESKTOPFILE
echo "Icon=${INSTALLDIR}/icon.png" >> $DESKTOPFILE

echo "done"

echo ""

echo "Start Fapeed with 'fapeed'"
echo "You also find it in the start menu."

