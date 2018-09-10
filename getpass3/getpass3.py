import sys

if sys.platform == 'win32' or sys.platform == 'cygwin':
	try:
		from msvcrt import *
		import colorama
		colorama.init()
		
		set_echo = '*'

		def getpass(label):
			print label,
			passwor = ''
			while True:
				inp = getch()
				if inp == '\r':
					break
				elif inp == '\b':
					print "\x1b[2K\x1b[1A"
					del passwor
					passwor = ''
					print label,
				elif inp == '\003':
					raise KeyboardInterrupt
				elif inp == '\04':
					raise EOFError
				else:
					sys.stdout.write(set_echo)
					passwor += inp
	
			print "\n",
			return  passwor
	except:
		print "Make sure that you have colorama module installed to use getpass2 module."
		print "If you don't have them you can either use 'pip install <module_name>',"
		print "or directly download from PyPI."

else:
	try:
		from getch import *
		
		set_echo = '*'

		def getpass(label):
			print label,
			passwor = ''
			while True:
				inp = getch()
				if inp == '\n':
					break
				elif inp == '\x7f':
					print "\033[2K\033[1A"
					del passwor
					passwor = ''
					print label,
				elif inp == '\003':
					raise KeyboardInterrupt
				elif inp == '\04':
					raise EOFError
				else:
					sys.stdout.write(set_echo)
					passwor += inp
		
			print "\n",
			return  passwor
	except:
		print "Make sure that you have getch module installed to use getpass2 module."
		print "If you don't have them you can either use 'pip install <module_name>',"
		print "or directly download from PyPI."
