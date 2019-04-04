from numpy import *
fname = "./sounding_TITAN.txt"
data = open(fname, 'r+')
#content = [x.strip(",") for x in data.readlines()]
units_P = raw_input("What units are Pressure in?\n>> ")
Pn		= input("Column of Pressure\n>> ")
if units_P == "Pa":
	P = (loadtxt(fname, unpack=True)[Pn])/100
elif units_P == "hPa":
	P = loadtxt(fname, unpack=True)[Pn]
elif units_P == "bar":
	P =loadtxt(fname,  unpack=True)[Pn] * 1000
else:
	P = loadtxt(fname,  unpack=True)[Pn]
##
units_Z = raw_input("What units is Altitude in?\n>> ")
Zn		= input("Column of Altitude\n>> ")
if units_Z == "km":
	Z = loadtxt(fname, unpack=True)[Zn]
elif units_Z == "m":
	Z = (loadtxt(fname, unpack=True)[Zn])/1000
else:
	Z = loadtxt(fname,  unpack=True)[Zn]
##
units_T = raw_input("What units is Temperature in?\n>> ")
Tn		= input("Column of Temperature\n>> ")
if units_T == "K":
	T = loadtxt(fname, unpack=True)[Tn]
elif units_T == "C":
	T = loadtxt(fname,  unpack=True)[Tn] + 273.15
else:
	T = loadtxt(fname, unpack=True)[Tn]
#Pr = insert(P, 0, 'Pressure (hPa)')
#Te = insert(T, 0, 'Temp (K)')
#Al = insert(Z, 0, 'Altitude (km)')
# First Column => Time
# Second Column => Potential
# 3rd Column => Altitude
# 4th Column => Temp
# 5th Column =>Pressure
savetxt(fname, vstack([Z,T,P]).T, comments="", header="HGHT (km)\t\tTEMP (K)\t\tPRES (hPa)", delimiter='\t\t', fmt='%1.3E')
