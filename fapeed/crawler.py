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

import os
from random import randint
import threading
from time import sleep
from fapeed.thread_safe_list import ThreadSafeList


class Crawler:

	LOW_BOUND = 80
	HIGH_BOUND = 100

	def __init__(self, rootpath) -> None:
		self.queue_filenames = ThreadSafeList()
		self.running = False
		self.rootpath = rootpath
		self.pause_crawl = False

	def crawler_loop(self) -> None:
		WORKING_EXTENSIONS = [".jpg", ".jpeg", ".tif", ".tiff", ".png", ".gif"]
		self.running = True
		self.loop_running = True
		skip_files = randint(0, 1000)

		print("Crawler started")

		while self.running:

			for root, d_names, f_names in os.walk(self.rootpath):
				for f_name in f_names:
					if skip_files > 0:
						skip_files -= 1
						continue
					else:
						skip_files = randint(0, 1000)
					sleep(0.0001)
					f_fullPath = os.path.join(root, f_name)
					f_nameOnly, f_ext = os.path.splitext(f_name)
					if f_ext.lower() in WORKING_EXTENSIONS:
						self.queue_filenames.append(f_fullPath)

						if self.queue_filenames.length() > self.HIGH_BOUND:
							while self.queue_filenames.length() > self.LOW_BOUND:
								sleep(0.01)
								if not self.running:
									break
					while self.pause_crawl:
						sleep(1)
				if not self.running:
					break
		self.loop_running = False

	def run(self) -> None:
		self.thread = threading.Thread(target=self.crawler_loop, args=())
		self.thread.daemon = True  # so these threads get killed when program exits
		self.thread.start()

	def is_running(self) -> bool:
		return self.thread.is_alive()

	def close(self) -> None:
		if not self.is_running():
			self.thread.join()

	def stop(self) -> None:
		self.running = False
		self.pause_crawl = False
		while self.loop_running:
			sleep(0.06)
		self.close()
		print("Crawler stopped")

	def pause(self) -> None:
		self.pause_crawl = True

	def resume(self) -> None:
		self.pause_crawl = False
