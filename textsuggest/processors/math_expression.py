import traceback
import sys
from math import *  # simpler + shorter (for users): math.sqrt() → sqrt()

def matches(text):

	return text.startswith('%')

def process(text):

	text = text[1:]

	try:
		return str(eval(text))

	except (SyntaxError, NameError, UnboundLocalError):
		sys.stderr.write(traceback.format_exc())
		sys.stderr.flush()
		sys.stderr.write('ERR_EXPRESSION: Invalid expression: %s' % text)

		sys.exit(3)
