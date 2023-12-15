from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import numpy as np
import pandas
import os
import cmaps
import math

def drawShp(iFilePath1, iColor, iLegend, iTitle, iUnit, iFilePath2):
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = -15, urcrnrlat = 85, llcrnrlon = 10, urcrnrlon = 195, resolution = "h")
	map.drawparallels(np.arange(-15., 85., 15.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 15.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile(r"H:\1_heatwave\data\0base\countries", "countries")	
	map.drawlsmask()
	iTable = pandas.read_csv(iFilePath1)
	latitude = np.array(iTable["latitude"][:])
	longitude = np.array(iTable["longitude"][:]) 
	plt.scatter(longitude, latitude, c = iColor, s = 1, label = iLegend)
	plt.legend(loc = "lower right", fontsize = 10)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	plt.title(iTitle, fontsize = 12)
	plt.text(195, 88, iUnit, fontsize = 8)
	plt.savefig(iFilePath2, dpi = 330)
	# plt.show()

def drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((929, 1783), np.nan)
	for row in range(0, 929):
		for column in range(0, 1783):
			if data2[928 - row, column] != -3.4028234663852886e+38:
				data3[row, column] = data2[928 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = -15, urcrnrlat = 85, llcrnrlon = 10, urcrnrlon = 195, resolution = "h")
	map.drawparallels(np.arange(-15., 85., 15.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 15.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12.093704, 190.393704, 1783)
	y1 = np.linspace(-11.03, 81.87, 929)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	plt.title(iTitle, fontsize = 12)
	plt.text(197, 88, iUnit, fontsize = 8)
	plt.savefig(iFilePath2, dpi = 330)
	# plt.show()

def drawRussia1(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((929, 1783), np.nan)
	for row in range(0, 929):
		for column in range(0, 1783):
			longitude = 12.093704 + 0.1 * column
			latitude = -11.03 + 0.1 * row 
			if data2[928 - row, column] != -3.4028234663852886e+38 and longitude >= 12.093704 and longitude <= 80 and latitude >= 40 and latitude <= 77.88:
				data3[row, column] = data2[928 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = 40, urcrnrlat = 77.88, llcrnrlon = 10, urcrnrlon = 80, resolution = "h")	
	map.drawparallels(np.arange(-15., 85., 10.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 10.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12.093704, 190.393704, 1783)
	y1 = np.linspace(-11.03, 81.87, 929)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	iTable = pandas.read_csv(iFilePath2)
	latitude = np.array(iTable["latitude"][:])
	longitude = np.array(iTable["longitude"][:]) 
	plt.scatter(longitude, latitude, c = "black", s = 3, label = "city")
	plt.text(38, 56, "Moscow", fontsize = 8)
	plt.legend(loc = "lower right", fontsize = 10)
	plt.title(iTitle, fontsize = 12)
	plt.text(81, 79, iUnit, fontsize = 8)
	plt.savefig(iFilePath3, dpi = 330)

def drawRussia2(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((360, 720), np.nan)
	for row in range(0, 360):
		for column in range(0, 720):
			longitude = 0.5 * column
			latitude = -90 + 0.5 * row 
			if math.isnan(data2[359 - row, column]):
				pass
			else:
				if longitude >= 10 and longitude <= 80 and latitude >= 40 and latitude <= 77.88:
					data3[row, column] = data2[359 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = 40, urcrnrlat = 77.88, llcrnrlon = 10, urcrnrlon = 80, resolution = "h")	
	map.drawparallels(np.arange(-15., 85., 10.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 10.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(0, 360, 720)
	y1 = np.linspace(-90, 90, 360)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	iTable = pandas.read_csv(iFilePath2)
	latitude = np.array(iTable["latitude"][:])
	longitude = np.array(iTable["longitude"][:]) 
	plt.scatter(longitude, latitude, c = "black", s = 3, label = "city")
	plt.text(38, 56, "Moscow", fontsize = 8)
	plt.legend(loc = "lower right", fontsize = 10)
	plt.title(iTitle, fontsize = 12)
	plt.text(81, 79, iUnit, fontsize = 8)
	plt.savefig(iFilePath3, dpi = 330)

def drawIndia(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((929, 1783), np.nan)
	for row in range(0, 929):
		for column in range(0, 1783):
			longitude = 12.093704 + 0.1 * column
			latitude = -11.03 + 0.1 * row 
			if data2[928 - row, column] != -3.4028234663852886e+38 and longitude >= 68 and longitude <= 98 and latitude >= 6 and latitude <= 36:
				data3[row, column] = data2[928 - row, column]
	fig = plt.figure(figsize = (5, 5), dpi = 330)
	map = Basemap(llcrnrlat = 6, urcrnrlat = 36, llcrnrlon = 68, urcrnrlon = 98, resolution = "h")	
	map.drawparallels(np.arange(5., 40., 5.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(65., 100., 5.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12.093704, 190.393704, 1783)
	y1 = np.linspace(-11.03, 81.87, 929)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "3%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.1, bottom = 0.01, right = 0.9, top = 0.99)
	iTable = pandas.read_csv(iFilePath2)
	latitude = np.array(iTable["latitude"][:])
	longitude = np.array(iTable["longitude"][:]) 
	plt.scatter(longitude, latitude, c = "black", s = 3, label = "city")
	plt.text(76.5, 29, "New Delhi", fontsize = 8)
	plt.legend(loc = "lower right", fontsize = 10)
	plt.title(iTitle, fontsize = 12)
	plt.text(98, 36.8, iUnit, fontsize = 8)
	plt.savefig(iFilePath3, dpi = 330)

def drawExposure(iFilePath1, iCmap, iTitle, iUnit, iFilePath2):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((860, 1679), np.nan)
	for row in range(0,  860):
		for column in range(0, 1679):
			if data2[859 - row, column] != -3.4028234663852886e+38:
				data3[row, column] = data2[859 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = -15, urcrnrlat = 85, llcrnrlon = 10, urcrnrlon = 195, resolution = "h")
	map.drawparallels(np.arange(-15., 85., 15.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 15.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12.09, 180, 1679)
	y1 = np.linspace(-11, 75,  860)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	plt.title(iTitle, fontsize = 12)
	plt.text(197, 88, iUnit, fontsize = 8)
	plt.savefig(iFilePath2, dpi = 330)

def drawVulneraility(iFilePath1, iCmap, iTitle, iUnit, iFilePath2):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((916, 1680), np.nan)
	for row in range(0,  916):
		for column in range(0, 1680):
			if data2[915 - row, column] != -3.4028234663852886e+38:
				data3[row, column] = data2[915 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = -15, urcrnrlat = 85, llcrnrlon = 10, urcrnrlon = 195, resolution = "h")
	map.drawparallels(np.arange(-15., 85., 15.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 15.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12, 180, 1680)
	y1 = np.linspace(-11, 81.89,  916)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	plt.title(iTitle, fontsize = 12)
	plt.text(197, 88, iUnit, fontsize = 8)
	plt.savefig(iFilePath2, dpi = 330)

def drawRisk(iFilePath1, iCmap, iTitle, iUnit, iFilePath2):
	data1 = gdal.Open(iFilePath1)
	data2 = data1.ReadAsArray()
	data3 = np.full((856, 1679), np.nan)
	for row in range(0,  856):
		for column in range(0, 1679):
			if data2[855 - row, column] != -3.4028234663852886e+38:
				data3[row, column] = data2[855 - row, column]
	fig = plt.figure(figsize = (8, 4.5), dpi = 330)
	map = Basemap(llcrnrlat = -15, urcrnrlat = 85, llcrnrlon = 10, urcrnrlon = 195, resolution = "h")
	map.drawparallels(np.arange(-15., 85., 15.), labels = [1, 0, 0, 0], color = "None", fontsize = 8)
	map.drawmeridians(np.arange(10., 180., 15.), labels = [0, 0, 0, 1], color = "None", fontsize = 8)
	map.readshapefile("I:\\1_heatwave\\data\\0base\\countries", "countries")
	map.drawlsmask()
	x1 = np.linspace(12.09, 180, 1679)
	y1 = np.linspace(-11, 75,  856)
	x2, y2 = np.meshgrid(x1, y1)
	x3, y3 = map(x2, y2)
	data4 = map.pcolor(x3, y3, np.squeeze(data3), cmap = iCmap)
	clobar = map.colorbar(data4, location = "right", size = "2%", pad = "1%")
	clobar.ax.tick_params(labelsize = 8)
	plt.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.95, top = 0.99)
	plt.title(iTitle, fontsize = 12)
	plt.text(197, 88, iUnit, fontsize = 8)
	plt.savefig(iFilePath2, dpi = 330)


def main():
# 绘制监测站
	iDirPath1 = r"H:\1_heatwave\data\0base"
	iField1 = "stations.csv"
	iFilePath1 = os.path.join(iDirPath1, iField1)
	iColor = None
	iLegend = "monitoring station"
	iTitle = "Monitoring station of OBOR"
	iUnit = ""
	iDirPath2 = r"H:\1_heatwave\reverse\Figure"
	iNumber = 1
	iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + "1015.png")
	drawShp(iFilePath1, iColor, iLegend, iTitle, iUnit, iFilePath2)

# 绘制医院
	# iDirPath1 = "I:\\1_heatwave\\assessment\\source\\BRI_hospital"
	# iField1 = "BRI_hospital.csv"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iColor = "red"
	# iLegend = "hospital"
	# iTitle = "Hospital of OBOR"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 2
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawShp(iFilePath1, iColor, iLegend, iTitle, iUnit, iFilePath2)

# 绘制体感温度
	# iDirPath1 = "I:\\1_heatwave\\data\\16statistics_temp\\All"
	# iField1 = "winterAll_avg.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Mean apparent temperature of winter over 30 years"
	# iUnit = "℃"
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 6
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制体感温度斜率
	# iDirPath1 = "I:\\1_heatwave\\data\\16statistics_temp\\Slope"
	# iField1 = "winter_slope.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Slope of mean apparent temperature in winter over 30 years"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 10
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制热浪
	# iDirPath1 = "I:\\1_heatwave\\data\\17statistics_heatwave\\mean_2"
	# iField1 = "end_mean.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Annual average HWED (ARTT = 80, ATT = 29, DT = 3)"
	# iUnit = "day"
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 40
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)


# 绘制热浪斜率
	# iDirPath1 = "I:\\1_heatwave\\data\\17statistics_heatwave\\Slope_2"
	# iField1 = "end_slope.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Slope of HWED over 30 years (ARTT = 80, ATT = 29, DT = 3)"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 46
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制俄罗斯热浪
	# iDirPath1 = "I:\\1_heatwave\\data\\15HW_YPT_HTEMPX_80_29"
	# iField1 = "2010_end.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iFilePath2 = "I:\\1_heatwave\\data\\0base\\cities.csv"
	# iCmap = cmaps.GMT_panoply
	# iTitle = "HWED of Russia in 2010 (ARTT = 80, ATT = 29, DT = 3)"
	# iUnit = "day"
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 28
	# iFilePath3 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRussia1(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3)

	# iDirPath1 = "I:\\1_heatwave\\compare2\\data"
	# iField1 = "Last_HW_DOY_2010.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iFilePath2 = "I:\\1_heatwave\\data\\0base\\cities.csv"
	# iCmap = cmaps.GMT_panoply
	# iTitle = "HWED of Russia in 2010 (Raei et al. (2018))"
	# iUnit = "day"
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 34
	# iFilePath3 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRussia2(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3)

# 绘制印度热浪
	# iDirPath1 = "I:\\1_heatwave\\data\\15HW_PT_HTEMPX_95"
	# iField1 = "2017_tmax.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iFilePath2 = "I:\\1_heatwave\\data\\0base\\cities.csv"
	# iCmap = "YlOrRd"
	# iTitle = "HWMAT of India in 2017"
	# iUnit = "℃"
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 23
	# iFilePath3 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawIndia(iFilePath1, iFilePath2, iCmap, iTitle, iUnit, iFilePath3)

# # 绘制危险性
# 	iDirPath1 = "I:\\1_heatwave\\assessment\\result"
# 	iField1 = "hazard_4.tif"
# 	iFilePath1 = os.path.join(iDirPath1, iField1)
# 	iCmap = cmaps.GMT_panoply
# 	iTitle = "Heat wave hazard"
# 	iUnit = ""
# 	iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
# 	iNumber = 47
# 	iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
# 	drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制暴露度
	# iDirPath1 = "I:\\1_heatwave\\assessment\\result"
	# iField1 = "exposure_5.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Heat wave exposure"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 48
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawExposure(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# # 绘制脆弱性
# 	iDirPath1 = "I:\\1_heatwave\\assessment\\result"
# 	iField1 = "vulnerability_4.tif"
# 	iFilePath1 = os.path.join(iDirPath1, iField1)
# 	iCmap = cmaps.GMT_panoply
# 	iTitle = "Heat wave vulnerability"
# 	iUnit = ""
# 	iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
# 	iNumber = 62
# 	iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
# 	drawVulneraility(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制风险
	# iDirPath1 = "I:\\1_heatwave\\assessment\\result"
	# iField1 = "risk_3.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Heat wave risk"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 63
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRisk(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制斜率
	# iDirPath1 = "I:\\1_heatwave\\data\\16statistics_temp\\Tend"
	# iField1 = "fall_tend.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Slope of HWED over 30 years (ARTT = 80, ATT = 29, DT = 3)"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 52
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制体感温度斜率
	# iDirPath1 = "I:\\1_heatwave\\data\\16statistics_temp\\Tend"
	# iField1 = "winter_tend_significant.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Slope of mean apparent temperature in winter over 30 years"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 55
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

# 绘制热浪斜率
	# iDirPath1 = "I:\\1_heatwave\\data\\17statistics_heatwave\\Tend"
	# iField1 = "dmax_tend_significant1.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Slope of HWMD over 30 years (ARTT = 80, ATT = 29, DT = 3)"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 58
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)


	# iDirPath1 = "I:\\1_heatwave\\data\\16statistics_temp\\check"
	# iField1 = "variance_mean_1.tif"
	# iFilePath1 = os.path.join(iDirPath1, iField1)
	# iCmap = cmaps.GMT_panoply
	# iTitle = "Uncertainty map of interpolation"
	# iUnit = ""
	# iDirPath2 = "I:\\1_heatwave\\reverse\\Figure"
	# iNumber = 65
	# iFilePath2 = os.path.join(iDirPath2, str(iNumber) + iTitle + ".png")
	# drawRaster(iFilePath1, iCmap, iTitle, iUnit, iFilePath2)

main()