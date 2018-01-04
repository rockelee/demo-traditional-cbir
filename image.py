#-*- coding: utf-8 -*-

import wx
import os
import glob
import time
from image_match_interface import feature_database_load,feature_database_release, ext_match_img, feature_release, match_release, codebook_load
from train_libext import lib_save
from ctypes import *

class myFrame(wx.Frame):
	def __init__(self):
		self.title='Image Matching'
		
		wx.Frame.__init__(self,parent=None,id=-1,pos=(0,0),title=self.title,size=(1280,720), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		
		self.panel1=wx.Panel(self,-1,pos=(-1,-1),size=(720,720),style=wx.SIMPLE_BORDER)
		self.multiText = wx.TextCtrl(self.panel1,-1,'',size=(720,440),pos=(-1,280),style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.multiText.SetInsertionPoint(0) 
		
		self.scroll3=wx.ScrolledWindow(self,-1,size=(555,240),pos=(720,-1))
		self.scroll3.SetScrollbars(1,1,1000,800)
		self.scroll3.SetScrollRate(10, 10)
		
		self.scroll2=wx.ScrolledWindow(self,-1,size=(555,454),pos=(720,240))
		self.panel2 = wx.Panel( self.scroll2, -1 )
		self.scroll2.SetScrollbars(1,1,1000,2000)
		self.scroll2.SetScrollRate(10, 10)
		
		wx.StaticText(self.panel1, -1, '码本路径：'.decode('utf-8'), (40,12),name='codebook')
		self.multiText1 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,10),style=wx.TE_READONLY)
		self.multiText1.SetInsertionPoint(0) 
		self.button12 = wx.Button(self.panel1, -1, '选择'.decode('utf-8'),pos=(400,10),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.cb_load, self.button12)
		
		wx.StaticText(self.panel1, -1, '样本图像路径：'.decode('utf-8'),pos=(16,42), name='training_data') #需要改变字体
		self.multiText2 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,40),style=wx.TE_READONLY)
		self.multiText2.SetInsertionPoint(0)
		self.button1 = wx.Button(self.panel1, -1, '选择'.decode('utf-8'), pos=(400, 40),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.choose_training_data, self.button1)
		self.button11 = wx.Button(self.panel1, -1, '提取特征库'.decode('utf-8'), pos=(460, 40), size=(80,25),name='ext_lib')
		self.Bind(wx.EVT_BUTTON, self.ext_lib, self.button11)
		 
		wx.StaticText(self.panel1, -1, '特征库路径：'.decode('utf-8'),(28,72), name='feature_lib')
		self.multiText3 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,70),style=wx.TE_READONLY)
		self.multiText3.SetInsertionPoint(0)
		self.button2 = wx.Button(self.panel1, -1, '加载'.decode('utf-8'), pos=(400, 70), size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.feadb_load, self.button2)
		self.button5 = wx.Button(self.panel1, -1, '释放'.decode('utf-8'), pos=(460, 70), size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.feadb_release, self.button5)
		self.button9 = wx.Button(self.panel1, -1, '查看'.decode('utf-8'), pos=(520, 70), size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.check_feadb, self.button9)
		
		wx.StaticText(self.panel1, -1, '待匹配特征库：'.decode('utf-8'),(16,102), name='test_data')
		self.multiText4 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,100),style=wx.TE_READONLY)
		self.multiText4.SetInsertionPoint(0)
		self.button10 = wx.Button(self.panel1, -1, '选择'.decode('utf-8'),pos=(400, 100),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.choose_feadb, self.button10)
		self.button13 = wx.Button(self.panel1, -1, '全匹配'.decode('utf-8'),pos=(460, 100),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.choose_feadb1, self.button13)
		
		wx.StaticText(self.panel1, -1, '样本图像路径：'.decode('utf-8'),(16,132), name='test_data')
		self.multiText8 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,130),style=wx.TE_READONLY)
		self.multiText8.SetInsertionPoint(0)
		self.button19 = wx.Button(self.panel1, -1, '选择'.decode('utf-8'), pos=(400, 130),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.matchJpgPath, self.button19)
		
		wx.StaticText(self.panel1, -1, '测试图像路径：'.decode('utf-8'),(16,162), name='test_data')
		self.multiText5 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,160),style=wx.TE_READONLY)
		self.multiText5.SetInsertionPoint(0)
		self.button3 = wx.Button(self.panel1, -1, '选择1'.decode('utf-8'), pos=(400, 160),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.openjpg1, self.button3)
		self.button4 = wx.Button(self.panel1, -1, '匹配'.decode('utf-8'), pos=(460, 160),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.ext_match, self.button4)
		self.button8 = wx.Button(self.panel1, -1, '释放1'.decode('utf-8'), pos=(520, 160),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.mat_release, self.button8)
		
		# wx.StaticText(self.panel1, -1, '测试图像路径：'.decode('utf-8'),(16,192), name='test_data')
		# self.multiText6 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,190),style=wx.TE_READONLY)
		# self.multiText6.SetInsertionPoint(0)
		# self.button17 = wx.Button(self.panel1, -1, '选择2'.decode('utf-8'), pos=(400, 190),size=(60,25))
		# self.Bind(wx.EVT_BUTTON,self.openjpg1,self.button17)
		# self.button5 = wx.Button(self.panel1, -1, '提取特征'.decode('utf-8'), pos=(460, 190),size=(60,25))
		# self.Bind(wx.EVT_BUTTON, self.ext, self.button5)
		# self.button6 = wx.Button(self.panel1, -1, '匹配特征'.decode('utf-8'), pos=(520, 190),size=(60,25))
		# self.Bind(wx.EVT_BUTTON, self.match, self.button6)
		# self.button7 = wx.Button(self.panel1, -1, '释放特征'.decode('utf-8'), pos=(580, 190),size=(60,25))
		# self.Bind(wx.EVT_BUTTON, self.fea_release, self.button7)
		# self.button18 = wx.Button(self.panel1, -1, '释放2'.decode('utf-8'), pos=(640, 190),size=(60,25))
		# self.Bind(wx.EVT_BUTTON,self.mat_release,self.button18)
		
		wx.StaticText(self.panel1, -1, '统计测试路径：'.decode('utf-8'),(16,192), name='test_data')
		self.multiText7 = wx.TextCtrl(self.panel1,-1,'',size=(300,25),pos=(100,190),style=wx.TE_READONLY)
		self.multiText7.SetInsertionPoint(0)
		self.button14 = wx.Button(self.panel1, -1, '选择'.decode("utf-8"), pos=(400,190),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.openjpg_statistical,self.button14)
		self.button16 = wx.Button(self.panel1, -1, '上一张'.decode("utf-8"), pos=(460,190),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.pre_img, self.button16)
		self.button15 = wx.Button(self.panel1, -1, '下一张'.decode("utf-8"), pos=(520,190),size=(60,25))
		self.Bind(wx.EVT_BUTTON, self.next_img, self.button15)
		
		self.choose_training_data_flag=0
		self.fealib_release_flag=0
		self.img_flag=0
		self.fea_release_flag=0
		self.mat_release_flag=0
		self.mat_release_flag2=0
		self.choose_lib_flag=0
		self.mach_jpg_path_flag=0
		self.statistical_flag=0
		self.codebook_flag=0
		
		self.train_pic_path=os.getcwd()
		self.feature_file_path=os.getcwd()
		self.test_pic_path=os.getcwd()
		self.statistical_test_path = os.getcwd()
		self.result_path=os.getcwd()
		self.lib=[]
		self.statistical_test_jpgs=[]
		
	def choose_training_data(self,event):
		print 'choose_training_data'
		self.multiText.AppendText('\n'+'选择样本路径'.decode('utf-8')+'\n')
		dlg=wx.DirDialog(self,message='choose a directory',
						defaultPath=self.train_pic_path,
						style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON,
					 pos = wx.DefaultPosition, size = wx.DefaultSize,name='training_data_path')
		if dlg.ShowModal() == wx.ID_OK:
			a=dlg.GetPath().split('\\')[-4:]#('image')[-1].split('\\')
			if len(a) == 4 and a[0] == 'image' and len(a[1])==6 and len(a[2])==2 and len(a[3])==2:
				self.train_pic_path=os.path.split(dlg.GetPath())[0] #self.train_pic_path用于保存当前选中目录的父目录,便于以后直接进入该父目录
				self.train_pic_path1=dlg.GetPath()  
				self.choose_training_data_flag=1
				self.multiText2.SetValue(self.train_pic_path1)
			else:
				self.multiText.AppendText('\n'+'样本路径不符合要求'.decode('utf-8')+'\n')
		dlg.Destroy()
	
	def ext_lib(self,event):
		print 'ext_lib'
		if self.choose_training_data_flag==0:
			print '没有选择样本路径'.decode('utf-8')
			self.multiText.AppendText('\n'+'选择样本路径'.decode('utf-8')+'\n')
		else :
			feadbfile = '.\\ft\\'+''.join(self.train_pic_path1.split('\\')[-3:])+ '_v' +time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()) +'.ft'
			self.multiText.AppendText('\n'+'正在提取特征库，请耐心等待. . . '.decode('utf-8')+'\n')
			print feadbfile
			print self.cb_path
			lib_save(self.train_pic_path1, feadbfile, self.cb_path)
			self.multiText.AppendText('\n'+'特征库提取完成'.decode('utf-8')+'\n')
	
	def feadb_load(self,event):
		print 'loading feadb'
		self.multiText.AppendText('\n'+'加载特征库文件. . .'.decode('utf-8')+'\n')
		file_wildcard = "feature files(*.ft)|*.ft|All files(*.*)|*.*"
		dlg = wx.FileDialog(self, message="load feature",
							defaultDir=self.feature_file_path, 
							style = wx.OPEN,wildcard = file_wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetPath()
			self.featureFilePath=self.filename
			self.feature_file_path=os.path.split(self.filename)[0]
			self.ReadLibFeature()
			self.multiText3.SetValue(self.feature_file_path)
		dlg.Destroy()
	
	def ReadLibFeature(self):
		a = feature_database_load(self.featureFilePath)
		if a==0:
			print "特征库文件加载成功".decode('utf-8')
			self.lib.append(self.featureFilePath)
			self.multiText.AppendText('\n'+'特征库文件加载成功'.decode('utf-8')+'\n')
			self.fealib_release_flag=1
		elif a==1:
			print "内存分配失败".decode('utf-8')
			self.multiText.AppendText('\n'+'内存分配失败'.decode('utf-8')+'\n')
		elif a==2:
			print "特征库文件加载失败".decode('utf-8')
			self.multiText.AppendText('\n'+'特征库文件加载失败'.decode('utf-8')+'\n')
		else :
			print "该建筑的特征库已加载，请重新选择".decode('utf-8')
			self.multiText.AppendText('\n'+'该建筑的特征库已加载，请重新选择'.decode('utf-8')+'\n')
	
	def feadb_release(self,event):
		print 'feadb_release'
		self.multiText.AppendText('\n'+'释放特征库文件. . .'.decode('utf-8')+'\n')
		file_wildcard = "feature files(*.ft)|*.ft|All files(*.*)|*.*"
		dlg = wx.FileDialog(self, message="load feature",
							defaultDir=self.feature_file_path, 
							style = wx.OPEN,wildcard = file_wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename1 = dlg.GetPath()
			self.featureFilePath1=self.filename1
			self.ReleaseLibFeature()
		dlg.Destroy()
	
	def ReleaseLibFeature(self):
		print "\treleaseing libfeature"
		if self.featureFilePath1 not in self.lib:
			print "请选择已加载的特征库释放".decode('utf-8')
			self.multiText.AppendText('\n'+"请选择已加载的特征库释放".decode('utf-8')+'\n')
		else:
			db_release_flag = feature_database_release(self.featureFilePath1)
			if db_release_flag == 0:
				print "释放特征库成功".decode('utf-8')
				self.lib.remove(self.featureFilePath1)
				if len(self.lib)==0:
					self.fealib_release_flag=0
				self.multiText.AppendText('\n'+'释放特征库成功'.decode('utf-8')+'\n')
			else :
				print "释放失败，没有该特征库".decode('utf-8')
				self.multiText.AppendText('\n'+'释放失败，没有该特征库'.decode('utf-8')+'\n')
	
	def check_feadb(self,event):
		print 'check_feadb'
		if len(self.lib)!=0:
			b = []
			for a in self.lib:
				b.append(a.split('\\')[-1])
			self.multiText.AppendText('\n'+'\n'.join(b)+'\n')
		else :
			self.fealib_release_flag=0
			self.multiText.AppendText('\n'+'没有特征库'.decode('utf-8')+'\n')
	
	def choose_feadb(self, event):
		print "choose the matching lib"
		if len(self.lib)!=0:
			self.multiText.AppendText('\n'+'从下面已加载的特征库选择待匹配特征库'.decode('utf-8')+'\n')
			b = []
			for a in self.lib:
				b.append(a.split('\\')[-1])
			self.multiText.AppendText('\n'.join(b)+'\n')
			file_wildcard = "feature files(*.ft)|*.ft|All files(*.*)|*.*"
			dlg = wx.FileDialog(self, message="load feature",
								defaultDir=self.feature_file_path, 
								style = wx.OPEN,wildcard = file_wildcard)
			if dlg.ShowModal() == wx.ID_OK:
				self.choosed_lib_tmp = dlg.GetPath()
				if self.choosed_lib_tmp not in self.lib:
					print "请选择已加载的特征库进行匹配".decode('utf-8')
					self.multiText.AppendText('\n'+'请选择已加载的特征库进行匹配'.decode('utf-8')+'\n')
				else:
					self.choose_lib_flag = 1
					self.choosed_lib = dlg.GetPath()
					print self.choosed_lib
					self.multiText4.SetValue(self.choosed_lib.split('\\')[-1])
					self.multiText.AppendText('\n'+'选择成功'.decode('utf-8')+'\n')
			dlg.Destroy()
		else:
			self.multiText.AppendText('\n'+'没有加载特征库，请先加载'.decode('utf-8')+'\n')

	def choose_feadb1(self, event):
		self.choosed_lib=None
		self.choose_lib_flag = 1
		self.multiText4.SetValue('all')
		self.multiText.AppendText('\n'+'选择了所有特征库进行匹配'.decode('utf-8')+'\n')
	
	def cb_load(self,event):
		print 'loading codebook'
		self.multiText.AppendText('\n'+'加载码本. . .'.decode('utf-8')+'\n')
		file_wildcard = 'codebook file(*.cb)|*.cb|All file(*.*)|*.*'
		dlg = wx.FileDialog(self, message = 'load codebook',
							defaultDir=os.getcwd(),
							style = wx.OPEN, wildcard=file_wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.cb_path=dlg.GetPath()
			self.ReadCodebook()
			self.multiText1.SetValue(self.cb_path)
		dlg.Destroy()
	
	def ReadCodebook(self):
		cb_load_flag = codebook_load(self.cb_path)
		if cb_load_flag == 0:
			print "码本加载成功".decode('utf-8')
			self.codebook_flag=1
			self.multiText.AppendText('\n'+'码本加载成功'.decode('utf-8')+'\n')
		elif cb_load_flag == 2:
			print "该码本已加载".decode('utf-8')
			self.multiText.AppendText('\n'+'该码本已加载'.decode('utf-8')+'\n')
		else:
			print "码本加载失败".decode('utf-8')
			self.multiText.AppendText('\n'+'码本加载失败'.decode('utf-8')+'\n')

	def matchJpgPath(self,event):
		print "chooese the matched jpgs' path"
		self.multiText.AppendText('\n'+'选择结果图像路径'.decode('utf-8')+'\n')
		dlg=wx.DirDialog(self,message='choose a directory',
						defaultPath=self.result_path,
						style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON,
					 pos = wx.DefaultPosition, size = wx.DefaultSize,name='training_data_path')
		if dlg.ShowModal() == wx.ID_OK:
			a=dlg.GetPath().split('\\')[-1]
			if a=='image':
				self.mach_jpg_path_flag=1
				self.match_jpg_path=dlg.GetPath()
				self.result_path=os.path.split(dlg.GetPath())[0]
				self.multiText8.SetValue(self.match_jpg_path)
			else:
				self.multiText.AppendText('\n'+'路径不合法'.decode('utf-8')+'\n')
		dlg.Destroy()
		
	def openjpg1(self,event):
		print event.GetEventObject().GetLabel()
		if len(self.statistical_test_jpgs)!=0:
			self.statistical_test_jpgs=[]
			self.statistical_flag=0
			self.multiText.AppendText('\n'+'退出统计测试模式'.decode('utf-8')+'\n')
			self.multiText7.Clear()
		if self.codebook_flag !=1:
			print "请加载码本".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载码本'.decode('utf-8')+'\n')
		elif self.fea_release_flag == 1:
			print "请释放特征".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放图像特征'.decode('utf-8')+'\n')
		elif self.mach_jpg_path_flag==0:
			print "请先选择显示结果图像的路径".decode('utf-8')
			self.multiText.AppendText('\n'+'请先选择显示结果图像的路径'.decode('utf-8')+'\n')
		elif self.mat_release_flag == 1:
			print "请释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择1的匹配结果'.decode('utf-8')+'\n')
		elif self.mat_release_flag2 == 1:
			print '请释放匹配2的结果'.decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择2的匹配结果'.decode('utf-8')+'\n')
		elif self.fealib_release_flag == 0:
			print "请先加载特征库文件".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载特征库文件'.decode('utf-8')+'\n')
		else:
			print 'open'
			self.multiText.AppendText('\n'+'读入图像. . .'.decode('utf-8')+'\n')
			file_wildcard = "Image files(*.jpg)|*.jpg|All files(*.*)|*.*"
			dlg = wx.FileDialog(self, message="choose a jpg file",
								defaultDir=self.test_pic_path,             
								style = wx.OPEN,wildcard = file_wildcard)
			if dlg.ShowModal() == wx.ID_OK:
				self.filename = dlg.GetPath()
				self.img=self.filename  
				self.test_pic_path=os.path.split(self.filename)[0]
				self.ReadJpg()
				if event.GetEventObject().GetLabel() == '选择1'.decode('utf-8'):
					self.multiText5.SetValue(self.filename)
					# self.multiText6.Clear()
					self.img_flag=1
				else:
					pass
					# self.multiText6.SetValue(self.filename)
					# self.multiText5.Clear()
					# self.img_flag=2
			dlg.Destroy()

	def ReadJpg(self):
		if self.filename:
			print 'readjpg'
			image=wx.Image(self.filename,wx.BITMAP_TYPE_ANY)
			image=image.Scale(500,200)
			self.sb1=wx.StaticBitmap(self.scroll3,-1,wx.BitmapFromImage(image))
			self.multiText.AppendText('\n'+'读入图像成功'.decode('utf-8')+'\n')
	
	def openjpg_statistical(self,event):
		if self.codebook_flag !=1:
			print "请加载码本".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载码本'.decode('utf-8')+'\n')
		elif self.fea_release_flag == 1:
			print "请释放特征".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放图像特征'.decode('utf-8')+'\n')
		elif self.mat_release_flag2 == 1:
			print "请释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择2的匹配结果'.decode('utf-8')+'\n')
		elif self.mat_release_flag == 1:
			print "请释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择1的匹配结果'.decode('utf-8')+'\n')
		elif self.mach_jpg_path_flag==0:
			print "请先选择显示结果图像的路径".decode('utf-8')
			self.multiText.AppendText('\n'+'请先选择显示结果图像的路径'.decode('utf-8')+'\n')
		elif self.fealib_release_flag == 0:
			print "请先加载特征库文件".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载特征库文件'.decode('utf-8')+'\n')
		else :
			print 'statistical test'
			self.multiText5.Clear()
			self.multiText.AppendText('\n'+'选择测试图片路径，注意是目录，不是文件'.decode('utf-8')+'\n')
			dlg=wx.DirDialog(self,message='choose a directory for statistical test',
							defaultPath=self.statistical_test_path,
							style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON,
						 pos = wx.DefaultPosition, size = wx.DefaultSize,name='statistical_test_path')
			if dlg.ShowModal() == wx.ID_OK:
				self.statistical_test_path = os.path.split(dlg.GetPath())[0]
				self.multiText7.SetValue(dlg.GetPath())
				self.statistical_test_jpgs=[]
				for roots,dirs,files in os.walk(dlg.GetPath()):
					for file in files:
						if ".jpg" in file:
							self.statistical_test_jpgs.append(os.path.join(roots,file))
				self.ordinal=-1
				self.statistical_flag=1
				self.statistical_result_txt='./result_'+time.strftime('%Y%m%d%H%M%S',time.localtime())+'.txt'
			dlg.Destroy()
	
	def pre_img(self,event):
		if self.statistical_flag == 0:
			self.multiText.AppendText('\n'+'请先选择统计测试路径'.decode('utf-8')+'\n')
		else:
			if self.ordinal > 0 :
				self.ordinal-=1
				self.filename=self.statistical_test_jpgs[self.ordinal]
				# self.ordinal-=1
				self.statisticalTest()
			elif self.ordinal == 0:
				self.multiText.AppendText('\n'+'统计测试的图片已经是第一张'.decode('utf-8')+'\n')
			else:
				self.multiText.AppendText('\n'+'请点击下一张'.decode('utf-8')+'\n')
	
	def next_img(self,event):
		if self.statistical_flag == 0:
			self.multiText.AppendText('\n'+'请先选择统计测试路径'.decode('utf-8')+'\n')
		else:
			if self.ordinal < len(self.statistical_test_jpgs) - 1:
				self.ordinal+=1
				self.filename=self.statistical_test_jpgs[self.ordinal]
				self.statisticalTest()
			else :
				self.multiText.AppendText('\n'+'统计测试的图片已全部检测完'.decode('utf-8')+'\n')
	
	def statisticalTest(self):
		print self.filename
		try:
			self.sb1.Destroy()
			for child in self.panel2.GetChildren():
				child.Destroy()
		except:
			pass
		finally:
			print 'statistical_test_match'
			self.ReadJpg()
			self.multiText.AppendText('\n'+'提取图像特征并匹配'.decode('utf-8')+'\n')
			self.match_result_p = ext_match_img(self.choosed_lib,self.filename)
			self.match_result = self.match_result_p.value
			match_release(self.match_result_p)
			# with open(self.statistical_result_txt,"a") as f:
				# f.write(self.filename+'\n')
				# for i in range(len(self.match_result)/18):
					# f.write(self.match_result[0+18*i : 6+18*i]+'\\'+
							# self.match_result[6+18*i : 8+18*i]+'\\'+
							# self.match_result[8+18*i : 10+18*i]+'\\'+
							# self.match_result[10+18*i : 12+18*i]+'\\'+
							# self.match_result[12+18*i : 18+18*i]+" : "+ str(i+1)+'\n')
				# f.write('\n\n')
			if self.choosed_lib == None:
				self.multiText.AppendText('\n'+'匹配结果为'.decode('utf-8')+'\n')
				self.fgs = wx.FlexGridSizer(rows=len(self.match_result)/18,cols=1,hgap=10,vgap=10)
				sb=[]
				for i in range(len(self.match_result)/18):
					self.multiText.AppendText(self.match_result[0+18*i:18+18*i]+'\n')
					relative_path=self.match_jpg_path+'\\'+self.match_result[0+18*i:6+18*i]+'\\'+self.match_result[6+18*i:8+18*i]+'\\'+self.match_result[8+18*i:10+18*i]+'\\'+self.match_result[10+18*i:12+18*i]+'\\'+self.match_result[12+18*i:18+18*i]
					print relative_path
					imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
					print imgs_path
					imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
					w,h=imgs.GetWidth(),imgs.GetHeight()
					imgs=imgs.Scale(500,100)
					self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
					self.fgs.Add(self.sb2)
			else:
				self.multiText.AppendText('\n'+'匹配上的商店是'.decode('utf-8')+self.match_result+'\n')
				self.fgs = wx.FlexGridSizer(rows=1,cols=1,hgap=10,vgap=10)
				sb=[]
				relative_path=self.match_jpg_path+'\\'+self.match_result[0:6]+'\\'+self.match_result[6:8]+'\\'+self.match_result[8:10]+'\\'+self.match_result[10:12]+'\\'+self.match_result[12:]
				print relative_path
				imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
				print imgs_path
				imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
				w,h=imgs.GetWidth(),imgs.GetHeight
				imgs=imgs.Scale(500,100)
				self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
				self.fgs.Add(self.sb2)
			self.box=wx.BoxSizer(wx.VERTICAL)
			self.box.Add(self.fgs, proportion=1, flag=wx.ALL, border=20)
			self.panel2.SetSizer(self.box)
			self.panel2.SetAutoLayout( True )
			self.panel2.Layout()
			self.panel2.Fit()
	
	def ext(self,event):
		if self.fea_release_flag == 1:
			print "请先释放图像特征".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放图像特征'.decode('utf-8')+'\n')
		elif self.mat_release_flag2 == 1:
			print "请先释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择2的匹配结果'.decode('utf-8')+'\n')
		elif self.img_flag != 2:
			print "请先读入图像".decode('utf-8')
			self.multiText.AppendText('\n'+'请先读入图像'.decode('utf-8')+'\n')
		elif self.fealib_release_flag == 0:
			print "请先加载特征库文件".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载特征库文件'.decode('utf-8')+'\n')
		else :
			print 'ext'
			self.multiText.AppendText('\n'+'提取图像特征'.decode('utf-8')+'\n')
			self.fea = ext_img(self.img)
			print self.fea,type(self.fea)
			for i in range(0,512):
				print self.fea[i],
			print '\n'
			self.fea_release_flag = 1
	
	def match(self,event):
		if self.mat_release_flag2 == 1:
			print "请先释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择2的匹配结果'.decode('utf-8')+'\n')
		elif self.fea_release_flag == 0 :
			print "请先提取图像特征".decode('utf-8')
			self.multiText.AppendText('\n'+'请先提取图像特征'.decode('utf-8')+'\n')
		elif self.img_flag == 0:
			print "请先读入图像".decode('utf-8')
			self.multiText.AppendText('\n'+'请先读入图像'.decode('utf-8')+'\n')
		elif self.fealib_release_flag == 0:
			print "请先加载特征库文件".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载特征库文件'.decode('utf-8')+'\n')
		elif self.choose_lib_flag == 0:
			print "没有选择待匹配的特征库".decode('utf-8')
			self.multiText.AppendText('\n'+"没有选择待匹配的特征库".decode('utf-8')+'\n')
		elif self.choosed_lib not in self.lib and self.choosed_lib != None:
			print "待匹配特征库不在已加载的特征库中".decode('utf-8')
			self.multiText.AppendText('\n'+"待匹配特征库不在已加载的特征库中".decode('utf-8')+'\n')
		else:
			try:
				for child in self.panel2.GetChildren():
					child.Destroy()
			except:
				pass
			finally:
				print 'match'
				self.multiText.AppendText('\n'+'特征匹配'.decode('utf-8')+'\n')
				self.match_result_p = match_img(self.choosed_lib, self.fea)
				self.match_result = self.match_result_p.value
				print self.match_result
				if self.choosed_lib == None:
					self.multiText.AppendText('\n'+'匹配结果为'.decode('utf-8')+'\n')
					self.fgs = wx.FlexGridSizer(rows=len(self.match_result)/18,cols=1,hgap=10,vgap=10)
					sb=[]
					for i in range(len(self.match_result)/18):
						self.multiText.AppendText(self.match_result[0+18*i:18+18*i]+'\n')
						relative_path='.\\image\\'+self.match_result[0+18*i:6+18*i]+'\\'+self.match_result[6+18*i:8+18*i]+'\\'+self.match_result[8+18*i:10+18*i]+'\\'+self.match_result[10+18*i:12+18*i]+'\\'+self.match_result[12+18*i:18+18*i]
						print relative_path
						imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
						print imgs_path
						imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
						imgs=imgs.Scale(500,100)
						self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
						self.fgs.Add(self.sb2)
				else:
					self.multiText.AppendText('\n'+'匹配上的商店是'.decode('utf-8')+self.match_result+'\n')
					self.fgs = wx.FlexGridSizer(rows=1,cols=1,hgap=10,vgap=10)
					sb=[]
					relative_path='.\\image\\'+self.match_result[0:6]+'\\'+self.match_result[6:8]+'\\'+self.match_result[8:10]+'\\'+self.match_result[10:12]+'\\'+self.match_result[12:]
					print relative_path
					imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
					print imgs_path
					imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
					imgs=imgs.Scale(500,100)
					self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
					self.fgs.Add(self.sb2)
				self.box=wx.BoxSizer(wx.VERTICAL)
				self.box.Add(self.fgs, proportion=1, flag=wx.ALL, border=20)
				self.panel2.SetSizer(self.box)
				self.panel2.SetAutoLayout( True )
				self.panel2.Layout()
				self.panel2.Fit()
				self.mat_release_flag2 = 1
	
	def ext_match(self,event):
		if self.fea_release_flag == 1:
			print "请先释放图像特征".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放图像特征'.decode('utf-8')+'\n')
		elif self.mat_release_flag == 1:
			print "请先释放匹配结果".decode('utf-8')
			self.multiText.AppendText('\n'+'请先释放选择1的匹配结果'.decode('utf-8')+'\n')
		elif self.img_flag != 1:
			print "请先读入图像".decode('utf-8')
			self.multiText.AppendText('\n'+'请先读入图像'.decode('utf-8')+'\n')
		elif self.fealib_release_flag==0:
			print "请先加载特征库文件".decode('utf-8')
			self.multiText.AppendText('\n'+'请先加载特征库文件'.decode('utf-8')+'\n')
		elif self.choose_lib_flag == 0:
			print "没有选择待匹配的图像库".decode('utf-8')
			self.multiText.AppendText('\n'+"没有选择待匹配的图像库".decode('utf-8')+'\n')
		elif self.choosed_lib not in self.lib and self.choosed_lib != None:
			print "待匹配特征库不在已加载的特征库中".decode('utf-8')
			self.multiText.AppendText('\n'+"待匹配特征库不在已加载的特征库中".decode('utf-8')+'\n')
		else:
			try:
				for child in self.panel2.GetChildren():
					child.Destroy()
			except:
				pass
			finally:
				print 'ext_match'
				self.multiText.AppendText('\n'+'提取图像特征并匹配'.decode('utf-8')+'\n')
				self.match_result_p = ext_match_img(self.choosed_lib,self.img)
				self.match_result = self.match_result_p.value
				if self.choosed_lib == None:
					self.multiText.AppendText('\n'+'匹配结果为'.decode('utf-8')+'\n')
					self.fgs = wx.FlexGridSizer(rows=len(self.match_result)/18,cols=1,hgap=10,vgap=10)
					sb=[]
					for i in range(len(self.match_result)/18):
						self.multiText.AppendText(self.match_result[0+18*i:18+18*i]+'\n')
						relative_path=self.match_jpg_path+'\\'+self.match_result[0+18*i:6+18*i]+'\\'+self.match_result[6+18*i:8+18*i]+'\\'+self.match_result[8+18*i:10+18*i]+'\\'+self.match_result[10+18*i:12+18*i]+'\\'+self.match_result[12+18*i:18+18*i]
						print relative_path
						imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
						print imgs_path
						imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
						imgs=imgs.Scale(500,100)
						self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
						self.fgs.Add(self.sb2)
				else:
					self.multiText.AppendText('\n'+'匹配上的商店是'.decode('utf-8')+self.match_result+'\n')
					self.fgs = wx.FlexGridSizer(rows=1,cols=1,hgap=10,vgap=10)
					sb=[]
					relative_path=self.match_jpg_path+'\\'+self.match_result[0:6]+'\\'+self.match_result[6:8]+'\\'+self.match_result[8:10]+'\\'+self.match_result[10:12]+'\\'+self.match_result[12:]
					print relative_path
					imgs_path=glob.glob(relative_path + '\\*.jpg')[0]
					print imgs_path
					imgs=wx.Image(imgs_path,wx.BITMAP_TYPE_ANY)
					imgs=imgs.Scale(500,100)
					self.sb2=wx.StaticBitmap(self.panel2,-1,wx.BitmapFromImage(imgs))
					self.fgs.Add(self.sb2)
				self.box=wx.BoxSizer(wx.VERTICAL)
				self.box.Add(self.fgs, proportion=1, flag=wx.ALL, border=20)
				self.panel2.SetSizer(self.box)
				self.panel2.SetAutoLayout( True )
				self.panel2.Layout()
				self.panel2.Fit()
				self.mat_release_flag = 1 

	def fea_release(self,event):
		if self.fea_release_flag == 0:
			print "没有图像特征，请先提取特征".decode('utf-8')
			self.multiText.AppendText('\n'+'没有图像特征，请先提取特征'.decode('utf-8')+'\n')
		else:
			print "fea_release"
			self.multiText.AppendText('\n'+'释放图像特征'.decode('utf-8')+'\n')
			feature_release(self.fea)
			self.fea_release_flag = 0
	
	def mat_release(self,event):
		if event.GetEventObject().GetLabel() == '释放1'.decode('utf-8'):
			if self.mat_release_flag == 0:
				print "没有匹配结果，请先匹配".decode('utf-8')
				self.multiText.AppendText('\n'+'没有匹配结果，请先匹配'.decode('utf-8')+'\n')
			else:
				print "mat_release"
				self.multiText.AppendText('\n'+'释放匹配结果'.decode('utf-8')+'\n')
				match_release(self.match_result_p)
				self.mat_release_flag=0
		else:
			if self.mat_release_flag2 == 0:
				print "没有匹配结果，请先匹配".decode('utf-8')
				self.multiText.AppendText('\n'+'没有匹配结果，请先匹配'.decode('utf-8')+'\n')
			else :
				print "mat_release"
				self.multiText.AppendText('\n'+'释放匹配结果'.decode('utf-8')+'\n')
				match_release(self.match_result_p)
				self.mat_release_flag2=0
		
class myApp(wx.App):
	def OnInit(self):
		self.frame=myFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

if __name__ == '__main__':
	app=myApp()
	app.MainLoop()