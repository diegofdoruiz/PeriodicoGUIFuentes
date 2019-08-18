from tkinter import ttk
from tkinter import *
from createfile import *

class Periodico:
	# Manage file data
	createfile = CreateFile()
	inputs = createfile.getInputs()

	def __init__(self, window):
		self.wind = window
		self.wind.title('Newspaper')

		############## Frame 1 ####################
		# Create a Frame container
		frame = LabelFrame(self.wind, text = 'Add A new Input')
		frame.grid(row = 0, column = 0, columnspan = 3, padx=20, pady = 20, sticky=W)

		# Topic Input
		Label(frame, text = 'Topic: ').grid(row = 1, column = 0, sticky=E)
		self.topic = Entry(frame)
		self.topic.focus()
		self.topic.grid(row = 1, column = 1)

		# MinNumberOfPages Input
		Label(frame, text = 'Min Number of Pages: ').grid(row = 2, column = 0, sticky=E)
		self.min_number_of_pages = Entry(frame)
		self.min_number_of_pages.grid(row = 2, column = 1)

		# MaxNumberOfPages Input
		Label(frame, text = 'Max Number of Pages: ').grid(row = 3, column = 0, sticky=E)
		self.max_number_of_pages = Entry(frame)
		self.max_number_of_pages.grid(row = 3, column = 1)

		# PotentialReadersPerPage Input
		Label(frame, text = 'Potential Readers Per Page: ').grid(row = 4, column = 0, sticky=E)
		self.potential_readers_per_page = Entry(frame)
		self.potential_readers_per_page.grid(row = 4, column = 1)

		# Button Add Input
		ttk.Button(frame, text = 'Add Input', command = self.add_imput).grid(row = 5, columnspan = 2, sticky= W + E)

		################ Frame 2 ####################
		# Create a Frame 2 container
		frame2 = LabelFrame(self.wind, text = 'Solve Inputs')
		frame2.grid(row = 0, column = 1, columnspan = 3, padx=10, pady = 20, sticky=W)

		# This will create style object 
		style = ttk.Style() 

		style.configure('W.TButton', font = ('calibri', 20, 'bold'), 
                borderwidth = '5') 

		# Ouput Messages
		self.message2 = Label(frame2, text = '', fg = 'red')
		self.message2.grid(row =0, column = 0, columnspan = 2, sticky = W + E)

		# Max number op pages
		Label(frame2, text = 'Total Newspaper Pages: ').grid(row = 1, column = 0, sticky=E)
		self.total_pages = Entry(frame2)
		self.total_pages.focus()
		self.total_pages.grid(row = 1, column = 1)

		# Button Solve 
		btn_solve = ttk.Button(frame2, text = 'Solve', command = self.callSolver, style = 'W.TButton')
		btn_solve.grid(row = 3, columnspan = 2, sticky = W + E)

		################### Table ####################

		# Ouput Messages
		self.message = Label(text = '', fg = 'blue')
		self.message.grid(row =5, column = 0, columnspan = 2, sticky = W + E)

		# Table
		self.tree = ttk.Treeview(height = 15, columns=('#1','#2','#3','#4'))
		self.tree.grid(row = 7, column = 0, columnspan = 2)
		self.tree.heading('#1', text = 'Topic', anchor = CENTER)
		self.tree.heading('#2', text = 'Min # Pages', anchor = CENTER)
		self.tree.heading('#3', text = 'Max # Pages', anchor = CENTER)
		self.tree.heading('#4', text = 'Pot Readers Page', anchor = CENTER)
		self.tree.column('#0', width=0)

		# Button Edit Input
		ttk.Button(text = 'Edit', command = self.edit_input).grid(row = 8, column = 0, sticky= W + E)

		# Button Delete Input
		ttk.Button(text = 'Delete', command = self.delete_input).grid(row = 8, column = 1, sticky= W + E)

	# List Inputs
	def list_inputs(self):
		#Toma los datos que estan guardados en el diccionario para mostrarlos
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)

		for inpu in self.inputs: 
			topic = self.inputs[inpu]['topic']
			min_p = self.inputs[inpu]['min_number_of_pages']
			max_p = self.inputs[inpu]['max_number_of_pages']
			pot_r = self.inputs[inpu]['potential_readers_per_page']
			self.tree.insert('', 0, text = inpu, values = [topic, min_p, max_p, pot_r])

	# Add new Input
	def add_imput(self):
		self.message['text'] = ''
		if self.validation():
			topic = self.topic.get()
			try:
				min_p = int(self.min_number_of_pages.get())
			except ValueError:
				self.message['text'] = 'Min number of pages is not number'
				return

			try:
				max_p = int(self.max_number_of_pages.get())
			except ValueError:
				self.message['text'] = 'Max number of pages is not a number'
				return

			try:
				pot_r = int(self.potential_readers_per_page.get())
			except ValueError:
				self.message['text'] = 'Potential readers is not a number'
				return
			#Toma los datos de la intefaz y se guarda cada entrada en un json	
			self.createfile.setInputs(topic, min_p, max_p, pot_r)
			self.message['text'] = 'Input {} added Succesfully'.format(self.topic.get())
			self.list_inputs()
			self.topic.delete(0, END)
			self.min_number_of_pages.delete(0, END)
			self.max_number_of_pages.delete(0, END)
			self.potential_readers_per_page.delete(0, END)
		else:
			self.message['text'] = 'Todos los campos son obligatorios'

	# Edit Input
	def edit_input(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['values'][0]	
		except IndexError as e:
			self.message['text'] = 'Please select an Input'
			return
		key = self.tree.item(self.tree.selection())['text']
		old_topic = self.tree.item(self.tree.selection())['values'][0]
		old_min_p = self.tree.item(self.tree.selection())['values'][1]
		old_max_p = self.tree.item(self.tree.selection())['values'][2]
		old_read_p = self.tree.item(self.tree.selection())['values'][3]
		
		# Window update Input
		self.edit_wind = Toplevel()
		self.edit_wind.title = 'Edit Input'

		#Inputs
		Label(self.edit_wind, text = 'Old Topic: ',).grid(row = 0, column = 1, sticky=E)
		new_topic = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_topic))
		new_topic.grid(row = 0, column = 2)

		Label(self.edit_wind, text = 'Old Min # Pages: ',).grid(row = 1, column = 1, sticky=E)
		new_min_p = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_min_p))
		new_min_p.grid(row = 1, column = 2)

		Label(self.edit_wind, text = 'Old Max # Pages: ',).grid(row = 2, column = 1, sticky=E)
		new_max_p = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_max_p))
		new_max_p.grid(row = 2, column = 2)

		Label(self.edit_wind, text = 'Old # Readers per Page: ',).grid(row = 3, column = 1, sticky=E)
		new_read_p = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_read_p))
		new_read_p.grid(row = 3, column = 2)

		Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(key, new_topic.get(), new_min_p.get(), new_max_p.get(), new_read_p.get())).grid(row = 4, column = 2, sticky = W + E)

	# Edit Input
	def edit_records(self, key, new_topic, new_min_p, new_max_p, new_read_p):
		self.inputs[key]['topic'] = new_topic
		self.inputs[key]['min_number_of_pages'] = new_min_p
		self.inputs[key]['max_number_of_pages'] = new_max_p
		self.inputs[key]['potential_readers_per_page'] = new_read_p
		self.edit_wind.destroy()
		self.message['text'] = 'Input {} updated Succesfully'.format(new_topic)
		self.list_inputs()

	# Delete Input
	def delete_input(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['values'][0]	
		except IndexError as e:
			self.message['text'] = 'Please select an Input'
			return
		key = self.tree.item(self.tree.selection())['text']
		self.message['text'] = 'Input {} removed Succesfully'.format(self.inputs[key]['topic'])
		del self.inputs[key]
		self.list_inputs()

	# Validate Fields
	def validation(self):
		l_topic = len(self.topic.get())
		l_min_p = len(self.min_number_of_pages.get())
		l_max_t = len(self.max_number_of_pages.get())
		l_readers_p = len(self.potential_readers_per_page.get())
		return l_topic and l_min_p and l_max_t and l_readers_p

	# Create an resolve problem
	def callSolver(self):
		self.message['text'] = ''
		self.message2['text'] = ''
		records = self.tree.get_children()
		if len(records) < 2:
			self.message2['text'] = 'Please add at least two inputs'
			return

		if self.total_pages.get() == '':
			self.message2['text'] = 'Please add Newspaper total pages'
			return

		try:
			total_pages = int(self.total_pages.get())
		except ValueError:
			self.message2['text'] = 'Total number of pages is not a number'
			return

		self.createfile.setNewspaperTotalpages(total_pages)
		self.createfile.createFileDZN()
		self.createfile.solve()
		self.displayResults()

	def displayResults(self):
		# inputs to show
		inputs = self.inputs

		# arrays from minizinc's solutions
		array_x = self.createfile.getLineX().split(', ')
		array_pages_x = self.createfile.getLinePagesX().split(', ')

		# Window show result
		self.result_wind = Toplevel()
		self.result_wind.title = 'Results'

		result_title = Label(self.result_wind, text = 'Results:', fg = 'darkgreen')
		result_title.grid(row = 0, column = 1, columnspan = 1)
		result_title.config(font=("Courier", 44))

		# Create a Frame 3 container in result window
		frame3 = LabelFrame(self.result_wind, text = 'Included Topics', fg = 'blue')
		frame3.grid(row = 1, column = 0, padx=20, sticky= W + E)
		frame3.config(font=("Courier", 15))

		# Create a Frame 3 container in result window
		frame4 = LabelFrame(self.result_wind, text = 'Non Included Topics', fg = 'red')
		frame4.grid(row = 1, column = 2, padx=20, sticky= W + E)
		frame4.config(font=("Courier", 15))

		iterator = 0
		readers = 0
		inc_rows = 0
		n_inc_rows = 0
		for inpu in inputs:
			if array_x[iterator] == 'true':
				readers = readers + int(inputs[inpu]['potential_readers_per_page']) * int(array_pages_x[iterator])
				text = '- '+inputs[inpu]['topic'] +': '+ array_pages_x[iterator] + ' pages'
				Label(frame3, text = text, fg = 'blue').grid(row = inc_rows, column = 0, sticky= W)
				inc_rows = inc_rows + 1
			else:
				text = '- '+inputs[inpu]['topic']
				Label(frame4, text = text, fg = 'red').grid(row = n_inc_rows, column = 0, sticky= W)
				n_inc_rows = n_inc_rows + 1
			iterator = iterator + 1

		total_readers_text = 'Pot. Readers: '+str(readers)
		total_readers = Label(self.result_wind, text = total_readers_text)
		total_readers.grid(row = 3, column = 1, columnspan=1, padx=20, sticky= W + E)
		total_readers.config(font=("Courier", 20))


if __name__=='__main__':
	window = Tk()
	application = Periodico(window)
	window.mainloop()