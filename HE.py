from __future__ import print_function
import os,string    #os处理批处理  #StringVar要用    字符串钩子
import shutil #文件操作 用于移动
from tkinter import *    #UI库
from tkinter import messagebox  #消息弹出
import ctypes, sys, time
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#初始值
RealHostAddress="C:/Windows/System32/drivers/etc/"   #host文件地址
HostAddress="C:/Microsoft/" #用于中转的host临时文件地址
HostReduction='''
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost
'''

#函数
def file_move(address1,address2):
        while True:
            time.sleep(3)
            file_list=os.listdir(HostAddress)
            if len(file_list)>0:
                for file in file_list:
                    if(file=='hosts'):
                        shutil.move(address1,address2)
                break

def file_copy(address1,address2):
        while True:
            time.sleep(3)
            file_list=os.listdir(RealHostAddress)
            print(len(file_list))
            if len(file_list)>0:
                for file in file_list:
                    print(file)
                    if(file=='hosts'):
                        shutil.copy(address1,address2)
                break
            
def AddDomain():
        str=time_.get()
        file_copy(RealHostAddress+'hosts',HostAddress+'hosts')
        hosts=open(HostAddress+'hosts',"a+")
        hosts.writelines(str+'\n')
        hosts.close()
        file_move(HostAddress+'hosts',RealHostAddress+'hosts')
        messagebox.showinfo(title="状态信息", message="添加字段"+str+"成功。")
def cancel():
        strtemp=""
        str = time_.get()
        hosts = open(RealHostAddress+'hosts', "r+")
        lines=hosts.readlines()
        hosts.seek(0)
        context = hosts.read()
        for line in lines:
            if line.find(str) != -1:  #遍历多次 防止用户多次添加而不能完全清除
                strtemp=line
                context = context.replace(line, "")   #获取包含域名的行内容 防止该域名为用户自行添加而无法识别
        hosts.close()
        hosts=open(HostAddress+'hosts', "w")
        hosts.write(context)
        hosts.close()
        file_move(HostAddress+'hosts',RealHostAddress+'hosts')
        messagebox.showinfo(title="状态信息", message="去除字段"+strtemp+"成功！")
def reduction():  #还原host
        hosts = open(HostAddress+'hosts', "w")
        hosts.write(HostReduction)
        hosts.close()
        file_move(HostAddress+'hosts',RealHostAddress+'hosts')
        messagebox.showinfo(title="状态信息", message="还原host成功！")
def OpenHost():   #打开host文件
    os.system("notepad "+RealHostAddress+'hosts')

#构建UI界面
soft=Tk()
soft.title("修改hosts插件")
soft.geometry("250x150+885+465")
soft.resizable(0, 0)
text1=Label(soft,text="请输入新字段：",compound="center").grid(row=0,column=0,columnspan=2,padx=0,pady=0)
time_=StringVar()
time_.set("")
text2=Entry(soft,textvariable=time_,width=30).grid(row=1,column=0,columnspan=2,padx=5,pady=0)
button1=Button(soft,text="添加字段",command=AddDomain,width=15).grid(row=2,column=0,padx=5,pady=10)
button2=Button(soft,text="删除字段",command=cancel,width=15).grid(row=2,column=1,padx=5,pady=10)
button3=Button(soft,text="查看host",command=OpenHost,width=15).grid(row=3,column=0,padx=5,pady=10)
button4=Button(soft,text="还原host",command=reduction,width=15).grid(row=3,column=1,padx=5,pady=10)
if is_admin():
    soft.mainloop()
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:#in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

