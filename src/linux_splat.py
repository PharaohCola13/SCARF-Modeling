import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.animation import *
from numpy import *
from PIL import Image, ImageTk
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
root_height = 730
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
		self.long_dms_min = tk.DoubleVar(value=0)
		self.long_dms_sec = tk.DoubleVar(value=0.0)


		self.lat_dms_deg = tk.DoubleVar(value=0)
		self.lat_dms_min = tk.DoubleVar(value=0)
		self.lat_dms_sec = tk.DoubleVar(value=0.0)

		self.antenna_alt = tk.DoubleVar(value=0.0)

		self.temphigh 	= tk.DoubleVar(value=0.0)
		self.templow  	= tk.DoubleVar(value=0.0)
		self.tempavg  	= tk.DoubleVar(value=0.0)

		self.pressavg 	= tk.DoubleVar(value=0.0)
		self.humiavg  	= tk.DoubleVar(value=0.0)

		self.elevation 	= tk.DoubleVar(value=0.0)
		self.bfield		= tk.DoubleVar(value=0.0)
		self.bfield_rel = tk.DoubleVar(value=0.0)
		self.star       = tk.StringVar(value="G Class")
		self.notes      = tk.StringVar()
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

		def writeecp(rel_humid, temphigh, templow, elevation, Bfield):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File", filetypes=[("Environmental Climate Profile Files", "*.ecp")])
			fileecp = open(fname, 'w')
			fileecp.write(str(rel_humid).ljust(10) + "; Relative Humidity" + "\n")
			fileecp.write(str(temphigh).ljust(10) + "; High Temperature (C)" + "\n")
			fileecp.write(str(templow).ljust(10) + "; Low Temperature (C)" + "\n")
			fileecp.write(str(elevation).ljust(10) + "; Elevation (m)" + "\n")
			fileecp.write(str(Bfield).ljust(10) + "; Planetary Magnetic Field (G)" + "\n")
			fileecp.close()

		def writeqth(name, lo_d, lo_m, lo_s, la_d, la_m, la_s, antenna):
			fname = filedialog.asksaveasfilename(initialdir="./", title="Leave yo File", filetypes=[("Location Files", "*.qth")])
			fileqth = open(fname, 'w')
			fileqth.write(str(name) + "\n")
			fileqth.write(str(la_d)+ " " + str(la_m)+ " " + str(la_s) + "\n")
			fileqth.write(str(lo_d)+ " " + str(lo_m)+ " " + str(lo_s) + "\n")
			fileqth.write(str(antenna) + "\n")
			fileqth.close()

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

		def bfield(B):
			B_rel = B/(7.981e10)
			return B_rel


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
			self.bfield_rel.set("{:0.2E}".format(bfield(self.bfield.get())))

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

		self.notes_input = tk.Text(master, width=50, height=20)
		self.notes_input.grid(row=0, column=4, columnspan=8, sticky='new', pady=430)
		self.notes = self.notes_input.get("1.0","end-1c")

		self.notes_button = tk.Button(master, text="Export Notes", height=2)
		self.notes_button.grid(row=0, column=2,columnspan=2, sticky='new',pady=430)

		n = 0
		self.name_label = tk.Label(master, text="Location Name:")
		self.name_label.grid(row=0, column=1, sticky='nw')

		self.name_entry = tk.Entry(master, width=7, textvariable=self.name)
		self.name_entry.grid(row=0, column=2, sticky='new')

##
		self.long_dms_label = tk.Label(master, text="Longitude")
		self.long_dms_label.grid(row=0, column=3, sticky='nw')

		self.long_dms_d = tk.Entry(master, width=4, textvariable=self.long_dms_deg)
		self.long_dms_d.grid(row=0, column=4, sticky='new', padx=(0,0))

		self.deg_lo = tk.Label(master, text=u"\u00B0",font=('Times', 13))
		self.deg_lo.grid(row=0, column=5, sticky='n')

		self.long_dms_m = tk.Entry(master, width=4, textvariable=self.long_dms_min)
		self.long_dms_m.grid(row=0, column=6, sticky='new')

		self.min_lo = tk.Label(master, text="'",font=('Times', 13))
		self.min_lo.grid(row=0, column=7, sticky='new')

		self.long_dms_s = tk.Entry(master, width=5, textvariable=self.long_dms_sec)
		self.long_dms_s.grid(row=0, column=8, columnspan=2, sticky='new', )

		self.sec_lo = tk.Label(master, text="''",font=('Times', 13))
		self.sec_lo.grid(row=0, column=10, sticky='new', )

##
		self.lat_dms_label = tk.Label(master, text="Latitude")
		self.lat_dms_label.grid(row=0, column=3, sticky='nw', pady=30)

		self.lat_dms_d = tk.Entry(master, width=4, textvariable=self.lat_dms_deg)
		self.lat_dms_d.grid(row=0, column=4, sticky='new', pady=30)

		self.deg_la = tk.Label(master, text=u"\u00B0", font=('Times', 13))
		self.deg_la.grid(row=0, column=5, sticky='new', pady=30)

		self.lat_dms_m = tk.Entry(master, width=4, textvariable=self.lat_dms_min)
		self.lat_dms_m.grid(row=0, column=6, sticky='new', pady=30, )

		self.min_la = tk.Label(master, text="'", font=('Times', 13))
		self.min_la.grid(row=0, column=7, sticky='new', pady=30)

		self.lat_dms_s = tk.Entry(master, width=5, textvariable=self.lat_dms_sec)
		self.lat_dms_s.grid(row=0, column=8, columnspan=2, sticky='new', pady=30)

		self.sec_la = tk.Label(master, text="''", font=('Times', 13))
		self.sec_la.grid(row=0, column=10, sticky='new', pady=30)

		self.ante_alt_label = tk.Label(master, text="Antenna Height"+ " "*6 + "(m)")
		self.ante_alt_label.grid(row=0, column=1, sticky='nw', pady=30)

		self.ante_alt_entry = tk.Entry(master, width=7, textvariable=self.antenna_alt)
		self.ante_alt_entry.grid(row=0, column=2, sticky='new', pady=30)

		self.createqth = tk.Button(master, command=lambda: writeqth(self.name.get(), self.long_dms_d.get(),self.long_dms_m.get(),self.long_dms_s.get(), self.lat_dms_d.get(),self.lat_dms_m.get(),self.lat_dms_s.get(), self.antenna_alt.get()), text="Generate QTH")
		self.createqth.grid(row=0, column=1, sticky='new', columnspan=1,  pady=60)
##
		self.temp_high_label = tk.Label(master, text="High Temperature"+ "\t" + "("+u"\u00B0"+"C)")
		self.temp_high_label.grid(row=0, column=1, sticky='nw', pady=90)

		self.temp_high_entry = tk.Entry(master, width=7, textvariable=self.temphigh)
		self.temp_high_entry.grid(row=0, column=2, sticky='new', pady=90)

		self.temp_low_label = tk.Label(master, text="Low Temperature"+ "\t" + "("+u"\u00B0"+"C)")
		self.temp_low_label.grid(row=0, column=1, sticky='nw', pady=120)
		
		self.temp_low_entry = tk.Entry(master, width=7, textvariable=self.templow)
		self.temp_low_entry.grid(row=0, column=2, sticky='new', pady=120)

		self.temp_avg_label = tk.Label(master, text="Avg. Temperature"+ "\t" + "("+u"\u00B0"+"C)")
		self.temp_avg_label.grid(row=0, column=1, sticky='nw', pady=150)

		self.temp_avg_entry = tk.Entry(master, width=7, textvariable=self.tempavg)
		self.temp_avg_entry.grid(row=0, column=2, sticky='new', pady=150)

		self.elevation_label = tk.Label(master, text="Elevation"+ "\t\t" + "(m)")
		self.elevation_label.grid(row=0, column=1, sticky='nw', pady=180)

		self.elevation_entry = tk.Entry(master, textvariable=self.elevation, width=8)
		self.elevation_entry.grid(row=0, column=2, sticky='nw', pady=180)

		self.humid_label = tk.Label(master, text="Rel. Humidity"+ " "*2 + "(%)")
		self.humid_label.grid(row=0, column=3, sticky='nw', pady=90)

		self.humid_scale = tk.Scale(master, from_=0, to=100, resolution=10, orient=tk.HORIZONTAL)
		self.humid_scale.grid(row=0, column=4, columnspan=8, sticky='new', pady=70)
		self.humid_scale.set(50)

		self.humid_avg_label = tk.Label(master, text="Avg. Humidity"+ " "*1 +"(mbar)")
		self.humid_avg_label.grid(row=0, column=3, sticky='nw', pady=120)

		self.humid_avg_calc = tk.Entry(master, textvariable=self.humiavg, width=8)
		self.humid_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=4, pady=120)

		self.press_avg_label = tk.Label(master, text="Avg. Pressure"+ " "*2 +"(mbar)")
		self.press_avg_label.grid(row=0, column=3, sticky='nw', pady=150)

		self.press_avg_calc = tk.Entry(master, textvariable=self.pressavg, width=8)
		self.press_avg_calc.grid(row=0, column=4, sticky='nw', columnspan=4, pady=150)

		self.abc_label = tk.Label(master, text="Atmospheric Bending Constant"+ " "*2 +"(N-Units)")
		self.abc_label.grid(row=0, column=3, columnspan=5, sticky='nw', pady=180)

		self.abc_entry = tk.Entry(master, textvariable=self.abc, width=8)
		self.abc_entry.grid(row=0, column=10, columnspan=2, sticky='new', pady=180)

		self.bfield_label = tk.Label(master, text="Magnetic Field (G)")
		self.bfield_label.grid(row=0, column=6, columnspan=4, sticky='nw', pady=120)

		self.bfield_entry = tk.Entry(master, textvariable=self.bfield, width=8)
		self.bfield_entry.grid(row=0, column=10,columnspan=2, sticky='nw', pady=120)

		self.bfield_rel_label = tk.Label(master, text="Rel. Magnetic Field (G)")
		self.bfield_rel_label.grid(row=0, column=6, columnspan=3, sticky='nw', pady=150)

		self.bfield_rel_entry = tk.Entry(master, textvariable=self.bfield_rel, width=8)
		self.bfield_rel_entry.grid(row=0, column=10,columnspan=2, sticky='nw', pady=150)

		self.pan_calc = tk.Button(master, text="Calculate", command=lambda: super_calc())
		self.pan_calc.grid(row=0, column=1, sticky='new', columnspan=1, pady=210)
	
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
		exportmenu.add_command(label="Export ECP <Ctrl+e>", command=lambda: writeecp(self.humid_scale.get(), self.temphigh.get(), self.templow.get(), self.elevation.get(), self.bfield.get()))


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

		self.ground_cond_label = tk.Label(master, text="Earth Conductivity"+ "\t" +  "(S/m)")
		self.ground_cond_label.grid(row=0, column=1, sticky='nw', pady=270)

		self.ground_cond_entry = tk.Entry(master, textvariable=self.earthcond, width=8)
		self.ground_cond_entry.grid(row=0, column=2, sticky='new', pady=270)

		self.frequency_label = tk.Label(master, text="Frequency"+ "\t" +  "(MHz)")
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

		self.radio_climate_label = tk.Label(master, text="--- Radio Climate Codes ---")
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

		self.ant_orient_label = tk.Label(master, text="--- Antenna Orientation ---")
		self.ant_orient_label.grid(row=0, column=5, columnspan=6, sticky='new', pady=240)

		self.ant_hori = tk.Radiobutton(master, text="Horizontal", value=0, variable=self.ant_orient)
		self.ant_hori.grid(row=0, column=5, columnspan=5, sticky='nw', pady=260)
		self.ant_vert = tk.Radiobutton(master, text="Vertical", value=1, variable=self.ant_orient)
		self.ant_vert.grid(row=0, column=5, columnspan=5, sticky='nw', pady=280)

		self.super_button = tk.Button(master, text="Generate LRP File", height=2,  command=lambda: writelrp(self.dielec.get(), self.earthcond.get(), self.abc.get(), self.frequency.get(), self.rad_cli.get(), self.ant_orient.get(), self.frac_sit.get(), self.frac_tim.get(), self.erp.get()))
		self.super_button.grid(row=0, column=1, sticky='new', pady=430)


		self.G = ImageTk.PhotoImage(Image.open("Gclass.png"))
		self.gclass = tk.Label(master, image=self.G)
		self.gclass.grid(row=0, column=1, sticky='new', pady=490)

		self.gclass_opt = tk.Radiobutton(master, value="G Class", text="G Class", variable=self.star)
		self.gclass_opt.grid(row=0, column=1, sticky='new', pady=480)

		self.M = ImageTk.PhotoImage(Image.open("Mclass.png"))
		self.mclass = tk.Label(master, image=self.M)
		self.mclass.grid(row=0, column=2, columnspan=2, sticky='new', pady=490)

		self.mclass_opt = tk.Radiobutton(master, value="M Class", text="M Class", variable=self.star)
		self.mclass_opt.grid(row=0, column=2,columnspan=2, sticky='new', pady=480)

		self.L = ImageTk.PhotoImage(Image.open("Lclass.png"))
		self.lclass = tk.Label(master, image=self.L)
		self.lclass.grid(row=0, column=2,columnspan=2,sticky='new', pady=610)

		self.lclass_opt = tk.Radiobutton(master, value="L Class", text="L Class", variable=self.star)
		self.lclass_opt.grid(row=0, column=2,columnspan=2, sticky='new', pady=600)

		self.O = ImageTk.PhotoImage(Image.open("Oclass.png"))
		self.oclass = tk.Label(master, image=self.O)
		self.oclass.grid(row=0, column=1, sticky='new', pady=610)

		self.oclass_opt = tk.Radiobutton(master, value="O Class", text="O Class", variable=self.star)
		self.oclass_opt.grid(row=0, column=1, sticky='new', pady=600)

		self.gclass_opt.config(bg=dim, fg="#FAD800", activebackground=dim, highlightthickness=0, activeforeground="#FAD800",selectcolor=dim)
		self.mclass_opt.config(bg=dim, fg="#FF0000", activebackground=dim, highlightthickness=0,activeforeground="#FF0000",selectcolor=dim)
		self.lclass_opt.config(bg=dim, fg="#FFFFFF", activebackground=dim, highlightthickness=0, activeforeground="#FFFFFF",selectcolor=dim)
		self.oclass_opt.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0,activeforeground=dimf,selectcolor=dim)

		def design(self):
			master.config(background=dim)
			labels 	= [self.name_label, self.frac_sit_label, self.ant_orient_label,
						 self.erp_label,self.radio_climate_label,self.frac_tim_label,
						 self.frequency_label,self.ground_cond_label,self.dielectric_label,
						 self.abc_label, self.press_avg_label,self.humid_avg_label,self.humid_label,
						 self.elevation_label,self.temp_avg_label, self.temp_low_label,
						 self.temp_high_label,self.long_dms_label,self.ante_alt_label,
						 self.deg_lo, self.min_lo, self.sec_lo,self.deg_la, self.min_la, self.sec_la,self.lat_dms_label,
						 self.bfield_label, self.bfield_rel_label, self.gclass, self.mclass, self.oclass, self.lclass]
			button 	= [self.super_button,self.pan_calc, self.createqth]
			scales 	= [self.humid_scale]
			menus 	= [menu, filemenu, plotmenu, tempplot, exportmenu, importmenu]
			entry 	= [self.erp_entry,self.frac_tim_entry,self.frequency_entry,self.ground_cond_entry,
						self.dielectric_entry, self.abc_entry,self.press_avg_calc,
						self.humid_avg_calc, self.elevation_entry, self.temp_avg_entry,self.temp_low_entry,
						self.temp_high_entry, self.name_entry, self.long_dms_d,self.long_dms_m,self.long_dms_s,
						self.lat_dms_d,self.lat_dms_m,self.lat_dms_s, self.bfield_entry, self.bfield_rel_entry]
			radio	= [self.ant_hori, self.ant_vert, self.climate_one, self.climate_two, self.climate_three, self.climate_four, self.climate_five, self.climate_six, self.climate_seven ]

			for m in scales:
				m.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0, troughcolor=dimf)
			for n in labels:
				n.config(bg=dim, fg=dimf, activebackground=dim)
			for o in radio:
				o.config(bg=dim, fg=dimf, activebackground=dim, highlightthickness=0, activeforeground=dimf,
						 selectcolor=dim)
			for p in button:
				p.config(bg=dim, fg=dimf, activebackground=dim, highlightbackground=dimf, activeforeground=dimf)
			for q in menus:
				q.config(bg=dim, fg=dimf, activebackground=dim, activeforeground=dimf)
		return design(self)

if __name__ == '__main__':
	root = tk.Tk()
	Radio(root)

	root.title("SPLAT! Configuratin File Generator")
	root.geometry(str(root_width) + "x" + str(root_height))#
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
