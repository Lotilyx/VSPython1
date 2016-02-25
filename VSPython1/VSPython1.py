# -- coding: utf-8 --

""" Function #1 of this script: Consume the flawed .csv files from AIS and automate the
	operations required to make them presentable to customers.
	
	TO DO list:
[x]	First: Remove lines of former PL-specific products which do not have a translation
			for the language which the file is in.
[x]	Second: automate the buttload of find/replace operations.
[ ]	Third: add flexibility with prompts and argv instead of using glorious global variables.
[ ]	Fourth: cleanup all the trope-y comments and junk that I've added (like this).
[x]	Fifth: rewrite the horribly inefficient text_fix function. (yep, completed before the others)
[ ] Sixth: add an option to concatenate articlevalues.
"""

import os
import csv
import re

# Instead of a path variable, I"m just going to use this for now ...
os.chdir("B:\\tests")

# ... so that I can use relative paths in the global variables. Suck it best practices.
in_file = "AIS_export_test.csv"
out_file = "AIS_export_test_outfile.csv"
strings_to_filter = ["Deutsch", "Nederlands", "English", "Francais", "Polski"]
flag_concat_values = True # execute the function that concatenates values, or not.

# NOTES TO SELF: 

# Errors related to a print() function in powershell when displaying unicode seem
# to mean that PowerShell is in cp850 mode. Functions that don't print to stdout should
# not be affected. Run in IDLE if print()-assisted debugging is required.

# !! re.sub operates on a string element from the list passed by csv.reader,
# that's why semicolons are not included in the string it gets passed.

def concatenate_values(fixit_list):
	for index in fixit_list[3:10:2], field2 in fixit_list[4:11:2]:
		print(field, field2)


regexes = {
"(?P<doublespaces>[\s]{2})":" ",
"(?P<punct_ats>((?<=\.)[@]))":" ",
"(?P<padding>[\s](?!.))":"",
"(?P<nopunct_ats>(?<=[a-zA-Z\)\d])[@])":". ",
"(?P<double_prds>[\.]{2})":".",
"(?P<double_coms>[\,]{2})":",",
"(?P<double_spcs>[\ ]{2})":" ",
"(?P<linestarts>((?<!\.|[a-z])[@]))":"",
}

regex_lineends = "(?P<lineends>(?<=[a-zA-Z\d])(?!.))" # has to stay separate.

def text_fix2(fixit):
	for regex, repl in regexes.items():
		fixit = [re.sub(regex, repl, element, flags=0) for element in fixit]
	fixit[2] = re.sub(regex_lineends, ".", fixit[2], flags=0)
	if flag_concat_values == True:
		concatenate_values(fixit)
	return fixit


# safely open the files
with open(in_file, "r", encoding="utf8") as infile, open(out_file, "w", encoding="utf8", newline="") as outfile:
	# define the writer
	writer = csv.writer(outfile, delimiter=";")
	# iterate over the source file
	for row in csv.reader(infile, delimiter=";"):
		# don't copy rows which have one of "strings_to_filter" in column 2
		try:
			if row[1] not in strings_to_filter:
				# take the remaining rows, call text_fix on them and write to file
				# I think this could be rewritten with map(function, iterable), which should
				# let me remove the list comprehension from text_fix2.
				writer.writerow(text_fix2(row))
		# row 1 never has a column 2
		except IndexError:
			pass