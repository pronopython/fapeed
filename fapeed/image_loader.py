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
from numpy import clip
import numpy
from scipy import ndimage

# Import pygame, hide welcome message because it messes with
# status output
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
from fapeed.fapeed_fapel import FapeedFapel
from fapeed.thread_safe_list import ThreadSafeList


class ImageLoader:

	LOW_BOUND = 50
	HIGH_BOUND = 100

	def __init__(self, filename_queue: ThreadSafeList) -> None:
		self.queue_images = ThreadSafeList()
		self.running = False
		self.pause_crawl = False
		self.filename_queue = filename_queue
		self.scale_size = (100, 100)
		self.mode = 0

	def loader_loop(self) -> None:
		self.running = True
		self.loop_running = True

		print("Image Loader started")

		while self.running:

			if self.filename_queue.length() > 0:
				sleep(0.002)  # type: ignore
				filename = self.filename_queue.pop()
				fapel = FapeedFapel()
				fapel.filename = filename

				try:
					fapel.surface = pygame.image.load(  # type: ignore
						filename
					).convert()
					aspect = fapel.surface.get_width() / fapel.surface.get_height()
					aspect_screen = self.scale_size[0] / self.scale_size[1]
					if aspect > aspect_screen:
						w = self.scale_size[0]
						h = w / aspect
					else:
						h = self.scale_size[1]
						w = h * aspect

					if self.mode == 0:
						fapel.surface = pygame.transform.smoothscale(fapel.surface, (w, h))  # type: ignore
					elif self.mode == 1:	# gray high pass filter
						fapel.surface = pygame.transform.scale(fapel.surface, (int(w / 2), int(h / 2)))  # type: ignore
						fapel.surface = pygame.transform.grayscale(fapel.surface)  # type: ignore
						self.high_pass_gray(fapel.surface)
						fapel.surface = pygame.transform.smoothscale(fapel.surface, (w, h))  # type: ignore
					elif self.mode == 2:	# black/white pixels
						fapel.surface = pygame.transform.smoothscale(fapel.surface, (w, h))  # type: ignore
						fapel.surface = pygame.transform.grayscale(fapel.surface)  # type: ignore
						self.high_pass_black_white(fapel.surface)
					elif self.mode == 3:	# blue/red pixels
						fapel.surface = pygame.transform.smoothscale(fapel.surface, (w, h))  # type: ignore
						fapel.surface = pygame.transform.grayscale(fapel.surface)  # type: ignore
						self.high_pass_blue_red(fapel.surface)
					elif self.mode == 4:	# fast scaling
						fapel.surface = pygame.transform.scale(fapel.surface, (w, h))  # type: ignore

				except pygame.error as message:
					print("Cannot load", filename)
					continue
				except FileNotFoundError as e:
					print("Cannot load", filename)
					continue

				self.queue_images.append(fapel)

				if self.queue_images.length() > self.HIGH_BOUND:
					while self.queue_images.length() > self.LOW_BOUND:
						sleep(0.01)
						if not self.running:
							break
				while self.pause_crawl:
					sleep(1)
				if not self.running:
					break
		self.loop_running = False

	def run(self) -> None:
		self.thread = threading.Thread(target=self.loader_loop, args=())
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
		print("Image Loader stopped")

	def pause(self) -> None:
		self.pause_crawl = True

	def resume(self) -> None:
		self.pause_crawl = False

	def fastsaturation(self, surf, sat): # TODO currently not used, remove?
		arr = pygame.surfarray.pixels3d(surf)
		parr = arr.astype("float", copy=True)
		parr **= 2
		parr[:, :, 0] *= 0.299
		parr[:, :, 1] *= 0.587
		parr[:, :, 2] *= 0.114
		parr[:, :, 0] += parr[:, :, 1] + parr[:, :, 2]
		parr[:, :, 0] **= 0.5
		parr[:, :, 1] = parr[:, :, 0]
		parr[:, :, 2] = parr[:, :, 0]
		arrdash = arr.astype("float", copy=True)
		arrdash -= parr
		arrdash *= sat
		arrdash += parr
		arrdash.clip(0, 255, arrdash)
		arr[:, :, :] = arrdash

	def contrast(self, surf, factor):
		arr = pygame.surfarray.pixels3d(surf)
		corr = (259 * (factor + 255)) / float((255 * (259 - factor)))
		arrdash = arr.astype("int16", copy=False)
		arrdash -= 128
		arrdash *= int(corr)
		arrdash += 128
		arrdash.clip(0, 255, arrdash)
		arr[:, :, :] = arrdash
		# pygame.surfarray.blit_array(surf, arrdash.astype("uint8", copy = False))
		del arrdash
		del arr

	def high_pass_black_white(self, surf):
		arr = pygame.surfarray.pixels3d(surf)

		kernel = numpy.array(
			[
				[-1, -1, -1, -1, -1],
				[-1, 1, 2, 1, -1],
				[-1, 2, 4, 2, -1],
				[-1, 1, 2, 1, -1],
				[-1, -1, -1, -1, -1],
			]
		)

		kernel = numpy.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])


		rgb_kernel = numpy.ones((3, 3, 3))
		rgb_kernel[:, :, 0] = kernel
		rgb_kernel[:, :, 1] = kernel
		rgb_kernel[:, :, 2] = kernel

		arrdash = arr.astype("int16", copy=False)

		parr = arrdash.astype("float", copy=True)
		parr /= 128

		highpass_5x5 = ndimage.convolve(parr, rgb_kernel)

		pygame.surfarray.blit_array(surf, highpass_5x5.astype("uint8", copy=False))

	def high_pass_blue_red(self, surf):
		arr = pygame.surfarray.pixels3d(surf)

		kernel = numpy.array(
			[
				[-1, -1, -1, -1, -1],
				[-1, 1, 2, 1, -1],
				[-1, 2, 4, 2, -1],
				[-1, 1, 2, 1, -1],
				[-1, -1, -1, -1, -1],
			]
		)

		# kernel = numpy.array([[-1, -1, -1],
		#           [-1,  8, -1],
		#           [-1, -1, -1]])

		rgb_kernel = numpy.ones((5, 5, 3))
		# rgb_kernel = numpy.ones((3, 3, 3))
		rgb_kernel[:, :, 0] = kernel
		rgb_kernel[:, :, 1] = kernel
		rgb_kernel[:, :, 2] = kernel


		arr -= 128
		parr = arr.astype("float", copy=True)
		parr /= 128

		highpass_5x5 = ndimage.convolve(parr, rgb_kernel)
		highpass_5x5[:, :, 0] = highpass_5x5[:, :, 0]
		highpass_5x5[:, :, 1] = 13
		highpass_5x5[:, :, 2] = 65

		pygame.surfarray.blit_array(surf, highpass_5x5.astype("uint8", copy=False))
	

	def high_pass_gray(self, surf):
		arr = pygame.surfarray.pixels3d(surf)

		kernel = numpy.array(
			[
				[-1, -1, -1, -1, -1],
				[-1, 1, 2, 1, -1],
				[-1, 2, 4, 2, -1],
				[-1, 1, 2, 1, -1],
				[-1, -1, -1, -1, -1],
			]
		)

		parr = arr.astype("float", copy=True)

		highpass_5x5 = ndimage.convolve(parr[:, :, 0], kernel)

		parr = numpy.empty((parr.shape[0], parr.shape[1], 3))
		parr[:, :, 0] = highpass_5x5
		parr[:, :, 1] = highpass_5x5
		parr[:, :, 2] = highpass_5x5

		parr /= 20
		arr = parr.astype("int", copy=True)
		arr += 150
		pygame.surfarray.blit_array(surf, arr.astype("uint8", copy=False))

		self.contrast(surf, 150)
