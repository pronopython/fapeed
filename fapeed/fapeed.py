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

import math
import os
import platform
from random import randint
import random
import subprocess
import sys
import time
from typing import NoReturn
from fapeed.crawler import Crawler
from fapeed.image_loader import ImageLoader
from fapeed.start_dialog import StartDialog

from fapeed.thread_safe_list import ThreadSafeList


# Import pygame, hide welcome message because it messes with
# status output
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


import pygame


class FapeedMainApp:

	MODES = ["dream", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

	def __init__(self) -> None:
		self.size = self.weight, self.heigth = (
			1400,
			768,
		)
		self.running = False

	def open_file(self, path) -> None:
		if platform.system() == "Windows":
			os.startfile(path)  # type: ignore
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path])
		else:
			subprocess.Popen(["xdg-open", path])

	def run(self) -> NoReturn:  # type: ignore

		self.root_dir = "."

		mode = 0

		if len(sys.argv) == 1:
			startDialog = StartDialog(FapeedMainApp.MODES)
			self.root_dir = startDialog.root_folder
			mode = startDialog.mode
		else:
			self.root_dir = sys.argv[1]
			if len(sys.argv) > 2:
				mode = int(sys.argv[2])

		pygame.init()

		pygame.display.set_caption("Fapeed")

		pygame.font.init()
		# TODO add icon
		# icon = pygame.image.load(dir_helper.get_install_dir() + "/icon.png")
		# pygame.display.set_icon(icon)

		self.display = pygame.display.set_mode(
			self.size, pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
		)

		clock = pygame.time.Clock()

		self.running = True

		self.crawler = Crawler(self.root_dir)
		self.crawler.run()

		self.image_loader = ImageLoader(self.crawler.queue_filenames)

		self.display = pygame.display.set_mode(
			self.size, pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF
		)

		self.last_shown_time = 0

		self.current_fapel = None
		self.current_fapels = []
		self.rewind_fapels = []
		offset_x = 0
		offset_y = 0
		max_rewind_fapels = 100

		#########################################################
		# Mode definition
		#########################################################

		if mode == 1:
			macro_block_w = 50
			macro_block_h = 50

			self.fps = 3

			pixelated = True
			setpix_table = [1, 1, 3, 3, 3, 5, 5, 8]

			simultaniously_shown_fapels = 5  # was 4
			random_position = True
			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		# Dream Mode
		if mode == 0:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 0.5

			pixelated = True
			setpix_table = [20, 50, 50, 50, 50, 80, 100, 150]
			simultaniously_shown_fapels = 5  # was 4
			random_position = True
			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		if mode == 2:
			macro_block_w = 10
			macro_block_h = 10

			self.fps = 2

			pixelated = True
			setpix_table = [1, 1, 3, 3, 3, 5, 5, 8]
			simultaniously_shown_fapels = 5  # was 4

			random_position = True
			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		if mode == 3:
			macro_block_w = 100
			macro_block_h = 100

			self.fps = 8

			pixelated = True
			setpix_table = [1, 1, 3, 3, 3, 5, 5, 8]
			simultaniously_shown_fapels = 5  # was 4

			random_position = True
			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		# one pic only
		if mode == 4:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 15

			pixelated = False
			setpix_table = [0]
			simultaniously_shown_fapels = 1

			random_position = False

			clear_screen = True
			colored_screen = False
			self.image_loader.mode = 4
			only_draw_on_change = True
		# one pic only
		if mode == 5:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 0.8

			simultaniously_shown_fapels = 2  # was 1

			pixelated = True
			setpix_table = [10]

			random_position = False

			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		# one pic only
		if mode == 6:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 15

			pixelated = False
			setpix_table = [0]

			simultaniously_shown_fapels = 2  # 2 will result in left/right position

			random_position = True

			clear_screen = False
			colored_screen = False
			self.image_loader.mode = 0
			only_draw_on_change = False
		# one pic only
		if mode == 7:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 1

			pixelated = False
			setpix_table = [0]
			simultaniously_shown_fapels = 1

			random_position = False

			clear_screen = True
			colored_screen = True

			self.image_loader.mode = 0
			only_draw_on_change = False

		# as mode 2 but more simultaniously
		if mode == 8:
			macro_block_w = 10
			macro_block_h = 10

			self.fps = 4

			pixelated = True
			setpix_table = [1, 1, 3, 3, 3, 5, 5, 8]
			simultaniously_shown_fapels = 7  # was 6

			random_position = True
			clear_screen = False
			colored_screen = False

			self.image_loader.mode = 0
			only_draw_on_change = False

		# one pic only, as 6 but with more overlap
		if mode == 9:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 15

			pixelated = False
			setpix_table = [0]

			simultaniously_shown_fapels = 1

			random_position = True

			clear_screen = False
			colored_screen = False

			self.image_loader.mode = 0
			only_draw_on_change = False

		# one pic only // convolute
		if mode == 10:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 0.5

			pixelated = True
			setpix_table = [10, 15, 15]

			simultaniously_shown_fapels = 1  # 2 will result in left/right position

			random_position = True

			clear_screen = False
			colored_screen = False

			self.image_loader.mode = 2
			only_draw_on_change = False

		# one pic only convolute gray
		if mode == 11:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 10

			pixelated = False
			setpix_table = [0]
			simultaniously_shown_fapels = 1

			random_position = False

			clear_screen = True
			colored_screen = True
			self.image_loader.mode = 1
			only_draw_on_change = False

		# one pic only // convolute
		if mode == 12:
			macro_block_w = 3
			macro_block_h = 3

			self.fps = 0.5

			pixelated = True
			setpix_table = [10, 15, 15]

			simultaniously_shown_fapels = 1  # 2 will result in left/right position

			random_position = True

			clear_screen = False
			colored_screen = False

			self.image_loader.mode = 3
			only_draw_on_change = False

		#########################################################
		# Start fapeed slideshow
		#########################################################

		self.image_loader.run()

		info = pygame.display.Info()
		view_w, view_h = info.current_w, info.current_h
		self.image_loader.scale_size = (view_w, view_h)  # type: ignore

		status_text = ""
		pause = False
		rewind_active = False
		rewind_position = 0
		show_info = False
		monofont = pygame.font.SysFont("monospace", 15)

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_PLUS:
						self.fps += 1
					elif event.key == pygame.K_MINUS:
						self.fps -= 1
						if self.fps < 1:
							self.fps = 1
					elif event.key == pygame.K_i:
						show_info = not show_info
					elif event.key == pygame.K_LEFT:
						if rewind_active:
							rewind_position += 1
							if rewind_position >= len(self.rewind_fapels):
								rewind_position = len(self.rewind_fapels) - 1
						else:
							rewind_active = True
							pause = True
							rewind_position = 0
							pygame.display.set_caption("Fapeed (rewind)")
					elif event.key == pygame.K_RIGHT:
						if rewind_active:
							rewind_position -= 1
							if rewind_position <= 0:
								rewind_position = 0
						else:
							rewind_active = True
							pause = True
							rewind_position = 0
							pygame.display.set_caption("Fapeed (rewind)")
					elif event.key == pygame.K_n:
						if rewind_active:
							self.open_file(self.rewind_fapels[rewind_position].filename)
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						pause = not pause
						rewind_active = False
						if pause:
							pygame.display.set_caption("Fapeed (paused)")
						else:
							pygame.display.set_caption("Fapeed")

			info = pygame.display.Info()
			view_w, view_h = info.current_w, info.current_h
			self.image_loader.scale_size = (view_w, view_h)  # type: ignore

			time_distance = 1 / self.fps
			current_time_distance = time.time() - self.last_shown_time
			redraw = not only_draw_on_change

			# fetch next image
			if not pause and (
				time_distance < current_time_distance
				and self.image_loader.queue_images.length() > 0
			):
				status_text = "FPS:" + str(math.ceil(1 / current_time_distance))

				self.current_fapel = self.image_loader.queue_images.pop()

				self.current_fapels.insert(0, self.current_fapel)
				self.rewind_fapels.insert(0, self.current_fapel)

				if len(self.current_fapels) > simultaniously_shown_fapels:
					self.current_fapels.pop()
				if len(self.rewind_fapels) > max_rewind_fapels:
					self.rewind_fapels.pop()

				if random_position:
					offset_y = randint(
						0, view_h - self.current_fapel.surface.get_height()
					)
					if int((view_w - self.current_fapel.surface.get_width())) < 30:
						self.current_fapel.offset_x = 0
					else:
						fixed_x = list(
							range(
								0,
								view_w - self.current_fapel.surface.get_width(),
								int(
									(view_w - self.current_fapel.surface.get_width())
									/ 20
								),
							)
						)
						random.shuffle(fixed_x)
						offset_x = fixed_x[0]
						self.current_fapel.offset_x = offset_x
						self.current_fapel.offset_y = offset_y

						best_x = offset_x
						best_score = -1
						for i in range(0, 30):
							score = 0
							for x in range(0, view_w, 30):
								overlaps = 0
								for fapel in self.current_fapels:
									if (
										fapel.offset_x < x
										and fapel.offset_x + fapel.surface.get_width()
										> x
									):
										overlaps += 1
								score += overlaps * overlaps
							if score < best_score or best_score < 0:
								best_score = score
								best_x = offset_x
							if len(fixed_x) > i + 1:
								offset_x = fixed_x[i]
							else:
								offset_x = randint(
									0, view_w - self.current_fapel.surface.get_width()
								)
							self.current_fapel.offset_x = offset_x
						self.current_fapel.offset_x = best_x
				else:
					self.current_fapel.offset_x = int(
						(view_w / 2) - (self.current_fapel.surface.get_width() / 2)
					)
					self.current_fapel.offset_y = int(
						(view_h / 2) - (self.current_fapel.surface.get_height() / 2)
					)

				self.current_fapel.setpix = random.choice(setpix_table)

				self.last_shown_time = time.time()

				redraw = True

			if redraw and self.current_fapel != None and not pause:
				if clear_screen:
					if not colored_screen:
						color = (0, 0, 0)
					else:
						color = pygame.transform.average_color(self.current_fapel.surface)  # type: ignore

					pygame.draw.rect(
						self.display,
						color,
						(
							0,
							0,
							view_w,
							view_h,
						),
					)

				self.current_fapels.reverse()
				if pixelated:
					for pos, current_fapel in enumerate(self.current_fapels):
						blocks_x = math.ceil(
							current_fapel.surface.get_width() / macro_block_w
						)
						blocks_y = math.ceil(
							current_fapel.surface.get_height() / macro_block_h
						)
						for i in range(
							0,
							int(
								((blocks_x * blocks_y) / current_fapel.setpix)
								* ((pos + 1) / len(self.current_fapels))
							),
						):
							dx = randint(0, blocks_x)
							dy = randint(0, blocks_y)
							edge = randint(0, 50)
							if (
								dx < edge
								or dy < edge
								or dx > blocks_x - edge
								or dy > blocks_y - edge
							):
								continue
							self.display.blit(
								current_fapel.surface,
								(
									current_fapel.offset_x + dx * macro_block_w,
									current_fapel.offset_y + dy * macro_block_h,
								),
								(
									dx * macro_block_w,
									dy * macro_block_h,
									macro_block_w,
									macro_block_h,
								),
							)
				else:
					self.display.blit(
						self.current_fapel.surface,
						(self.current_fapel.offset_x, self.current_fapel.offset_y),
					)
				self.current_fapels.reverse()

				if show_info:
					label = monofont.render(status_text, 1, (255, 0, 0))
					self.display.blit(label, (3, 3))
				pygame.display.update()

				pygame.display.flip()
				redraw = False

			if pause and rewind_active:
				color = (0, 0, 0)
				pygame.draw.rect(
					self.display,
					color,
					(
						0,
						0,
						view_w,
						view_h,
					),
				)

				label = monofont.render("rewind", 1, (255, 0, 0))
				self.display.blit(label, (3, 3))

				rewind_fapel = self.rewind_fapels[rewind_position]

				self.display.blit(
					rewind_fapel.surface,
					(rewind_fapel.offset_x,rewind_fapel.offset_y),
				)
				pygame.display.update()

				pygame.display.flip()

		self.crawler.stop()
		self.image_loader.stop()


if __name__ == "__main__":
	app = FapeedMainApp()
	app.run()


def main() -> NoReturn:
	app = FapeedMainApp()
	app.run()
