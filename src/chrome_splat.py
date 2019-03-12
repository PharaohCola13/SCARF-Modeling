import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import *
from numpy import *
from PIL import Image
import sys
from time import sleep

try:
	import tkinter as tk
	from tkinter.colorchooser import askcolor
	
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


root_width = 1350
root_height = 601
offset 		= 0
## Start of Application
class Radio(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self ,master)
		self.createWidgets(master)

	def createWidgets(self, master):
		self.fig = plt.figure(figsize=(6, 6))
		
		self.name = tk.StringVar(value="RAVIOLI")

		self.long_dms_deg = tk.DoubleVar(value=-160)
		self.long_dms_min = tk.DoubleVar(value=0.0)
		self.long_dms_sec = tk.DoubleVar(value=0.0)

		self.long_dd = tk.DoubleVar(value=0.0)

		self.lat_dms_deg = tk.DoubleVar(value=0.0)
		self.lat_dms_min = tk.DoubleVar(value=0.0)
		self.lat_dms_sec = tk.DoubleVar(value=0.0)

		self.lat_dd = tk.DoubleVar(value=0.0)

		self.map_ew = tk.StringVar()
		self.map_ns = tk.StringVar()

		self.antenna_alt = tk.DoubleVar(value=0.0)

		self.temphigh = tk.DoubleVar(value=0.0)
		self.templow  = tk.DoubleVar(value=0.0)
		self.tempavg  = tk.DoubleVar(value=0.0)

		self.pressavg = tk.DoubleVar(value=0.0)
		self.humiavg  = tk.DoubleVar(value=0.0)

		self.elevation = tk.DoubleVar(value=0.0)
		
		self.abc = tk.StringVar(value=0.0)

		self.dielec = tk.DoubleVar(value=0.0)
		self.earthcond = tk.DoubleVar(value=0.0)
		self.frequency = tk.DoubleVar(value=0.0)
		self.rad_cli = tk.IntVar(value=5)
		self.ant_orient = tk.IntVar(value=1)

		self.frac_sit = tk.DoubleVar()
		self.frac_tim = tk.DoubleVar()

		self.active_plot = tk.StringVar()

		self.erp = tk.DoubleVar()

		canvas = FigureCanvasTkAgg(self.fig, master)
		canvas.get_tk_widget().grid(row=0, column=0, sticky='new')
		master.update_idletasks()
		canvas.draw()

		def writeqth(name, longitude, latitude, antenna):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File", filetypes=[("Location Files", "*.qth")])
			fileqth = open(fname, 'w')
			fileqth.write(str(name) + "\n")
			fileqth.write(str(latitude) + "\n")
			fileqth.write(str(longitude) + "\n")
			fileqth.write(str(antenna) + "\n")
			fileqth.close()

		def writelrp(dielectric, conductivity, bending, frequency, radio_climate, polarization, frac_sit, frac_time, erp):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File", filetypes=[("Irregular Terrian Model Files", "*.lrp")])
			filelrp = open(fname, 'w')
			filelrp.write(str(dielectric).ljust(10) + "; Earth Dielectric Constant (Relative permittivity)" + "\n")
			filelrp.write(str(conductivity).ljust(10) + "; Earth Conductivity (Siemens per meter)" + "\n")
			filelrp.write(str(bending).ljust(10) + "; Atmospheric Bending Constant (N-Units)" + "\n")
			filelrp.write(str(frequency).ljust(10) + "; Frequency in MHz (20 MHz to 20 GHz)" + "\n")
			filelrp.write(str(radio_climate).ljust(10) + "; Radio Climate" + "\n")
			filelrp.write(str(polarization).ljust(10) + "; Polarization (0 = Horizontal, 1 = Vertical)" + "\n")
			filelrp.write(str(frac_sit).ljust(10) + "; Fraction of situations" + "\n")
			filelrp.write(str(frac_time).ljust(10) + "; Fraction of time" + "\n")
			filelrp.write(str(erp).ljust(10) + "; ERP" + "\n")
			filelrp.close()

		def writeecp(rel_humid, temphigh, templow, elevation):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File", filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'w')
			fileecp.write(str(rel_humid).ljust(10) + "; Relative Humidity" + "\n")
			fileecp.write(str(temphigh).ljust(10) + "; High Temperature (C)" + "\n")
			fileecp.write(str(templow).ljust(10) + "; Low Temperature (C)" + "\n")
			fileecp.write(str(elevation).ljust(10) + "; Elevation (m)" + "\n")
			fileecp.close()

		def Decimal_Degrees(deg, minu, sec):
			DD = deg + (minu/60.) + (sec/3600.)
			return DD

		def humid_calc(T, H):
			e = (H * 6.1121 * exp((17.502 * (T))/((T)+(240.97))))/100
			return e
		def pressure(altitude, T):
			P = 1013.25 * (1 - ((0.0065 * altitude)/((T+273.15) + 0.0065 * altitude)))**(5.257)
			return P

		def atmo_bend(e, T, P):
			N = 77.6 * (P/(T+273.15)) + 3.73e5 * (e/(T+273.15)**2)	
			return N
		def map_direction():
			if self.long_dd.get() < 0:
				self.map_ew.set(u"\u00B0" + "E")
			else:
				self.map_ew.set(u"\u00B0" + "W")
			if self.lat_dd.get() < 0:
				self.map_ns.set(u"\u00B0" + "S")
			else:
				self.map_ns.set(u"\u00B0" + "N")

		def temp_abc_dependence(fig, HT, LT,e, P, name, altitude):
			plt.clf()
			temp_abc= plt.scatter(linspace(LT+273.15, HT+273.15), atmo_bend(e, linspace(LT, HT), P))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0,0))
			plt.title("Location: {}\nTemperature Dependence on the Atmospheric Bending Constant at {} m".format(name, altitude), pad=20, fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Atmospheric Bending Constant (N-Units)")
			canvas.draw_idle()
			canvas.draw()

		def temp_press_dependence(fig, HT, LT, altitude, name):
			plt.clf()
			temp_press = plt.scatter(linspace(LT+273.15, HT+273.15), pressure(altitude, linspace(LT, HT)))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0,0))
			plt.title("Location: {}\nTemperature Dependence on Air Pressure at {} m".format(name, altitude), pad=20, fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Pressure (mbars)")
			canvas.draw_idle()
			canvas.draw()

		def temp_humi_dependence(fig, HT, LT, H, name, altitude):
			plt.clf()
			temp_humid = plt.scatter(linspace(LT+273.15, HT+273.15), humid_calc(linspace(LT, HT), H))
			plt.tick_params(axis='both')
			plt.ticklabel_format(axis='both', style='sci', useMathText=True, scilimits=(0,0))
			plt.title("Location: {}\nTemperature Dependence on Humidity at {} m".format(name, altitude), pad=20, fontsize='medium')
			plt.xlabel("Temperature (K)")
			plt.ylabel("Humidity (mbars)")
			canvas.draw_idle()
			canvas.draw()

		def super_calc():
			self.tempavg.set(float(self.temphigh.get())/2. + float(self.templow.get())/2.)
			self.humiavg.set(round(humid_calc(self.tempavg.get(), self.humid_scale.get()), 3))
			self.pressavg.set(round(pressure(self.elevation.get(), self.tempavg.get()), 3))
			self.abc.set(str(round(atmo_bend(self.humiavg.get(), self.tempavg.get() + 273.15, self.pressavg.get()), 3)))

		def readqth():
			fname = filedialog.askopenfilename(title="Get yo file", filetypes=[("Location Files", "*.qth")])
			fileqth = open(fname, 'r')
			content = [x.strip() for x in fileqth.readlines()]
			self.name.set(content[0])
			self.long_dd.set(content[2])
			self.lat_dd.set(content[1])
			self.antenna_alt.set(content[3])

		def readlrp():
			fname = filedialog.askopenfilename(title="Get yo file", filetypes=[("Irregular Terrian Model Files", "*.lrp")])
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
			fname = filedialog.askopenfilename(title="Get yo file", filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'r')
			content = [x.split(";")[0] for x in fileecp.readlines()]
			content = [x.strip() for x in content[0:7]]
			self.humid_scale.set(content[0])
			self.temphigh.set(content[1])
			self.templow.set(content[2])
			self.elevation.set(content[3])
			self.abc.set(content[4])
			self.dielec.set(content[5])
			self.earthcond.set(content[6])

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

		def event_writeqth(event):
			writeqth(self.name.get(), self.long_dd.get(), self.lat_dd.get(), self.antenna_alt.get())

		def event_writelrp(event):
			writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(), self.frequency.get(), self.rad_cli.get(), self.ant_orient.get(), self.frac_sit.get(), self.frac_tim.get(), self.erp.get())

		def event_writeecp(event):
			writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(), self.elevation.get())
	
		def event_super_calc(event):
			super_calc()

		def update_plot(plot):
			if plot == "temp_abc":
				temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humiavg.get(), self.pressavg.get(), self.name.get(), self.elevation.get())
			elif plot == "temp_pres":
				temp_press_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.elevation.get(), self.name.get())
			elif plot == "temp_humi":
				temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humid_scale.get(), self.name.get(), self.elevation.get())
			else:
				print("Not a valid Plot option")
		def event_update_plot(event):
			update_plot(self.active_plot.get())

##		
		n = 0
		self.name_label = tk.Label(master, text="Location Name:")
		self.name_label.grid(row=0, column=1, sticky='nw')

		self.name_entry = tk.Entry(master, width=7, textvariable=self.name)
		self.name_entry.grid(row=0, column=2, sticky='new')

##
		self.long_dms_label = tk.Label(master, text="Longitude")
		self.long_dms_label.grid(row=0, column=3, sticky='nw')

		self.long_dms_d = tk.Entry(master, width=3, textvariable=self.long_dms_deg)
		self.long_dms_d.grid(row=0, column=4, sticky='new', padx=(0,0))

		tk.Label(master, text=u"\u00B0").grid(row=0, column=5, sticky='new', padx=(0,0))

		self.long_dms_m = tk.Entry(master, width=3, textvariable=self.long_dms_min)
		self.long_dms_m.grid(row=0, column=6, sticky='new', padx=(0,n))

		tk.Label(master, text="'").grid(row=0, column=7, sticky='new', padx=(0,n))

		self.long_dms_s = tk.Entry(master, width=4, textvariable=self.long_dms_sec)
		self.long_dms_s.grid(row=0, column=8, sticky='new', padx=(0,n))

		tk.Label(master, text="''").grid(row=0, column=9, sticky='new', padx=(0,n))

##
		self.lat_dms_label = tk.Label(master, text="Latitude")
		self.lat_dms_label.grid(row=0, column=3, sticky='nw', pady=30)

		self.lat_dms_d = tk.Entry(master, width=3, textvariable=self.lat_dms_deg)
		self.lat_dms_d.grid(row=0, column=4, sticky='new', pady=30, padx=(0,n))

		tk.Label(master, text=u"\u00B0").grid(row=0, column=5, sticky='new', pady=30, padx=(0,n))

		self.lat_dms_m = tk.Entry(master, width=3, textvariable=self.lat_dms_min)
		self.lat_dms_m.grid(row=0, column=6, sticky='new', pady=30, padx=(0,n))

		tk.Label(master, text="'").grid(row=0, column=7, sticky='new', pady=30, padx=(0,n))

		self.lat_dms_s = tk.Entry(master, width=4, textvariable=self.lat_dms_sec)
		self.lat_dms_s.grid(row=0, column=8, sticky='new', pady=30, padx=(0,n))

		tk.Label(master, text="''").grid(row=0, column=9, sticky='new', pady=30, padx=(0,n))

##
		tk.Label(master, text=u"\u2192").grid(row=0, column=10, sticky='new')
		tk.Label(master, text=u"\u2192").grid(row=0, column=10, sticky='new', pady=30)

##
		self.long_dd_entry = tk.Entry(master, width=7, textvariable=self.long_dd)
		self.long_dd_entry.grid(row=0, column=11, sticky='new')

		self.lat_dd_entry = tk.Entry(master, width=7, textvariable=self.lat_dd)
		self.lat_dd_entry.grid(row=0, column=11, sticky='new', pady=30)


		self.map_dir_ew = tk.Label(master, text=str(self.map_ew.get()))
		self.map_dir_ew.grid(row=0, column=12,  sticky='nw', padx=2)

		self.long_convert = tk.Button(master, text="Convert", command=lambda: self.long_dd.set(Decimal_Degrees(float(self.long_dms_d.get()), float(self.long_dms_m.get()), float(self.long_dms_s.get()))))
		self.long_convert.grid(row=0, column=13, sticky='new')

		self.lat_convert = tk.Button(master, text="Convert", command=lambda: self.lat_dd.set(Decimal_Degrees(float(self.lat_dms_d.get()), float(self.lat_dms_m.get()), float(self.lat_dms_s.get()))))
		self.lat_convert.grid(row=0, column=13, sticky='new', pady=30)
##
		self.ante_alt_label = tk.Label(master, text="Antenna Height"+ " "*6 + "(m)")
		self.ante_alt_label.grid(row=0, column=1, sticky='nw', pady=30)

		self.ante_alt_entry = tk.Entry(master, width=7, textvariable=self.antenna_alt)
		self.ante_alt_entry.grid(row=0, column=2, sticky='new', pady=30)
		

		self.createqth = tk.Button(master, command=lambda: writeqth(self.name.get(), self.long_dd.get(), self.lat_dd.get(), self.antenna_alt.get()), text="Generate QTH")
		self.createqth.grid(row=0, column=1, sticky='new', columnspan=1,  pady=55)

##
	
		self.temp_high_label = tk.Label(master, text="High Temperature"+ " "*2 + "("+u"\u00B0"+"C)")
		self.temp_high_label.grid(row=0, column=1, sticky='nw', pady=90)

		self.temp_high_entry = tk.Entry(master, width=7, textvariable=self.temphigh)
		self.temp_high_entry.grid(row=0, column=2, sticky='new', pady=90)

		self.temp_low_label = tk.Label(master, text="Low Temperature"+ " "*3 + "("+u"\u00B0"+"C)")
		self.temp_low_label.grid(row=0, column=1, sticky='nw', pady=120)
		
		self.temp_low_entry = tk.Entry(master, width=7, textvariable=self.templow)
		self.temp_low_entry.grid(row=0, column=2, sticky='new', pady=120)

		self.temp_avg_label = tk.Label(master, text="Avg. Temperature"+ " "*2 + "("+u"\u00B0"+"C)")
		self.temp_avg_label.grid(row=0, column=1, sticky='nw', pady=150)

		self.temp_avg_entry = tk.Entry(master, width=7, textvariable=self.tempavg)
		self.temp_avg_entry.grid(row=0, column=2, sticky='new', pady=150)

		self.elevation_label = tk.Label(master, text="Elevation"+ " "*16 + "(m)")
		self.elevation_label.grid(row=0, column=1, sticky='nw', pady=180)

		self.elevation_entry = tk.Entry(master, textvariable=self.elevation, width=8)
		self.elevation_entry.grid(row=0, column=2, sticky='nw', pady=180)

		self.humid_label = tk.Label(master, text="Rel. Humidity"+ " "*3 + "(%)")
		self.humid_label.grid(row=0, column=3, sticky='nw', pady=90)

		self.humid_scale = tk.Scale(master, from_=0, to=100, resolution=10, orient=tk.HORIZONTAL)
		self.humid_scale.grid(row=0, column=4, columnspan=6, sticky='new', pady=70)
		self.humid_scale.set(50)

		self.humid_avg_label = tk.Label(master, text="Avg. Humidity"+ " "*2 +"(mbar)")
		self.humid_avg_label.grid(row=0, column=3, sticky='nw', pady=120)

		self.humid_avg_calc = tk.Entry(master, textvariable=self.humiavg, width=8)
		self.humid_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=4, pady=120)

		self.press_avg_label = tk.Label(master, text="Avg. Pressure"+ " "*3 +"(mbar)")
		self.press_avg_label.grid(row=0, column=3, sticky='nw', pady=150)

		self.press_avg_calc = tk.Entry(master, textvariable=self.pressavg, width=8)
		self.press_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=4, pady=150)

		self.abc_label = tk.Label(master, text="Bending Const."+ " "*1 +"(N-Units)")
		self.abc_label.grid(row=0, column=3, sticky='nw', pady=180)

		self.abc_entry = tk.Entry(master, textvariable=self.abc, width=8)
		self.abc_entry.grid(row=0, column=4, sticky='new', pady=180)

		self.pan_calc = tk.Button(master, text="Calculate", command=lambda: super_calc())
		self.pan_calc.grid(row=0, column=1, sticky='new', columnspan=1, pady=205)
	
##
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
		
		exportmenu.add_command(label="Export QTH <Ctrl+q>", command=lambda: writeqth(self.name.get(), self.long_dd.get(), self.lat_dd.get(), self.antenna_alt.get()))
		exportmenu.add_command(label="Export LRP <Ctrl+l>", command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(), self.frequency.get(), self.rad_cli.get(), self.ant_orient.get(), self.frac_sit.get(), self.frac_tim.get(), self.erp.get()))
		exportmenu.add_command(label="Export ECP <Ctrl+e>", command=lambda: writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(), self.elevation.get()))	


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

		tempplot.add_radiobutton(label="Temp. vs. A.B.C.", variable=self.active_plot, value="temp_abc", command=lambda: temp_abc_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humiavg.get(), self.pressavg.get(), self.name.get(), self.elevation.get()))
		tempplot.add_radiobutton(label="Temp. vs Pressure", variable=self.active_plot, value="temp_pres", command=lambda: temp_press_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.elevation.get(), self.name.get()))
		tempplot.add_radiobutton(label="Temp. vs Humidity", variable=self.active_plot, value="temp_humi",command=lambda: temp_humi_dependence(self.fig, self.temphigh.get(), self.templow.get(), self.humid_scale.get(), self.name.get(), self.elevation.get()))


		menu.add_command(label="Update Plot", command=lambda: update_plot(self.active_plot.get()))
##

		self.dielectric_label = tk.Label(master, text="Dielectric Constant")
		self.dielectric_label.grid(row=0, column=1, sticky='nw', pady=240)

		self.dielectric_entry = tk.Entry(master, textvariable=self.dielec, width=8)
		self.dielectric_entry.grid(row=0, column=2, sticky='new', pady=240)

		self.ground_cond_label = tk.Label(master, text="Earth Conductivity (S/m)")
		self.ground_cond_label.grid(row=0, column=1, sticky='nw', pady=270)

		self.ground_cond_entry = tk.Entry(master, textvariable=self.earthcond, width=8)
		self.ground_cond_entry.grid(row=0, column=2, sticky='new', pady=270)

		self.frequency_label = tk.Label(master, text="Frequency (MHz)")
		self.frequency_label.grid(row=0, column=1, sticky='nw', pady=300)

		self.frequency_entry = tk.Entry(master, textvariable=self.frequency, width=8)
		self.frequency_entry.grid(row=0, column=2, sticky='new', pady=300)
		
		self.frac_sit_label = tk.Label(master, text="Fraction of Situations")
		self.frac_sit_label.grid(row=0, column=1,  sticky='nw', pady=330)

		self.frac_sit_entry = tk.Entry(master, textvariable=self.frac_sit, width=4)
		self.frac_sit_entry.grid(row=0, column=2, sticky='new', pady=330)

		self.frac_tim_label = tk.Label(master, text="Fraction of Time")
		self.frac_tim_label.grid(row=0, column=1,  sticky='nw', pady=360)

		self.frac_tim_entry = tk.Entry(master, textvariable=self.frac_tim, width=4)
		self.frac_tim_entry.grid(row=0, column=2, sticky='new', pady=360)

		self.erp_label = tk.Label(master, text="Effective Radiated Power (W)")
		self.erp_label.grid(row=0, column=1, sticky='nw', pady=390)

		self.erp_entry = tk.Entry(master, textvariable=self.erp, width=8)
		self.erp_entry.grid(row=0, column=2, sticky='new', pady=390)
##

		self.radio_climate_label = tk.Label(master, text="Radio Climate Codes")
		self.radio_climate_label.grid(row=0, column=3, columnspan=3, sticky='new', pady=240)

		self.climate_one = tk.Radiobutton(master, text="Equatorial", value=1, variable=self.rad_cli)
		self.climate_one.grid(row=0, column=3, columnspan=3, sticky='nw', pady=260)

		self.climate_two = tk.Radiobutton(master, text="Continental Subtropical", value=2, variable=self.rad_cli)
		self.climate_two.grid(row=0, column=3, columnspan=3, sticky='nw', pady=280)

		self.climate_three = tk.Radiobutton(master, text="Maritime Suptropical", value=3, variable=self.rad_cli)
		self.climate_three.grid(row=0, column=3,columnspan=3, sticky='nw', pady=300)

		self.climate_four = tk.Radiobutton(master, text="Desert", value=4, variable=self.rad_cli)
		self.climate_four.grid(row=0, column=3, columnspan=3,sticky='nw', pady=320)

		self.climate_five = tk.Radiobutton(master, text="Continental Temperate", value=5, variable=self.rad_cli)
		self.climate_five.grid(row=0, column=3, columnspan=3,sticky='nw', pady=340)

		self.climate_six = tk.Radiobutton(master, text="Maritime Temperate (land)", value=6, variable=self.rad_cli)
		self.climate_six.grid(row=0, column=3, columnspan=3,sticky='nw', pady=360)

		self.climate_seven = tk.Radiobutton(master, text="Maritime Temperate (sea)", value=7, variable=self.rad_cli)
		self.climate_seven.grid(row=0, column=3, columnspan=3,sticky='nw', pady=380)
##

		self.ant_orient_label = tk.Label(master, text="Antenna Orientation")
		self.ant_orient_label.grid(row=0, column=7, columnspan=6, sticky='new', pady=240)

		self.ant_hori = tk.Radiobutton(master, text="Horizontal", value=0, variable=self.ant_orient)
		self.ant_hori.grid(row=0, column=7, columnspan=5, sticky='nw', pady=260)
		self.ant_vert = tk.Radiobutton(master, text="Vertical", value=1, variable=self.ant_orient)
		self.ant_vert.grid(row=0, column=7, columnspan=5, sticky='nw', pady=280)

		self.super_button = tk.Button(master, text="Generate LRP File", height=2,  command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(), self.frequency.get(), self.rad_cli.get(), self.ant_orient.get(), self.frac_sit.get(), self.frac_tim.get(), self.erp.get()))
		self.super_button.grid(row=0, column=1, sticky='new', pady=430)

		def design():
			labels = [self.name_label]
if __name__ == '__main__':
	root = tk.Tk()
	Radio(root)

	root.title("SPLAT! Configuratin File Generator")
	root.geometry(str(root_width) + "x" + str(root_height))
	root.maxsize(str(root_width), str(root_height))
	root.minsize(str(600), str(root_height))


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
