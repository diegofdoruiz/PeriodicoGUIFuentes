import os

class CreateFile(object):

	"""docstring for ClassName"""
	def __init__(self):
		self.file = None
		# Temp Inputs Dict
		self.inputs = {}
		self.current_input = 0
		self.newspaper_total_of_pages = 0
		self.minizinc_path = '/Applications/MiniZincIDE.app/Contents/Resources/minizinc'
		self.line_x = ''
		self.line_pages_x = ''

	# Return inputs dict
	def getInputs(self):
		return self.inputs

	# Return result line_x
	def getLineX(self):
		return self.line_x

	# Return result line_pages_x
	def getLinePagesX(self):
		return self.line_pages_x

	# Add new input to dict
	def setInputs(self, topic, min_p, max_p, pot_r):
		#Inputs es un diccionario. Guarda cada valor a medida que se entrega en la interfaz
		new_input = {}
		new_input['topic'] = topic
		new_input['min_number_of_pages'] = min_p
		new_input['max_number_of_pages'] = max_p
		new_input['potential_readers_per_page'] = pot_r
		self.inputs[self.current_input] = new_input
		self.current_input = self.current_input + 1

	def setNewspaperTotalpages(self, total):
		self.newspaper_total_of_pages = total

	# From dict to file dzn
	def createFileDZN(self):
		self.file = open('files/data.dzn', "w")
		self.file.write("% Data\n")
		self.file.write("%  data.dzn\n")
		self.file.write("\n")

		# n topics
		#Escribe en el archivo data.dzn
		self.file.write("n = "+str(len(self.inputs))+";\n");

		# potential readers per page
		self.file.write("PotentialReaders = [")
		control = 0
		for inpu in self.inputs:
			control = control + 1
			if control == len(self.inputs):
				self.file.write(str(self.inputs[inpu]['potential_readers_per_page']))
			else:
				self.file.write(str(self.inputs[inpu]['potential_readers_per_page'])+", ")
		self.file.write("];\n")

		# min number of pages per topic
		self.file.write("MinTopicPages = [")
		control = 0
		for inpu in self.inputs:
			control = control + 1
			if control == len(self.inputs):
				self.file.write(str(self.inputs[inpu]['min_number_of_pages']))
			else:
				self.file.write(str(self.inputs[inpu]['min_number_of_pages'])+", ")
		self.file.write("];\n")

		# max number of pages per topic
		self.file.write("MaxTopicPages = [")
		control = 0
		for inpu in self.inputs:
			control = control + 1
			if control == len(self.inputs):
				self.file.write(str(self.inputs[inpu]['max_number_of_pages']))
			else:
				self.file.write(str(self.inputs[inpu]['max_number_of_pages'])+", ")
		self.file.write("];\n")


		# max number of pages
		self.file.write("NewspaperTotalPages = "+str(self.newspaper_total_of_pages)+";")
		self.file.close()

	# Solve with minizinc and write in out.txt
	def solve(self):
		#Prepara los datos para visualizar en la interfaz y escribir en el archivo de salida
		command = self.minizinc_path + ' --solver Gecode files/model.mzn files/data.dzn > files/out.txt'
		os.system(command)

		#Read out.txt
		# Open the file with read only permit
		file_out = open('files/out.txt')

		# use readline() to read the first line
		line = file_out.readline()

		while line:
			# split line
			tokens = line.split()

			if len(tokens) != 0 and tokens[0] in ("x"):
				# line with varibles x
				self.line_x = line
			elif len(tokens) != 0 and tokens[0] in ("pages_x"):
				#line with pager per variable xi
				self.line_pages_x = line

			# use realine() to read next line
			line = file_out.readline()
		#close file_out file
		file_out.close()

		# clean results line_x only: false, true, false, ...
		#Limpia los resultados
		self.line_x = self.line_x[19:-4]

		# clean results line_pages_x only: 5, 7, 2, ....
		self.line_pages_x = self.line_pages_x[25:-4]		