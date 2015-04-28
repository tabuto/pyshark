import unittest
from pyshark import PyShark,PyLogin
class SharkTester(unittest.TestCase):
	
	def setUp(self):
		self.pyshark = PyShark("tester123067","pyshark_test.db")
		a = PyLogin()
		a.setName("testA");
		a.setUsername("user_A");
		a.setURL("AAA.com")
		a.setPassword(self.pyshark.encrypt("myAAAPassword32"));
		a.setNotes("just a test");
		print a
		b = PyLogin()
		b.setName("testB");
		b.setUsername("user_B");
		b.setURL("BBB.com")
		b.setPassword(self.pyshark.encrypt("myBBBPassword32"));
		b.setNotes("just a test for B");
		print b
		self.testLogins = [a,b]
		
	
	def test_AA_insert_login(self):
		result = True;
		for l in self.testLogins:
			l_res = self.pyshark.addLogin(l)
			result = (l_res and result)
		
		self.assertTrue(result)
		
	
	def test_B_getALLLogin(self):
		logins = self.pyshark.getAll();
		self.assertEqual(len(self.testLogins),len(logins))
	
	def test_C_checkALLLogin(self):
		logins = self.pyshark.getAll();
		log_dict = {}
		for l in logins:
			l.setPassword(self.pyshark.decrypt( l.getPassword() ))
			log_dict[l.getName()]=l
		result = True;
		
		for l2 in self.testLogins:
			l2.setPassword(self.pyshark.decrypt( l2.getPassword() ))
			l2.setId(log_dict[l2.getName()].getId())
			test = l2.__dict__ == log_dict[l2.getName()].__dict__
			result = (result and test)
			if(not result):
				print "Error"
				print l2.__dict__
				print "\n not equal to "
				print log_dict[l2.getName()].__dict__
		self.assertTrue(result)
'''		
	def test_C_insert_note(self):
		testNote='note2Test43253443654567453678645346765435678654356786543'
		pyguiclinote.setNoteText(testNote)
		pyguiclinote.setNoteId(1)
		pyguiclinote.insertNote()	
		text = pyguiclinote.getNoteTextById()
		self.assertEqual(text, testNote)

	def test_D_show_note_list(self):
		test = "-- Note List -- \n1] note2Test432534436545674\n"
		result = pyguiclinote.getAllNotes()
		self.assertEqual(result, test)
	
	def test_E_edit_note(self):
		testNote='note2Test edited 432443278822946'
		pyguiclinote.setNoteText(testNote)
		pyguiclinote.setNoteId(1)
		result = pyguiclinote.editNote()	
		self.assertTrue(result)
'''


if __name__ == '__main__':
	unittest.main()
