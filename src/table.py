import matplotlib

matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import *
from numpy import *
import datetime
from PIL import Image, ImageTk
import sys
from time import sleep

try:
	import tkinter as tk
	from tkinter.colorchooser import askcolor
	from tkinter import filedialog

except ImportError:
	import Tkinter as tk
	from tkColorChooser import askcolor
	import tkFileDialog as filedialog


## Start of Application
class Radio(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.createWidgets(master)

	def createWidgets(self, master):
		self.element = tk.StringVar()
		column1 = [('H', 'Hydrogen'),
				   ('Li', 'Lithium'),
				   ('Na', 'Sodium'),
				   ('K', 'Potassium'),
				   ('Rb', 'Rubidium'),
				   ('Cs', 'Cesium'),
				   ('Fr', 'Francium')
				   ]
		column2 = [('Be', 'Beryllium'),
				   ('Mg', 'Magnesium'),
				   ('Ca', 'Calcium'),
				   ('Sr', 'Strontium'),
				   ('Ba', 'Barium'),
				   ('Ra', 'Radium')
				   ]
		column3 = [('Sc', 'Scandium'),
				   ('Y', 'Yttrium'),
				   ('La >|', 'Lanthanum'),
				   ('Ac >|', 'Actinium')
				   ]
		column4 = [('Ti', 'Titanium'),
				   ('Zr', 'Zirconium'),
				   ('Hf', 'Hafnium'),
				   ('Rf', 'Rutherfordium')
				   ]
		column5 = [('V', 'Vanadium'),
				   ('Nb', 'Niobium'),
				   ('Ta', 'Tantalum'),
				   ('Db', 'Dubnium')]

		column6 = [('Cr', 'Chromium'),
				   ('Mo', 'Molybdenum'),
				   ('W', 'Tungsten'),
				   ('Sg', 'Seaborgium')]
		column7 = [('Mn', 'Manganese'),
				   ('Tc', 'Technetium'),
				   ('Re', 'Rhenium'),
				   ('Bh', 'Bohrium')]
		column8 = [('Fe', 'Iron'),
				   ('Ru', 'Ruthenium'),
				   ('Os', 'Osmium'),
				   ('Hs', 'Hassium')]
		column9 = [('Co', 'Cobalt'),
				   ('Rh', 'Rhodium'),
				   ('Ir', 'Iridium'),
				   ('Mt', 'Meitnerium')]
		column10 = [('Ni', 'Nickel'),
					('Pd', 'Palladium'),
					('Pt', 'Platinum'),
					('Ds', 'Darmstadtium')]
		column11 = [('Cu', 'Copper'),
					('Ag', 'Silver'),
					('Au', 'Gold'),
					('Rg', 'Roentgenium')]
		column12 = [('Zn', 'Zinc'),
					('Cd', 'Cadmium'),
					('Hg', 'Mercury'),
					('Cn', 'Copernicium')]
		column13 = [('B', 'Boron'),
					('Al', 'Aluminum'),
					('Ga', 'Gallium'),
					('In', 'Indium'),
					('Tl', 'Thallium'),
					('Nh', 'Nihonium')]
		column14 = [('C', 'Carbon'),
					('Si', 'Silicon'),
					('Ge', 'Germanium'),
					('Sn', 'Tin'),
					('Pb', 'Lead'),
					('Fl', 'Flerovium')]
		column15 = [('N', 'Nitrogen'),
					('P', 'Phosphorus'),
					('As', 'Arsenic'),
					('Sb', 'Antimony'),
					('Bi', 'Bismuth'),
					('Mc', 'Moscovium')]
		column16 = [('O', 'Oxygen'),
					('S', 'Sulfur'),
					('Se', 'Selenium'),
					('Te', 'Tellurium'),
					('Po', 'Polonium'),
					('Lv', 'Livermorium')]
		column17 = [('F', 'Fluorine'),
					('Cl', 'Chlorine'),
					('Br', 'Bromine'),
					('I', 'Iodine'),
					('At', 'Astatine'),
					('Ts', 'Tennessine')]
		column18 = [('He', 'Helium'),
					('Ne', 'Neon'),
					('Ar', 'Argon'),
					('Kr', 'Krypton'),
					('Xe', 'Xenon'),
					('Rn', 'Radon'),
					('Og', 'Oganesson')]


		row8 = [
			('>| Ce', 'Cerium'),
			('Pr', 'Praseodymium'),
			('Nd', 'Neodymium'),
			('Pm', 'Promethium'),
			('Sm', 'Samarium'),
			('Eu', 'Europium'),
			('Gd', 'Gadolinium'),
			('Tb', 'Terbium'),
			('Dy', 'Dyprosium'),
			('Ho', 'Holmium'),
			('Er', 'Erbium'),
			('Tm', 'Thulium'),
			('Yb', 'Ytterbium'),
			('Lu', 'Lutetium')
			]
		row9 = [
			('>| Th', 'Thorium'),
			('Pa', 'Protactinium'),
			('U', 'Uranium'),
			('Np', 'Neptunium'),
			('Pu', 'Plutonium'),
			('Am', 'Americium'),
			('Cm', 'Curium'),
			('Bk', 'Berkelium'),
			('Cf', 'Californium'),
			('Es', 'Einsteinium'),
			('Fm', 'Fermium'),
			('Md', 'Mendelevium'),
			('No', 'Nobelium'),
			('Lr', 'Lawrencium')]
		periodic_table = []
		s = 5
		def config(r, c, col):
			for b in col:
				ele = tk.Checkbutton(master, text=b[0], onvalue=b[1], offvalue=b[1], width=s, height=s, bg='grey', variable=self.element)
				ele.grid(row=r, column=c)
				periodic_table.append(b)
				r += 1
				if r > 7:
					r = 1
					c += 1



		def config2(r, c, col):
			for b in col:
				ele = tk.Checkbutton(master, text=b[0],onvalue=b[1], offvalue=b[1], width=s, height=s, bg='grey', variable=self.element)
				ele.grid(row=r, column=c)
				periodic_table.append(b)
				r += 1
				if r > 10:
					r = 1
					c += 1

		def config4(r, c, col):
			for b in col:
				ele = tk.Checkbutton(master, text=b[0],onvalue=b[1], offvalue=b[1], width=s, height=s, bg='grey', variable=self.element)
				ele.grid(row=r, column=c)
				periodic_table.append(b)
				c += 1
				if c > 18:
					c = 1
					r += 1

		config(1, 0, column1)
		config(2, 1, column2)
		config(4, 2, column3)
		config2(4, 3, column4)
		config2(4, 4, column5)
		config(4, 5, column6)
		config(4, 6, column7)
		config(4, 7, column8)
		config(4, 8, column9)
		config(4, 9, column10)
		config(4, 10, column11)
		config(4, 11, column12)
		config(2, 12, column13)
		config(2, 13, column14)
		config(2, 14, column15)
		config(2, 15, column16)
		config(2, 16, column17)
		config(1, 17, column18)
		config4(11, 3, row8)
		config4(12, 3, row9)

if __name__ == '__main__':
	root = tk.Tk()
	icon = ImageTk.PhotoImage(file='radio.png')
	root.tk.call('wm', 'iconphoto', root._w, icon)

	Radio(root)

	def quit():
		global root
		root.quit()
		root.destroy()

	root.protocol("WM_DELETE_WINDOW", quit)
	root.update()
	root.update_idletasks()

	def quit(self):
		global root
		root.quit()
		root.destroy()

	root.bind("<Escape>", quit)
	root.mainloop()