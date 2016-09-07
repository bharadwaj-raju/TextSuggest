import traceback
import sys

def matches(text):

	return text.startswith('%')

def process(text):

	text = text[1:]

	try:
		return str(eval(text))

	except:
		sys.stderr.write(traceback.format_exc())
		sys.stderr.flush()
		sys.stderr.write('ERR_EXPRESSION: Invalid expression: %s' % text)

		sys.exit(3)
