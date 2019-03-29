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

root_width = 1150
root_height = 720
offset = 0

## Constants
R = 8.3144598 # Ideal Gas Law Constant
c = 2.99e8 # Speed of Light

## Start of Application
class Radio(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.createWidgets(master)

	def createWidgets(self, master):
		self.fig            = plt.figure(figsize=(5, 5))

		self.name           = tk.StringVar(value="Steve")

		self.lat_dms_deg    = tk.DoubleVar(value=31)
		self.lat_dms_min    = tk.DoubleVar(value=12)
		self.lat_dms_sec    = tk.DoubleVar(value=0)

		self.long_dms_deg   = tk.DoubleVar(value=29)
		self.long_dms_min   = tk.DoubleVar(value=55)
		self.long_dms_sec   = tk.DoubleVar(value=0)

		self.antenna_alt    = tk.DoubleVar(value=0.0)

		self.name2          = tk.StringVar(value="Stereo")

		self.lat_dms_deg2   = tk.DoubleVar(value=30)
		self.lat_dms_min2   = tk.DoubleVar(value=2)
		self.lat_dms_sec2   = tk.DoubleVar(value=0)

		self.long_dms_deg2  = tk.DoubleVar(value=31)
		self.long_dms_min2  = tk.DoubleVar(value=14)
		self.long_dms_sec2  = tk.DoubleVar(value=0)

		self.antenna_alt2	= tk.DoubleVar(value=0.0)
		self.dist           = tk.DoubleVar()
		self.mean_rad       = tk.DoubleVar(value=6371)

		self.temphigh       = tk.DoubleVar(value=0.0)
		self.templow        = tk.DoubleVar(value=0.0)
		self.tempavg        = tk.DoubleVar(value=0.0)

		self.pressavg       = tk.DoubleVar(value=0.0)
		self.humiavg        = tk.DoubleVar(value=0.0)

		self.elevation      = tk.DoubleVar(value=0.0)
		self.bfield         = tk.DoubleVar(value=0.0)
		self.bfield_rel     = tk.DoubleVar(value=0.0)

		self.star           = tk.StringVar(value="G")
		self.solarm         = tk.DoubleVar(value=0.0)
		self.solarlum       = tk.DoubleVar(value=0.0)

		self.location       = tk.StringVar(value=self.name.get())

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

		self.grav_acc 		= tk.DoubleVar()
		self.atmo_mole		= tk.DoubleVar()

		canvas = FigureCanvasTkAgg(self.fig, master)
		canvas.get_tk_widget().grid(row=0, column=0, sticky='new')
		master.update_idletasks()
		canvas.draw()

		def writelrp(dielectric, conductivity, bending, frequency, radio_climate, polarization, frac_sit, frac_time,
					 erp):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Irregular Terrain Model Files", "*.lrp")])
			filelrp = open(fname, 'w')
			filelrp.write(str(dielectric).ljust(10)     + "\t; Earth Dielectric Constant (Relative permittivity)" + "\n")
			filelrp.write(str(conductivity).ljust(10)   + "\t; Earth Conductivity (Siemens per meter)" + "\n")
			filelrp.write(str(bending).ljust(10)        + "\t; Atmospheric Bending Constant (N-Units)" + "\n")
			filelrp.write(str(frequency).ljust(10)      + "\t; Frequency in MHz (20 MHz to 20 GHz)" + "\n")
			filelrp.write(str(radio_climate).ljust(10)  + "\t; Radio Climate" + "\n")
			filelrp.write(str(polarization).ljust(10)   + "\t; Polarization (0 = Horizontal, 1 = Vertical)" + "\n")
			filelrp.write(str(frac_sit).ljust(10)       + "\t; Fraction of situations" + "\n")
			filelrp.write(str(frac_time).ljust(10)      + "\t; Fraction of time" + "\n")
			filelrp.write(str(erp).ljust(10)            + "\t; ERP" + "\n")
			filelrp.close()

		def writeecp(rel_humid, temphigh, templow, elevation, bending, dielectric, conduct):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File",
												 filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'w')
			fileecp.write(str(self.star.get())       	+   "\t; Spectral Class of Main Star" + "\n")
			fileecp.write(str(self.bfield.get())   		+   "\t; Magnetic Field (G)" + "\n")
			fileecp.write(str(self.grav_acc.get())		+ 	"\t; Gravitational Acceleration (m/s^2)" + "\n")
			fileecp.write(str(self.mean_rad.get())		+ 	"\t; Mean Radius (km)"+"\n")
			fileecp.write("---\t"*6+"\n")
			fileecp.write(str(rel_humid) 				+   "\t; Relative Humidity" + "\n")
			fileecp.write(str(temphigh) 				+   "\t; High Temperature (C)" + "\n")
			fileecp.write(str(templow) 					+   "\t; Low Temperature (C)" + "\n")
			fileecp.write(str(elevation) 				+   "\t; Elevation (m)" + "\n")
			fileecp.write(str(bending)    				+   "\t; Atmospheric Bending Constant (N-Units)" + "\n")
			fileecp.write(str(dielectric) 				+   "\t; Dielectric Constant" + "\n")
			fileecp.write(str(conduct)  				+   "\t; Ground Conductivity (S/m)" + "\n")
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
			content = [x.strip() for x in content]
			self.star.set(content[0])
			self.bfield.set(content[1])
			self.grav_acc.set(content[2])
			self.mean_rad.set(content[3])
			self.humid_scale.set(content[5])
			self.temphigh.set(content[6])
			self.templow.set(content[7])
			self.elevation.set(content[8])
			self.abc.set(content[9])
			self.dielec.set(content[10])
			self.earthcond.set(content[11])

		def Decimal_Degrees(deg, minu, sec):
			DD = deg + (minu / 60.) + (sec / 3600.)
			return DD

		def humid_calc(T, H):
			e = (H * 6.1121 * exp((17.502 * (T)) / ((T) + (240.97)))) / 100
			return e

		def pressure(altitude, T):
			global R
			g = self.grav_acc.get()
			P = 1013.25 * (1 - ((0.0065 * altitude) / ((T + 273.15) + 0.0065 * altitude))) ** (5.257)
			#P = (exp((altitude * g)/(R*T))) * 1/1013.25
			return P

		def atmo_bend(e, T, P):
			N = 77.6 * (P / (T + 273.15)) + 3.73e5 * (e / (T + 273.15) ** 2)
			return N

		def bfield(B):
			B_rel = B / (7.981e10)
			return B_rel

		def altitude(T):
			z = absolute(((T-273.15) - 15.04)/(-0.00649))
			return z

		def distance(self):
			h 		= self.antenna_alt.get()
			phi1    = deg2rad(float(self.lat_dms_deg.get()      + self.lat_dms_min.get()/60.      + self.lat_dms_sec.get()/3600.))
			phi2    = deg2rad(float(self.lat_dms_deg2.get()     + self.lat_dms_min2.get()/60.     + self.lat_dms_sec2.get()/3600.))
			long1   = deg2rad(float(self.long_dms_deg.get()     + self.long_dms_min.get()/60.     + self.long_dms_sec.get()/3600.))
			long2   = deg2rad(float(self.long_dms_deg2.get()    + self.long_dms_min2.get()/60.    + self.long_dms_sec2.get()/3600.))
			r = self.mean_rad.get()
			#D = sqrt(2*r * h + h**2)
			D = r*absolute(arctan((sqrt((cos(phi2) * sin(long2-long1))**2 + (cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(long2-long1))**2)/(sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(long2-long1)))))
			return D

		def fresnel_zone(d):
			w 	= (3e8)/self.frequency.get()
		#	d 	= self.dist.get()/2
			F_n = sqrt((w*d*d)/(d+d))
			return F_n

		def fresnel_dependence(fig, name):
			plt.clf()
			fres = plt.scatter(linspace(0, self.dist.get()), fresnel_zone(linspace(0.1, self.dist.get()/2)))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0, 0))
			plt.title("Location: {}\nFresnel Zone Clearance".format(name),pad=20,
					  fontsize='medium')
			plt.xlabel("Distance")
			plt.ylabel("Fresnel Zone Radius")
			canvas.draw_idle()
			canvas.draw()

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

		def path_loss_dependence(fig, D, F, namet,namer, altitude):
			plt.clf()
			d = arange(0.1, self.dist.get(), 0.001)
			h = self.antenna_alt.get()
			loss = 32.45 + 20 * log10(F) + 20*log10(d*h)
			path_loss = plt.scatter(d,loss, marker="_")
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', useMathText=True)
			plt.title("Path loss profile between {} and {} at {} m".format(namet, namer, altitude), pad=20,
					  fontsize='medium')
			plt.xlim(0)
			plt.xlabel("Distance (km)")
			plt.ylabel("Path Loss (dB)")
			plt.grid(color='k', linestyle='--', linewidth=0.5)
			canvas.draw_idle()
			canvas.draw()


		def soundings(self):
			plt.clf()
			fname = filedialog.askopenfilename(title="Get yo file",
											   filetypes=[("Sounding Data Files", "*.txt")])
			data = open(fname, 'r')
			Z = loadtxt(fname, skiprows=1, unpack=True)[0]
			T = loadtxt(fname, skiprows=1, unpack=True)[1]
			P = loadtxt(fname, skiprows=1, unpack=True)[2]
			temp_alt = plt.scatter(T, Z)
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True)
			plt.title("Location: {}\nTemperature Dependence on Altitude to {} m".format("Fix", max(Z)), pad=20,
					  fontsize='medium')
			plt.axvline(273.15)
			plt.axhline(10)
			plt.xlabel("Temperature (K)")
			plt.ylabel("Altitude (km)")
			canvas.draw_idle()
			canvas.draw()

		def super_calc():
			self.tempavg.set(float(self.temphigh.get()) / 2. + float(self.templow.get()) / 2.)
			self.humiavg.set(round(humid_calc(self.tempavg.get(), self.humid_scale.get()), 3))
			self.pressavg.set(round(pressure(self.elevation.get(), self.tempavg.get()), 3))
			self.abc.set(str(round(atmo_bend(self.humiavg.get(), self.tempavg.get() + 273.15, self.pressavg.get()), 3)))
			self.bfield_rel.set("{:0.2E}".format(bfield(self.bfield.get())))
			self.dist.set(round(distance(self),4))

		def event_super_calc(event):
			super_calc()

		def update_plot(plot):
			if plot == "temp_abc":
				temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humiavg.get(),
									self.pressavg.get(), self.name.get(), self.elevation.get())
			elif plot == "temp_pres":
				temp_press_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.elevation.get(),
									  self.name.get())
			elif plot == "temp_humi":
				temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humid_scale.get(),
									 self.name.get(), self.elevation.get())
			elif plot == "path_loss":
				path_loss_dependence(self.fig, self.dist.get(), self.frequency.get(),
									 self.name.get(),self.name2.get(), self.elevation.get())
			elif plot == "sound":
				soundings(self)
			elif plot == "fresnel":
				fresnel_dependence(self.fig)
			else:
				def plot_error():
					top = tk.Toplevel()
					top.title = "Error"
					top.geometry("200x100")

					msg = tk.Message(top, text="Not a Valid Plotting Option")
					msg.grid(row=0, column=1,columnspan=2, sticky='nsew')

					def quit():
						top.quit()
						top.destroy()

					end = tk.Button(top, text="Dismiss", command=quit)
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
		self.name_one = tk.Radiobutton(master, value=self.name.get(), text="Location Name:", variable=self.location)
		self.name_one.grid(row=0, column=1, sticky='nw')

		self.name_entry = tk.Entry(master, width=10, textvariable=self.name)
		self.name_entry.grid(row=0, column=2, sticky='new')

		##
		self.lat_dms_label = tk.Label(master, text="Latitude:")
		self.lat_dms_label.grid(row=0, column=3, sticky='nw')

		self.lat_dms_d = tk.Entry(master, width=4, textvariable=self.lat_dms_deg)
		self.lat_dms_d.grid(row=0, column=3, sticky='new', padx=(50,0))

		self.deg_la = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_la.grid(row=0, column=4, sticky='nw', padx=(0,120))

		self.lat_dms_m = tk.Entry(master, width=4, textvariable=self.lat_dms_min)
		self.lat_dms_m.grid(row=0, column=4, columnspan=1,sticky='nw', padx=(10,0))

		self.min_la = tk.Label(master, text="'", font=('Times', 13))
		self.min_la.grid(row=0, column=4, sticky='nw', padx=(40,0))

		self.lat_dms_s = tk.Entry(master, width=5, textvariable=self.lat_dms_sec)
		self.lat_dms_s.grid(row=0, column=4, sticky='nw', padx=(50,0))

		self.sec_la = tk.Label(master, text="''", font=('Times', 13))
		self.sec_la.grid(row=0, column=4, sticky='nw', padx=(90,0))

		self.long_dms_label = tk.Label(master, text="Longitude:")
		self.long_dms_label.grid(row=0, column=4, sticky='nw', padx=(100,0))

		self.long_dms_d = tk.Entry(master, width=4, textvariable=self.long_dms_deg)
		self.long_dms_d.grid(row=0, column=4, sticky='nw', padx=(160, 0))

		self.deg_lo = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_lo.grid(row=0, column=4, sticky='nw', padx=(190,0))

		self.long_dms_m = tk.Entry(master, width=4, textvariable=self.long_dms_min)
		self.long_dms_m.grid(row=0, column=4, sticky='nw', padx=(200,0))

		self.min_lo = tk.Label(master, text="'", font=('Times', 13))
		self.min_lo.grid(row=0, column=4, sticky='nw', padx=(230,0))

		self.long_dms_s = tk.Entry(master, width=5, textvariable=self.long_dms_sec)
		self.long_dms_s.grid(row=0, column=4, sticky='nw', padx=(240.0))

		self.sec_lo = tk.Label(master, text="''", font=('Times', 13))
		self.sec_lo.grid(row=0, column=4, sticky='nw', padx=(280,0))

## Location 2


		self.name_two = tk.Radiobutton(master, value=self.name2.get(), variable=self.location, text="Location Name:")
		self.name_two.grid(row=0, column=1, sticky='nw', pady=30)

		self.name_entry2 = tk.Entry(master, width=10, textvariable=self.name2)
		self.name_entry2.grid(row=0, column=2, sticky='new', pady=30)

		##
		self.lat_dms_label2 = tk.Label(master, text="Latitude:")
		self.lat_dms_label2.grid(row=0, column=3, sticky='nw', pady=30)

		self.lat_dms_d2 = tk.Entry(master, width=4, textvariable=self.lat_dms_deg2)
		self.lat_dms_d2.grid(row=0, column=3, sticky='new', pady=30, padx=(50,0))

		self.deg_la2 = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_la2.grid(row=0, column=4, sticky='nw', pady=30, padx=(0,120))

		self.lat_dms_m2 = tk.Entry(master, width=4, textvariable=self.lat_dms_min2)
		self.lat_dms_m2.grid(row=0, column=4,columnspan=1, sticky='nw', pady=30, padx=(10,0))

		self.min_la2 = tk.Label(master, text="'", font=('Times', 13))
		self.min_la2.grid(row=0, column=4, sticky='nw', pady=30, padx=(40,0))

		self.lat_dms_s2 = tk.Entry(master, width=5, textvariable=self.lat_dms_sec2)
		self.lat_dms_s2.grid(row=0, column=4, sticky='nw', pady=30, padx=(50,0))

		self.sec_la2 = tk.Label(master, text="''", font=('Times', 13))
		self.sec_la2.grid(row=0, column=4, sticky='nw', pady=30, padx=(90,0))

		self.long_dms_label2 = tk.Label(master, text="Longitude:")
		self.long_dms_label2.grid(row=0, column=4, sticky='nw', pady=30, padx=(100,0))

		self.long_dms_d2 = tk.Entry(master, width=4, textvariable=self.long_dms_deg2)
		self.long_dms_d2.grid(row=0, column=4, sticky='nw', pady=30, padx=(160,0))

		self.deg_lo2 = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_lo2.grid(row=0, column=4, sticky='nw', pady=30, padx=(190,0))

		self.long_dms_m2 = tk.Entry(master, width=4, textvariable=self.long_dms_min2)
		self.long_dms_m2.grid(row=0, column=4, sticky='nw', pady=30, padx=(200,0))

		self.min_lo2 = tk.Label(master, text="'", font=('Times', 13))
		self.min_lo2.grid(row=0, column=4, sticky='nw', pady=30, padx=(230,0))

		self.long_dms_s2 = tk.Entry(master, width=5, textvariable=self.long_dms_sec2)
		self.long_dms_s2.grid(row=0, column=4, pady=30, sticky='nw', padx=(240,0))

		self.sec_lo2 = tk.Label(master, text="''", font=('Times', 13))
		self.sec_lo2.grid(row=0, column=4, sticky='nw', pady=30, padx=(280,0))

		##


		self.createqth = tk.Button(master, command=lambda: writeqth(self.antenna_alt.get()),
								   text="Generate QTH")
		self.createqth.grid(row=0, column=1, sticky='new', columnspan=1, pady=65)


		##
		self.temp_high_label = tk.Label(master, text="High Temperature" + "\t" + "(" + u"\u00B0" + "C)")
		self.temp_high_label.grid(row=0, column=1, sticky='nw', pady=110)

		self.temp_high_entry = tk.Entry(master, width=7, textvariable=self.temphigh)
		self.temp_high_entry.grid(row=0, column=2, sticky='new', pady=110)

		self.temp_low_label = tk.Label(master, text="Low Temperature" +"\t" + "(" + u"\u00B0" + "C)")
		self.temp_low_label.grid(row=0, column=1, sticky='nw', pady=140)

		self.temp_low_entry = tk.Entry(master, width=7, textvariable=self.templow)
		self.temp_low_entry.grid(row=0, column=2, sticky='new', pady=140)

		self.temp_avg_label = tk.Label(master, text="Avg. Temperature" + "\t" + "(" + u"\u00B0" + "C)")
		self.temp_avg_label.grid(row=0, column=1, sticky='nw', pady=170)

		self.temp_avg_entry = tk.Entry(master, width=7, textvariable=self.tempavg)
		self.temp_avg_entry.grid(row=0, column=2, sticky='new', pady=170)

		self.elevation_label = tk.Label(master, text="Elevation" + "\t\t" + "(m)")
		self.elevation_label.grid(row=0, column=1, sticky='nw', pady=200)

		self.elevation_entry = tk.Entry(master, textvariable=self.elevation, width=10)
		self.elevation_entry.grid(row=0, column=2, sticky='nw', pady=200)

		self.humid_label = tk.Label(master, text="Rel. Humidity" + " " * 2 + "(%)")
		self.humid_label.grid(row=0, column=3, sticky='nw', pady=110)

		self.humid_scale = tk.Scale(master, from_=0, to=100, resolution=10, orient=tk.HORIZONTAL, width=15, length=255)
		self.humid_scale.grid(row=0, column=4,columnspan=2, sticky='nw', pady=93)
		self.humid_scale.set(50)

		self.humid_avg_label = tk.Label(master, text="Avg. Humidity" + " " * 1 + "(mbar)")
		self.humid_avg_label.grid(row=0, column=3, sticky='nw', pady=140)

		self.humid_avg_calc = tk.Entry(master, textvariable=self.humiavg, width=8)
		self.humid_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=1, pady=140)

		self.press_avg_label = tk.Label(master, text="Avg. Pressure" + " " * 2 + "(mbar)")
		self.press_avg_label.grid(row=0, column=3, sticky='nw', pady=170)

		self.press_avg_calc = tk.Entry(master, textvariable=self.pressavg, width=8)
		self.press_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=1, pady=170)

		self.antenna_alt_label = tk.Label(master, text="Antenna Height")
		self.antenna_alt_label.grid(row=0, column=4, sticky='nw', pady=140, padx=(100,0))

		self.antenna_alt_entry = tk.Entry(master, textvariable=self.antenna_alt, width=8)
		self.antenna_alt_entry.grid(row=0, column=4, sticky='nw', pady=140, padx=(200,0))
# LRP File Contents
##
		self.lrp_value_label = tk.Label(master, text="--- LRP Quantities ---")
		self.lrp_value_label.grid(row=0, column=1, columnspan=2, sticky='new', pady=255)
		self.lrp_value_label.config(bg=dim, fg="#FFF300", activebackground=dim, font=('Times', 9))

		self.dielectric_label = tk.Label(master, text="Dielectric Constant")
		self.dielectric_label.grid(row=0, column=1, sticky='nw', pady=280)

		self.dielectric_entry = tk.Entry(master, textvariable=self.dielec, width=8)
		self.dielectric_entry.grid(row=0, column=2, sticky='new', pady=280)

		self.ground_cond_label = tk.Label(master, text="Earth Conductivity" + "\t" + "(S/m)")
		self.ground_cond_label.grid(row=0, column=1, sticky='nw', pady=310)

		self.ground_cond_entry = tk.Entry(master, textvariable=self.earthcond, width=8)
		self.ground_cond_entry.grid(row=0, column=2, sticky='new', pady=310)

		self.abc_label = tk.Label(master, text="Bending Const." + "(N-Units)")
		self.abc_label.grid(row=0, column=1, sticky='nw', pady=340)

		self.abc_entry = tk.Entry(master, textvariable=self.abc, width=8)
		self.abc_entry.grid(row=0, column=2,sticky='new', pady=340)

		self.frequency_label = tk.Label(master, text="Frequency" + "\t" + "(MHz)")
		self.frequency_label.grid(row=0, column=1, sticky='nw', pady=370)

		self.frequency_entry = tk.Entry(master, textvariable=self.frequency, width=8)
		self.frequency_entry.grid(row=0, column=2, sticky='new', pady=370)

		self.frac_sit_label = tk.Label(master, text="Fraction of Situations")
		self.frac_sit_label.grid(row=0, column=1, sticky='nw', pady=400)

		self.frac_sit_entry = tk.Entry(master, textvariable=self.frac_sit, width=4)
		self.frac_sit_entry.grid(row=0, column=2, sticky='new', pady=400)

		self.frac_tim_label = tk.Label(master, text="Fraction of Time")
		self.frac_tim_label.grid(row=0, column=1, sticky='nw', pady=430)

		self.frac_tim_entry = tk.Entry(master, textvariable=self.frac_tim, width=4)
		self.frac_tim_entry.grid(row=0, column=2, sticky='new', pady=430)

		self.erp_label = tk.Label(master, text="Eff. Radiated Power (W)")
		self.erp_label.grid(row=0, column=1, sticky='nw', pady=460)

		self.erp_entry = tk.Entry(master, textvariable=self.erp, width=8)
		self.erp_entry.grid(row=0, column=2, sticky='new', pady=460)
##
		self.radio_climate_label = tk.Label(master, text="--- Radio Climate Codes ---")
		self.radio_climate_label.grid(row=0, column=3,columnspan=4, sticky='nw', pady=255)
		self.radio_climate_label.config(bg=dim, fg="#FFF300", activebackground=dim, font=('Times', 9))

		self.climate_one = tk.Radiobutton(master, text="Equatorial", value=1, variable=self.rad_cli)
		self.climate_one.grid(row=0, column=3, columnspan=4, sticky='nw', pady=280)

		self.climate_two = tk.Radiobutton(master, text="Continental Subtropical", value=2, variable=self.rad_cli)
		self.climate_two.grid(row=0, column=3, columnspan=4, sticky='nw', pady=300)

		self.climate_three = tk.Radiobutton(master, text="Maritime Suptropical", value=3, variable=self.rad_cli)
		self.climate_three.grid(row=0, column=3, columnspan=4, sticky='nw', pady=320)

		self.climate_four = tk.Radiobutton(master, text="Desert", value=4, variable=self.rad_cli)
		self.climate_four.grid(row=0, column=3, columnspan=4, sticky='nw', pady=340)

		self.climate_five = tk.Radiobutton(master, text="Continental Temperate", value=5, variable=self.rad_cli)
		self.climate_five.grid(row=0, column=3, columnspan=4, sticky='nw', pady=360)

		self.climate_six = tk.Radiobutton(master, text="Maritime Temperate (land)", value=6, variable=self.rad_cli)
		self.climate_six.grid(row=0, column=3, columnspan=4, sticky='nw', pady=380)

		self.climate_seven = tk.Radiobutton(master, text="Maritime Temperate (sea)", value=7, variable=self.rad_cli)
		self.climate_seven.grid(row=0, column=3, columnspan=4, sticky='nw', pady=400)
##
		self.ant_orient_label = tk.Label(master, text="--- Antenna Orientation ---")
		self.ant_orient_label.grid(row=0, column=3, columnspan=4, sticky='nw', pady=420, padx=(0,0))
		self.ant_orient_label.config(bg=dim, fg="#FFF300", activebackground=dim, font=('Times', 9))

		self.ant_hori = tk.Radiobutton(master, text="Horizontal", value=0, variable=self.ant_orient)
		self.ant_hori.grid(row=0, column=3, columnspan=4, sticky='nw', pady=440, padx=(0,0))
		self.ant_vert = tk.Radiobutton(master, text="Vertical", value=1, variable=self.ant_orient)
		self.ant_vert.grid(row=0, column=3, columnspan=4, sticky='nw', pady=460, padx=(0,0))


		self.grav_acc_label = tk.Label(master, text="Grav. Acc. (m/s^2)")
		self.grav_acc_label.grid(row=0, column=4, sticky='nw', pady=280, padx=(100,0))

		self.grav_acc_entry = tk.Entry(master, textvariable=self.grav_acc, width=8)
		self.grav_acc_entry.grid(row=0, column=4, sticky='nw', pady=280, padx=(200,0))

		self.atmo_mole_label = tk.Label(master, text="Atmos. Molar Mass")
		self.atmo_mole_label.grid(row=0, column=4,sticky='nw', pady=310, padx=(100,0))

		self.atmo_mole_entry = tk.Entry(master, textvariable=self.atmo_mole, width=8)
		self.atmo_mole_entry.grid(row=0, column=4, sticky='nw', pady=310, padx=(200,0))

		self.bfield_label = tk.Label(master, text="B-Field (G)")
		self.bfield_label.grid(row=0, column=4,sticky='nw', pady=340, padx=(100,0))

		self.bfield_entry = tk.Entry(master, textvariable=self.bfield, width=8)
		self.bfield_entry.grid(row=0, column=4,sticky='nw', pady=340, padx=(200,0))

		self.bfield_rel_label = tk.Label(master, text="Rel. B-Field (G)")
		self.bfield_rel_label.grid(row=0, column=4, sticky='nw', pady=370, padx=(100,0))

		self.bfield_rel_entry = tk.Entry(master, textvariable=self.bfield_rel, width=8)
		self.bfield_rel_entry.grid(row=0, column=4, sticky='nw', pady=370, padx=(200,0))

		self.mean_rad_label = tk.Label(master, text="Mean Radius (km)")
		self.mean_rad_label.grid(row=0, column=4, sticky='nw', pady=400, padx=(100,0))

		self.mean_rad_entry = tk.Entry(master, textvariable=self.mean_rad, width=8)
		self.mean_rad_entry.grid(row=0, column=4, sticky='nw', pady=400, padx=(200,0))

		self.dist_label = tk.Label(master, text="Distance (km)")
		self.dist_label.grid(row=0, column=4,sticky='nw', pady=430, padx=(100,0))

		self.dist_entry = tk.Entry(master, textvariable=self.dist, width=8)
		self.dist_entry.grid(row=0, column=4, sticky='nw', pady=430, padx=(200,0))

		self.pan_calc = tk.Button(master, text="Calculate", height=2,
								  command=lambda: super_calc())
		self.pan_calc.grid(row=0, column=4,sticky='nw', pady=502, padx=(200,0))

##
# Create LRP File
##

		self.lrp_button = tk.Button(master, text="Generate LRP File", height=2,
									command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(),
															 self.frequency.get(), self.rad_cli.get(),
															 self.ant_orient.get(), self.frac_sit.get(),
															 self.frac_tim.get(), self.erp.get()))
		self.lrp_button.grid(row=0, column=1, sticky='new', pady=502)

		# Create ECP File
		##
		self.ecp_button = tk.Button(master, text="Generate ECP File", height=2,
									command=lambda: writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(),
															 self.elevation.get(), self.abc.get(), self.dielec.get(),
															 self.earthcond.get()))
		self.ecp_button.grid(row=0, column=1, sticky='new', pady=550)
##
# Notes
##
		self.notes_input = tk.Text(master, width=50, height=11, font=('Times', 10), fg="#00d1ff", bg="#282d2f",
								   cursor="star", insertbackground="#00d1ff")
		self.notes_input.grid(row=0, column=2, columnspan=3,sticky='nw', pady=502)

		self.notes_button = tk.Button(master, text="Export Notes", height=2, command=lambda: write_notes())
		self.notes_button.grid(row=0, column=1, sticky='new', pady=598)

		self.note_insert = tk.Button(master, text="Import Notes", height=2, command=lambda: read_notes())
		self.note_insert.grid(row=0, column=1, sticky='new', pady=646)

##
		self.M = ImageTk.PhotoImage(Image.open("images/Mclass.png"))
		self.mclass = tk.Button(master, image=self.M, command=lambda:self.star.set("M"), highlightcolor="#FF0000", highlightbackground="#FF0000")
		self.mclass.grid(row=0, column=0,sticky='nw', pady=502)

		self.mclass_opt = tk.Checkbutton(master, onvalue="M", text="M Class", variable=self.star)
		self.mclass_opt.grid(row=0, column=0,sticky='nw', pady=502, padx=20)

		self.K = ImageTk.PhotoImage(Image.open("images/Kclass.png"))
		self.kclass = tk.Button(master, image=self.K, command=lambda:self.star.set("K"),
								highlightcolor="#FFA200", highlightbackground="#FFA200")
		self.kclass.grid(row=0, column=0, sticky='nw', pady=502, padx=(110,0))

		self.kclass_opt = tk.Checkbutton(master, onvalue="K", text="K Class", variable=self.star)
		self.kclass_opt.grid(row=0, column=0, sticky='nw', pady=502, padx=(130,0))

		self.G = ImageTk.PhotoImage(Image.open("images/Gclass.png"))
		self.gclass = tk.Button(master, image=self.G, command=lambda:self.star.set("G"),highlightcolor="#FAD800", highlightbackground="#FAD800")
		self.gclass.grid(row=0, column=0, sticky='nw', pady=502, padx=220)

		self.gclass_opt = tk.Checkbutton(master, onvalue="G", text="G Class", variable=self.star)
		self.gclass_opt.grid(row=0, column=0, sticky='nw', pady=502, padx=240)

		self.F = ImageTk.PhotoImage(Image.open("images/Fclass.png"))
		self.fclass = tk.Button(master, image=self.F, command=lambda:self.star.set("F"),
								highlightcolor="#FFF48B", highlightbackground="#FFF48B")
		self.fclass.grid(row=0, column=0, sticky='nw', pady=502, padx=(330,0))

		self.fclass_opt = tk.Checkbutton(master, onvalue="F", text="F Class", variable=self.star)
		self.fclass_opt.grid(row=0, column=0, sticky='nw', pady=502, padx=(350,0))

		self.A = ImageTk.PhotoImage(Image.open("images/Aclass.png"))
		self.aclass = tk.Button(master, image=self.A, command=lambda:self.star.set("A"),
								highlightcolor="#8BF4FF", highlightbackground="#8BF4FF")
		self.aclass.grid(row=0, column=0, sticky='nw', pady=502, padx=(440, 0))

		self.aclass_opt = tk.Checkbutton(master, onvalue="A", text="A Class", variable=self.star)
		self.aclass_opt.grid(row=0, column=0, sticky='nw', pady=502, padx=(460,0))

		self.O = ImageTk.PhotoImage(Image.open("images/Oclass.png"))
		self.oclass = tk.Button(master, image=self.O, command=lambda: self.star.set("O"), highlightcolor=dimf, highlightbackground=dimf)
		self.oclass.grid(row=0, column=0, sticky='nw', pady=612, padx=(0,0))

		self.oclass_opt = tk.Checkbutton(master, onvalue="O", text="O Class", variable=self.star)
		self.oclass_opt.grid(row=0, column=0, sticky='nw', pady=612, padx=(20, 0))

		self.D = ImageTk.PhotoImage(Image.open("images/Dclass.png"))
		self.dclass = tk.Button(master, image=self.D, command=lambda:self.star.set("D"))
		self.dclass.grid(row=0, column=0, sticky='nw', pady=612, padx=(110,0))

		self.dclass_opt = tk.Checkbutton(master, onvalue="D", text="D Class", variable=self.star)
		self.dclass_opt.grid(row=0, column=0, sticky='nw', pady=612, padx=(130, 0))


		self.gclass_opt.config(bg=dim, fg="#FAD800", activebackground=dim, highlightthickness=1,
							   activeforeground="#FAD800", selectcolor=dim, font=('Times', 9),
							   highlightcolor="#FAD800", highlightbackground="#FAD800")

		self.mclass_opt.config(bg=dim, fg="#FF0000", activebackground=dim, highlightthickness=1,
							   activeforeground="#FF0000", selectcolor=dim, font=('Times', 9),
							   highlightcolor="#FF0000", highlightbackground="#FF0000")

		self.kclass_opt.config(bg=dim, fg="#FFA200", activebackground=dim, highlightthickness=1,
							   activeforeground="#FFA200", selectcolor=dim, font=('Times', 9),
							   highlightcolor="#FFA200", highlightbackground="#FFA200")

		self.dclass_opt.config(bg=dim, fg="#FFFFFF", activebackground=dim, highlightthickness=1,
							   activeforeground="#FFFFFF", selectcolor=dim, font=('Times', 9))

		self.fclass_opt.config(bg=dim, fg="#FFF48B", activebackground=dim, highlightthickness=1,
							   activeforeground="#FFF48B", selectcolor=dim, font=('Times', 9),
							   highlightcolor="#FFF48B", highlightbackground="#FFF48B")

		self.aclass_opt.config(bg=dim, fg="#8BF4FF", activebackground=dim, highlightthickness=1,
						   activeforeground="#8BF4FF", selectcolor=dim, font=('Times', 9),
							   highlightcolor="#8BF4FF", highlightbackground="#8BF4FF")

		self.oclass_opt.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=1, activeforeground=dimf,
							   selectcolor=dim, font=('Times', 9), highlightcolor=dimf, highlightbackground=dimf)

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

		master.bind("<Return>", event_super_calc)
		master.bind("<Prior>", event_update_plot)

		plotmenu = tk.Menu(menu)
		menu.add_cascade(label="Correlations", menu=plotmenu)

		plotmenu.add_radiobutton(label="Path Loss", variable=self.active_plot, value="path_loss",selectcolor=dimf,
								 command=lambda: path_loss_dependence(self.fig, self.dist.get(), self.frequency.get(),
																	  self.name.get(),self.name2.get(), self.elevation.get()))
		plotmenu.add_radiobutton(label="Sounding", variable=self.active_plot, value="sound",selectcolor=dimf,
								 command=lambda: soundings(self))
		plotmenu.add_radiobutton(label="Fresnel Zone", variable=self.active_plot, value="fresnel",selectcolor=dimf,
								 command=lambda: fresnel_dependence(self.fig))
		tempplot = tk.Menu(plotmenu)
		plotmenu.add_cascade(label="Temperature", menu=tempplot)

		tempplot.add_radiobutton(label="Temp. vs. A.B.C.", variable=self.active_plot, value="temp_abc",selectcolor=dimf,
								 command=lambda: temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(),
																	 self.humiavg.get(), self.pressavg.get(),
																	 self.name.get(), self.elevation.get()))
		tempplot.add_radiobutton(label="Temp. vs Pressure", variable=self.active_plot, value="temp_pres",selectcolor=dimf,
								 command=lambda: temp_press_dependence(self.fig, self.temphigh.get(),
																	   self.templow.get(), self.elevation.get(),
																	   self.name.get()))
		tempplot.add_radiobutton(label="Temp. vs Humidity", variable=self.active_plot, value="temp_humi",selectcolor=dimf,
								 command=lambda: temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(),
																	  self.humid_scale.get(), self.name.get(),
																	  self.elevation.get()))
		menu.add_command(label="Update Plot",activeforeground="#80FF75", command=lambda: update_plot(self.active_plot.get()))
		menu.add_command(label="Save Plot",activeforeground="#80FF75", command=lambda: plt.savefig("{}_{}.png".format(self.name.get(),self.active_plot.get())))

		def design(self):
			master.config(background=dim)
			labels = [self.frac_sit_label,
					  self.erp_label, self.frac_tim_label,
					  self.frequency_label, self.ground_cond_label, self.dielectric_label,
					  self.abc_label, self.press_avg_label, self.humid_avg_label, self.humid_label,
					  self.elevation_label, self.temp_avg_label, self.temp_low_label,
					  self.temp_high_label, self.long_dms_label,self.lat_dms_label,self.lat_dms_label2,
					  self.deg_lo, self.min_lo, self.sec_lo, self.deg_la, self.min_la, self.sec_la,
					  self.bfield_label, self.bfield_rel_label, self.gclass, self.mclass, self.oclass, self.dclass, self.kclass,
					  self.fclass, self.aclass, self.long_dms_label2, self.deg_lo2, self.min_lo2, self.sec_lo2,
					  self.deg_la2, self.min_la2, self.sec_la2, self.mean_rad_label, self.dist_label, self.atmo_mole_label,
					  self.grav_acc_label, self.antenna_alt_label]
			button = [self.lrp_button, self.pan_calc, self.createqth, self.notes_button, self.ecp_button, self.note_insert]
			scales = [self.humid_scale]
			menus = [menu, filemenu, plotmenu, tempplot, exportmenu, importmenu]
			entry = [self.erp_entry, self.frac_tim_entry, self.frequency_entry, self.ground_cond_entry,
					 self.dielectric_entry, self.abc_entry, self.press_avg_calc,
					 self.humid_avg_calc, self.elevation_entry, self.temp_avg_entry, self.temp_low_entry,
					 self.temp_high_entry, self.name_entry, self.long_dms_d, self.long_dms_m, self.long_dms_s,
					 self.lat_dms_d, self.lat_dms_m, self.lat_dms_s, self.bfield_entry, self.bfield_rel_entry,
					 self.frac_sit_entry,self.name_entry2, self.long_dms_d2, self.long_dms_m2, self.long_dms_s2,
					 self.lat_dms_d2, self.lat_dms_m2, self.lat_dms_s2,self.mean_rad_entry, self.dist_entry,
					 self.atmo_mole_entry, self.grav_acc_entry, self.antenna_alt_entry]
			radio = [self.ant_hori, self.ant_vert, self.climate_one, self.climate_two, self.climate_three,
					 self.climate_four, self.climate_five, self.climate_six, self.climate_seven, self.name_one,self.name_two]

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
	icon = ImageTk.PhotoImage(file='images/icon.png')
	root.tk.call('wm', 'iconphoto', root._w, icon)
	Radio(root)

	root.title("SPLAT! Configuration File Generator")
	root.geometry(str(root_width) + "x" + str(root_height))  #
   # root.attributes('-fullscreen', True)

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
	root.mainloop()
