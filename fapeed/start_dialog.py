#!/usr/bin/python3
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

import abc
import os
from tkinter import (
	BOTH,
	N,
	S,
	W,
	E,
	Button,
	Entry,
	Frame,
	Label,
	OptionMenu,
	StringVar,
	Tk,
	filedialog,
)


class SelectionSingleItem:
	__metaclass__ = abc.ABCMeta

	def __init__(
		self,
		description,
		initValue,
	) -> None:
		self.description = description
		self.initValue = initValue


class SelectionFolder(SelectionSingleItem):
	def __init__(self, parent, description, initValue) -> None:
		super().__init__(description, initValue)
		self.frame = Frame(parent)
		self.value = self.initValue
		self.frame.columnconfigure(1, weight=1)
		Label(self.frame, text=description).grid(column=0, row=0, sticky=W)
		self.dirText = StringVar(self.frame, self.initValue)
		self.dirText.trace_add("write", self.valueChanged)
		Entry(self.frame, textvariable=self.dirText).grid(column=1, row=0, sticky=W + E)
		Button(self.frame, text="Select", command=self.buttonClicked).grid(
			column=2, row=0, sticky=E
		)

	def buttonClicked(self) -> None:
		selected_folder = filedialog.askdirectory()
		if selected_folder != "" and len(selected_folder) > 0:
			selected_folder = os.path.abspath(selected_folder)
			self.dirText.set(selected_folder)

	def valueChanged(self, *args) -> None:
		self.value = self.dirText.get()

	def getFrame(self) -> Frame:
		return self.frame


class SelectionList(SelectionSingleItem):
	def __init__(self, parent, description, initValue, list_values) -> None:
		super().__init__(description, initValue)
		self.frame = Frame(parent)
		self.list_values = list_values
		self.listText = StringVar(self.frame, self.initValue)
		self.value = self.list_values.index(self.listText.get())
		self.frame.columnconfigure(1, weight=1)
		Label(self.frame, text=description).grid(column=0, row=0, sticky=W)

		self.listText.trace_add("write", self.valueChanged)

		OptionMenu(self.frame, self.listText, *list_values).grid(
			column=1, row=0, sticky=W
		)

	def valueChanged(self, *args) -> None:
		self.value = self.list_values.index(self.listText.get())

	def getFrame(self) -> Frame:
		return self.frame


class StartDialog:
	def __init__(self, modes):
		self.root_folder = ""
		self.mode = 0
		self.window = Tk()

		self.window.geometry("800x200")
		self.window.title("Fapeed")

		frm = Frame(self.window)
		frm.grid(sticky=N + S + W + E)
		frm.columnconfigure(0, weight=1)

		row = 0

		Label(frm, text="Slideshow settings").grid(column=0, row=row, sticky=W)
		row += 1

		self.selection_folder = SelectionFolder(frm, "Slideshow root dir", ".")
		self.selection_folder.getFrame().grid(
			column=0, row=row, ipadx=10, padx=10, sticky=W + E
		)
		row += 1

		self.selection_mode = SelectionList(frm, "Mode", modes[0], modes)
		self.selection_mode.getFrame().grid(
			column=0, row=row, ipadx=10, padx=10, sticky=W + E
		)
		row += 1

		bframe = Frame(frm)
		Button(bframe, text="Start", command=self.actionStart).grid(
			column=1, row=0, ipadx=5, sticky=E
		)
		Button(bframe, text="Exit", command=self.actionExit).grid(
			column=0, row=0, ipadx=5, sticky=E
		)
		bframe.grid(column=0, row=row, sticky=E)
		row += 1

		frm.pack(expand=True, fill=BOTH)

		self.window.protocol("WM_DELETE_WINDOW", self.actionExit)

		self.window.mainloop()

	def actionStart(self):
		self.root_folder = self.selection_folder.value
		self.mode = self.selection_mode.value
		self.window.destroy()

	def actionExit(self):
		exit()
