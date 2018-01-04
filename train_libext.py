#-*- coding: utf-8 -*-
__author__ = 'Administrator'
from ctypes import *
import glob

libc = CDLL("FeatureLibExtract.dll")

# libc.TrainCodebook.argstype = [c_char_p, c_char_p, c_int]
# libc.FeatureLibLoad.argtypes = [c_char_p]

# libc.FeatureExtract.restype = c_int
libc.FeatureLibExtract.argtypes = [c_char_p, c_char_p,c_char_p]


# def train_codebook(folder,codebookfile,featuredim):
	# libc.TrainCodebook(folder,codebookfile,featuredim)


def lib_save(folder,databasefile,codebook_file):
	libc.FeatureLibExtract(folder,databasefile,codebook_file)


if __name__ == '__main__':
	folder = '.\\image\\420111\\01\\03'
	# codebookfile = 'codebook_1024_jiafang_2781.2781'
	# featuredim = 1024
	# train_codebook(folder,codebookfile,featuredim)
	
	feadbfile = '.\\ft\\'+''.join(folder.split('\\')[-3:])+'.ft'
	print feadbfile
	raw_input()
	lib_save(folder,feadbfile)
	# lib_save(folder,feadbfile)
	# lib_save()
