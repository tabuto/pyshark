#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import sqlite3 as lite
import hashlib

title = 'pyShark'
version = '1.0.0'
authors = 'tabuto83'
dateversion = '2015-04-25'

BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

'''
USED QUERIES
'''
QRY_S_TEST="SELECT name FROM sqlite_master WHERE type='table' AND name='logins'"
QRY_C_LOGIN="CREATE TABLE logins(Id INT  PRIMARY KEY NOT NULL, name TEXT NOT NULL UNIQUE, username TEXT, password TEXT,notes TEXT, url TEXT, actived int)"
QRY_S_NEXT_LOGIN="SELECT MAX(Id)+1 FROM logins"
QRY_I_LOGIN="INSERT INTO logins(Id,name,username,password,notes,url,actived) VALUES(?,?,?,?,?,?,1)"
QRY_S_ALL_LOGIN="SELECT Id,name,username,password,notes,url,actived from logins order by name asc"
QRY_D_LOGIN="DELETE FROM logins WHERE Id = ?"
QRY_U_LOGIN ="UPDATE logins set name=?, username=?,password=?,notes=?,url=?,actived=1 WHERE Id=?"


import base64
from Crypto.Cipher import AES
from Crypto import Random
import os.path


class AESCipher:
    def __init__( self, key ):
        self.key = hashlib.sha256(key).digest()

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        #iv=hashlib.sha512(self.key).digest()[16:]
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))


class PyLogin():
	
	def __init__(self,name="new login",username=" ",password=" "):
		self.__ID=0
		self.__name=name
		self.__username=username
		self.__password=password
		self.__notes=" "
		self.__URL=" "
	
	def getId(self):
		return self.__ID
	
	def setId(self,id):
		self.__ID=id
	
	def getName(self):
		return self.__name
	
	def setName(self, name):
		self.__name=name
	
	def getUsername(self):
		return self.__username
	
	def setUsername(self,username):
		self.__username=username
	
	def getPassword(self):
		return self.__password

	
	def setPassword(self,password):
		self.__password=password

	def getNotes(self):
		return self.__notes
	
	def setNotes(self, notes):
		self.__notes=notes
	
	def getURL(self):
		return self.__URL
	
	def setURL(self, URL):
		self.__URL=URL

	def __str__(self):
		return str(self.getId())+" - "+self.getName()+" - "+self.getUsername()+" - "+self.getPassword() +" - "+self.getURL()
	

class PyShark():
	
	def __init__(self,secret,db="pyshark.db"):
		'''
		init the db connection and retrieve all login
		'''
		self.__DB=db
		self.__CON=self.__createConnection()
		self.__secret= secret
		self.__aes = AESCipher(secret);
		self.__logins = {} 
		
	
	def encrypt(self,plaintext):
		return self.__aes.encrypt(plaintext);

	def decrypt(self,ciphertext):
		return self.__aes.decrypt(ciphertext);
		
	def __createConnection(self):
		if os.path.isfile(self.__DB):
			print "data base file found!"
			con = lite.connect(self.__DB)
			con.text_factory = str
			return con;
		else:
			print "data base file not found...will create"
			con = lite.connect(self.__DB)	
			cur = con.cursor()    
			cur.execute(QRY_C_LOGIN)
			con.commit()
			con.text_factory = str
			return con;
	
	def addLogin(self, pyLogin):
		if(not pyLogin or pyLogin.getId()>0):
			return False
		cur = self.__CON.cursor()
		nextval = 0
		cur.execute(QRY_S_NEXT_LOGIN)
		fetchval = cur.fetchone()
		if(fetchval[0]):
			nextval= fetchval[0]
		else:
			nextval=1
		#
		#"INSERT INTO logins(Id,name,username,password,notes,url,actived) VALUES(?,?,?,?,?,?,1)"
		cur.execute(QRY_I_LOGIN,(nextval,pyLogin.getName(),pyLogin.getUsername(),pyLogin.getPassword(),pyLogin.getNotes(),pyLogin.getURL(), ) )
		self.__CON.commit()
		return True
	
	def deleteLogin(self,pyLogin):
		if(not pyLogin or pyLogin.getId()<=0):
			return False
		cur = self.__CON.cursor()
		cur.execute(QRY_D_LOGIN,(pyLogin.getId(),))
		self.__CON.commit()
		return True
	
	def editLogin(self,pyLogin):
		if(not pyLogin or pyLogin.getId()<=0):
			return False
		cur = self.__CON.cursor()
		cur.execute(QRY_U_LOGIN,(pyLogin.getName(),pyLogin.getUsername(),pyLogin.getPassword(),pyLogin.getNotes(),pyLogin.getURL(),pyLogin.getId(),))
		self.__CON.commit()
		return True
	
	def getAll(self):
	
		cur = self.__CON.cursor()
		cur.execute(QRY_S_ALL_LOGIN)
		rows = cur.fetchall()
		result =[]
		for row in rows:
			o = PyLogin()
			o.setId(row[0])
			o.setName(str(row[1].encode('utf-8')))
			o.setUsername(str(row[2].encode('utf-8')))
			o.setPassword(str(row[3].encode('utf-8')))
			o.setNotes(str(row[4].encode('utf-8')))
			o.setURL(str(row[5]))
			#Id,name,username,password,notes,url,actived
			#print o
			result.append(o)
		return result
		

def __entry_point():
	shark = PyShark("pippo123067")
	#print len(shark.getAll());
	googlelogin = PyLogin()
	googlelogin.setName("test");
	googlelogin.setUsername("tabuto83");
	googlelogin.setURL("google.com")
	googlelogin.setPassword(shark.encrypt("myPassword32"));
	googlelogin.setNotes("qeesta è solo una prova del cazzo!");
	shark.addLogin(googlelogin)
	
	'''
	aes = AESCipher("pippo");
	enc = aes.encrypt("segretissimo");
	print enc
	print "\n\nDecripted: "+aes.decrypt(enc)
	'''
    
    
def main():
    pass

if __name__ == "__main__":
	pass
	#__entry_point()
