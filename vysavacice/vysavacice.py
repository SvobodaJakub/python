# Author: Jakub Svoboda
# License: To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.


class Vysavacice:
	"""Reads words from a word list file and matches them into concatenations that share the common beginning/end of the individual word pairs. E.g. words PICTURE and RELAXATION from the list form a concatenated word PICTURELAXATION. The class also provides intermediary data that can be used for other purposes."""

	def __init__(self, word_list_file_name, glue_len_num_of_chars, word_len_limit):
		self.wordlist = self.read_word_list_file(word_list_file_name, word_len_limit, glue_len_num_of_chars)
		self.word_endings_dict, self.word_beginnings_dict = self.create_word_glue_dicts(self.wordlist, glue_len_num_of_chars)
		self.concatenated_words_dict, self.concatenated_equations_dict, self.dict_glue_numofwords, self.dict_numofwords_listofglues = self.match_glue_words(self.word_endings_dict, self.word_beginnings_dict, glue_len_num_of_chars)
		self.exploded_list_eq, self.exploded_list_words = self.explode_concats_ascending_order(self.dict_numofwords_listofglues, self.concatenated_equations_dict, self.concatenated_words_dict)


	def read_word_list_file(self, file_name, word_len_limit, glue_len_num_of_chars):
		"""Reads words from a file and saves them into a list. Assumes that there is one word per line and the file is in UTF-8."""
		wordlist=list() # in-memory representation of the wordlist
		with open(file_name, "rb") as f:
			for line in f:
				# assuming the file is in utf-8
				byte_string = line.rstrip() # strip the newline
				unicode_string = unicode(byte_string, "utf-8") # convert the byte-based string which holds utf8-encoded data into a true unicode string
				# do not use too short words; do not use too long words - they are usually not funny
				if len(unicode_string) > glue_len_num_of_chars and len(unicode_string) < word_len_limit:
					wordlist.append(unicode_string) 
		return wordlist



	def create_word_glue_dicts(self, word_list, match_char_num):
		"""Creates two dictionaries with endings/beginnings and the respective words."""
		word_endings_dict = {} # dict of string:list (ending:list of words with that ending)
		word_beginnings_dict = {}
		howmany = match_char_num
		for word in word_list:
			word_end = word[-howmany:]
			word_beg = word[:howmany]
			end_found = word_end in word_endings_dict
			beg_found = word_beg in word_beginnings_dict
			if end_found:
				endings_list = word_endings_dict[word_end]
				endings_list.append(word) 
			else:
				endings_list = list()
				endings_list.append(word) 
				word_endings_dict[word_end] = endings_list
			if beg_found:
				beginnings_list = word_beginnings_dict[word_beg]
				beginnings_list.append(word) 
			else:
				beginnings_list = list()
				beginnings_list.append(word) 
				word_beginnings_dict[word_beg] = beginnings_list
		return word_endings_dict, word_beginnings_dict



	def match_glue_words(self, word_endings_dict, word_beginnings_dict, glue_len_num_of_chars):
		"""Matches ends of words from word_endings_dict with beginnings of words from word_beginnings_dict."""
		glue_count = {} # dict of string:integer (glue/start/end string:number of words created using this glue string)
		glue_count2 = {} # dict of integer:list (number of words created using this glue string:list of glue/start/end string)
		concatenated_words_dict = {} # dict of string:list (glue:list of words with that glue)
		concatenated_equations_dict = {} # dict of string:list (glue:list of word concatenation equations with that glue)
		count_set = set() # set of counts of words for individual glue strings
		howmany = glue_len_num_of_chars

		# match beginnings and ends
		for glue in word_endings_dict:
			if glue in word_beginnings_dict:
				endings_list = word_endings_dict[glue]
				beginnings_list = word_beginnings_dict[glue]
				glued_words_list = list()
				glued_equations_list = list()
				glued_words_count = 0
				for word1 in endings_list:
					for word2 in beginnings_list:
						concatenated = word1 + word2[howmany:]
						concatenated_equation = u"".join((word1, u" + ", word2, u" = ", concatenated))
						glued_words_list.append(concatenated)
						glued_equations_list.append(concatenated_equation)
						glued_words_count += 1
				# save the glued words and all accompanying information
				if glued_words_count > 0:
					concatenated_words_dict[glue] = glued_words_list
					concatenated_equations_dict[glue] = glued_equations_list
					glue_count[glue] = glued_words_count
					if glued_words_count in glue_count2:
						glue_count2[glued_words_count].append(glue)
					else:
						new_list = list()
						new_list.append(glue)
						glue_count2[glued_words_count] = new_list
					count_set.add(glued_words_count)
		return concatenated_words_dict, concatenated_equations_dict, glue_count, glue_count2

			
	def explode_concats_ascending_order(self, dict_numofwords_listofglues, concatenated_equations_dict, concatenated_words_dict):
		"""Explodes concatenations from concatenated_equations_dict, concatenated_words_dict according to the list of incidence for individual glue strings in ascending order. Concatenations with unique glue strings are listed first and after that are listed concatenations with more and more common glue strings."""
		count_list = sorted(dict_numofwords_listofglues.keys()) # ascending order
		exploded_list_eq = list()
		exploded_list_words = list()
		for glue_count in count_list:
			glue_list = dict_numofwords_listofglues[glue_count]
			for glue in glue_list:
				eq_list = concatenated_equations_dict[glue]
				for eq in eq_list:
					exploded_list_eq.append(eq)
				word_list = concatenated_words_dict[glue]
				for word in word_list:
					exploded_list_words.append(word)
		return exploded_list_eq, exploded_list_words

	def print_result(self):
		"""Prints the result of all concatenations."""
		for word in self.exploded_list_eq:
			## printing unicode sometimes throws an error (TODO: why?) but printing binary str with utf-8-encoded text is OK
			## assuming that the OS uses utf-8
			print word.encode("utf-8")


	
import unittest
import os
 
class VysavaciceUnittest(unittest.TestCase):

	def setUp(self):
		pass
		f = open("unittest_vysavacice_tmp.txt", "w")
		f.write("wordabc\n")
		f.write("worddef\n")
		f.write("wrodabc\n")
		f.write("foobarword\n")
		f.write("foobarwrod\n")
		f.write("foobarwo\n")
		f.write("wotoolongwordxxxxxxxxxxxxxbc\n")
		f.close()
		## endings
		## - bc: wordabc, wrodabc, wotoolongwordxxxxxxxxxxxxxbc
		## - ef: worddef
		## - rd: foobarword
		## - od: foobarwrod
		## - wo: foobarwo
		## beginnings
		## - wo: wordabc, worddef, wotoolongwordxxxxxxxxxxxxxbc
		## - wr: wrodabc
		## - fo: foobarword, foobarwrod

	def tearDown(self):
		os.remove("unittest_vysavacice_tmp.txt")

	def test_read_word_list_file(self):
		filename = "unittest_vysavacice_tmp.txt"
		len_limit = 11
		glue_len = 2
		vys = Vysavacice(filename, len_limit, glue_len)
		wordlist = vys.read_word_list_file(filename, len_limit, glue_len)
		self.assertIn("wordabc", wordlist)
		self.assertIn("foobarwrod", wordlist)
		self.assertNotIn("wotoolongwordxxxxxxxxxxxxxbc", wordlist)
		
	def test_create_word_glue_dicts(self):
		filename = "unittest_vysavacice_tmp.txt"
		len_limit = 11
		glue_len = 2
		vys = Vysavacice(filename, len_limit, glue_len)
		wordlist = vys.read_word_list_file(filename, len_limit, glue_len)
		word_endings_dict, word_beginnings_dict = vys.create_word_glue_dicts(wordlist, glue_len)

		self.assertIn("bc", word_endings_dict)
		self.assertIn("ef", word_endings_dict)
		self.assertIn("rd", word_endings_dict)
		self.assertIn("od", word_endings_dict)
		self.assertIn("wo", word_beginnings_dict)
		self.assertIn("wr", word_beginnings_dict)
		self.assertIn("fo", word_beginnings_dict)
		self.assertIn("wordabc", word_endings_dict["bc"])
		self.assertIn("wrodabc", word_endings_dict["bc"])# tests that multiple words are correctly registered for one ending
		self.assertIn("foobarword", word_endings_dict["rd"])
		self.assertIn("wrodabc", word_beginnings_dict["wr"])
		self.assertIn("foobarword", word_beginnings_dict["fo"])
		self.assertIn("foobarwrod", word_beginnings_dict["fo"])# tests that multiple words are correctly registered for one beginning
		self.assertNotIn("wotoolongwordxxxxxxxxxxxxxbc", word_beginnings_dict["wo"])

	def test_match_glue_words(self):
		filename = "unittest_vysavacice_tmp.txt"
		len_limit = 11
		glue_len = 2
		vys = Vysavacice(filename, len_limit, glue_len)
		wordlist = vys.read_word_list_file(filename, len_limit, glue_len)
		word_endings_dict, word_beginnings_dict = vys.create_word_glue_dicts(wordlist, glue_len)
		concatenated_words_dict, concatenated_equations_dict, dict_glue_numofwords, dict_numofwords_listofglues = vys.match_glue_words(word_endings_dict, word_beginnings_dict, glue_len)

		self.assertIn("foobarwordabc", concatenated_words_dict["wo"])
		self.assertIn("foobarworddef", concatenated_words_dict["wo"])

	def test_explode_concats(self):
		filename = "unittest_vysavacice_tmp.txt"
		len_limit = 11
		glue_len = 2
		vys = Vysavacice(filename, len_limit, glue_len)
		wordlist = vys.read_word_list_file(filename, len_limit, glue_len)
		word_endings_dict, word_beginnings_dict = vys.create_word_glue_dicts(wordlist, glue_len)
		concatenated_words_dict, concatenated_equations_dict, dict_glue_numofwords, dict_numofwords_listofglues = vys.match_glue_words(word_endings_dict, word_beginnings_dict, glue_len)
		exploded_list_eq, exploded_list_words = vys.explode_concats_ascending_order(dict_numofwords_listofglues, concatenated_equations_dict, concatenated_words_dict)

		self.assertIn("foobarwordabc", exploded_list_words)
		self.assertIn("foobarworddef", exploded_list_words)

		



# runs the test suite if run as a standalone program
if __name__ == '__main__':
    unittest.main()
