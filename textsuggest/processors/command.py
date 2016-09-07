import subprocess as sp

def matches(text):

	return text.startswith('#')

def process(text):

	text = text[1:]

	result = sp.check_output(text, shell=True).decode('utf-8').rstrip().replace('\\n', '\n')

	return result
