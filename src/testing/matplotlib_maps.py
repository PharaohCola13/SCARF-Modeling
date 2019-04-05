# https://stackoverflow.com/questions/40374441/python-basemap-module-impossible-to-import
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=-76.5,llcrnrlat=7., urcrnrlon=-75.9,urcrnrlat=7.5, resolution = 'h', epsg=3115)
map.arcgisimage(service='Specialty/DeLorme_World_Base_Map', xpixels = 1500, verbose= True)
#map.arcgisimage(service='NatGeo_World_Map', xpixels = 2000, verbose= False)
plt.show()
plt.close()
