# -*- coding:utf-8 -*-
# author : ROBINE Thomas

## Imports 

import sys
import os
import argparse
import subprocess
from subprocess import Popen as popen
from pypng.code import png as png

## Delimiter

delimiter = "#####"

## Functions

def loadImage(filepath):
	''' (String) -> int, int, list of list of list of int, dictionary

	>>> loadImage("organigramme.PNG")
	1920, 1080, [[[0, 163, 184, 255], ... , [17, 56, 204, 134]],
						.			  ...			.
						.			  ... 			.
						.			  ...			.
				 [[58, 98, 234, 175], ... , [186, 0, 17, 255]]], {'greyscale': False, 'alpha': True, 'planes': 4, 'bitdepth': 8, 'interlace': 0, 
	'size': (1920, 1080), 'gamma': 0.45455, 'physical': _Resolution(x=4724, y=4724, unit_is_meter=True)}  
	'''
	file = png.Reader(filepath)
	width, height, pixels, info = file.asRGBA8()
	pixels_list = list(pixels)
	pixels_image = []
	channel = 0
	for row in pixels_list:
		line = []
		pixel = []
		for value in row:
			pixel.append(value)
			if channel < 3:
				channel += 1
			else:
				line.append(pixel)
				pixel = []
				channel = 0
		pixels_image.append(line)
	return width, height, pixels_image, info

def sanityCheck(width, height, message):
	''' (list of list of bytes, list of characters) -> Boolean

	>>> sanityCheck(1920, 1080, 'Hello')
	True 
	'''
	capacity = width * height * 4 // 8
	if len(message) <= capacity:
		return True
	return False

def stringToBinary(message):
	''' (String) -> list of binaries

	>>> stringToBinary('Hello!')
	0110100001100101011011000110110001101111001000010010001100100011001000110010001100100011
	'''
	return ''.join([format(ord(i), "08b") for i in message])

def intToBinary(pixel_values):
	''' (list of int) -> list of binaries

	>>> intToBinary([242, 244, 241, 255])
	[11110010, 11110100, 11110001, 11111111]
	'''
	return [format(i, "08b") for i in pixel_values]

def encryptMessage(binary_message, pixels):
	''' (list of binaries, list of list of list of int) -> list of list of list of int

	>>> write(0110100001100101011011000110110001101111001000010010001100100011001000110010001100100011, [[[15, 27, 32, 63], ..., [154, 254, 0, 13]], ..., 
	[[14, 27, 65, 98], ..., [154, 67, 198, 203]]])
	[[[15, 27, 32, 63], ..., [154, 254, 0, 13]], ..., [[14, 27, 65, 98], ..., [154, 67, 198, 203]]]
	'''
	index = 0
	binary_message_length = len(binary_message)
	for row in pixels:
		for pixel_values in row:
			r, g, b, a = intToBinary(pixel_values)
			if index < binary_message_length:
				pixel_values[0] = int(r[:-1]+binary_message[index], 2)
				index += 1
			if index < binary_message_length:
				pixel_values[1] = int(g[:-1]+binary_message[index], 2)
				index += 1
			if index < binary_message_length:
				pixel_values[2] = int(b[:-1]+binary_message[index], 2)
				index += 1
			if index < binary_message_length:
				pixel_values[3] = int(a[:-1]+binary_message[index], 2)
				index += 1
			else:
				break
	return pixels

def from3DTo2D(pixels):
	''' (list of list of list of int) -> list of list of int

	>>> from3DTo2D([[[15, 27, 32, 63], ..., [154, 254, 0, 13]], ..., [[14, 27, 65, 98], ..., [154, 67, 198, 203]]])
	[[15, 27, 32, 63, ..., 154, 254, 0, 13], ..., [14, 27, 65, 98, ..., 154, 67, 198, 203]]
	'''
	matrix = []
	for row in pixels:
		line = []
		for values in row:
			for value in values:
				line.append(value)
		matrix.append(line)
	return matrix

def saveImage(width, height, pixels, info, name):
	''' (int, int, list of list of list of int, dictionary, string) -> NoneType

	>>> saveImage(image_width, image_height, mmodified_pixels, image_info, "modified_"+image)
	'''
	useful_info = ['greyscale', 'alpha', 'planes', 'bitdepth', 'interlace', 'size', 'gamma']
	keywords = {key: info[key] for key in useful_info if key in info}
	pixels2D = from3DTo2D(pixels)
	writer = png.Writer(width, height, **keywords)
	filename, extension = os.path.splitext(name)
	name = filename+"_modified"+extension
	file = open(name, 'wb')
	writer.write(file, pixels2D)
	file.close()

def binaryToString(octets):
	''' (list of characters) -> String

	>>> binaryToString(['11111111', '01010100'])
	Hello
	'''
	string_message = ""
	for byte in octets:
		string_message += chr(int(byte, 2))
		if string_message[-len(delimiter):] == delimiter: #check if we have reached the delimeter
			break
	return string_message[:-len(delimiter)] #remove the delimiter to show the original hidden message

def decryptMessage(pixels):
	''' (list of list of list of int) -> String

	>>> decryptMessage([[[15, 27, 32, 63], ..., [154, 254, 0, 13]], ..., [[14, 27, 65, 98], ..., [154, 67, 198, 203]]])
	Hello!
	'''
	binary_message = ""
	for row in pixels:
		for pixel_values in row:
			r, g, b, a = intToBinary(pixel_values)
			binary_message += r[-1]
			binary_message += g[-1]
			binary_message += b[-1]
			binary_message += a[-1]
	octets = [binary_message[i: i+8] for i in range(0, len(binary_message), 8)]
	return binaryToString(octets)
	
## Main

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = 'Hide a text into a png file or read text from a png file')
	parser.add_argument('image', help = 'png file path, mandatory')
	parser.add_argument('-w', dest = 'write', action = 'store_true', help = 'switch to enable write mode. If not specified, default mode will be set on read mode')
	parser.add_argument('-f', dest = 'file', help = 'Read text from file. If neither [-f] nor [-t] are specified, the text will be read from terminal entry')
	parser.add_argument('-t', dest = 'text', help = 'Read text from arguments. If neither [-f] nor [-t] are specified, the text will be read from terminal entry')
	args = parser.parse_args()

	if args.write != False:
		text = ""
		if args.file != None:
			file = open(args.file, 'r')
			text = file.read()
			file.close()
		elif args.text != None:
			text = args.text
		else:
			text = input('Text to insert :')
		image_width, image_height, pixels, image_info = loadImage(args.image)
		if sanityCheck(image_width, image_height, text):
			text += delimiter
			text_bytes = stringToBinary(text)
			modified_pixels = encryptMessage(text_bytes, pixels)
			saveImage(image_width, image_height, modified_pixels, image_info, args.image)
		else:
			exit("The message can't fit in the image")
	else:
		image_width, image_height, pixels, image_info = loadImage(args.image)
		sp = popen('strings', shell = True, stdout = subprocess.PIPE)
		sys.stdout.write(decryptMessage(pixels)+"\n")
		sys.stdout.close()
		