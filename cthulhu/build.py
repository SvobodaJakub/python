import hashlib
import random
import base64

class NameGenerator(object):
	def __init__(self):
		self.uniq_gen_conversions = {}
		self.uniq_gen_results = set()
	#TODO static function
	def transform(self, input):
		# source: http://ephemer.kapsi.fi/FhtagnGenerator.php?count=500&format=text&fhtagn=yes
		corpus = "PhngluimglwnafhCthulhuRlyehwgahnaglfhtagnChaugnarFaugnCthulhuTsathogguaepshoggstellbsnarluhulnsyhahyaaglftaghuYoggothogngAzathothbthnkfthrodshugggofnnftaghufRlyehSuhnAzathothhaigothaTsathogguaaiytharanakorrenaCthulhuychphgebnogfhtagnngshuggfmlatghgebvulgtmhYoggothgokasyhahgnaiihepaglphkyarnakkyarnakogphfmlatghkadishtuorreCthulhulwnafhhngluicnghftngAzathothshaggahcshtunggliphlegethgokasllhashaggAzathothliheeehyennnbugnghafhupadghshagggnaiihchChtenfffgothagebebunmamgnythmnahnfhtagnmghriichbugothhphlegethchmnahntharanakfehyephyhahathgshtungglisgnwahlnghaftaghunghftftaghugothafllllathgsuhnb" # len == 595; 593 is a prime number

		sha512 = hashlib.sha512(input).digest()
		cthulhu_string = ""
		for dig_index in range(0,len(sha512),2):
			byte1 = ord(sha512[dig_index])
			byte2 = ord(sha512[dig_index+1])
			selected_char = (byte1 * 256 + byte2) % (len(corpus)-2)
			cthulhu_string += corpus[selected_char]
			cthulhu_string += corpus[selected_char+1]
		selected_len = 8
		selected_len += (ord(hashlib.sha256(input).digest()[0]) % 31)
		return cthulhu_string[:selected_len]
	def __call__(self, orig_name):
		if orig_name in self.uniq_gen_conversions:
			return self.uniq_gen_conversions[orig_name]
		else:
			transformed = self.transform(orig_name)
			while transformed in self.uniq_gen_results:
				# generate a result that is unique among all the results
				transformed = self.transform(transformed + "orig_name")
			self.uniq_gen_results.add(transformed)
			self.uniq_gen_conversions[orig_name] = transformed
			return transformed

class ObfuscationConfig(object):
	files = [("src/genzip04.py", "build/eylru.py")]
	names = [

"save_balooned_contentxml", 
"process_step_to_scramble", 
"processing_step", 
"contentxml_gen", 
"part2_beg", 
"part2_end", 
"contextxml_read", 
"contentxml", 
"template_path", 
"save_stored", 
"write_odt",
"writegen", 

"shared_dict", "scramble", "patchGlueStepsTogetherOrdered", "GlueStepsTogetherOrdered", "GlueStepsTogether", "self", "sorted_keys", "shared_obj", "glue_instance", "decorated", "start", "chain_pos", "pos_of_curr_fun", "order_str", "next_fun", "chain_values_nop", "last_called_fun", "chain_keys", "chain_copy", "chain",


"shrobj" ,

"odt_contents_mimetype",
"odt_contents_META_INF_manifest_xml",
"odt_contents_manifest_rdf",
"odt_contents_meta_xml",
"odt_contents_settings_xml",
"odt_contents_styles_xml",
"odt_contents_content_xml_part",
"odt_contents_meta_xml"


]
	decorator = "process_step_to_scramble"


namegen = NameGenerator()
print(namegen("hello"))
print(namegen("testhello"))
print(namegen("teasdfsthello"))
print(namegen("taasdfsthello"))
print(namegen("tsadfaaasdfsthello"))
print(namegen("tsadfsfdfaaasdfsthello"))
print ObfuscationConfig.decorator


for (origfilename, newfilename) in ObfuscationConfig.files:


	# step 1 - the individual functions decorated with GlueStepsTogether are redecorated so as to be decorated with GlueStepsTogetherOrdered and with a unique string that controls the order
	def_indiv_sortstrings = []
	with open(origfilename, "r") as forig, open(newfilename + "._step01_" , "w") as fnew:
		def_indiv_count = 0
		curr_def_indiv = ""
		def_indiv_list = []
		inside_def_indiv = False
		inside_def_indiv_firstline = False
		inside_def_area = False
		for line in forig:

			newline = line
			
			if inside_def_indiv and not inside_def_indiv_firstline and len(newline)>2 and (newline[0].isalpha() or newline[0] == "@"):
				# this line doesn't belong to the last decorated function anymore
				inside_def_indiv = False
				def_indiv_list.append(curr_def_indiv)
				curr_def_indiv = ""
	

			if not inside_def_indiv and (("@" + ObfuscationConfig.decorator) in newline):
				# a new decorated function
				inside_def_indiv = True
				inside_def_indiv_firstline = True
				inside_def_area = True
				def_indiv_count += 1
				sortstring = "sortstring{:04d}".format(def_indiv_count)
				newline = newline.replace(ObfuscationConfig.decorator, ObfuscationConfig.decorator + '("{}")'.format(sortstring))
				def_indiv_sortstrings.append(sortstring)
				curr_def_indiv += newline
				print("+= {} ..........to this: {}\n".format(newline, curr_def_indiv))
			elif inside_def_indiv:
				inside_def_indiv_firstline = False
				curr_def_indiv += newline
				print("+= {} ..........to this: {}\n".format(newline, curr_def_indiv))
			elif not inside_def_indiv and inside_def_area and (("@" + ObfuscationConfig.decorator) not in newline):
				# something else than the individual decorated functions for reordering -> flush all the decorated functions so far into the output

				inside_def_area = False
				random.shuffle(def_indiv_list)
				for indiv in def_indiv_list:
					print("writing this: {}".format(indiv))
					fnew.write(indiv)
				def_indiv_list = []

				# and write the current line
				fnew.write(newline)
			elif (ObfuscationConfig.decorator + ".start()") in newline:
				# for further obfuscation, apply the patch
				fnew.write(newline.replace(ObfuscationConfig.decorator + ".start()", "patchGlueStepsTogetherOrdered(" + ObfuscationConfig.decorator + ")"))
				fnew.write(newline)

				# because with the patched version of GlueStepsTogetherOrdered the original decorator instance is now just a function and the individual steps of the execution chain are executed one by one by repeated calling of the function, let's write the function call enought times here
				for i in range(def_indiv_count + 1):
					fnew.write(newline.replace(ObfuscationConfig.decorator + ".start()", ObfuscationConfig.decorator + "()"))
			elif (ObfuscationConfig.decorator + " = GlueStepsTogether(") in newline:
				fnew.write(newline.replace(ObfuscationConfig.decorator + " = GlueStepsTogether(", ObfuscationConfig.decorator + " = GlueStepsTogetherOrdered("))
			else:
				fnew.write(newline)
		random.shuffle(def_indiv_list)
		for indiv in def_indiv_list:
			fnew.write(indiv)

	# obfuscate the ordering strings in the decorators but keep the alphabetical order
	def_indiv_sortstrings_obfus = []	
	for s in def_indiv_sortstrings:
		def_indiv_sortstrings_obfus.append(namegen(s))
	def_indiv_sortstrings_obfus.sort()
	def_indiv_sortstrings_obfus_dict = dict(zip(def_indiv_sortstrings, def_indiv_sortstrings_obfus))


	# step2 - replace the specified names and decorator strings with an obfuscated version
	with open(newfilename + "._step01_" , "r") as forig, open(newfilename + "._step02_" , "w") as fnew:
		inside_docstring = False
		for line in forig:
			newline = line

			# search and replace
			for name in ObfuscationConfig.names:
				newline = newline.replace(name, namegen(name))
			for key, value in def_indiv_sortstrings_obfus_dict.items():
				newline = newline.replace(key, value)

			# strip comments
			# (very simplistic implementation - doesn't allow for # symbols inside comments)
			if "#" in newline:
				pos = newline.find("#")
				newline = newline[:pos] + newline[-1:]

			# strip docstrings
			# (very simplistic implementation - doesn't allow for ordinary multiline strings)
			if '"""' in newline:
				pos = newline.find('"""')
				beg = newline[:pos]
				end = newline[pos+3:]
				two_found = '"""' in end
				if not inside_docstring and two_found:
					newline = "\n"
				elif not inside_docstring and not two_found:
					newline = "\n"
					inside_docstring = True
				elif inside_docstring:
					newline = "\n"
					inside_docstring = False
			else:
				if inside_docstring:
					newline = "\n"
					
					

			print("\n{}\n->\n{}\n".format(line, newline))
			fnew.write(newline)

	string_obfus_dict = {}
	# step3 - build a dictionary of all used strings and obfuscate them 
	# a very brave assumption here is that there is only one string per line and each string takes only one line
	with open(newfilename + "._step02_", "r") as forig, open(newfilename + "._step03_", "w") as fnew:
		for line in forig:
			newline = line
			used_quote = None
			for i in range(0, len(line)):
				if line[i] == '"':
					used_quote = '"'
					break
				if line[i] == "'":
					used_quote = "'"
					break
			if used_quote is not None:
				pos1 = line.find(used_quote)
				part1 = line[:pos1]
				rest = line[pos1+1:]
				rest = rest[::-1] # reverse
				pos2 = rest.find(used_quote) # finds the first occurrence from the end of the original string
				part3 = rest[:pos2] # the end of the line after the string
				part3 = part3[::-1] # reverse back
				part2 = rest[pos2+1:] # the string on the line
				part2 = part2[::-1] # reverse back
				if part2 in string_obfus_dict:
					part2obfus = string_obfus_dict[part2]
				else:
					part2obfus = namegen(part2)
					string_obfus_dict[part2] = part2obfus
				newline = part1 + part2obfus + part3
			fnew.write(newline)

	with open(newfilename + "._step03_", "r") as forig, open(newfilename, "w") as fnew:
		fnew.write("import base64\n")
		globals_new_name = namegen("globals")
		fnew.write("{} = globals\n".format(globals_new_name))
		for clear_str, obf_name in string_obfus_dict.items():
			enc_clear_str = base64.b64encode(clear_str)
			enc_obf_name = base64.b64encode(obf_name)
			fnew.write("{}()[base64.b64decode('{}')] = base64.b64decode('{}')\n".format(globals_new_name, enc_obf_name, enc_clear_str))
		print(str(string_obfus_dict))
		for line in forig:
			fnew.write(line)

			
import shutil
shutil.copyfile("src/cthulhu.py", "bin/cthulhu.py")
shutil.copyfile("build/eylru.py", "bin/eylru.py")

