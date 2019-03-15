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

dim = "#303030"  # Background
dimf = "#00C0FF"  # Font Color
disa = "#d400ff"  # Disabled Text

day = '#c6dcff'
dayf = '#008721'
days = '#e500ff'

offset = 0


## Start of Application
class Radio(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.createWidgets(master)

	def createWidgets(self, master):
		self.fig            = plt.figure(figsize=(5, 5))

		self.name           = tk.StringVar(value="RAVIOLI")

		self.long_dms_deg   = tk.DoubleVar(value=-160)
		self.long_dms_min   = tk.DoubleVar(value=0)
		self.long_dms_sec   = tk.DoubleVar(value=0.0)

		self.lat_dms_deg    = tk.DoubleVar(value=0)
		self.lat_dms_min    = tk.DoubleVar(value=0)
		self.lat_dms_sec    = tk.DoubleVar(value=0.0)
		self.antenna_alt    = tk.DoubleVar(value=0.0)

		self.name2           = tk.StringVar(value="RAVIOLI2")

		self.long_dms_deg2   = tk.DoubleVar(value=-160)
		self.long_dms_min2   = tk.DoubleVar(value=0)
		self.long_dms_sec2   = tk.DoubleVar(value=0.0)

		self.lat_dms_deg2    = tk.DoubleVar(value=0)
		self.lat_dms_min2    = tk.DoubleVar(value=0)
		self.lat_dms_sec2    = tk.DoubleVar(value=0.0)

		self.antenna_alt2    = tk.DoubleVar(value=0.0)
		self.dist           = tk.DoubleVar()
		self.mean_rad       = tk.DoubleVar()

		self.temphigh       = tk.DoubleVar(value=0.0)
		self.templow        = tk.DoubleVar(value=0.0)
		self.tempavg        = tk.DoubleVar(value=0.0)

		self.pressavg       = tk.DoubleVar(value=0.0)
		self.humiavg        = tk.DoubleVar(value=0.0)

		self.elevation      = tk.DoubleVar(value=0.0)
		self.bfield         = tk.DoubleVar(value=0.0)
		self.bfield_rel     = tk.DoubleVar(value=0.0)

		self.star           = tk.StringVar(value="G Class")
		self.solarm         = tk.DoubleVar(value=0.0)
		self.solarlum       = tk.DoubleVar(value=0.0)

		self.location       = tk.IntVar(value=1)

		self.notes          = tk.StringVar()

		self.abc            = tk.StringVar(value=0.0)
		self.dielec         = tk.DoubleVar(value=0.0)
		self.earthcond      = tk.DoubleVar(value=0.0)
		self.frequency      = tk.DoubleVar(value=0.0)
		self.rad_cli        = tk.IntVar(value=5)
		self.ant_orient     = tk.IntVar(value=1)

		self.frac_sit       = tk.DoubleVar()
		self.frac_tim       = tk.DoubleVar()

		self.active_plot    = tk.StringVar()

		self.erp            = tk.DoubleVar()

		canvas = FigureCanvasTkAgg(self.fig, master)
		canvas.get_tk_widget().grid(row=0, column=0, sticky='new')
		master.update_idletasks()
		canvas.draw()

		def writelrp(dielectric, conductivity, bending, frequency, radio_climate, polarization, frac_sit, frac_time,
					 erp):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Irregular Terrian Model Files", "*.lrp")])
			filelrp = open(fname, 'w')
			filelrp.write(str(dielectric).ljust(10)     + "; Earth Dielectric Constant (Relative permittivity)" + "\n")
			filelrp.write(str(conductivity).ljust(10)   + "; Earth Conductivity (Siemens per meter)" + "\n")
			filelrp.write(str(bending).ljust(10)        + "; Atmospheric Bending Constant (N-Units)" + "\n")
			filelrp.write(str(frequency).ljust(10)      + "; Frequency in MHz (20 MHz to 20 GHz)" + "\n")
			filelrp.write(str(radio_climate).ljust(10)  + "; Radio Climate" + "\n")
			filelrp.write(str(polarization).ljust(10)   + "; Polarization (0 = Horizontal, 1 = Vertical)" + "\n")
			filelrp.write(str(frac_sit).ljust(10)       + "; Fraction of situations" + "\n")
			filelrp.write(str(frac_time).ljust(10)      + "; Fraction of time" + "\n")
			filelrp.write(str(erp).ljust(10)            + "; ERP" + "\n")
			filelrp.close()

		def writeecp(rel_humid, temphigh, templow, elevation, bending, dielectric, conduct, Bfield, star):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'w')
			fileecp.write(str(rel_humid).ljust(10)  + "; Relative Humidity" + "\n")
			fileecp.write(str(temphigh).ljust(10)   + "; High Temperature (C)" + "\n")
			fileecp.write(str(templow).ljust(10)    + "; Low Temperature (C)" + "\n")
			fileecp.write(str(elevation).ljust(10)  + "; Elevation (m)" + "\n")
			fileecp.write(str(bending).ljust(10)    +"; Atmospheric Bending Constant (N-Units)" + "\n")
			fileecp.write(str(dielectric).ljust(10) + "; Dielectric Constant" + "\n")
			fileecp.write(str(conduct).ljust(10)    + "; Ground Conductivity (S/m)" + "\n")
			fileecp.write(str(Bfield).ljust(10)     + "; Planetary Magnetic Field (G)" + "\n")
			fileecp.write(str(star).ljust(10)       + "; Spectral Class of Main Star" + "\n")
			fileecp.close()

		def writeqth(antenna):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Location Files", "*.qth")])
			fileqth = open(fname, 'w')
			if self.location.get() == 1:
				fileqth.write(str(self.name.get()) + "\n")
				fileqth.write(str(self.lat_dms_deg.get()) + " " + str(self.lat_dms_min.get()) + " " + str(self.lat_dms_sec.get()) + "\n")
				fileqth.write(str(self.long_dms_deg.get()) + " " + str(self.long_dms_min.get()) + " " + str(self.lat_dms_sec.get()) + "\n")
				fileqth.write(str(antenna) + "\n")
				fileqth.close()
			elif self.location.get() == 2:
				fileqth.write(str(self.name2.get()) + "\n")
				fileqth.write(str(self.lat_dms_deg2.get()) + " " + str(self.lat_dms_min2.get()) + " " + str(self.lat_dms_sec2.get()) + "\n")
				fileqth.write(str(self.long_dms_deg2.get()) + " " + str(self.long_dms_min2.get()) + " " + str(self.lat_dms_sec2.get()) + "\n")
				fileqth.write(str(antenna) + "\n")
				fileqth.close()


		def readqth():
			fname = filedialog.askopenfilename(title="Get yo file", filetypes=[("Location Files", "*.qth")])
			fileqth = open(fname, 'r')
			if self.location.get() == 1:
				content = [x.strip() for x in fileqth.readlines()]
				content = [x.split() for x in content]
				self.name.set(content[0][0])
				self.lat_dms_deg.set(content[1][0])
				self.lat_dms_min.set(content[1][1])
				self.lat_dms_sec.set(content[1][2])
				self.long_dms_deg.set(content[2][0])
				self.long_dms_min.set(content[2][1])
				self.long_dms_sec.set(content[2][2])
				self.antenna_alt.set(content[3][0])
			if self.location.get() == 2:
				content = [x.strip() for x in fileqth.readlines()]
				content = [x.split() for x in content]
				self.name2.set(content[0][0])
				self.lat_dms_deg2.set(content[1][0])
				self.lat_dms_min2.set(content[1][1])
				self.lat_dms_sec2.set(content[1][2])
				self.long_dms_deg2.set(content[2][0])
				self.long_dms_min2.set(content[2][1])
				self.long_dms_sec2.set(content[2][2])
				self.antenna_alt2.set(content[3][0])

		def readlrp():
			fname = filedialog.askopenfilename(title="Get yo file",
											   filetypes=[("Irregular Terrian Model Files", "*.lrp")])
			filelrp = open(fname, 'r')
			content = [x.split(";")[0] for x in filelrp.readlines()]
			content = [x.strip() for x in content[0:9]]
			self.dielec.set(content[0])
			self.earthcond.set(content[1])
			self.abc.set(content[2])
			self.frequency.set(content[3])
			self.rad_cli.set(content[4])
			self.ant_orient.set(content[5])
			self.frac_sit.set(content[6])
			self.frac_tim.set(content[7])
			self.erp.set(content[8])

		def readecp():
			fname = filedialog.askopenfilename(title="Get yo file",
											   filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'r')
			content = [x.split(";")[0] for x in fileecp.readlines()]
			content = [x.strip() for x in content[0:9]]
			self.humid_scale.set(content[0])
			self.temphigh.set(content[1])
			self.templow.set(content[2])
			self.elevation.set(content[3])
			self.abc.set(content[4])
			self.dielec.set(content[5])
			self.earthcond.set(content[6])
			self.bfield.set(content[7])
			self.star.set(content[8])

		def Decimal_Degrees(deg, minu, sec):
			DD = deg + (minu / 60.) + (sec / 3600.)
			return DD

		def humid_calc(T, H):
			e = (H * 6.1121 * exp((17.502 * (T)) / ((T) + (240.97)))) / 100
			return e

		def pressure(altitude, T):
			P = 1013.25 * (1 - ((0.0065 * altitude) / ((T + 273.15) + 0.0065 * altitude))) ** (5.257)
			return P

		def atmo_bend(e, T, P):
			N = 77.6 * (P / (T + 273.15)) + 3.73e5 * (e / (T + 273.15) ** 2)
			return N

		def bfield(B):
			B_rel = B / (7.981e10)
			return B_rel

		def distance(self):
			phi1 = self.lat_dms_deg.get() + self.lat_dms_min.get()/60 +self.lat_dms_sec.get()/3600
			phi2 = self.lat_dms_deg2.get() + self.lat_dms_min2.get()/60 +self.lat_dms_sec2.get()/3600
			long1 = self.long_dms_deg.get() + self.long_dms_min.get()/60 + self.long_dms_sec.get()/3600
			long2 = self.long_dms_deg2.get() + self.long_dms_min2.get()/60 + self.long_dms_sec2.get()/3600
			r = self.mean_rad.get()
			D = 2*r*arcsin(sqrt((sin((phi2-phi1)/2)**2 + cos(phi1) *cos(phi2) * (sin((long2 - long1)/2))**2)))
			return D


		def temp_abc_dependence(fig, HT, LT, e, P, name, altitude):
			plt.clf()
			temp_abc = plt.scatter(linspace(LT + 273.15, HT + 273.15), atmo_bend(e, linspace(LT, HT), P))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0, 0))
			plt.title("Location: {}\nTemperature Dependence on the Atmospheric Bending Constant at {} m".format(name,altitude),pad=20,
					  fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Atmospheric Bending Constant (N-Units)")
			canvas.draw_idle()
			canvas.draw()

		def temp_press_dependence(fig, HT, LT, altitude, name):
			plt.clf()
			temp_press = plt.scatter(linspace(LT + 273.15, HT + 273.15), pressure(altitude, linspace(LT, HT)))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0, 0))
			plt.title("Location: {}\nTemperature Dependence on Air Pressure at {} m".format(name, altitude), pad=20,
					  fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Pressure (mbars)")
			canvas.draw_idle()
			canvas.draw()

		def temp_humi_dependence(fig, HT, LT, H, name, altitude):
			plt.clf()
			temp_humid = plt.scatter(linspace(LT + 273.15, HT + 273.15), humid_calc(linspace(LT, HT), H))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0, 0))
			plt.title("Location: {}\nTemperature Dependence on Humidity at {} m".format(name, altitude), pad=20,
					  fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Humidity (mbars)")
			canvas.draw_idle()
			canvas.draw()

		def super_calc():
			self.tempavg.set(float(self.temphigh.get()) / 2. + float(self.templow.get()) / 2.)
			self.humiavg.set(round(humid_calc(self.tempavg.get(), self.humid_scale.get()), 3))
			self.pressavg.set(round(pressure(self.elevation.get(), self.tempavg.get()), 3))
			self.abc.set(str(round(atmo_bend(self.humiavg.get(), self.tempavg.get() + 273.15, self.pressavg.get()), 3)))
			self.bfield_rel.set("{:0.2E}".format(bfield(self.bfield.get())))
			self.dist.set(round(distance(self),4))

		def clearqth(event):
			self.long_dd.set(0)
			self.lat_dd.set(0)
			self.antenna_alt.set(0)

		def clearlrp(event):
			self.dielec.set(0.00)
			self.earthcond.set(0.000)
			self.abc.set(0.000)
			self.frequency.set(0.0)
			self.rad_cli.set(5)
			self.ant_orient.set(1)
			self.frac_sit.set(0.00)
			self.frac_tim.set(0.00)
			self.erp.set(0.000)

		def clearecp(event):
			self.humid_scale.set(0.0)
			self.temphigh.set(0.0)
			self.templow.set(0.0)
			self.elevation.set(0.0)
			self.abc.set(0.0)
			self.dielec.set(0.0)
			self.earthcond.set(0.0)

		def event_readqth(event):
			readqth()

		def event_readlrp(event):
			readlrp()

		def event_readecp(event):
			readecp()

		###
		def event_writeqth(event):
			writeqth(self.name.get(), self.long_dd.get(), self.lat_dd.get(), self.antenna_alt.get())
		###

		def event_writelrp(event):
			writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(), self.frequency.get(), self.rad_cli.get(),
					 self.ant_orient.get(), self.frac_sit.get(), self.frac_tim.get(), self.erp.get())

		def event_writeecp(event):
			writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(), self.elevation.get(), self.abc.get(), self.dielec.get(), self.earthcond.get(), self.bfield.get(), self.star.get())

		def event_super_calc(event):
			super_calc()

		def update_plot(plot):
			if plot == "temp_abc":
				temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humiavg.get(),
									self.pressavg.get(), self.name.get(), self.elevation.get())
			elif plot == "temp_pres":
				temp_press_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.elevation.get(),
									  self.name.get())
			#			elif plot == "temp_humi":
			#				temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humid_scale.get(),
			#									 self.name.get(), self.elevation.get())
			elif plot == "temp_humi":
				def plot_error():
					top = tk.Toplevel()
					top.title = "Error"
					top.geometry("200x100")

					msg = tk.Message(top, text="Not a Valid Plotting Option")
					msg.grid(row=0, column=1,columnspan=2, sticky='nsew')

					end = tk.Button(top, text="Dismiss", command=top.destroy)
					end.grid(row=1, column=0, sticky='nsew', columnspan=2)
					top.mainloop()
				return plot_error()

		def event_update_plot(event):
			update_plot(self.active_plot.get())

		def write_notes():
			note = self.notes_input.get("1.0", "end")
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Any File", "*")])
			filenote = open(fname, 'w')
			filenote.write(note)
			filenote.close()
		def read_notes():
			fname = filedialog.askopenfilename(initialdir='./', title="Get Yo File",
											   filetypes=[("Any File", "*")])
			filenote = open(fname, 'r')
			self.notes_input.delete("1.0", "end")
			for x in filenote.readlines():
				content = x
				self.notes_input.insert("insert", content)

		##

		self.note_insert = tk.Button(master, command=lambda: read_notes())
		self.note_insert.grid(row=0, column=1, pady=600)

		n = 0
		self.name_label = tk.Label(master, text="Location Name:")
		self.name_label.grid(row=0, column=1, sticky='nw')

		self.name_entry = tk.Entry(master, width=7, textvariable=self.name)
		self.name_entry.grid(row=0, column=2, sticky='new')

		##
		self.long_dms_label = tk.Label(master, text="Longitude")
		self.long_dms_label.grid(row=0, column=3, sticky='nw')

		self.long_dms_d = tk.Entry(master, width=4, textvariable=self.long_dms_deg)
		self.long_dms_d.grid(row=0, column=4, sticky='new', padx=(0, 0))

		self.deg_lo = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_lo.grid(row=0, column=5, sticky='n')

		self.long_dms_m = tk.Entry(master, width=4, textvariable=self.long_dms_min)
		self.long_dms_m.grid(row=0, column=6, sticky='new')

		self.min_lo = tk.Label(master, text="'", font=('Times', 13))
		self.min_lo.grid(row=0, column=7, sticky='new')

		self.long_dms_s = tk.Entry(master, width=5, textvariable=self.long_dms_sec)
		self.long_dms_s.grid(row=0, column=8, columnspan=2, sticky='new', )

		self.sec_lo = tk.Label(master, text="''", font=('Times', 13))
		self.sec_lo.grid(row=0, column=10, sticky='new', )

		##
		self.lat_dms_label = tk.Label(master, text="Latitude")
		self.lat_dms_label.grid(row=0, column=3, sticky='nw', pady=30)

		self.lat_dms_d = tk.Entry(master, width=4, textvariable=self.lat_dms_deg)
		self.lat_dms_d.grid(row=0, column=4, sticky='new', pady=30)

		self.deg_la = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_la.grid(row=0, column=5, sticky='new', pady=30)

		self.lat_dms_m = tk.Entry(master, width=4, textvariable=self.lat_dms_min)
		self.lat_dms_m.grid(row=0, column=6, sticky='new', pady=30)

		self.min_la = tk.Label(master, text="'", font=('Times', 13))
		self.min_la.grid(row=0, column=7, sticky='new', pady=30)

		self.lat_dms_s = tk.Entry(master, width=5, textvariable=self.lat_dms_sec)
		self.lat_dms_s.grid(row=0, column=8, columnspan=2, sticky='new', pady=30)

		self.sec_la = tk.Label(master, text="''", font=('Times', 13))
		self.sec_la.grid(row=0, column=10, sticky='new', pady=30)

		self.ante_alt_label = tk.Label(master, text="Antenna Height" + " " * 6 + "(m)")
		self.ante_alt_label.grid(row=0, column=1, sticky='nw', pady=30)

		self.ante_alt_entry = tk.Entry(master, width=7, textvariable=self.antenna_alt)
		self.ante_alt_entry.grid(row=0, column=2, sticky='new', pady=30)

		self.createqth = tk.Button(master, command=lambda: writeqth(self.name.get(), self.long_dms_d.get(),
																	self.long_dms_m.get(), self.long_dms_s.get(),
																	self.lat_dms_d.get(), self.lat_dms_m.get(),
																	self.lat_dms_s.get(), self.antenna_alt.get()),
								   text="Generate QTH")
		self.createqth.grid(row=0, column=1, sticky='new', columnspan=1, pady=65)
		##
		self.temp_high_label = tk.Label(master, text="High Temperature" + "\t" + "(" + u"\u00B0" + "C)")
		self.temp_high_label.grid(row=0, column=1, sticky='nw', pady=110)

		self.temp_high_entry = tk.Entry(master, width=7, textvariable=self.temphigh)
		self.temp_high_entry.grid(row=0, column=2, sticky='new', pady=110)

		self.temp_low_label = tk.Label(master, text="Low Temperature" + "\t" + "(" + u"\u00B0" + "C)")
		self.temp_low_label.grid(row=0, column=1, sticky='nw', pady=140)

		self.temp_low_entry = tk.Entry(master, width=7, textvariable=self.templow)
		self.temp_low_entry.grid(row=0, column=2, sticky='new', pady=140)

		self.temp_avg_label = tk.Label(master, text="Avg. Temperature" + "\t" + "(" + u"\u00B0" + "C)")
		self.temp_avg_label.grid(row=0, column=1, sticky='nw', pady=170)

		self.temp_avg_entry = tk.Entry(master, width=7, textvariable=self.tempavg)
		self.temp_avg_entry.grid(row=0, column=2, sticky='new', pady=170)

		self.elevation_label = tk.Label(master, text="Elevation" + "\t\t" + "(m)")
		self.elevation_label.grid(row=0, column=1, sticky='nw', pady=200)

		self.elevation_entry = tk.Entry(master, textvariable=self.elevation, width=8)
		self.elevation_entry.grid(row=0, column=2, sticky='nw', pady=200)

		self.humid_label = tk.Label(master, text="Rel. Humidity" + " " * 2 + "(%)")
		self.humid_label.grid(row=0, column=3, sticky='nw', pady=110)

		self.humid_scale = tk.Scale(master, from_=0, to=100, resolution=10, orient=tk.HORIZONTAL, width=20)
		self.humid_scale.grid(row=0, column=4, columnspan=8, sticky='new', pady=85)
		self.humid_scale.set(50)

		self.humid_avg_label = tk.Label(master, text="Avg. Humidity" + " " * 1 + "(mbar)")
		self.humid_avg_label.grid(row=0, column=3, sticky='nw', pady=140)

		self.humid_avg_calc = tk.Entry(master, textvariable=self.humiavg, width=8)
		self.humid_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=1, pady=140)

		self.press_avg_label = tk.Label(master, text="Avg. Pressure" + " " * 2 + "(mbar)")
		self.press_avg_label.grid(row=0, column=3, sticky='nw', pady=170)

		self.press_avg_calc = tk.Entry(master, textvariable=self.pressavg, width=8)
		self.press_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=1, pady=170)

		self.abc_label = tk.Label(master, text="Atmospheric Bending Constant" + " " * 2 + "(N-Units)")
		self.abc_label.grid(row=0, column=3, columnspan=5, sticky='nw', pady=200)

		self.abc_entry = tk.Entry(master, textvariable=self.abc, width=8)
		self.abc_entry.grid(row=0, column=10, columnspan=2, sticky='new', pady=200)

		self.bfield_label = tk.Label(master, text="B-Field (G)")
		self.bfield_label.grid(row=0, column=6, columnspan=4, sticky='nw', pady=140)

		self.bfield_entry = tk.Entry(master, textvariable=self.bfield, width=8)
		self.bfield_entry.grid(row=0, column=10, columnspan=2, sticky='nw', pady=140)

		self.bfield_rel_label = tk.Label(master, text="Rel. B-Field (G)")
		self.bfield_rel_label.grid(row=0, column=6, columnspan=3, sticky='nw', pady=170)

		self.bfield_rel_entry = tk.Entry(master, textvariable=self.bfield_rel, width=8)
		self.bfield_rel_entry.grid(row=0, column=10, columnspan=2, sticky='nw', pady=170)

		self.pan_calc = tk.Button(master, text="Calculate", command=lambda: super_calc())
		self.pan_calc.grid(row=0, column=1, sticky='new', pady=235)

##

		self.dielectric_label = tk.Label(master, text="Dielectric Constant")
		self.dielectric_label.grid(row=0, column=1, sticky='nw', pady=280)

		self.dielectric_entry = tk.Entry(master, textvariable=self.dielec, width=8)
		self.dielectric_entry.grid(row=0, column=2, sticky='new', pady=280)

		self.ground_cond_label = tk.Label(master, text="Earth Conductivity" + "\t" + "(S/m)")
		self.ground_cond_label.grid(row=0, column=1, sticky='nw', pady=310)

		self.ground_cond_entry = tk.Entry(master, textvariable=self.earthcond, width=8)
		self.ground_cond_entry.grid(row=0, column=2, sticky='new', pady=310)

		self.frequency_label = tk.Label(master, text="Frequency" + "\t" + "(MHz)")
		self.frequency_label.grid(row=0, column=1, sticky='nw', pady=340)

		self.frequency_entry = tk.Entry(master, textvariable=self.frequency, width=8)
		self.frequency_entry.grid(row=0, column=2, sticky='new', pady=340)

		self.frac_sit_label = tk.Label(master, text="Fraction of Situations")
		self.frac_sit_label.grid(row=0, column=1, sticky='nw', pady=370)

		self.frac_sit_entry = tk.Entry(master, textvariable=self.frac_sit, width=4)
		self.frac_sit_entry.grid(row=0, column=2, sticky='new', pady=370)

		self.frac_tim_label = tk.Label(master, text="Fraction of Time")
		self.frac_tim_label.grid(row=0, column=1, sticky='nw', pady=400)

		self.frac_tim_entry = tk.Entry(master, textvariable=self.frac_tim, width=4)
		self.frac_tim_entry.grid(row=0, column=2, sticky='new', pady=400)

		self.erp_label = tk.Label(master, text="Effective Radiated Power (W)")
		self.erp_label.grid(row=0, column=1, sticky='nw', pady=430)

		self.erp_entry = tk.Entry(master, textvariable=self.erp, width=8)
		self.erp_entry.grid(row=0, column=2, sticky='new', pady=430)
		##

		self.radio_climate_label = tk.Label(master, text="--- Radio Climate Codes ---")
		self.radio_climate_label.grid(row=0, column=3, columnspan=3, sticky='new', pady=260)

		self.climate_one = tk.Radiobutton(master, text="Equatorial", value=1, variable=self.rad_cli)
		self.climate_one.grid(row=0, column=3, columnspan=3, sticky='nw', pady=290)

		self.climate_two = tk.Radiobutton(master, text="Continental Subtropical", value=2, variable=self.rad_cli)
		self.climate_two.grid(row=0, column=3, columnspan=3, sticky='nw', pady=320)

		self.climate_three = tk.Radiobutton(master, text="Maritime Suptropical", value=3, variable=self.rad_cli)
		self.climate_three.grid(row=0, column=3, columnspan=3, sticky='nw', pady=350)

		self.climate_four = tk.Radiobutton(master, text="Desert", value=4, variable=self.rad_cli)
		self.climate_four.grid(row=0, column=3, columnspan=3, sticky='nw', pady=380)

		self.climate_five = tk.Radiobutton(master, text="Continental Temperate", value=5, variable=self.rad_cli)
		self.climate_five.grid(row=0, column=3, columnspan=3, sticky='nw', pady=410)

		self.climate_six = tk.Radiobutton(master, text="Maritime Temperate (land)", value=6, variable=self.rad_cli)
		self.climate_six.grid(row=0, column=3, columnspan=3, sticky='nw', pady=440)

		self.climate_seven = tk.Radiobutton(master, text="Maritime Temperate (sea)", value=7, variable=self.rad_cli)
		self.climate_seven.grid(row=0, column=3, columnspan=3, sticky='nw', pady=470)
		##

		self.ant_orient_label = tk.Label(master, text="--- Antenna Orientation ---")
		self.ant_orient_label.grid(row=0, column=5, columnspan=6, sticky='new', pady=260)

		self.ant_hori = tk.Radiobutton(master, text="Horizontal", value=0, variable=self.ant_orient)
		self.ant_hori.grid(row=0, column=5, columnspan=5, sticky='nw', pady=290)
		self.ant_vert = tk.Radiobutton(master, text="Vertical", value=1, variable=self.ant_orient)
		self.ant_vert.grid(row=0, column=5, columnspan=5, sticky='nw', pady=320)

		self.lrp_button = tk.Button(master, text="Generate LRP File", height=2,
									  command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(),
															   self.frequency.get(), self.rad_cli.get(),
															   self.ant_orient.get(), self.frac_sit.get(),
															   self.frac_tim.get(), self.erp.get()))
		self.lrp_button.grid(row=0, column=1, sticky='new', pady=476)

		self.ecp_button = tk.Button(master, text="Generate ECP File", height=2, command=lambda: writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(),
														self.elevation.get(), self.abc.get(), self.dielec.get(),
														self.earthcond.get(), self.bfield.get(), self.star.get()))
		self.ecp_button.grid(row=0, column=1, sticky='new', pady=538)

		self.notes_input = tk.Text(master, width=42, height=40, font=('Times', 12), fg="#00d1ff", bg="#282d2f", cursor="star", insertbackground="#00d1ff")
		self.notes_input.grid(row=0, column=16, columnspan=8, sticky='n', pady=0)

		self.notes_button = tk.Button(master, text="Export Notes", height=2, command=lambda: write_notes())
		self.notes_button.grid(row=0, column=2, columnspan=2, sticky='new', pady=538)


		self.G = ImageTk.PhotoImage(Image.open("Gclass.png"))
		self.gclass = tk.Label(master, image=self.G)
		self.gclass.grid(row=0, column=0, sticky='nw', pady=610, padx=100)

		self.gclass_opt = tk.Radiobutton(master, value="G Class", text="G Class", variable=self.star)
		self.gclass_opt.grid(row=0, column=0, sticky='nw', pady=600,padx=100)

		self.M = ImageTk.PhotoImage(Image.open("Mclass.png"))
		self.mclass = tk.Label(master, image=self.M)
		self.mclass.grid(row=0, column=0,sticky='nw', pady=610)

		self.mclass_opt = tk.Radiobutton(master, value="M Class", text="M Class", variable=self.star)
		self.mclass_opt.grid(row=0, column=0,sticky='nw', pady=600)

		self.L = ImageTk.PhotoImage(Image.open("Lclass.png"))
		self.lclass = tk.Label(master, image=self.L)
		self.lclass.grid(row=0, column=0, sticky='nw', pady=610, padx=300)

		self.lclass_opt = tk.Radiobutton(master, value="L Class", text="L Class", variable=self.star)
		self.lclass_opt.grid(row=0, column=0, sticky='nw', pady=600, padx=300)

		self.O = ImageTk.PhotoImage(Image.open("Oclass.png"))
		self.oclass = tk.Label(master, image=self.O)
		self.oclass.grid(row=0, column=0, sticky='nw', pady=610, padx=200)

		self.oclass_opt = tk.Radiobutton(master, value="O Class", text="O Class", variable=self.star)
		self.oclass_opt.grid(row=0, column=0, sticky='nw', pady=600, padx=200)

		self.gclass_opt.config(bg=dim, fg="#FAD800", activebackground=dim, highlightthickness=0,
							   activeforeground="#FAD800", selectcolor=dim, font=('Times', 9))
		self.mclass_opt.config(bg=dim, fg="#FF0000", activebackground=dim, highlightthickness=0,
							   activeforeground="#FF0000", selectcolor=dim, font=('Times', 9))
		self.lclass_opt.config(bg=dim, fg="#FFFFFF", activebackground=dim, highlightthickness=0,
							   activeforeground="#FFFFFF", selectcolor=dim, font=('Times', 9))
		self.oclass_opt.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0, activeforeground=dimf,
							   selectcolor=dim, font=('Times', 9))

		menu = tk.Menu(master)
		master.config(menu=menu)

		filemenu = tk.Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)

		importmenu = tk.Menu(filemenu)
		filemenu.add_cascade(label="Import", menu=importmenu)

		importmenu.add_command(label="Import QTH <Alt+q>", command=lambda: readqth())
		importmenu.add_command(label="Import LRP <Alt+l>", command=lambda: readlrp())
		importmenu.add_command(label="Import ECP <Alt+e>", command=lambda: readecp())

		exportmenu = tk.Menu(filemenu)
		filemenu.add_cascade(label="Export", menu=exportmenu)

		exportmenu.add_command(label="Export QTH <Ctrl+q>",
							   command=lambda: writeqth(self.antenna_alt.get()))
		exportmenu.add_command(label="Export LRP <Ctrl+l>",
							   command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(),
														self.frequency.get(), self.rad_cli.get(), self.ant_orient.get(),
														self.frac_sit.get(), self.frac_tim.get(), self.erp.get()))
		exportmenu.add_command(label="Export ECP <Ctrl+e>",
							   command=lambda: writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(),
														self.elevation.get(), self.abc.get(), self.dielec.get(),
														self.earthcond.get(), self.bfield.get(), self.star.get()))

		master.bind("<Alt-q>", event_readqth)
		master.bind("<Alt-l>", event_readlrp)
		master.bind("<Alt-e>", event_readecp)

		master.bind("<Control-q>", event_writeqth)
		master.bind("<Control-l>", event_writelrp)
		master.bind("<Control-e>", event_writeecp)

		master.bind("<F1>>", clearqth)
		master.bind("<F2>", clearlrp)
		master.bind("<F3>", clearecp)

		master.bind("<Return>", event_super_calc)
		master.bind("<Prior>", event_update_plot)

		plotmenu = tk.Menu(menu)
		menu.add_cascade(label="Correlations", menu=plotmenu)

		tempplot = tk.Menu(plotmenu)
		plotmenu.add_cascade(label="Temperature", menu=tempplot)

		tempplot.add_radiobutton(label="Temp. vs. A.B.C.", variable=self.active_plot, value="temp_abc",
								 command=lambda: temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(),
																	 self.humiavg.get(), self.pressavg.get(),
																	 self.name.get(), self.elevation.get()))
		tempplot.add_radiobutton(label="Temp. vs Pressure", variable=self.active_plot, value="temp_pres",
								 command=lambda: temp_press_dependence(self.fig, self.temphigh.get(),
																	   self.templow.get(), self.elevation.get(),
																	   self.name.get()))
		tempplot.add_radiobutton(label="Temp. vs Humidity", variable=self.active_plot, value="temp_humi",
								 command=lambda: temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(),
																	  self.humid_scale.get(), self.name.get(),
																	  self.elevation.get()))
		menu.add_command(label="Update Plot",activeforeground="#80FF75", command=lambda: update_plot(self.active_plot.get()))
		menu.add_command(label="Save Plot",activeforeground="#80FF75", command=lambda: plt.savefig("{}_{}.png".format(self.name.get(),self.active_plot.get())))


		def design(self):
			master.config(background=dim)
			labels = [self.name_label, self.frac_sit_label, self.ant_orient_label,
					  self.erp_label, self.radio_climate_label, self.frac_tim_label,
					  self.frequency_label, self.ground_cond_label, self.dielectric_label,
					  self.abc_label, self.press_avg_label, self.humid_avg_label, self.humid_label,
					  self.elevation_label, self.temp_avg_label, self.temp_low_label,
					  self.temp_high_label, self.long_dms_label, self.ante_alt_label,
					  self.deg_lo, self.min_lo, self.sec_lo, self.deg_la, self.min_la, self.sec_la, self.lat_dms_label,
					  self.bfield_label, self.bfield_rel_label, self.gclass, self.mclass, self.oclass, self.lclass]
			button = [self.lrp_button, self.pan_calc, self.createqth, self.notes_button, self.ecp_button]
			scales = [self.humid_scale]
			menus = [menu, filemenu, plotmenu, tempplot, exportmenu, importmenu]
			entry = [self.erp_entry, self.frac_tim_entry, self.frequency_entry, self.ground_cond_entry,
					 self.dielectric_entry, self.abc_entry, self.press_avg_calc,
					 self.humid_avg_calc, self.elevation_entry, self.temp_avg_entry, self.temp_low_entry,
					 self.temp_high_entry, self.name_entry, self.long_dms_d, self.long_dms_m, self.long_dms_s,
					 self.lat_dms_d, self.lat_dms_m, self.lat_dms_s, self.bfield_entry, self.bfield_rel_entry,
					 self.frac_sit_entry, self.ante_alt_entry]
			radio = [self.ant_hori, self.ant_vert, self.climate_one, self.climate_two, self.climate_three,
					 self.climate_four, self.climate_five, self.climate_six, self.climate_seven]

			fs = 9
			for m in scales:
				m.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0, troughcolor=dimf, font=('Times', fs))
			for n in labels:
				n.config(bg=dim, fg=dimf, activebackground=dim, font=('Times', fs))
			for o in radio:
				o.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0, activeforeground=dimf,
						 selectcolor=dim, font=('Times', fs))
			for p in button:
				p.config(bg=dim, fg=dimf, activebackground=dim, highlightbackground=dimf, activeforeground=dimf, font=('Times', fs))
			for q in menus:
				q.config(bg=dim, fg=dimf, activebackground=dim, activeforeground=dimf, font=('Times', fs))
			for r in entry:
				r.config(font=('Times', fs))
		return design(self)

if __name__ == '__main__':
	root = tk.Tk()
	Radio(root)

	root.title("SPLAT! Configuratin File Generator")
#	root.geometry(str(root_width) + "x" + str(root_height))  #
	root.attributes('-fullscreen', True)

	#	root.maxsize(str(root_width), str(root_height))
	#	root.minsize(str(600), str(root_height))

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

	# icon = ImageTk.PhotoImage(file='icon.png')

	# root.tk.call('wm', 'iconphoto', root._w, icon)
	root.mainloop()
