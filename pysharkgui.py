#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
PySharkGui beta

This script create a simple tkinter GUI
to manage accounts and passwords using PyShark module

authors: tabuto83
last modified: May 2015
website: 
"""

#from Tkinter import Tk, Text, BOTH, W, N, E, S
from pyshark import PyShark
from ttk import Frame, Button, Label, Style
import Tkinter
from Tkinter import *
import tkMessageBox
import logging
logging.basicConfig(filename='pyshark.log',level=logging.DEBUG)
     
'''
Main Window
'''
class PySharkGui(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
        self._selectedLogin=None
        self.pyshark = PyShark("tester123067","pyshark_test.db")
        logging.debug("Start PySharkGui")
    
    def showLogin(self):
        logging.debug("Show Login: "+str(self._selectedLogin))
    
    def deleteLogin(self):
        if(not self._selectedLogin):
            return
        result = tkMessageBox.askquestion("Delete", "Are You Sure delete: "+str(self._selectedLogin)+"?", icon='warning')
        if result == 'yes':
            print "Delete Login: "+str(self._selectedLogin)
        else:
            print "Login: "+str(self._selectedLogin)+" will not deleted"

    def copyUsername(self):
        logging.debug("copy Username: "+str(self._selectedLogin))
    
    def copyUrl(self):
        print "copy URL: "+str(self._selectedLogin)    
           
    def copyPassword(self):
        print "copy password: "+str(self._selectedLogin)

    def showHelpCallback(self):
        print "ShowHelpCallback "
        
        t = Toplevel(self)
        t.wm_title("Help")
        t.style = Style()
        t.style.theme_use("default")
        #t.pack(fill=BOTH, expand=1)
        t.columnconfigure(1, weight=1)
        t.columnconfigure(3, pad=7)
        t.rowconfigure(5, weight=1)
        t.rowconfigure(7, pad=7)
       
        r=0
        area = Text(t,height=20, width=50)
        scroll = Scrollbar(t, command=area.yview)
        area.configure(yscrollcommand=scroll.set)
        area.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        area.tag_configure('big', font=('Verdana', 20, 'bold'))
        area.tag_configure('color', foreground='#476042', font=('Tempus Sans ITC', 12, 'bold'))
        area.grid(row=r, column=0, columnspan=2, rowspan=2, padx=3, sticky=E+W+N)
        area.insert(END, "Py Shark Help\n\n",'big')
        area.insert(END,"Just a text Widget\nin two lines\n")
        area.config(state=DISABLED)


    def showCallback(self,add=False):
        print "ShowCallback: "+str(self._selectedLogin)
        
        t = Toplevel(self)
        t.wm_title("ShowLogin")
        t.style = Style()
        t.style.theme_use("default")
        #t.pack(fill=BOTH, expand=1)

        t.columnconfigure(1, weight=1)
        t.columnconfigure(3, pad=7)
        t.rowconfigure(5, weight=1)
        t.rowconfigure(7, pad=7)
        nameLbl = Label(t, text="Login Name " )
        name = Entry(t)
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        r = 0;
        nameLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        name.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        usernameLbl = Label(t, text="Username " )
        username = Entry(t)
        usernameLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        username.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        pswdLbl = Label(t, text="Password " )
        pswd = Entry(t,show="*")
        pswdLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        pswd.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        urlLbl = Label(t, text="URL " )
        url = Entry(t)
        urlLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        url.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        areaLbl = Label(t, text="Notes " )
        areaLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        r+=1
        area = Text(t)
        area.grid(row=r, column=0, columnspan=2, rowspan=2, padx=3, sticky=E+W+N)
        
        sbtn = Button(t, text="Save")
        sbtn.grid(row=0, column=2, pady=2)
        
        ebtn = Button(t, text="Edit")
        ebtn.grid(row=1, column=2, pady=3)
        
        pbtn = Button(t, text="Show Password")
        pbtn.grid(row=2, column=2, pady=4)
        
        if(self._selectedLogin and not add):
             print "ShowCallback: "+str(self._selectedLogin)
             name.insert(0, str(self._selectedLogin))
        else:
             print "ShowCallback for add new "    
    def addCallBack(self):
        self.showCallback(True);
    
    def selectEvent(self,event):
        print "select"
        widget = event.widget
        index = widget.nearest(event.y)
        item = widget.get(index)
        self._selectedLogin = item
        print "Do something with", index, item
    
    def context_menu(self,event, menu):
        print "select"
        widget = event.widget
        index = widget.nearest(event.y)
        _, yoffset, _, height = widget.bbox(index)
        if event.y > height + yoffset + 5: # XXX 5 is a niceness factor :)
             # Outside of widget.
             return
        item = widget.get(index)
        self._selectedLogin = item
        print "Do something with", index, item
        menu.post(event.x_root, event.y_root)
    
    def quit(self):
        self.parent.quit()
        print "Exit application"
        return 0;
    
    def saveItemCallback(self):
        if(self._selectedLogin):
             print "Update "+str(self._selectedLogin) 
    
    def initUI(self):
      
        self.parent.title("PyShark")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(7, pad=7)
        
        lbl = Label(self, text="Logins")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        #MENUBAR
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.quit)
        fileMenu.add_command(label="Backup Cloud", command=self.quit)
        fileMenu.add_command(label="Backup Local", command=self.quit)
        fileMenu.add_command(label="Exit", command=self.quit)
        
        aboutMenu = Menu(menubar)
        aboutMenu.add_command(label="Credits", command=self.quit)
        aboutMenu.add_command(label="Help", command=self.showHelpCallback)
        
        menubar.add_cascade(label="PyShark", menu=fileMenu)
        menubar.add_cascade(label="About", menu=aboutMenu)
        
        
        #CONTEXT MENU
        aqua = self.parent.tk.call('tk', 'windowingsystem') == 'aqua'
        menu = Tkinter.Menu()
        menu.add_command(label=u'Copy Password',command=self.copyPassword )
        menu.add_command(label=u'Copy UserName',command=self.copyUsername)
        menu.add_command(label=u'Copy URL',command=self.copyUrl)
        menu.add_command(label=u'Show',command=self.showCallback)
        menu.add_command(label=u'Delete',command=self.deleteLogin)
        
        #LISTBOX
        scrollbar = Scrollbar(self)
        listbox = Listbox(self,yscrollcommand = scrollbar.set)
        for item in ["google", "twitter", "facebook", "bank"]:
             listbox.insert(END, item)
        
        listbox.bind('<Button-1>', lambda event :self.selectEvent(event) )
        listbox.bind('<2>' if aqua else '<3>', lambda e: self.context_menu(e, menu))
       
        #area = Text(self)
        #area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
        listbox.grid(row=1, column=0, columnspan=1, rowspan=4, padx=5, sticky=E+W+S+N)
        scrollbar.grid(row=1,column=1,rowspan=4,sticky=N+W+S )
        
        abtn = Button(self, text="Show",command = self.showCallback)
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Add", command=self.addCallBack)
        cbtn.grid(row=2, column=3, pady=4)
        
        dbtn = Button(self, text="Delete",command=self.deleteLogin)
        dbtn.grid(row=3, column=3, pady=5)
        
        #sbtn = Button(self, text="Save")
        #sbtn.grid(row=4, column=3, pady=6)
        
        #hbtn = Button(self, text="Help",command=self.showHelpCallback)
        #hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="Close",command=self.quit)
        obtn.grid(row=5, column=3)        
              

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = PySharkGui(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
