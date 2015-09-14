# Author: Jakub Svoboda
# License: To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.

import vysavacice
import random

# initialize Vysavacice
vys = vysavacice.Vysavacice("nouns.txt", 3, 9)

# print all concatenated words
vys.print_result()

# initialize another Vysavacice
vys2 = vysavacice.Vysavacice("nouns.txt", 2, 7)

# open a file with normal text and print out a vysavacice-ized text

with open("text.txt", "rb") as f:
	for line in f:
		# assuming the file is in utf-8
		byte_string = line.rstrip() # strip the newline
		unicode_string = unicode(byte_string, "utf-8") # convert the byte-based string which holds utf8-encoded data into a true unicode string
		words = unicode_string.split(" ")
		new_line = u""
		for word in words:
			end = word[-2:] # to be the glue string with another word
			without_end = word[:-2] # the beginning of the original word left after removing the to-be-glue string
			if end in vys2.word_beginnings_dict:
				list_of_matches = vys2.word_beginnings_dict[end]
				list_len = len(list_of_matches)
				rand_pos = random.randrange(0, list_len, 1)
				rand_concat = list_of_matches[rand_pos] # random word to be concatenated
				new_word = without_end + rand_concat
				new_line += new_word + u" "
			else:
				new_line += word + u" "
		print new_line.encode("utf-8")




