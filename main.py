# -*- coding:utf-8 -*-
# author : ROBINE Thomas

## Imports 

import argparse
from pypng.code import png as png

## Functions

def sanityCheck(image, message):
	''' (list of list of bytes, list of characters) -> Boolean

	>>> sanityCheck([[156, 203, 187], [98, 23, 234]], 'Bonjour à tous')
	False
	>>> sanityCheck([[156, 203, 187], [98, 23, 234]], 'Hello')
	True 
	'''
	print(len(image), len(image[0]))

def writeToRGB():
	print()

def writeToRGBA():
	print()

def referral():
	print()

def read():
	print()


## Main

parser = argparse.ArgumentParser()

parser.add_argument('-png', dest = 'image', required = True)
parser.add_argument('-m', dest = 'mode', choices = ['read', 'r', 'write', 'w'])
parser.add_argument('-f', dest = 'file')
parser.add_argument('-t', dest = 'text')

args = parser.parse_args()

mode = args.mode
image = args.image
file = args.file
text = args.text

if mode == None or mode == "read" or mode == 'r':
	print('mode : read mode')
	print('image :', image)
else:
	print('mode : write mode')
	print('image : ', image)
	if file != None:
		print('Reading from :', file)
	elif text != None:
		print('Inserting :', text)
	else:
		text = input('Text to insert :')
		print('text :', text)
		sanityCheck(image, text)