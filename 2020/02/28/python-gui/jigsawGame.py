# jigsawGame.py writed by dna049(茶茶白) at 2020/2/28
import wx
import os
import urllib.request as urlrequest
from datetime import *
from random import randint

from 

import tkinter as tk             #用于选择文件夹
from tkinter import filedialog

class jigsawGame(wx.Frame):
    def __init__(self, *args, **kw):
        super(jigsawGame, self).__init__(*args, **kw)
        self.Centre()
        # 选择文件
        self.fileOpen = False
        self.fileLoad = False
        self.order = [i for i in range(9)]
        self.eB = 8
        self.pnl = wx.Panel(parent = self, style = wx.BORDER_NONE)
        welcome1 = wx.StaticText(self.pnl, pos=(20,521), \
            label = '欢迎来到我的博客： ')
        blog1 = wx.StaticText(self.pnl, pos = (190,521),
            label = r'dna049.com')
        blog1.SetForegroundColour('pink')
        welcome2 = wx.StaticText(self.pnl, pos=(440,521), \
            label = '老博客： ')
        blog2 = wx.StaticText(self.pnl, pos = (521,521),
            label = r'521zyl.github.io')
        blog2.SetForegroundColour('pink')
        self.hint = wx.StaticText(self.pnl, pos=(720,20), \
            label = '操作：\n上下左右\nWASD', \
            style = wx.ALIGN_CENTER)
        font = blog1.GetFont()
        font.PointSize += 2
        font = font.Bold()
        self.hint.SetFont(font)
        self.hint.SetForegroundColour('pink')
        self.hint.Hide()

        font.PointSize += 3
        welcome1.SetFont(font)  
        welcome2.SetFont(font)
        blog1.SetFont(font)
        blog2.SetFont(font)
        

        self.st = wx.StaticText(self.pnl, pos =(200,200), \
            label = '鼠标点击空白处\n选择一个照片来玩拼图吧', \
            style = wx.ALIGN_CENTER)
        font.PointSize += 10
        self.font = font.Bold()
        self.st.SetFont(self.font)
        self.st.SetForegroundColour('red')

        self.pnl.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.pnl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        url = 'https://521zly.github.io/2020/02/26/python-learning/yes.png'

    def myFile(self):
        chooseFile = tk.Tk()
        chooseFile.withdraw()
        fileName = filedialog.askopenfilename()
        return fileName

    def writeFile(self):
        im = wx.Image(self.fileName).ConvertToBitmap()
        (sizeW,sizeH) = im.GetSize()
        t = max(0.2,sizeW/720,sizeH/550)+0.02
        im.SetSize((int(sizeW/t),int(sizeH/t)))
        (sizeW,sizeH) = im.GetSize()
        sizeW //= 3;sizeH //= 3
        self.img = []
        for i in range(8):
            self.img += [im.GetSubBitmap(( (i%3)*sizeW,(i//3)*sizeH,sizeW,sizeH))]
        self.img += [wx.Bitmap.FromRGBA(sizeW,sizeH,255,255,255)]
        ps = [((x%3)*(sizeW +1), (x//3)*(sizeH+1)) for x in range(9)]
        self.sbt = [wx.StaticBitmap(self.pnl, bitmap = self.img[i],\
            pos=ps[i],size=(sizeW,sizeH) ) for i in range(9)] 

    def on_left_down(self, event):
        if(not self.fileOpen):
            self.fileName = self.myFile()
            if os.path.basename(self.fileName).split('.')[-1] in ['png','jpg','jpeg']:
                self.fileOpen = True
                self.st.Destroy()
                self.run()   

    def OnKeyDown(self, event):
        if(not self.isFinish()):
            keycode = event.GetKeyCode()
            if keycode in [wx.WXK_LEFT, ord('A')]:
                self.moveLeft()
            elif keycode in [wx.WXK_RIGHT, ord('D')]:
                self.moveRight()
            elif keycode in [wx.WXK_UP, ord('W'), ]:
                self.moveUp()
            elif keycode in [wx.WXK_DOWN, ord('S'),]:
                self.moveDown()
            else:
                event.Skip()
        self.pnl.Layout()
        self.isFinish()

    def run(self):
        if(not self.fileLoad):
            self.fileLoad = True
            self.writeFile()
            self.disorder()
            self.pnl.Layout()
            self.hint.Show()


    def disorder(self):
        for i in range(22): self.move(randint(0,3))

    def sbtNew(self, posB, posA):
        (x,y) = self.order[posB],self.order[posA] 
        self.order[posB],self.order[posA] = (y,x)
        self.sbt[posB].SetBitmap(self.img[y])
        self.sbt[posA].SetBitmap(self.img[x])

    def move(self, direction):
        if direction == 0:      self.moveLeft()
        elif direction == 1:    self.moveRight()
        elif direction == 2:    self.moveUp()
        else:                   self.moveDown()

    def moveLeft(self):
        if(self.eB+1 in range(9)):   self.sbtNew(self.eB, self.eB+1);self.eB+=1

    def moveRight(self):
        if(self.eB-1 in range(9)):   self.sbtNew(self.eB, self.eB-1);self.eB-=1

    def moveUp(self):
        if(self.eB+3 in range(9)):   self.sbtNew(self.eB, self.eB+3);self.eB+=3

    def moveDown(self):
        if(self.eB-3 in range(9)):   self.sbtNew(self.eB, self.eB-3);self.eB-=3

    def isFinish(self):
        if self.order == [i for i in range(9)]:
            self.yes = wx.StaticText(self.pnl, pos =(600,400), \
            label = '拼图成功',style=wx.ALIGN_CENTER)
            self.yes.SetFont(self.font)
            self.yes.SetForegroundColour('pink')
            return True
        else:   return False


if __name__ == '__main__':
    loveDays = datetime.now() - datetime(2019,10,20) 
    app = wx.App()
    myGame = jigsawGame(None, \
        title='茶茶白喜欢zly妹妹的第'+str(loveDays.days)+'天',\
        size = (800, 600),\
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
    myGame.Show()
    app.MainLoop()
