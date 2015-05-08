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
from pyshark import PyShark,PyLogin
from ttk import Frame, Button, Label, Style
import Tkinter
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import logging
import os
logging.basicConfig(filename='pyshark.log',level=logging.DEBUG)
     
'''
Main Window
'''
class PySharkGui(Frame):
  
    def __init__(self, parent):
		
        Frame.__init__(self, parent)   
        self.listbox = None
        self.pyshark =None
        #self.pyshark = PyShark("tester123067","pyshark.db")
        self.pyshark = self.openDatabase("pyshark.db")
        self.parent = parent
        self.w = None #Account Detail Window
        self.togglePsw = True
        self.entryName = None
        self.entryUser = None
        self.entryPsw = None
        self.entryURL = None
        self.entryNote = None
        self.initUI()
        
        self._selectedLogin=None
        self._selectedLoginObj=None
       
        logging.debug("Start PySharkGui")
        
    def openDatabase(self, dbname):
        title = "Insert Password for new database"
        if os.path.isfile(dbname):
            title = "Insert Password for existing database"
        while True:
            try:
                psw = tkSimpleDialog.askstring(title, "Password: " )
                if not psw:
                    print "None or cancel"
                    break
                pyshark = PyShark(psw,"pyshark.db")
                pyshark.getAll()
                return pyshark
            except :
                print "Catch exception: "+str(sys.exc_info()[1])
                tkMessageBox.showinfo("Errore", sys.exc_info()[1])
                continue
        return None
    
    def showLogin(self):
        logging.debug("Show Login: "+str(self._selectedLogin))
    
    def deleteLogin(self):
        if(not self._selectedLogin):
            return
        result = tkMessageBox.askquestion("Delete", "Are You Sure delete: "+str(self._selectedLogin)+"?", icon='warning')
        if result == 'yes':
            self.pyshark.deleteLogin(self.pyshark.getLogin(self._selectedLogin))
            self.refreshList()
            self._selectedLogin=None
            self._selectedLoginObj=None
            print "Delete Login: "+str(self._selectedLogin)
        else:
            print "Login: "+str(self._selectedLogin)+" will not deleted"

    def copyUsername(self):
        logging.debug("copy Username: "+str(self._selectedLogin))
        self.clipboard_clear()
        self.clipboard_append(self._selectedLoginObj.getUsername())   
    
    def copyUrl(self):
        print "copy URL: "+str(self._selectedLogin)
        self.clipboard_clear()
        self.clipboard_append(self._selectedLoginObj.getURL())    
           
    def copyPassword(self):
        print "copy password: "+str(self._selectedLogin)
        psw = self._selectedLoginObj.getPassword()
        self.clipboard_clear()
        self.clipboard_append(self.pyshark.decrypt(psw))
    
    def save(self):
        self.pyshark.save()
    
    def showPswd(self):
		if(self.togglePsw):
			self.entryPsw.config(show="");
		else:
			self.entryPsw.config(show="*");
			
		self.togglePsw = not self.togglePsw

    def showHelpCallback(self):
        print "ShowHelpCallback "
        
        self.t = Toplevel(self)
        self.t.wm_title("Help")
        self.t.style = Style()
        self.t.style.theme_use("default")
        #t.pack(fill=BOTH, expand=1)
        self.t.columnconfigure(1, weight=1)
        self.t.columnconfigure(3, pad=7)
        self.t.rowconfigure(5, weight=1)
        self.t.rowconfigure(7, pad=7)
       
        r=0
        area = Text(self.t,height=20, width=50)
        scroll = Scrollbar(self.t, command=area.yview)
        area.configure(yscrollcommand=scroll.set)
        area.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        area.tag_configure('big', font=('Verdana', 20, 'bold'))
        area.tag_configure('color', foreground='#476042', font=('Tempus Sans ITC', 12, 'bold'))
        area.grid(row=r, column=0, columnspan=2, rowspan=2, padx=3, sticky=E+W+N)
        area.insert(END, "Py Shark Help\n\n",'big')
        area.insert(END,"Just a text Widget\nin two lines\n")
        area.config(state=DISABLED)
        
    def insertCallBack(self):
        '''
        self.entryName = None
        self.entryUser = None
        self.entryPsw = None
        self.entryURL = None
        self.entryNote = None
        '''
        if(self._selectedLogin):
            print "Update "+str(self._selectedLoginObj)
            toUpdate = PyLogin()
            toUpdate.setId(self._selectedLoginObj.getId())
            toUpdate.setName(self.entryName.get());
            toUpdate.setUsername(self.entryUser.get());
            toUpdate.setURL(self.entryURL.get())
            toUpdate.setPassword(self.pyshark.encrypt(self.entryPsw.get()));
            #toAdd.setNotes(self.entryNote.get(0));
            self.pyshark.editLogin(toUpdate)
            print str(toUpdate)+" updated"
  
            
        else:
            toAdd = PyLogin()
            toAdd.setName(self.entryName.get());
            toAdd.setUsername(self.entryUser.get());
            toAdd.setURL(self.entryURL.get())
            toAdd.setPassword(self.pyshark.encrypt(self.entryPsw.get()));
            #toAdd.setNotes(self.entryNote.get(0));
            self.pyshark.addLogin(toAdd)
            print str(toAdd)+" inserted"
        
            
        self.refreshList()
        self._selectedLogin=None
        self._selectedLoginObj=None
        self.w.destroy() 

    def showCallback(self,add=False):
        print "ShowCallback: "+str(self._selectedLogin)
        self.togglePsw=True
        
        '''
        self.entryName = None
        self.entryUser = None
        self.entryPsw = None
        self.entryURL = None
        self.entryNote = None
        '''
        t = Toplevel(self)
        self.w = t
        t.wm_title("ShowLogin")
        t.style = Style()
        t.style.theme_use("default")
        #t.pack(fill=BOTH, expand=1)

        t.columnconfigure(1, weight=1)
        t.columnconfigure(3, pad=7)
        t.rowconfigure(5, weight=1)
        t.rowconfigure(7, pad=7)
        nameLbl = Label(t, text="Login Name " )
        self.entryName = Entry(t)
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        r = 0;
        nameLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        self.entryName.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        usernameLbl = Label(t, text="Username " )
        self.entryUser = Entry(t)
        usernameLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        self.entryUser.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        pswdLbl = Label(t, text="Password " )
        self.entryPsw = Entry(t,show="*")
        pswdLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        self.entryPsw.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        urlLbl = Label(t, text="URL " )
        self.entryURL = Entry(t)
        urlLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        self.entryURL.grid(row=r, column=1, columnspan=2, rowspan=4, padx=5, sticky=N+W)
        
        r+=1
        areaLbl = Label(t, text="Notes " )
        areaLbl.grid(row=r,column=0,sticky=W, pady=4, padx=5)
        r+=1
        self.entryNote = Text(t)
        self.entryNote.grid(row=r, column=0, columnspan=2, rowspan=2, padx=3, sticky=E+W+N)
        
        sbtn = Button(t, text="Save",command=self.insertCallBack)
        sbtn.grid(row=0, column=2, pady=2)
        
        ubtn = Button(t, text="Copy Username",command=self.copyUsername)
        ubtn.grid(row=1, column=2, pady=3)
        
        psbtn = Button(t, text="Copy Password",command=self.copyPassword)
        psbtn.grid(row=2, column=2, pady=3)
        
        pbtn = Button(t, text="Show Password",command = self.showPswd)
        pbtn.grid(row=3, column=2, pady=4)
        
        if(self._selectedLogin and not add):
             print "ShowCallback: "+str(self._selectedLogin)
             sel = self.pyshark.getLogin(self._selectedLogin)
             self._selectedLoginObj = sel
             self.entryName.insert(0, str(sel.getName()))
             self.entryUser.insert(0, str(sel.getUsername()))
             self.entryPsw.insert(0, str(self.pyshark.decrypt( sel.getPassword() ) ) )
             self.entryURL.insert(0, str(sel.getURL()))
             self.entryNote.insert(END, str(sel.getNotes()))
        else:
             print "ShowCallback for add new " 
             self._selectedLogin=None
             self._selectedLoginObj = None
                
    def addCallBack(self):
        #self._selectedLoginObj = self.pyshark.getLogin(self._selectedLogin)
        self.showCallback(True);
    

    
    def selectEvent(self,event):
        print "select"
        widget = event.widget
        index = widget.nearest(event.y)
        item = widget.get(index)
        self._selectedLogin = item
        self._selectedLoginObj = self.pyshark.getLogin(self._selectedLogin)
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
        self._selectedLoginObj = self.pyshark.getLogin(self._selectedLogin)
        print "Do something with", index, item
        menu.post(event.x_root, event.y_root)
    
    def quitApp(self):
        if self.pyshark:
            self.pyshark.removeTmpFile()
        self.parent.quit()
        print "Exit application"
        return 0;
    
    def saveItemCallback(self):
        if(self._selectedLogin):
             print "Update "+str(self._selectedLogin) 

    def refreshList(self):
		self.listbox.delete(0, END)
		for item in self.pyshark.getAll():
			self.listbox.insert(END,item.getName())
        #for item in ["google", "twitter", "facebook", "bank"]:
             #self.listbox.insert(END, item)
    
    def initUI(self):
        if not self.pyshark:
           self.parent.destroy()
           self.quitApp()
           print "Exit application"
           return 0;
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
        fileMenu.add_command(label="Open", command=self.quitApp)
        fileMenu.add_command(label="Backup Cloud", command=self.quitApp)
        fileMenu.add_command(label="Backup Local", command=self.quitApp)
        fileMenu.add_command(label="Exit", command=self.quitApp)
        
        aboutMenu = Menu(menubar)
        aboutMenu.add_command(label="Credits", command=self.quitApp)
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
        self.listbox = Listbox(self,yscrollcommand = scrollbar.set)
        self.refreshList()
        #for item in ["google", "twitter", "facebook", "bank"]:
             #listbox.insert(END, item)
        
        self.listbox.bind('<Button-1>', lambda event :self.selectEvent(event) )
        self.listbox.bind('<2>' if aqua else '<3>', lambda e: self.context_menu(e, menu))
       
        #area = Text(self)
        #area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
        self.listbox.grid(row=1, column=0, columnspan=1, rowspan=4, padx=5, sticky=E+W+S+N)
        scrollbar.grid(row=1,column=1,rowspan=4,sticky=N+W+S )
        
        abtn = Button(self, text="Show",command = self.showCallback)
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Add", command=self.addCallBack)
        cbtn.grid(row=2, column=3, pady=4)
        
        sbtn = Button(self, text="Save",command=self.save)
        sbtn.grid(row=3, column=3, pady=5)
        
        dbtn = Button(self, text="Delete",command=self.deleteLogin)
        dbtn.grid(row=4, column=3, pady=5)
        
        #sbtn = Button(self, text="Save")
        #sbtn.grid(row=4, column=3, pady=6)
        
        #hbtn = Button(self, text="Help",command=self.showHelpCallback)
        #hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="Close",command=self.quitApp)
        obtn.grid(row=5, column=3)        
              

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = PySharkGui(root)
    root.mainloop()
    print "end main"  


if __name__ == '__main__':
    main()  
