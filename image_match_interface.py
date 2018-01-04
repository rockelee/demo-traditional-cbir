#-*- coding: utf-8 -*-
__author__ = 'Administrator'
from ctypes import *
import glob

libc = CDLL("hes_sift_fv_dll.dll")

libc.CodebookLoad.restype = c_int
libc.CodebookLoad.argtypes = [c_char_p]

libc.FeatureLibLoad.restype = c_int
libc.FeatureLibLoad.argtypes = [c_char_p]

libc.FeatureLibRelease.restype = c_int
libc.FeatureLibRelease.argtypes = [c_char_p]

type_p_int = POINTER(c_int)
# libc.FeatureRelease.restype = c_int
libc.FeatureRelease.argtypes = [type_p_int]

# libc.ImageIdRelease.restype = c_int
libc.ImageIdRelease.argtypes = [c_char_p]

# libc.FeatureExtract.restype = type_p_int
# libc.FeatureExtract.argtypes = [c_char_p]

# libc.FeatureMatch.restype = c_char_p
# libc.FeatureMatch.argtypes = [c_char_p, type_p_int]

libc.FeatureExtractMatch.argtypes = [c_char_p, c_char_p]

def codebook_load(cb):
    return libc.CodebookLoad(cb)

def feature_database_load(featureFilePath):
    # print type(featureFilePath)
    return libc.FeatureLibLoad(featureFilePath)

def feature_database_release(featureFilePath):
    return libc.FeatureLibRelease(featureFilePath)

def feature_release(pfeature):
    # print libc.FeatureRelease(pFeature)
    libc.FeatureRelease(pfeature)
    # return libc.FeatureRelease(pfeature)

def match_release(image_id):
    libc.ImageIdRelease(image_id)
    # return libc.ImageIdRelease(image_id)

# def ext_img(imgPath):
    # # print type(imgPath)
    # c_ext = libc.FeatureExtract(imgPath)
    # return libc.FeatureExtract(imgPath)
    

# def match_img(featureFilePath, pfeature):
    # c_match = libc.FeatureMatch(featureFilePath,pfeature)
    # c_match_p = c_char_p(c_match)
    # # print c_match,type(c_match)
    # # print c_match_p,type(c_match_p)
    # return c_match_p
    

def ext_match_img(featureFilePath,imagePath):
    # libc.FeatureExtractMatch.restype = c_char_p
    c_match = libc.FeatureExtractMatch(featureFilePath,imagePath)
    c_match_p = c_char_p(c_match)
    # return libc.FeatureExtractMatch(featureFilePath, imagePath)
    # print c_match,type(c_match)
    # print c_match_p,type(c_match_p)
    return c_match_p

if __name__ == '__main__':
    
    print codebook_load('.\\codebook_1024_jiafang_2781.cb')
    # folder = 'C:\\Users\LILINHAN\\Desktop\\wx\\MapMaker\\photo\\yx\\a\\Loc'#"E:\\dataset\\MapMaker\\photo\\yx\\a"
    featureFilePath1 = ".\\ft\\4201110101.ft"    #默认本目录
    img = ".\\1_15\\01\\215_142_0_day_shang.jpg"

    # feature_database_extract_save(folder, featureFilePath)   
    print feature_database_load(featureFilePath1)           #测试加载特征文件
    print feature_database_load(featureFilePath1)           #测试加载特征文件
    print feature_database_release(featureFilePath1)        #测试释放特征文件
    print '\n\n'

    print feature_database_load(featureFilePath1)
    match_results = ext_match_img(featureFilePath1, img)    #测试提取并匹配图片,该函数内部会释放提取的特征
    print type(match_results), match_results
    match_release(match_results)                           #测试释放匹配结果
    print '\n\n'


    b = ext_img(img)                                       #测试提取特征
    print type(b),b
    match_results = match_img(featureFilePath1, b)          #测试匹配图片
    print type(match_results), match_results
    feature_release(b)                                     #需要释放特征
    match_release(match_results)                           #需要释放匹配结果

    featureFilePath2 = ".\\ft\\4201110101.ft"    #默认本目录
    img = ".\\1_15\\02\\318_460_day_center_xia.jpg"
    print feature_database_load(featureFilePath2)           #测试加载特征文件
    print feature_database_release(featureFilePath2)        #测试释放特征文件
    print '\n\n'

    feature_database_load(featureFilePath2)
    match_results = ext_match_img(featureFilePath2, img)    #测试提取并匹配图片,该函数内部会释放提取的特征
    print type(match_results), match_results
    match_release(match_results)                           #测试释放匹配结果
    print '\n\n'


    b = ext_img(img)                                       #测试提取特征
    print type(b),b
    match_results = match_img(featureFilePath2, b)          #测试匹配图片
    print type(match_results), match_results
    feature_release(b)                                     #需要释放特征
    match_release(match_results)                           #需要释放匹配结果

