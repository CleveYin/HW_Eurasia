import xlwt
import pandas
import numpy
import datetime
import shutil
import os
import math
# import arcpy
# from arcpy.sa import *
import gdal, ogr, os, osr
import datetime
# arcpy.CheckOutExtension("Spatial")
from collections import Counter
# from scipy import stats

# import os
# import arcpy
# from arcpy.sa import *
# arcpy.CheckOutExtension("Spatial")

def ArrayToRaster(dataArray, filePath1):
	rasterOrigin = (12.093704000000002, 81.87)
	NoData_value = -3.4028234663852886e+38
	cols = dataArray.shape[1]
	rows = dataArray.shape[0]
	originX = rasterOrigin[0]
	originY = rasterOrigin[1]
	pixelWidth = 0.1
	pixelHeight = -0.1
	driver = gdal.GetDriverByName('GTiff')
	outRaster = driver.Create(filePath1, cols, rows, 1, gdal.GDT_Float32)
	outRaster.SetGeoTransform([originX, pixelWidth, 0, originY, 0.0, pixelHeight])
	outband = outRaster.GetRasterBand(1)
	outband.WriteArray(dataArray)
	outband.SetNoDataValue(NoData_value)				
	outRasterSRS = osr.SpatialReference()
	outRasterSRS.ImportFromEPSG(4326)
	outRaster.SetProjection(outRasterSRS.ExportToWkt())
	outband.FlushCache()


def CalTemp(dirPath1, field1, field2):
	raster_0 = Raster("F:\\1_paper_heat wave\\data\\14HTEMPX\\1989\\19890101.tif")
	springAll_sum = raster_0
	summerAll_sum = raster_0
	fallAll_sum = raster_0
	winterAll_sum = raster_0
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		springYear_sum = raster_0
		summerYear_sum = raster_0
		fallYear_sum = raster_0
		winterYear_sum = raster_0
		springYear_len = 0
		summerYear_len = 0
		fallYear_len = 0
		winterYear_len = 0
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				if filename[-4: ] == ".tif" and filename[4: 6] in ["03", "04", "05"]:
					springYear_sum = springYear_sum + Raster(filePath1)
					springYear_len = springYear_len + 1
				elif filename[-4: ] == ".tif" and filename[4: 6] in ["06", "07", "08"]:
					summerYear_sum = summerYear_sum + Raster(filePath1)
					summerYear_len = summerYear_len + 1
				elif filename[-4: ] == ".tif" and filename[4: 6] in ["09", "10", "11"]:
					fallYear_sum = fallYear_sum + Raster(filePath1)
					fallYear_len = fallYear_len + 1
				elif filename[-4: ] == ".tif" and filename[4: 6] in ["12", "01", "02"]:
					winterYear_sum = winterYear_sum + Raster(filePath1)
					winterYear_len = winterYear_len + 1
		springYear_sum = springYear_sum - raster_0
		summerYear_sum = summerYear_sum - raster_0
		fallYear_sum = fallYear_sum - raster_0
		winterYear_sum = winterYear_sum - raster_0
		springYear_avg = springYear_sum / springYear_len
		summerYear_avg = summerYear_sum / summerYear_len
		fallYear_avg = fallYear_sum / fallYear_len
		winterYear_avg = winterYear_sum / winterYear_len
		dirPath3 = dirPath1.replace(field1, field2, 1)
		springYear_avg.save(os.path.join(dirPath3, "spring" + str(index1) + "_avg.tif"))
		summerYear_avg.save(os.path.join(dirPath3, "summer" + str(index1) + "_avg.tif"))
		fallYear_avg.save(os.path.join(dirPath3, "fall" + str(index1) + "_avg.tif"))
		winterYear_avg.save(os.path.join(dirPath3, "winter" + str(index1) + "_avg.tif"))		
		springAll_sum = springAll_sum + springYear_avg
		summerAll_sum = summerAll_sum + summerYear_avg
		fallAll_sum = fallAll_sum + fallYear_avg
		winterAll_sum = winterAll_sum + winterYear_avg
		print(str(index1) + " is done!")
	springAll_sum = springAll_sum - raster_0
	summerAll_sum = summerAll_sum - raster_0
	fallAll_sum = fallAll_sum - raster_0
	winterAll_sum = winterAll_sum -  raster_0
	springAll_avg = springAll_sum / 30
	summerAll_avg = summerAll_sum / 30
	fallAll_avg = fallAll_sum / 30
	winterAll_avg = winterAll_sum / 30
	# dirPath3 = dirPath1.replace(field1, field2, 1)
	# springAll_avg.save(os.path.join(dirPath3, "springAll_avg.tif"))
	# summerAll_avg.save(os.path.join(dirPath3, "summerAll_avg.tif"))
	# fallAll_avg.save(os.path.join(dirPath3, "fallAll_avg.tif"))
	# winterAll_avg.save(os.path.join(dirPath3, "winterAll_avg.tif"))

def CalSlope(dirPath1, field1):
	for dirPath, dirname, filenames in os.walk(dirPath1):
		tifFilenames = []
		for filename in filenames:
			if filename[-4: ] == ".tif" and field1 in filename:
				tifFilenames.append(filename)	
		data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
		index1 = 0
		print(tifFilenames)
		for tifFilename in tifFilenames:
			filePath1 = os.path.join(dirPath1, tifFilename)
			raster_data = gdal.Open(filePath1)
			raster_value = raster_data.ReadAsArray()
			data_3d[index1, :, :] = raster_value
			index1 = index1 + 1
		slopeArray = numpy.full((929, 1783), -3.4028234663852886e+38)
		varianceArray = numpy.full((929, 1783), -3.4028234663852886e+38)
		for index2 in range(0, 929):
			for index3 in range(0, 1783):
				allDataList = data_3d[:, index2, index3].tolist()
				if -3.4028234663852886e+38 not in allDataList:
					x = numpy.array(range(1989, 2019))
					y = numpy.array(allDataList)
					numerator = 0
					denominator = 0
					x_mean = numpy.mean(x)
					y_mean = numpy.mean(y)
					variance_sum = 0
					for index4 in range(0, len(x)):
						numerator = numerator + (x[index4] - x_mean) * (y[index4] - y_mean)
						denominator = denominator + numpy.square(x[index4] - x_mean)
						variance_sum = variance_sum + numpy.power((y[index4] - y_mean), 2)
					slope = numerator / denominator
					variance = variance_sum / len(x)
					slopeArray[index2, index3] = slope
					varianceArray[index2, index3] = variance
		dirPath2 = dirPath1.replace("15HW_YPT_HTEMPX_80_29", "17statistics_heatwave", 1)
		filePath2 = os.path.join(dirPath2, field1 + "_slope.tif")
		filePath3 = os.path.join(dirPath2, field1 + "_variance.tif")		
		ArrayToRaster(slopeArray, filePath2)
		ArrayToRaster(varianceArray, filePath3)
	print(field1 + " is done!")

# ?????
def CalHeatwave(iAttribute, dirPath1, dirPath2):
	raster_0 = Raster(os.path.join(dirPath1, "1989_" + iAttribute + ".tif"))
	raster_sum = raster_0
	for dirPath, dirname, filenames in os.walk(dirPath1):
		for filename in filenames:
			if filename[-4: ] == ".tif" and iAttribute in filename:
				print(os.path.join(dirPath1, filename))
				raster = Raster(os.path.join(dirPath1, filename))
				raster_sum = raster_sum + raster
	raster_sum = raster_sum - raster_0
	raster_mean = raster_sum / 30
	raster_sum.save(os.path.join(dirPath2, iAttribute + "_sum.tif"))
	raster_mean.save(os.path.join(dirPath2, iAttribute + "_mean.tif"))


def CalMean(dirPath2):
	for dirPath, dirname, filenames in os.walk(dirPath2):
		tifFilenames = []
		for filename in filenames:
			if filename[-4: ] == ".tif":
				tifFilenames.append(filename)		
		data_3d = numpy.full((len(tifFilenames), 929, 1783), -3.4028234663852886e+38)
		index = 0
		for tifFilename in tifFilenames:
			filePath1 = os.path.join(dirPath2, tifFilename)
			raster_data = gdal.Open(filePath1)
			raster_value = raster_data.ReadAsArray()
			data_3d[index, :, :] = raster_value
			index = index + 1
		meanArray = numpy.full((929, 1783), -3.4028234663852886e+38)
		for index2 in range(0, 929):
			for index3 in range(0, 1783):
				allDataArray = data_3d[:, index2, index3]
				meanArray[index2, index3] = numpy.mean(allDataArray)
		filePath2 = "F:\\1_paper_heat wave\\data\\16statistics_temp\\check\\variance_mean.tif"
		ArrayToRaster(meanArray, filePath2)

	# for index1 in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index1))
	# 	for dirPath, dirname, filenames in os.walk(dirPath2):
	# 		tifFilenames = []
	# 		for filename in filenames:
	# 			if filename[-4: ] == ".tif":
	# 				tifFilenames.append(filename)		
	# 		data_3d = numpy.full((len(tifFilenames), 929, 1783), -3.4028234663852886e+38)
	# 		index = 0
	# 		for tifFilename in tifFilenames:
	# 			filePath1 = os.path.join(dirPath2, tifFilename)
	# 			raster_data = gdal.Open(filePath1)
	# 			raster_value = raster_data.ReadAsArray()
	# 			data_3d[index, :, :] = raster_value
	# 			index = index + 1
	# 		meanArray = numpy.full((929, 1783), -3.4028234663852886e+38)
	# 		for index2 in range(0, 929):
	# 			for index3 in range(0, 1783):
	# 				allDataArray = data_3d[:, index2, index3]
	# 				meanArray[index2, index3] = numpy.mean(allDataArray)
	# 		filePath2 = "F:\\1_paper_heat wave\\data\\16statistics_temp\\check\\year\\variance_mean_" + str(index1) + ".tif"
	# 		ArrayToRaster(meanArray, filePath2)
	# 	print(str(index1) + " is done!")


	# raster_0 = Raster("F:\\1_paper_heat wave\\data\\23variance\\1989\\19890101.tif")
	# raster_sum = raster_0
	# for index1 in range(1989, 1994):
	# 	length = 0
	# 	dirPath2 = os.path.join(dirPath1, str(index1))
	# 	for dirPath, dirname, filenames in os.walk(dirPath2):
	# 		for filename in filenames:
	# 			if filename[-4: ] == ".tif":
	# 				print(os.path.join(dirPath2, filename))
	# 				raster = Raster(os.path.join(dirPath2, filename))
	# 				raster_sum = raster_sum + raster
	# 				length = length + 1
	# 	print(str(index1) + " is done!")
	# raster_sum = raster_sum - raster_0
	# raster_mean = raster_sum / length
	# # raster_sum.save("F:\\1_paper_heat wave\\data\\16statistics_temp\\check\\variance_sum_1.tif")
	# raster_mean.save("F:\\1_paper_heat wave\\data\\16statistics_temp\\check\\year\\variance_mean_1.tif")


def main():
	# dirPath1 = "F:\\1_paper_heat wave\\data\\18statistics_6\\source"
	# attribute1 = "0701.t"
	# statistics1(dirPath1, attribute1)
	# attribute1 = "0901.t"
	# statistics1(dirPath1, attribute1)
	# attribute1 = "1101.t"
	# statistics1(dirPath1, attribute1)
	# attribute1 = "end"
	# statistics1(dirPath1, attribute1)
	# attribute1 = "tmax"
	# statistics1(dirPath1, attribute1)
	# attribute1 = "dmax"
	# statistics1(dirPath1, attribute1)

	# dirPath1 = "F:\\1_paper_heat wave\\data\\14HTEMPX"
	# field1 = "14HTEMPX"
	# field2 = "16statistics_temp"
	# CalTemp(dirPath1, field1, field2)

	# dirPath1 = "F:\\1_paper_heat wave\\data\\16statistics_temp\\Year"
	# season = "spring"
	# CalSlope(dirPath1, season)
	# season = "summer"
	# CalSlope(dirPath1, season)	
	# season = "fall"
	# CalSlope(dirPath1, season)
	# season = "winter"
	# CalSlope(dirPath1, season)

	# iAttribute = "end"
	# dirPath1 = "F:\\1_paper_heat wave\\data\\15HW_YPT_HTEMPX_80_29"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\17statistics_heatwave"
	# CalHeatwave(iAttribute, dirPath1, dirPath2)

	# dirPath1 = "F:\\1_paper_heat wave\\data\\15HW_YPT_HTEMPX_80_29"
	# attribute1 = "freq"
	# CalSlope(dirPath1, attribute1)
	# attribute1 = "dura"
	# CalSlope(dirPath1, attribute1)	
	# attribute1 = "dmax"
	# CalSlope(dirPath1, attribute1)	
	# attribute1 = "tmax"
	# CalSlope(dirPath1, attribute1)	
	# attribute1 = "start"
	# CalSlope(dirPath1, attribute1)	
	# attribute1 = "end"
	# CalSlope(dirPath1, attribute1)	

	# iAttribute = "ARTT"
	# dirPath1 = "F:\\1_paper_heat wave\\data\\14ARTT_80\\Year"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\14ARTT_80"
	# CalHeatwave(iAttribute, dirPath1, dirPath2)

	dirPath1 = "F:\\1_paper_heat wave\\data\\16statistics_temp\\check\\year"
	CalMean(dirPath1)

main()
