# jigsawGame.py writed by dna049(茶茶白) at 2020/2/28
# 这是个加注释的版本，有些望文生义的我就不注释了
import wx 
import os 
import base64 
from datetime import *
from random import randint
import urllib.request as urlrequest 	# 用于从网上加载图片

import tkinter as tk 		# 用于选择文件夹
from tkinter import filedialog # 用于选择文件夹
from wx.lib.embeddedimage import PyEmbeddedImage 	# 用于把数据变成位图

class jigsawGame(wx.Frame):
	def __init__(self, *args, **kw): #这个方法只会在最开始调用一次
		super(jigsawGame, self).__init__(*args, **kw)
		self.Centre()  	# 整个窗口出现在屏幕正中心
		# 选择文件
		self.fileOpen = False 	# 标记是否选择了正确(.png,.jpg,.jpeg)的文件
		self.fileLoad = False 	# 标记是否读取了文件(因为只需读取一次)
		self.order = [i for i in range(9)] 	# 0-8这9个位置的初始值都是0-8，后面会变动
		self.eB = 8 	#标记空白块的位置，8就是右下角
		# 创建面板（面板上可以放按钮，文本框，静态文本，图层等等东西）
		# style 参数设置是让他可以接收到上下左右键！
		self.pnl = wx.Panel(parent = self, style = wx.BORDER_NONE)
		# 这个就是左下角的欢迎界面，还有字体的设置
		welcome = wx.StaticText(self.pnl, pos=(20,520), \
			label = '欢迎来到我的博客:\n新博客:', \
			style = wx.ALIGN_RIGHT)
		blog = wx.StaticText(self.pnl, pos = (180,520),
			label = 'dna049.com\n521zyl.github.io')
		blog.SetForegroundColour('pink')
		font = blog.GetFont()
		font.PointSize += 2
		font = font.Bold()
		welcome.SetFont(font)
		blog.SetFont(font)

		# 这个是操作提示的静态文本
		self.hint = wx.StaticText(self.pnl, pos=(710,20), \
			label = '操作：\n上下左右\nWASD\n\n\n\n\n\n 注意聚焦\n 当前窗口', \
			style = wx.ALIGN_CENTER)
		self.hint.SetFont(font)
		self.hint.SetForegroundColour('pink')
		self.hint.Hide()

		# 一开始的界面中提示按鼠标的静态文本，贼大的那个
		self.st = wx.StaticText(self.pnl, pos =(200,200), \
			label = '鼠标点击空白处\n选择一个照片来玩拼图吧', \
			style = wx.ALIGN_CENTER)
		font.PointSize += 16
		self.font = font.Bold()
		self.st.SetFont(self.font)
		self.st.SetForegroundColour('red')

		# 绑定鼠标左键和下面的on_left_down方法
		self.pnl.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
		#绑定键盘事件和下面的OnKeyDown方法
		self.pnl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# 出现让你选择图片的界面，返回文件绝对路径的文件名
	def myFile(self):
		chooseFile = tk.Tk()
		chooseFile.withdraw()
		fileName = filedialog.askopenfilename()
		return fileName

		# 从网上下一个表情包，返回值是位图用来加载
	def onlineFile(self):
		url = 'https://521zly.github.io/2020/02/28/python-gui/yes.png'
		image = urlrequest.urlopen(url).read()
		bData = base64.b64encode(image)
		pData = bData.decode()
		self.urlYes = PyEmbeddedImage(pData).GetBitmap()

		# 把从本地选择出的图片进行调整大小，调整完之后切成3*3的块，然后在画板上画出来
		# 并且进行标记好更新，逻辑代码很短归功于Python的短小精湛！
	def writeFile(self):
		tmp = wx.Image(self.fileName)
		im = tmp.ConvertToBitmap()
		(sizeW,sizeH) = im.GetSize()
		t = max(0.2,sizeW/720,sizeH/550)+0.02
		im = tmp.Scale(int(sizeW/t),int(sizeH/t)).ConvertToBitmap()
		(sizeW,sizeH) = im.GetSize()
		sizeW //= 3;sizeH //= 3
		self.img = []
		for i in range(8):
			self.img += [im.GetSubBitmap(( (i%3)*sizeW,(i//3)*sizeH,sizeW,sizeH))]
		self.img += [wx.Bitmap.FromRGBA(sizeW,sizeH,255,255,255)]
		ps = [((x%3)*(sizeW +1), (x//3)*(sizeH+1)) for x in range(9)]
		self.sbt = [wx.StaticBitmap(self.pnl, bitmap = self.img[i],\
			pos=ps[i],size=(sizeW,sizeH) ) for i in range(9)] 

		# 检测到鼠标左键按下，就开始看文件打开过没有，打开了就无视，没打开就开启文件选择
		# 打开成功之后就把部分提示关闭，然后开始为下一步拼图做准备
	def on_left_down(self, event):
		if(not self.fileOpen):
			self.fileName = self.myFile()
			if os.path.basename(self.fileName).split('.')[-1] in ['png','jpg','jpeg']:
				self.fileOpen = True
				self.st.Destroy()
				self.run()   

	def run(self):
		if(not self.fileLoad):
			self.fileLoad = True
			self.onlineFile()
			self.writeFile()
			self.disorder()
			self.pnl.Layout()
			self.hint.Show()


	def disorder(self):
		for i in range(22): self.move(randint(0,3))


		#如果已经完成了，那就不让你再玩了，否则就开始按键检测然后还是移动
	def OnKeyDown(self, event):
		if(self.fileLoad and not self.isFinish()):
			myKey = [wx.WXK_LEFT, ord('A'), wx.WXK_RIGHT, ord('D'), wx.WXK_UP, ord('W'), wx.WXK_DOWN, ord('S')]
			keycode = event.GetKeyCode()
			self.move(myKey.index(keycode)//2 if (keycode in myKey) else -1)
		self.pnl.Layout()
		self.isFinish()

	def move(self, direction):
		if direction == 0:      self.moveLeft()
		elif direction == 1:    self.moveRight()
		elif direction == 2:	self.moveUp()
		elif direction == 3:	self.moveDown()

		#判断是否是合理移动，合理就丢给下面函数更新
	def moveLeft(self):
		if(self.eB+1 in range(9)):   self.sbtNew(self.eB, self.eB+1);self.eB+=1

	def moveRight(self):
		if(self.eB-1 in range(9)):   self.sbtNew(self.eB, self.eB-1);self.eB-=1

	def moveUp(self):
		if(self.eB+3 in range(9)):   self.sbtNew(self.eB, self.eB+3);self.eB+=3

	def moveDown(self):
		if(self.eB-3 in range(9)):   self.sbtNew(self.eB, self.eB-3);self.eB-=3


		# 如果操作合理，那就更新每个格子上的图片，并更新order列表
	def sbtNew(self, posB, posA):
		(x,y) = self.order[posB],self.order[posA] 
		self.order[posB],self.order[posA] = (y,x)
		self.sbt[posB].SetBitmap(self.img[y])
		self.sbt[posA].SetBitmap(self.img[x])

		# 每次有按键的时候检测是否拼好了，拼好了就把表情包打印出来
	def isFinish(self):
		if self.order == [i for i in range(9)]:
			wx.StaticBitmap(parent = self.pnl, bitmap = self.urlYes, pos=(500,300))
			return True
		else:   return False

		# 程序入口，进入__init__ 函数后，就开始进行鼠标和键盘的监听循环中
if __name__ == '__main__':
	loveDays = datetime.now() - datetime(2019,10,20) 
	app = wx.App()
	# 创建上面类的对象，标题是喜欢zly妹妹，窗口不允许最大化，也不能调整大小
	myGame = jigsawGame(None, \
		title='茶茶白喜欢zly妹妹的第'+str(loveDays.days)+'天',\
		size = (800, 600),\
		style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
	myGame.Show()
	app.MainLoop()
