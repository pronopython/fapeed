@echo off
REM ##############################################################################################
REM #
REM # Fapeed - Adult Slideshow App
REM #
REM # For updates see git-repo at
REM # https://github.com/pronopython/fapeed
REM #
REM ##############################################################################################
REM #
REM # Copyright (C) PronoPython
REM #
REM # Contact me at pronopython@proton.me
REM #
REM # This program is free software: you can redistribute it and/or modify it
REM # under the terms of the GNU General Public License as published by the
REM # Free Software Foundation, either version 3 of the License, or
REM # (at your option) any later version.
REM #
REM # This program is distributed in the hope that it will be useful,
REM # but WITHOUT ANY WARRANTY; without even the implied warranty of
REM # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM # GNU General Public License for more details.
REM #
REM # You should have received a copy of the GNU General Public License
REM # along with this program.  If not, see <https://www.gnu.org/licenses/>.
REM #
REM ##############################################################################################

WHERE fapeed_printModuleDir
IF %ERRORLEVEL% NEQ 0 (
	ECHO installing Fapeed module via pip
	pip install .
)

for /f %%i in ('fapeed_printModuleDir') do set INSTALLDIR=%%i
echo Fapeed module installed in: %INSTALLDIR%

echo.
echo Installing Start Menu shortcut

pyshortcut -n Fapeed -i "%INSTALLDIR%\icon.ico"  "%INSTALLDIR%\..\..\..\Scripts\fapeed_no_cli.exe"

echo done

echo Start Fapeed with 'fapeed'
echo You also find it in the start menu.

pause
