import os
import xlwt
import pandas
import numpy
import datetime
import shutil
import math
import datetime
from collections import Counter
from scipy import stats
import random

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

# import gdal, ogr, os, osr

# 创建文件夹
def CreateDir(dirPath):
	if os.path.exists(dirPath):
		pass
	else:
		os.makedirs(dirPath)
	return dirPath

# 选择需要用的文件
def SelectFiles(filePath, dirPath1):
	data = pandas.DataFrame(pandas.read_csv(filePath))
	stationList1 = data["ID"]
	stationList2 = []
	for station in stationList1:
		stationList2.append(str(station))
	for index in range(2016, 2020):
		dirPath2 = os.path.join(dirPath1, str(index))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				if filename[0: 6] in stationList2:
					filePath1 = os.path.join(dirPath2, filename)
					filePath2 = filePath1.replace("1download", "2select", 1)
					shutil.copy(filePath1, filePath2)
		print(str(index) + " is done!")

# 将txt格式转换为csv格式
def TxtToCSV(dirPath1):
	for index in range(2016, 2020):
		dirPath2 = os.path.join(dirPath1, str(index))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				filePath2 = filePath1.replace("3unpack", "4XLS", 1).replace(".op", ".xls", 1)
				filePath3 = filePath1.replace("3unpack", "5CSV", 1).replace(".op", ".csv", 1)
				f = open(filePath1, encoding = "gbk", errors = "ignore")
				table1 = xlwt.Workbook()
				sheet = table1.add_sheet("sheet1", cell_overwrite_ok = True)
				x = 0
				while True:
					line = f.readline()
					if not line:
						break
					sheet.write(x, 0, line[0: 6])
					sheet.write(x, 1, line[7: 12])
					sheet.write(x, 2, line[14: 18])
					sheet.write(x, 3, line[18: 22])
					sheet.write(x, 4, line[14: 22])		
					sheet.write(x, 5, line[24: 30])
					sheet.write(x, 6, line[31: 33])
					sheet.write(x, 7, line[35: 41])
					sheet.write(x, 8, line[42: 44])
					sheet.write(x, 9, line[46: 52])
					sheet.write(x, 10, line[53: 55])
					sheet.write(x, 11, line[57: 63])
					sheet.write(x, 12, line[64: 66])
					sheet.write(x, 13, line[68: 73])
					sheet.write(x, 14, line[74: 76])
					sheet.write(x, 15, line[78: 83])
					sheet.write(x, 16, line[84: 86])
					sheet.write(x, 17, line[88: 93])
					sheet.write(x, 18, line[95: 100])
					sheet.write(x, 19, line[102: 108])
					sheet.write(x, 20, line[108: 109])		
					sheet.write(x, 21, line[110: 116])		
					sheet.write(x, 22, line[116: 117])		
					sheet.write(x, 23, line[118: 123])		
					sheet.write(x, 24, line[123: 124])		
					sheet.write(x, 25, line[125: 130])		
					sheet.write(x, 26, line[132: 138])		
					x += 1
				f.close()
				table1.save(filePath2)
				table2 = pandas.DataFrame(pandas.read_excel(filePath2))
				table2.columns = ["STN---", "WBAN", "YEAR", "MODA", "YEARMODA", "TEMP", "NTEMP", \
					"DEWP", "NDEWP", "SLP", "NSLP", "STP", "NSTP", "VISIB", "NVISIB", "WDSP", "NWDSP", "MXSPD", "GUST", "MAX", "TMAX", \
					"MIN", "TMIN", "PRCP", "TPRCP", "SNDP", "FRSHTT"]
				table2.to_csv(filePath3, index = False)
		print(str(index) + " is done!")

# 缺失值处理
def RMissingPro(dirPath1):
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				filePath2 = filePath1.replace("5CSV", "6null", 1)
				table1 = pandas.DataFrame(pandas.read_csv(filePath1))
				table1.replace(9999.9, "NA", inplace = True)
				table1.replace(999.9, "NA", inplace = True)
				table1.replace(99.99, "NA", inplace = True)
				table1.drop(["WBAN", "YEAR", "MODA", "NTEMP", "NDEWP", "SLP", "NSLP", "STP", "NSTP", "VISIB", \
					"NVISIB", "NWDSP", "MXSPD", "GUST", "TMAX", "TMIN", "TPRCP", "SNDP", "FRSHTT"], axis = 1, inplace = True)
				table1.to_csv(filePath2, index = False)
		print(str(index1) + " is done!")

# 计算体感温度
def Calculate(filePath1, dirPath1):
	table1 = pandas.DataFrame(pandas.read_csv(filePath1))
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath2 = os.path.join(dirPath2, filename)
				filePath3 = filePath2.replace("7null", "8AT", 1)
				table2 = pandas.DataFrame(pandas.read_csv(filePath2))
				columnList = list(table2)
				if "DEWP" in columnList and "TEMP" in columnList and "MAX" in columnList and "MIN" in columnList and "WDSP" in columnList:
					DewpList = table2["DEWP"]				
					TempList = table2["TEMP"]
					MaxList = table2["MAX"]
					MinList = table2["MIN"]
					WdspList = table2["WDSP"]
					HTempList = []
					HMaxList = []
					HMinList = []
					ATempList = []
					AMaxList = []
					AMinList = []
					CTempList = []
					CMaxList = []
					CMinList = []
					for index2 in range(len(table2)):
						DEWP = 5 / 9 * (DewpList[index2] -32)
						CTEMP = 5 / 9 * (TempList[index2] -32)
						CMAX = 5 / 9 * (MaxList[index2] -32)
						CMIN = 5 / 9 * (MinList[index2] -32)
						WDSP = WdspList[index2]
						HTEMP = CTEMP + 0.5555 * (6.11 * math.exp(5417.753 * ((1 / 273.16) - (1 / (DEWP +273.16)))) - 10)
						HMAX = CMAX + 0.5555 * (6.11 * math.exp(5417.753 * ((1 / 273.16) - (1 / (DEWP +273.16)))) - 10)
						HMIN = CMIN + 0.5555 * (6.11 * math.exp(5417.753 * ((1 / 273.16) - (1 / (DEWP +273.16)))) - 10)
						UTEMP = (DEWP + 19.2 - 0.8400 * CTEMP) / (0.1980 + 0.0017 * CTEMP)
						ETEMP = UTEMP / 100 * 6.105 * math.exp(17.27 * CTEMP / (237.7 + CTEMP))
						ATEMP = 1.07 * CTEMP + 0.2 * ETEMP - 0.65 * WDSP -2.7
						UAMX = (DEWP + 19.2 - 0.8400 * CMAX) / (0.1980 + 0.0017 * CMAX)
						EMAX = UAMX / 100 * 6.105 * math.exp(17.27 * CMAX / (237.7 + CMAX))
						AMAX = 1.07 * CMAX + 0.2 * EMAX - 0.65 * WDSP -2.7
						UMIN = (DEWP + 19.2 - 0.8400 * CMIN) / (0.1980 + 0.0017 * CMIN)
						EMIN = UMIN / 100 * 6.105 * math.exp(17.27 * CMIN / (237.7 + CMIN))
						AMIN = 1.07 * CMIN + 0.2 * EMIN - 0.65 * WDSP -2.7
						HTempList.append(HTEMP)
						HMaxList.append(HMAX)
						HMinList.append(HMIN)
						ATempList.append(ATEMP)
						AMaxList.append(AMAX)
						AMinList.append(AMIN)
						CTempList.append(CTEMP)
						CMaxList.append(CMAX)
						CMinList.append(CMIN)
					HTempSeries = pandas.Series(HTempList)
					HMaxSeries = pandas.Series(HMaxList)
					HMinSeries = pandas.Series(HMinList)
					ATempSeries = pandas.Series(ATempList)
					AMaxSeries = pandas.Series(AMaxList)
					AMinSeries = pandas.Series(AMinList)
					CTempSeries = pandas.Series(CTempList)
					CMaxSeries = pandas.Series(CMaxList)
					CMinSeries = pandas.Series(CMinList)
					table2.insert(3, "HTEMP", HTempSeries)
					table2.insert(4, "HMAX", HMaxSeries)
					table2.insert(5, "HMIN", HMinSeries)
					table2.insert(6, "ATEMP", ATempSeries)
					table2.insert(7, "AMAX", AMaxSeries)
					table2.insert(8, "AMIN", AMinSeries)
					table2.insert(9, "CTEMP", CTempSeries)
					table2.insert(10, "CMAX", CMaxSeries)
					table2.insert(11, "CMIN", CMinSeries)				
					stationList = table2["STN..."]
					latitudeList = []
					longitudeList = []
					elevationList = []
					tag = 0
					for index3 in range(len(stationList)):
						station1 = stationList[index3]
						for index4 in range(tag, len(table1)):
							station2 = table1["ID"][index4]
							if station1 == station2:
								latitudeList.append(table1["LATITUDE"][index4])
								longitudeList.append(table1["LONGITUDE"][index4])
								elevationList.append(table1["ELEVATION"][index4])
								tag = index4
								break
					LATITUDE = pandas.Series(latitudeList)
					LONGITUDE = pandas.Series(longitudeList)
					ELEVATION = pandas.Series(elevationList)
					table2.insert(2, "LATITUDE", LATITUDE)
					table2.insert(3, "LONGITUDE", LONGITUDE)
					table2.insert(4, "ELEVATION", ELEVATION)
					table2.to_csv(filePath3, index = False)
		print(str(index1) + " is done!")

# 插值前准备：将温度修正到零平面
def Correct(dirPath1):
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				filePath2 = filePath1.replace("8AT", "9XT", 1)
				table1 = pandas.DataFrame(pandas.read_csv(filePath1))
				HTempList = table1["HTEMP"]
				HMaxList = table1["HMAX"]
				HMinList = table1["HMIN"]
				ATempList = table1["ATEMP"]
				AMaxList = table1["AMAX"]
				AMinList = table1["AMIN"]
				CTempList = table1["CTEMP"]
				CMaxList = table1["CMAX"]
				CMinList = table1["CMIN"]
				ElevationList = table1["ELEVATION"]
				HTempXList = []
				HMaxXList = []
				HMinXList = []
				ATempXList = []
				AMaxXList = []
				AMinXList = []
				CTempXList = []
				CMaxXList = []
				CMinXList = []
				for index in range(len(table1)):
					ELEVATION = ElevationList[index]
					HTEMPX = HTempList[index] + 0.0065 * ELEVATION
					HMAXX = HMaxList[index] + 0.0065 * ELEVATION
					HMINX = HMinList[index] + 0.0065 * ELEVATION
					ATEMPX = ATempList[index] + 0.0065 * ELEVATION
					AMAXX = AMaxList[index] + 0.0065 * ELEVATION
					AMINX = AMinList[index] + 0.0065 * ELEVATION
					CTEMPX = CTempList[index] + 0.0065 * ELEVATION
					CMAXX = CMaxList[index] + 0.0065 * ELEVATION
					CMINX = CMinList[index] + 0.0065 * ELEVATION
					HTempXList.append(HTEMPX)
					HMaxXList.append(HMAXX)
					HMinXList.append(HMINX)
					ATempXList.append(ATEMPX)
					AMaxXList.append(AMAXX)
					AMinXList.append(AMINX)
					CTempXList.append(CTEMPX)
					CMaxXList.append(CMAXX)
					CMinXList.append(CMINX)
				HTempXSeries = pandas.Series(HTempXList)
				HMaxXSeries = pandas.Series(HMaxXList)
				HMinXSeries = pandas.Series(HMinXList)
				ATempXSeries = pandas.Series(ATempXList)
				AMaxXSeries = pandas.Series(AMaxXList)
				AMinXSeries = pandas.Series(AMinXList)
				CTempXSeries = pandas.Series(CTempXList)
				CMaxXSeries = pandas.Series(CMaxXList)
				CMinXSeries = pandas.Series(CMinXList)
				table1.insert(6, "HTEMPX", HTempXSeries)
				table1.insert(7, "HMAXX", HMaxXSeries)
				table1.insert(8, "HMINX", HMinXSeries)
				table1.insert(9, "ATEMPX", ATempXSeries)
				table1.insert(10, "AMAXX", AMaxXSeries)
				table1.insert(11, "AMINX", AMinXSeries)
				table1.insert(12, "CTEMPX", CTempXSeries)
				table1.insert(13, "CMAXX", CMaxXSeries)
				table1.insert(14, "CMINX", CMinXSeries)					
				table1.to_csv(filePath2, index = False)
		print(str(index1) + " is done!")

# 文件合并
def MergeFile(dirPath1):
	for index in range(1989, 2019):
		table1 = pandas.DataFrame()
		dirPath2 = os.path.join(dirPath1, str(index))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)	
				table2 = pandas.DataFrame(pandas.read_csv(filePath1))
				table1 = pandas.concat([table1, table2], sort = False)
		filePath2 = os.path.dirname(dirPath2).replace("9XT", "10merge", 1) + "\\" + str(index) + ".csv"
		table1 = table1.sort_values("YEARMODA")
		table1.to_csv(filePath2, index = False)
		print(str(index) + " is done!")

# 插值前准备：将文件拆分为每日文件
def DailyData(dirPath1):
	for dirPath, dirname, filenames in os.walk(dirPath1):
		for filename in filenames:
			filePath1 = os.path.join(dirPath1, filename)			
			table1 = pandas.DataFrame(pandas.read_csv(filePath1))
			year = filePath1[-8: -4]
			dateList = table1["YEARMODA"].unique()
			table2 = pandas.DataFrame()
			DATE = pandas.Series(dateList)
			table2.insert(0, "DATE", DATE)
			filePath2 = "F:\\1_paper_heat wave\\data\\12check\\" + year + ".csv"
			table2.to_csv(filePath2)
			for date in dateList:
				filePath3 = dirPath1.replace("10merge", "11daily", 1) + "\\" + str(year) + "\\" + str(date) + ".csv"
				table3 = table1[table1["YEARMODA"].isin([date])]
				table3.to_csv(filePath3, index = False)
			print(str(year) + " is done!")	

# 插值前准备：文本数据空间化
def CsvToLayer(dirPath1):
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		arcpy.env.workspace = dirPath2
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				filePath2 = filePath1.replace("11daily", "13Layer", 1).replace(".csv", ".lyr", 1)
				if os.path.exists(filePath2):
					pass
				else:
					arcpy.MakeXYEventLayer_management(filePath1, "LONGITUDE", "LATITUDE", filename, "F:\\1_paper_heat wave\\data\\0base\\GCS_WGS_1984.prj")
					arcpy.SaveToLayerFile_management(filename, filePath2, "RELATIVE")
		print(str(index1) + " is done!")

# 插值
def PointToRaster(dirPath1, field1):
	for index1 in range(2015, 2016):
		dirPath2 = os.path.join(dirPath1, str(index1))
		arcpy.env.workspace = dirPath2
		extent = "F:\\1_paper_heat wave\\data\\0base\\extent_1.shp"
		arcpy.env.extent = extent
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				if filename[-4: ] == ".lyr":
					filePath1 = os.path.join(dirPath2, filename)
					# filePath2 = filePath1.replace("13layer", "14" + field1 + "_1", 1).replace(".lyr", ".tif", 1)
					# filePath3 = filePath1.replace("13layer", "14" + field1 + "_2", 1).replace(".lyr", ".tif", 1)
					# filePath4 = filePath1.replace("13Layer", "14Raster_2", 1).replace(".lyr", ".tif", 1)
					filePath5 = filePath1.replace("13layer", "25kriging", 1).replace(".lyr", ".tif", 1)				
					filePath6 = filePath1.replace("13layer", "26variance", 1).replace(".lyr", ".tif", 1)
					filePath7 = filePath1.replace("13layer", "27" + field1, 1).replace(".lyr", ".tif", 1)
					if os.path.exists(filePath5):
						print(filePath5, filePath6)
						pass
					else:
						print(filePath5, filePath6)
						raster_kriging = Kriging(filePath1, field1, KrigingModelOrdinary("SPHERICAL", 0.371455), 0.0083333333, RadiusVariable(12), filePath6)
						raster_kriging.save(filePath5)
						# raster_kriging = Kriging(filePath1, field1, KrigingModelOrdinary("SPHERICAL", 0.371455), 0.1)
						# raster_kriging.save(filePath2)
						# raster_extract = ExtractByMask(raster_kriging, extent)
						# raster_extract.save(filePath3)
						raster_correct = Raster(filePath5) - 0.0065 * Raster("F:\\1_paper_heat wave\\data\\0base\\dem_bri.tif")
						raster_correct.save(filePath7)
				else:
					filePath1 = os.path.join(dirPath2, filename)
					os.remove(filePath1)
		print(str(index1) + " is done!")

# 插值模型检验
def CheckInterpolate(dirPath1, field1):
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				filePath2 = filePath1.replace("11daily", "18daily_check", 1)
				if os.path.exists(filePath2):
					pass
				else:
					table1 = pandas.DataFrame(pandas.read_csv(filePath1))
					latitudeList = table1["LATITUDE"]
					longitudeList = table1["LONGITUDE"]
					fieldList = table1[field1]
					sampleIndexList = random.sample(range(0, len(table1)), int(len(table1) * 0.15))
					sampleTable = pandas.DataFrame(columns = ("LATITUDE", "LONGITUDE", field1))
					for sampleIndex in sampleIndexList:
						sampleTable = sampleTable.append(pandas.DataFrame({"LATITUDE": [latitudeList[sampleIndex]], "LONGITUDE": [longitudeList[sampleIndex]], field1: [fieldList[sampleIndex]]}), ignore_index=True)
					sampleTable.to_csv(filePath2)
		print(str(index1) + " is done!")		

# 数组转栅格
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

# 基于固定阈值计算热浪
def HeatWave1(dirPath1, field1, field2, tempTag, durationTag):
	for index1 in range(2017, 2018):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			tifFilenames = []
			for filename in filenames:
				if filename[-4: ] == ".tif":
					tifFilenames.append(filename)		
			data_3d = numpy.zeros(shape = (len(tifFilenames), 929, 1783))
			index = 0
			for tifFilename in tifFilenames:
				filePath1 = os.path.join(dirPath2, tifFilename)
				raster_data = gdal.Open(filePath1)
				raster_value = raster_data.ReadAsArray()
				data_3d[index, :, :] = raster_value
				index = index + 1
			frequencyArray = numpy.zeros(shape = (929, 1783))
			durationArray = numpy.zeros(shape = (929, 1783))
			startDateArray = numpy.zeros(shape = (929, 1783))
			endDateArray = numpy.zeros(shape = (929, 1783))
			meanTempArray = numpy.zeros(shape = (929, 1783))
			minTempArray = numpy.zeros(shape = (929, 1783))
			maxTempArray = numpy.zeros(shape = (929, 1783))
			meanDuraArray = numpy.zeros(shape = (929, 1783))
			minDuraArray = numpy.zeros(shape = (929, 1783))
			maxDuraArray = numpy.zeros(shape = (929, 1783))			
			allDataList = []
			for index2 in range(0, 929):
				for index3 in range(0, 1783):
					if data_3d[0, index2, index3] != -3.4028234663852886e+38:
						allDataList = data_3d[:, index2, index3].tolist()
						hotDataList = []
						for index4 in range(len(allDataList)):
							if allDataList[index4] >= tempTag:
								hot_temp = allDataList[index4]
								hot_date = tifFilenames[index4][0: 8]
								hotDataList.append([hot_temp, hot_date])
						duration1 = 1
						frequency = 0
						totalDuration = 0
						startDateList = []
						endDateList = []	
						meanTempList = []
						minTempList = []
						maxTempList = []	
						durationList = []		
						for index5 in range(0, len(hotDataList) - 1):
							date1 = datetime.datetime.strptime(hotDataList[index5][1], "%Y%m%d")
							date2 = datetime.datetime.strptime(hotDataList[index5 + 1][1], "%Y%m%d")
							if date2 - date1 == numpy.timedelta64(1, "D") and date2 != datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d"):
								duration1 = duration1 + 1
							elif date2 - date1 != numpy.timedelta64(1, "D") or (date2 - date1 == numpy.timedelta64(1, "D") and date2 == datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d")):
								if duration1 >= durationTag:
									startDateString = hotDataList[index5 - (duration1 - 1)][1]
									endDateString = hotDataList[index5][1]
									startDate = datetime.date(int(startDateString[0: 4]), int(startDateString[4: 6]), int(startDateString[6: 8]))
									startDateCount = startDate.strftime("%j")
									endDate = datetime.date(int(endDateString[0: 4]), int(endDateString[4: 6]), int(endDateString[6: 8]))
									endDateCount = endDate.strftime("%j")							    
									tempList = []
									for index6 in range(index5 - (duration1 - 1), index5 + 1):
										tempList.append(hotDataList[index6][0])
									sum1 = 0
									for temp in tempList:
										sum1 = sum1 + temp
									meanTemp1 = sum1 / len(tempList)
									minTemp = min(tempList)
									maxTemp = max(tempList)
									frequency = frequency + 1
									totalDuration = totalDuration + duration1
									startDateList.append(startDateCount)
									endDateList.append(endDateCount)
									meanTempList.append(meanTemp1)
									minTempList.append(minTemp)
									maxTempList.append(maxTemp)
									durationList.append(duration1)
								duration1 = 1
						if frequency == 0:
							totalDuration = -3.4028234663852886e+38
							totalStartDate = -3.4028234663852886e+38
							totalEndDate = -3.4028234663852886e+38
							totalMeanTemp = -3.4028234663852886e+38
							totalMinTemp = -3.4028234663852886e+38
							totalMaxTemp = -3.4028234663852886e+38
							totalMeanDura = -3.4028234663852886e+38
							totalMinDura = -3.4028234663852886e+38
							totalMaxDura = -3.4028234663852886e+38
						else:
							totalStartDate = min(startDateList)
							totalEndDate = max(endDateList)
							sum2 = 0
							for meanTemp2 in meanTempList:
								sum2 = sum2 + meanTemp2
							totalMeanTemp = sum2 / len(meanTempList)
							totalMinTemp = min(minTempList)
							totalMaxTemp = max(maxTempList)	
							sum3 = 0
							for duration2 in durationList:
								sum3 = sum3 + duration2
							totalMeanDura = sum3 / len(durationList)
							totalMinDura = min(durationList)
							totalMaxDura = max(durationList)				
						frequencyArray[index2, index3] = frequency
						durationArray[index2, index3] = totalDuration
						startDateArray[index2, index3] = totalStartDate
						endDateArray[index2, index3] = totalEndDate
						meanTempArray[index2, index3] = totalMeanTemp
						minTempArray[index2, index3] = totalMinTemp
						maxTempArray[index2, index3] = totalMaxTemp
						meanDuraArray[index2, index3] = totalMeanDura
						minDuraArray[index2, index3] = totalMinDura
						maxDuraArray[index2, index3] = totalMaxDura
					if raster_value[index2, index3] == -3.4028234663852886e+38:
						frequencyArray[index2, index3] = -3.4028234663852886e+38
						durationArray[index2, index3] = -3.4028234663852886e+38
						startDateArray[index2, index3] = -3.4028234663852886e+38
						endDateArray[index2, index3] = -3.4028234663852886e+38
						meanTempArray[index2, index3] = -3.4028234663852886e+38
						minTempArray[index2, index3] = -3.4028234663852886e+38
						maxTempArray[index2, index3] = -3.4028234663852886e+38
						meanDuraArray[index2, index3] = -3.4028234663852886e+38
						minDuraArray[index2, index3] = -3.4028234663852886e+38
						maxDuraArray[index2, index3] = -3.4028234663852886e+38						
			dirPath3 = dirPath1.replace(field1, field2, 1)
			filePath2 = os.path.join(dirPath3, str(index1) + "_freq.tif")
			filePath3 = os.path.join(dirPath3, str(index1) + "_dura.tif")
			filePath4 = os.path.join(dirPath3, str(index1) + "_start.tif")
			filePath5 = os.path.join(dirPath3, str(index1) + "_end.tif")
			filePath6 = os.path.join(dirPath3, str(index1) + "_tmean.tif")
			filePath7 = os.path.join(dirPath3, str(index1) + "_tmin.tif")
			filePath8 = os.path.join(dirPath3, str(index1) + "_tmax.tif")
			filePath9 = os.path.join(dirPath3, str(index1) + "_dmean.tif")
			filePath10 = os.path.join(dirPath3, str(index1) + "_dmin.tif")
			filePath11 = os.path.join(dirPath3, str(index1) + "_dmax.tif")
			ArrayToRaster(frequencyArray, filePath2)
			ArrayToRaster(durationArray, filePath3)
			ArrayToRaster(startDateArray, filePath4)
			ArrayToRaster(endDateArray, filePath5)
			ArrayToRaster(meanTempArray, filePath6)
			ArrayToRaster(minTempArray, filePath7)
			ArrayToRaster(maxTempArray, filePath8)
			ArrayToRaster(meanDuraArray, filePath9)
			ArrayToRaster(minDuraArray, filePath10)
			ArrayToRaster(maxDuraArray, filePath11)
		print(str(index1) + " is done!")

# 计算每日平均体感温度
def CalculateTemp1(dirPath1, field1, field2):
	rasterList1 = []
	dateList = []
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				if filename[-4: ] == ".tif":
					rasterList1.append(filePath1)
				if filename[-4: ] == ".tif" and filename[-8: -4] not in dateList:
					dateList.append(filename[-8: -4])
	dateList.sort()
	for date in dateList:
		rasterList2 = []
		for raster1 in rasterList1:
			if raster1[-8: -4] == date:
				rasterList2.append(raster1)
		raster_sum = Raster(rasterList2[0])
		raster_sum = raster_sum - Raster(rasterList2[0])
		for raster2 in rasterList2:
			raster_sum = raster_sum + Raster(raster2)
		raster_mean = raster_sum / len(rasterList2)
		dirPath2 = dirPath1.replace(field1, field2)
		filePath2 = os.path.join(dirPath2, date + ".tif")
		raster_mean.save(filePath2)

# 基于平均体感温度计算热浪
def HeatWave2(dirPath1, dirPath2, field1, field2, percentage1, durationTag):
	for dirPath, dirname, filenames in os.walk(dirPath1):
		tifFilenames = []
		for filename in filenames:
			if filename[-4: ] == ".tif":
				tifFilenames.append(filename)		
		ref_data_3d = numpy.zeros(shape = (len(tifFilenames), 929, 1783))
		index = 0
		dateList1 = []
		for tifFilename in tifFilenames:
			filePath1 = os.path.join(dirPath1, tifFilename)
			raster_data = gdal.Open(filePath1)
			raster_row = raster_data.RasterXSize
			raster_column = raster_data.RasterYSize				
			raster_band = raster_data.GetRasterBand(1)
			raster_value = raster_band.ReadAsArray(0, 0, raster_row, raster_column)
			ref_data_3d[index, :, :] = raster_value
			dateList1.append(tifFilename[-8: -4])
			index = index + 1	
	for index1 in range(1989, 2019):
		dirPath3 = os.path.join(dirPath2, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath3):
			tifFilenames = []
			for filename in filenames:
				if filename[-4: ] == ".tif":
					tifFilenames.append(filename)		
			data_3d = numpy.zeros(shape = (len(tifFilenames), 929, 1783))
			index = 0
			dateList2 = []
			for tifFilename in tifFilenames:
				filePath1 = os.path.join(dirPath3, tifFilename)
				raster_data = gdal.Open(filePath1)
				raster_row = raster_data.RasterXSize
				raster_column = raster_data.RasterYSize				
				raster_band = raster_data.GetRasterBand(1)
				raster_value = raster_band.ReadAsArray(0, 0, raster_row, raster_column)
				data_3d[index, :, :] = raster_value
				dateList2.append(tifFilename[-8: -4])
				index = index + 1
			frequencyArray = numpy.zeros(shape = (929, 1783))
			durationArray = numpy.zeros(shape = (929, 1783))
			startDateArray = numpy.zeros(shape = (929, 1783))
			endDateArray = numpy.zeros(shape = (929, 1783))
			meanTempArray = numpy.zeros(shape = (929, 1783))
			minTempArray = numpy.zeros(shape = (929, 1783))
			maxTempArray = numpy.zeros(shape = (929, 1783))
			meanDuraArray = numpy.zeros(shape = (929, 1783))
			minDuraArray = numpy.zeros(shape = (929, 1783))
			maxDuraArray = numpy.zeros(shape = (929, 1783))			
			allDataList = []
			for index2 in range(0, 929):
				for index3 in range(0, 1783):
					if data_3d[0, index2, index3] > -3.4e+38:
						allDataList = data_3d[:, index2, index3].tolist()
						hotDataList = []
						for index4 in range(len(allDataList)):
							tag = 0
							for index5 in range(tag, len(dateList1)):
								if dateList1[index5] == dateList2[index4]:
									tag = index5
									if allDataList[index4] >= ref_data_3d[index5, index2, index3] * percentage1 / 100:
										hot_temp = allDataList[index4]
										hot_date = tifFilenames[index4][0: 8]
										hotDataList.append([hot_temp, hot_date])
									break
						duration1 = 1
						frequency = 0
						totalDuration = 0
						startDateList = []
						endDateList = []	
						meanTempList = []
						minTempList = []
						maxTempList = []	
						durationList = []			
						for index6 in range(0, len(hotDataList) - 1):
							date1 = datetime.datetime.strptime(hotDataList[index6][1], "%Y%m%d")
							date2 = datetime.datetime.strptime(hotDataList[index6 + 1][1], "%Y%m%d")
							if date2 - date1 == numpy.timedelta64(1, "D"):
								duration1 = duration1 + 1
							else:
								if duration1 >= durationTag:
									startDateString = hotDataList[index6 - (duration1 - 1)][1]
									endDateString = hotDataList[index6][1]
									startDate = datetime.date(int(startDateString[0: 4]), int(startDateString[4: 6]), int(startDateString[6: 8]))
									startDateCount = startDate.strftime("%j")
									endDate = datetime.date(int(endDateString[0: 4]), int(endDateString[4: 6]), int(endDateString[6: 8]))
									endDateCount = endDate.strftime("%j")							    
									tempList = []
									for index7 in range(index6 - (duration1 - 1), index6 + 1):
										tempList.append(hotDataList[index7][0])
									sum1 = 0
									for temp in tempList:
										sum1 = sum1 + temp
									meanTemp1 = sum1 / len(tempList)
									minTemp = min(tempList)
									maxTemp = max(tempList)
									frequency = frequency + 1
									totalDuration = totalDuration + duration1
									startDateList.append(startDateCount)
									endDateList.append(endDateCount)
									meanTempList.append(meanTemp1)
									minTempList.append(minTemp)
									maxTempList.append(maxTemp)
									durationList.append(duration1)
								duration1 = 1
						if frequency == 0:
							totalStartDate = 99999999
							totalEndDate = 99999999
							totalMeanTemp = 99999999
							totalMinTemp = 99999999
							totalMaxTemp = 99999999
							totalMeanDura = 99999999
							totalMinDura = 99999999
							totalMaxDura = 99999999
						else:
							totalStartDate = min(startDateList)
							totalEndDate = max(endDateList)
							sum2 = 0
							for meanTemp2 in meanTempList:
								sum2 = sum2 + meanTemp2
							totalMeanTemp = sum2 / len(meanTempList)
							totalMinTemp = min(minTempList)
							totalMaxTemp = max(maxTempList)	
							sum3 = 0
							for duration2 in durationList:
								sum3 = sum3 + duration2
							totalMeanDura = sum3 / len(durationList)
							totalMinDura = min(durationList)
							totalMaxDura = max(durationList)				
						frequencyArray[index2, index3] = frequency
						durationArray[index2, index3] = totalDuration
						startDateArray[index2, index3] = totalStartDate
						endDateArray[index2, index3] = totalEndDate
						meanTempArray[index2, index3] = totalMeanTemp
						minTempArray[index2, index3] = totalMinTemp
						maxTempArray[index2, index3] = totalMaxTemp
						meanDuraArray[index2, index3] = totalMeanDura
						minDuraArray[index2, index3] = totalMinDura
						maxDuraArray[index2, index3] = totalMaxDura
					if raster_value[index2, index3] < -3.4e+38:
						frequencyArray[index2, index3] = 99999999
						durationArray[index2, index3] = 99999999
						startDateArray[index2, index3] = 99999999
						endDateArray[index2, index3] = 99999999
						meanTempArray[index2, index3] = 99999999
						minTempArray[index2, index3] = 99999999
						maxTempArray[index2, index3] = 99999999
						meanDuraArray[index2, index3] = 99999999
						minDuraArray[index2, index3] = 99999999
						maxDuraArray[index2, index3] = 99999999						
			dirPath4 = dirPath2.replace(field1, field2, 1)
			filePath2 = os.path.join(dirPath4, str(index1) + "_freq.tif")
			filePath3 = os.path.join(dirPath4, str(index1) + "_dura.tif")
			filePath4 = os.path.join(dirPath4, str(index1) + "_start.tif")
			filePath5 = os.path.join(dirPath4, str(index1) + "_end.tif")
			filePath6 = os.path.join(dirPath4, str(index1) + "_tmean.tif")
			filePath7 = os.path.join(dirPath4, str(index1) + "_tmin.tif")
			filePath8 = os.path.join(dirPath4, str(index1) + "_tmax.tif")
			filePath9 = os.path.join(dirPath4, str(index1) + "_dmean.tif")
			filePath10 = os.path.join(dirPath4, str(index1) + "_dmin.tif")
			filePath11 = os.path.join(dirPath4, str(index1) + "_dmax.tif")
			ArrayToRaster(frequencyArray, filePath2)
			ArrayToRaster(durationArray, filePath3)
			ArrayToRaster(startDateArray, filePath4)
			ArrayToRaster(endDateArray, filePath5)
			ArrayToRaster(meanTempArray, filePath6)
			ArrayToRaster(minTempArray, filePath7)
			ArrayToRaster(maxTempArray, filePath8)
			ArrayToRaster(meanDuraArray, filePath9)
			ArrayToRaster(minDuraArray, filePath10)
			ArrayToRaster(maxDuraArray, filePath11)
		print(str(index1) + " is done!")

# 计算每日最频体感温度
def CalculateTemp2(dirPath1, field1, field2):
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			tifFilenames = []
			for filename in filenames:
				if filename[-4: ] == ".tif":
					tifFilenames.append(filename)		
			data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
			index = 0
			for tifFilename in tifFilenames:
				filePath1 = os.path.join(dirPath2, tifFilename)
				raster_data = gdal.Open(filePath1)
				raster_value = raster_data.ReadAsArray()
				data_3d[index, :, :] = raster_value
				index = index + 1
			MFATArray = numpy.full((929, 1783), numpy.nan)
			for row in range(0, 929):
				for column in range(0, 1783):
					dayValueArray = data_3d[:, row, column]
					dayValueArray = dayValueArray.astype(int)
					MFATArray[row][column] = Counter(dayValueArray).most_common(1)[0][0]
					if MFATArray[row][column] != -2147483648:
						print(Counter(dayValueArray).most_common(1)[0], data_3d.shape, row, column)
			dirPath3 = dirPath1.replace(field1, field2, 1)
			filePath2 = os.path.join(dirPath3, str(index1) + ".tif")
			ArrayToRaster(MFATArray, filePath2)
			print(str(index1) + " is done!")

# 计算百分位数体感温度
def CalculateTemp3(dirPath1, percentage1, field1, field2):
	rasterList1 = []
	dateList = []
	for index1 in range(1989, 2019):
		dirPath2 = os.path.join(dirPath1, str(index1))
		for dirPath, dirname, filenames in os.walk(dirPath2):
			for filename in filenames:
				filePath1 = os.path.join(dirPath2, filename)
				if filename[-4: ] == ".tif":
					rasterList1.append(filePath1)
				if filename[-4: ] == ".tif" and filename[-8: -4] not in dateList:
					dateList.append(filename[-8: -4])
	dateList.sort()
	for date in dateList:
		dirPath3 = dirPath1.replace(field1, field2, 1)
		filePath2 = os.path.join(dirPath3, str(date) + ".tif")
		if os.path.exists(filePath2):
			print(str(date) + " is done!")		
		else:		
			rasterList2 = []
			for raster1 in rasterList1:
				if raster1[-8: -4] == date:
					rasterList2.append(raster1)
			data_3d = numpy.full((len(rasterList2), 929, 1783), numpy.nan)
			index = 0
			for raster2 in rasterList2:
				raster_data = gdal.Open(raster2)
				raster_value = raster_data.ReadAsArray()
				data_3d[index, :, :] = raster_value
				index = index + 1
			PercArray = numpy.full((929, 1783), numpy.nan)
			for row in range(0, 929):
				for column in range(0, 1783):
					if data_3d[0, row, column] == -3.4028234663852886e+38:
						pass
					else:
						dayValueArray = data_3d[:, row, column]
						PercArray[row][column] = numpy.percentile(dayValueArray, percentage1)
			ArrayToRaster(PercArray, filePath2)
			print(str(date) + " is done!")		

# 基于百分位体感温度计算热浪
def HeatWave3(dirPath1, dirPath2, field1, field2, percentage1, durationTag):
	for dirPath, dirname, filenames in os.walk(dirPath1):
		tifFilenames = []
		for filename in filenames:
			if filename[-4: ] == ".tif":
				tifFilenames.append(filename)		
		ref_data_3d = numpy.full((len(tifFilenames), 929, 1783), -3.4028234663852886e+38)
		index = 0
		dateList1 = []
		for tifFilename in tifFilenames:
			filePath1 = os.path.join(dirPath1, tifFilename)
			raster_data = gdal.Open(filePath1)			
			raster_value = raster_data.ReadAsArray()
			ref_data_3d[index, :, :] = raster_value
			dateList1.append(tifFilename[-8: -4])
			index = index + 1	
	for index1 in range(1989, 2019):
		dirPath4 = dirPath2.replace(field1, field2, 1)
		filePathDetect = os.path.join(dirPath4, str(index1) + "_freq.tif")
		if os.path.exists(filePathDetect):
			print(str(index1) + " is done!")
		else:
			dirPath3 = os.path.join(dirPath2, str(index1))
			for dirPath, dirname, filenames in os.walk(dirPath3):
				tifFilenames = []
				for filename in filenames:
					if filename[-4: ] == ".tif":
						tifFilenames.append(filename)		
				data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
				index = 0
				dateList2 = []
				for tifFilename in tifFilenames:
					filePath1 = os.path.join(dirPath3, tifFilename)
					raster_data = gdal.Open(filePath1)
					raster_value = raster_data.ReadAsArray()
					data_3d[index, :, :] = raster_value
					index = index + 1
					dateList2.append(tifFilename[-8: -4])
				frequencyArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				durationArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				startDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				endDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)			
				allDataList = []
				for index2 in range(0, 929):
					for index3 in range(0, 1783):
						yearValueArray = data_3d[:, index2, index3]
						tempTag = numpy.percentile(yearValueArray, percentage1)				
						if data_3d[0, index2, index3] != -3.4028234663852886e+38:
							# print(index2, index3, tempTag)
							allDataList = data_3d[:, index2, index3].tolist()
							hotDataList = []
							for index4 in range(len(dateList2)):
								for index_ref in range(index4, len(dateList1)):
									if dateList2[index4] == dateList1[index_ref]:
										if allDataList[index4] >= tempTag and allDataList[index4] >= ref_data_3d[index_ref, index2, index3]:
											hot_temp = allDataList[index4]
											hot_date = tifFilenames[index4][0: 8]
											hotDataList.append([hot_temp, hot_date])
										break
							duration1 = 1
							frequency = 0
							totalDuration = 0
							startDateList = []
							endDateList = []	
							meanTempList = []
							minTempList = []
							maxTempList = []	
							durationList = []		
							for index5 in range(0, len(hotDataList) - 1):
								date1 = datetime.datetime.strptime(hotDataList[index5][1], "%Y%m%d")
								date2 = datetime.datetime.strptime(hotDataList[index5 + 1][1], "%Y%m%d")
								if date2 - date1 == numpy.timedelta64(1, "D") and date2 != datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d"):
									duration1 = duration1 + 1
								elif date2 - date1 != numpy.timedelta64(1, "D") or (date2 - date1 == numpy.timedelta64(1, "D") and date2 == datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d")):
									if duration1 >= durationTag:
										startDateString = hotDataList[index5 - (duration1 - 1)][1]
										endDateString = hotDataList[index5][1]
										startDate = datetime.date(int(startDateString[0: 4]), int(startDateString[4: 6]), int(startDateString[6: 8]))
										startDateCount = startDate.strftime("%j")
										endDate = datetime.date(int(endDateString[0: 4]), int(endDateString[4: 6]), int(endDateString[6: 8]))
										endDateCount = endDate.strftime("%j")							    
										tempList = []
										for index6 in range(index5 - (duration1 - 1), index5 + 1):
											tempList.append(hotDataList[index6][0])
										sum1 = 0
										for temp in tempList:
											sum1 = sum1 + temp
										meanTemp1 = sum1 / len(tempList)
										minTemp = min(tempList)
										maxTemp = max(tempList)
										frequency = frequency + 1
										totalDuration = totalDuration + duration1
										startDateList.append(startDateCount)
										endDateList.append(endDateCount)
										meanTempList.append(meanTemp1)
										minTempList.append(minTemp)
										maxTempList.append(maxTemp)
										durationList.append(duration1)
									duration1 = 1
							if frequency == 0:
								totalDuration = 0
								totalStartDate = -3.4028234663852886e+38
								totalEndDate = -3.4028234663852886e+38
								totalMeanTemp = -3.4028234663852886e+38
								totalMinTemp = -3.4028234663852886e+38
								totalMaxTemp = -3.4028234663852886e+38
								totalMeanDura = 0
								totalMinDura = 0
								totalMaxDura = 0
							else:
								totalStartDate = min(startDateList)
								totalEndDate = max(endDateList)
								sum2 = 0
								for meanTemp2 in meanTempList:
									sum2 = sum2 + meanTemp2
								totalMeanTemp = sum2 / len(meanTempList)
								totalMinTemp = min(minTempList)
								totalMaxTemp = max(maxTempList)	
								sum3 = 0
								for duration2 in durationList:
									sum3 = sum3 + duration2
								totalMeanDura = sum3 / len(durationList)
								totalMinDura = min(durationList)
								totalMaxDura = max(durationList)				
							frequencyArray[index2, index3] = frequency
							durationArray[index2, index3] = totalDuration
							startDateArray[index2, index3] = totalStartDate
							endDateArray[index2, index3] = totalEndDate
							meanTempArray[index2, index3] = totalMeanTemp
							minTempArray[index2, index3] = totalMinTemp
							maxTempArray[index2, index3] = totalMaxTemp
							meanDuraArray[index2, index3] = totalMeanDura
							minDuraArray[index2, index3] = totalMinDura
							maxDuraArray[index2, index3] = totalMaxDura				
				filePath2 = os.path.join(dirPath4, str(index1) + "_freq.tif")
				filePath3 = os.path.join(dirPath4, str(index1) + "_dura.tif")
				filePath4 = os.path.join(dirPath4, str(index1) + "_start.tif")
				filePath5 = os.path.join(dirPath4, str(index1) + "_end.tif")
				filePath6 = os.path.join(dirPath4, str(index1) + "_tmean.tif")
				filePath7 = os.path.join(dirPath4, str(index1) + "_tmin.tif")
				filePath8 = os.path.join(dirPath4, str(index1) + "_tmax.tif")
				filePath9 = os.path.join(dirPath4, str(index1) + "_dmean.tif")
				filePath10 = os.path.join(dirPath4, str(index1) + "_dmin.tif")
				filePath11 = os.path.join(dirPath4, str(index1) + "_dmax.tif")
				ArrayToRaster(frequencyArray, filePath2)
				ArrayToRaster(durationArray, filePath3)
				ArrayToRaster(startDateArray, filePath4)
				ArrayToRaster(endDateArray, filePath5)
				ArrayToRaster(meanTempArray, filePath6)
				ArrayToRaster(minTempArray, filePath7)
				ArrayToRaster(maxTempArray, filePath8)
				ArrayToRaster(meanDuraArray, filePath9)
				ArrayToRaster(minDuraArray, filePath10)
				ArrayToRaster(maxDuraArray, filePath11)
			print(str(index1) + " is done!")
			del data_3d

def CalARTT(dirPath2, field1, field2, percentage1):
	for index1 in range(1989, 2019):
		dirPath4 = dirPath2.replace(field1, field2, 1)
		filePathDetect = os.path.join(dirPath4, str(index1) + "_ARTT.tif")
		if os.path.exists(filePathDetect):
			print(str(index1) + " is done!")
		else:
			dirPath3 = os.path.join(dirPath2, str(index1))
			for dirPath, dirname, filenames in os.walk(dirPath3):
				tifFilenames = []
				for filename in filenames:
					if filename[-4: ] == ".tif":
						tifFilenames.append(filename)		
				data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
				index = 0
				for tifFilename in tifFilenames:
					filePath1 = os.path.join(dirPath3, tifFilename)
					raster_data = gdal.Open(filePath1)
					raster_value = raster_data.ReadAsArray()
					data_3d[index, :, :] = raster_value
					index = index + 1
				ARTTArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				for index2 in range(0, 929):
					for index3 in range(0, 1783):
						if data_3d[0, index2, index3] != -3.4028234663852886e+38:
							yearValueArray = data_3d[:, index2, index3]
							tempTag = numpy.percentile(yearValueArray, percentage1)
							ARTTArray[index2, index3] = tempTag
				filePath2 = os.path.join(dirPath4, str(index1) + "_ARTT.tif")
				ArrayToRaster(ARTTArray, filePath2)				
			print(str(index1) + " is done!")

def HeatWave4(dirPath2, field1, field2, percentage1, durationTag):
	for index1 in range(1989, 2019):
		dirPath4 = dirPath2.replace(field1, field2, 1)
		filePathDetect = os.path.join(dirPath4, str(index1) + "_freq.tif")
		if os.path.exists(filePathDetect):
			print(str(index1) + " is done!")
		else:
			dirPath3 = os.path.join(dirPath2, str(index1))
			for dirPath, dirname, filenames in os.walk(dirPath3):
				tifFilenames = []
				for filename in filenames:
					if filename[-4: ] == ".tif":
						tifFilenames.append(filename)		
				data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
				index = 0
				dateList2 = []
				for tifFilename in tifFilenames:
					filePath1 = os.path.join(dirPath3, tifFilename)
					raster_data = gdal.Open(filePath1)
					raster_value = raster_data.ReadAsArray()
					data_3d[index, :, :] = raster_value
					index = index + 1
					dateList2.append(tifFilename[-8: -4])
				frequencyArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				durationArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				startDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				endDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)			
				allDataList = []
				for index2 in range(0, 929):
					for index3 in range(0, 1783):
						yearValueArray = data_3d[:, index2, index3]
						tempTag = numpy.percentile(yearValueArray, percentage1)				
						if data_3d[0, index2, index3] != -3.4028234663852886e+38:
							allDataList = data_3d[:, index2, index3].tolist()
							hotDataList = []
							for index4 in range(len(allDataList)):
								if allDataList[index4] >= tempTag and allDataList[index4] >= 29:
									hot_temp = allDataList[index4]
									hot_date = tifFilenames[index4][0: 8]
									hotDataList.append([hot_temp, hot_date])
							duration1 = 1
							frequency = 0
							totalDuration = 0
							startDateList = []
							endDateList = []	
							meanTempList = []
							minTempList = []
							maxTempList = []	
							durationList = []		
							for index5 in range(0, len(hotDataList) - 1):
								date1 = datetime.datetime.strptime(hotDataList[index5][1], "%Y%m%d")
								date2 = datetime.datetime.strptime(hotDataList[index5 + 1][1], "%Y%m%d")
								if date2 - date1 == numpy.timedelta64(1, "D") and date2 != datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d"):
									duration1 = duration1 + 1
								elif date2 - date1 != numpy.timedelta64(1, "D") or (date2 - date1 == numpy.timedelta64(1, "D") and date2 == datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d")):
									if duration1 >= durationTag:
										startDateString = hotDataList[index5 - (duration1 - 1)][1]
										endDateString = hotDataList[index5][1]
										startDate = datetime.date(int(startDateString[0: 4]), int(startDateString[4: 6]), int(startDateString[6: 8]))
										startDateCount = startDate.strftime("%j")
										endDate = datetime.date(int(endDateString[0: 4]), int(endDateString[4: 6]), int(endDateString[6: 8]))
										endDateCount = endDate.strftime("%j")							    
										tempList = []
										for index6 in range(index5 - (duration1 - 1), index5 + 1):
											tempList.append(hotDataList[index6][0])
										sum1 = 0
										for temp in tempList:
											sum1 = sum1 + temp
										meanTemp1 = sum1 / len(tempList)
										minTemp = min(tempList)
										maxTemp = max(tempList)
										frequency = frequency + 1
										totalDuration = totalDuration + duration1
										startDateList.append(startDateCount)
										endDateList.append(endDateCount)
										meanTempList.append(meanTemp1)
										minTempList.append(minTemp)
										maxTempList.append(maxTemp)
										durationList.append(duration1)
									duration1 = 1
							if frequency == 0:
								totalDuration = 0
								totalStartDate = -3.4028234663852886e+38
								totalEndDate = -3.4028234663852886e+38
								totalMeanTemp = -3.4028234663852886e+38
								totalMinTemp = -3.4028234663852886e+38
								totalMaxTemp = -3.4028234663852886e+38
								totalMeanDura = 0
								totalMinDura = 0
								totalMaxDura = 0
							else:
								totalStartDate = min(startDateList)
								totalEndDate = max(endDateList)
								sum2 = 0
								for meanTemp2 in meanTempList:
									sum2 = sum2 + meanTemp2
								totalMeanTemp = sum2 / len(meanTempList)
								totalMinTemp = min(minTempList)
								totalMaxTemp = max(maxTempList)	
								sum3 = 0
								for duration2 in durationList:
									sum3 = sum3 + duration2
								totalMeanDura = sum3 / len(durationList)
								totalMinDura = min(durationList)
								totalMaxDura = max(durationList)				
							frequencyArray[index2, index3] = frequency
							durationArray[index2, index3] = totalDuration
							startDateArray[index2, index3] = totalStartDate
							endDateArray[index2, index3] = totalEndDate
							meanTempArray[index2, index3] = totalMeanTemp
							minTempArray[index2, index3] = totalMinTemp
							maxTempArray[index2, index3] = totalMaxTemp
							meanDuraArray[index2, index3] = totalMeanDura
							minDuraArray[index2, index3] = totalMinDura
							maxDuraArray[index2, index3] = totalMaxDura				
				filePath2 = os.path.join(dirPath4, str(index1) + "_freq.tif")
				filePath3 = os.path.join(dirPath4, str(index1) + "_dura.tif")
				filePath4 = os.path.join(dirPath4, str(index1) + "_start.tif")
				filePath5 = os.path.join(dirPath4, str(index1) + "_end.tif")
				filePath6 = os.path.join(dirPath4, str(index1) + "_tmean.tif")
				filePath7 = os.path.join(dirPath4, str(index1) + "_tmin.tif")
				filePath8 = os.path.join(dirPath4, str(index1) + "_tmax.tif")
				filePath9 = os.path.join(dirPath4, str(index1) + "_dmean.tif")
				filePath10 = os.path.join(dirPath4, str(index1) + "_dmin.tif")
				filePath11 = os.path.join(dirPath4, str(index1) + "_dmax.tif")
				ArrayToRaster(frequencyArray, filePath2)
				ArrayToRaster(durationArray, filePath3)
				ArrayToRaster(startDateArray, filePath4)
				ArrayToRaster(endDateArray, filePath5)
				ArrayToRaster(meanTempArray, filePath6)
				ArrayToRaster(minTempArray, filePath7)
				ArrayToRaster(maxTempArray, filePath8)
				ArrayToRaster(meanDuraArray, filePath9)
				ArrayToRaster(minDuraArray, filePath10)
				ArrayToRaster(maxDuraArray, filePath11)
			print(str(index1) + " is done!")
			del data_3d

def HeatWave5(dirPath2, field1, field2, filePath12, durationTag):
	raster_data_ref = gdal.Open(filePath12)
	raster_value_ref = raster_data_ref.ReadAsArray()
	for index1 in range(1989, 2019):
		dirPath4 = dirPath2.replace(field1, field2, 1)
		filePathDetect = os.path.join(dirPath4, str(index1) + "_freq.tif")
		if os.path.exists(filePathDetect):
			print(str(index1) + " is done!")
		else:
			dirPath3 = os.path.join(dirPath2, str(index1))
			for dirPath, dirname, filenames in os.walk(dirPath3):
				tifFilenames = []
				for filename in filenames:
					if filename[-4: ] == ".tif":
						tifFilenames.append(filename)		
				data_3d = numpy.full((len(tifFilenames), 929, 1783), numpy.nan)
				index = 0
				dateList2 = []
				for tifFilename in tifFilenames:
					filePath1 = os.path.join(dirPath3, tifFilename)
					raster_data = gdal.Open(filePath1)
					raster_value = raster_data.ReadAsArray()
					data_3d[index, :, :] = raster_value
					index = index + 1
					dateList2.append(tifFilename[-8: -4])
				frequencyArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				durationArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				startDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				endDateArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxTempArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				meanDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				minDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)
				maxDuraArray = numpy.full((929, 1783), -3.4028234663852886e+38)			
				allDataList = []
				for index2 in range(0, 929):
					for index3 in range(0, 1783):
						if data_3d[0, index2, index3] != -3.4028234663852886e+38:
							allDataList = data_3d[:, index2, index3].tolist()
							hotDataList = []
							for index4 in range(len(allDataList)):
								if allDataList[index4] >= raster_value_ref[index2, index3] and allDataList[index4] >= 29:
									hot_temp = allDataList[index4]
									hot_date = tifFilenames[index4][0: 8]
									hotDataList.append([hot_temp, hot_date])
							duration1 = 1
							frequency = 0
							totalDuration = 0
							startDateList = []
							endDateList = []	
							meanTempList = []
							minTempList = []
							maxTempList = []	
							durationList = []		
							for index5 in range(0, len(hotDataList) - 1):
								date1 = datetime.datetime.strptime(hotDataList[index5][1], "%Y%m%d")
								date2 = datetime.datetime.strptime(hotDataList[index5 + 1][1], "%Y%m%d")
								if date2 - date1 == numpy.timedelta64(1, "D") and date2 != datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d"):
									duration1 = duration1 + 1
								elif date2 - date1 != numpy.timedelta64(1, "D") or (date2 - date1 == numpy.timedelta64(1, "D") and date2 == datetime.datetime.strptime(hotDataList[len(hotDataList) - 1][1], "%Y%m%d")):
									if duration1 >= durationTag:
										startDateString = hotDataList[index5 - (duration1 - 1)][1]
										endDateString = hotDataList[index5][1]
										startDate = datetime.date(int(startDateString[0: 4]), int(startDateString[4: 6]), int(startDateString[6: 8]))
										startDateCount = startDate.strftime("%j")
										endDate = datetime.date(int(endDateString[0: 4]), int(endDateString[4: 6]), int(endDateString[6: 8]))
										endDateCount = endDate.strftime("%j")							    
										tempList = []
										for index6 in range(index5 - (duration1 - 1), index5 + 1):
											tempList.append(hotDataList[index6][0])
										sum1 = 0
										for temp in tempList:
											sum1 = sum1 + temp
										meanTemp1 = sum1 / len(tempList)
										minTemp = min(tempList)
										maxTemp = max(tempList)
										frequency = frequency + 1
										totalDuration = totalDuration + duration1
										startDateList.append(startDateCount)
										endDateList.append(endDateCount)
										meanTempList.append(meanTemp1)
										minTempList.append(minTemp)
										maxTempList.append(maxTemp)
										durationList.append(duration1)
									duration1 = 1
							if frequency == 0:
								totalDuration = 0
								totalStartDate = -3.4028234663852886e+38
								totalEndDate = -3.4028234663852886e+38
								totalMeanTemp = -3.4028234663852886e+38
								totalMinTemp = -3.4028234663852886e+38
								totalMaxTemp = -3.4028234663852886e+38
								totalMeanDura = 0
								totalMinDura = 0
								totalMaxDura = 0
							else:
								totalStartDate = min(startDateList)
								totalEndDate = max(endDateList)
								sum2 = 0
								for meanTemp2 in meanTempList:
									sum2 = sum2 + meanTemp2
								totalMeanTemp = sum2 / len(meanTempList)
								totalMinTemp = min(minTempList)
								totalMaxTemp = max(maxTempList)	
								sum3 = 0
								for duration2 in durationList:
									sum3 = sum3 + duration2
								totalMeanDura = sum3 / len(durationList)
								totalMinDura = min(durationList)
								totalMaxDura = max(durationList)				
							frequencyArray[index2, index3] = frequency
							durationArray[index2, index3] = totalDuration
							startDateArray[index2, index3] = totalStartDate
							endDateArray[index2, index3] = totalEndDate
							meanTempArray[index2, index3] = totalMeanTemp
							minTempArray[index2, index3] = totalMinTemp
							maxTempArray[index2, index3] = totalMaxTemp
							meanDuraArray[index2, index3] = totalMeanDura
							minDuraArray[index2, index3] = totalMinDura
							maxDuraArray[index2, index3] = totalMaxDura				
				filePath2 = os.path.join(dirPath4, str(index1) + "_freq.tif")
				filePath3 = os.path.join(dirPath4, str(index1) + "_dura.tif")
				filePath4 = os.path.join(dirPath4, str(index1) + "_start.tif")
				filePath5 = os.path.join(dirPath4, str(index1) + "_end.tif")
				filePath6 = os.path.join(dirPath4, str(index1) + "_tmean.tif")
				filePath7 = os.path.join(dirPath4, str(index1) + "_tmin.tif")
				filePath8 = os.path.join(dirPath4, str(index1) + "_tmax.tif")
				filePath9 = os.path.join(dirPath4, str(index1) + "_dmean.tif")
				filePath10 = os.path.join(dirPath4, str(index1) + "_dmin.tif")
				filePath11 = os.path.join(dirPath4, str(index1) + "_dmax.tif")
				ArrayToRaster(frequencyArray, filePath2)
				ArrayToRaster(durationArray, filePath3)
				ArrayToRaster(startDateArray, filePath4)
				ArrayToRaster(endDateArray, filePath5)
				ArrayToRaster(meanTempArray, filePath6)
				ArrayToRaster(minTempArray, filePath7)
				ArrayToRaster(maxTempArray, filePath8)
				ArrayToRaster(meanDuraArray, filePath9)
				ArrayToRaster(minDuraArray, filePath10)
				ArrayToRaster(maxDuraArray, filePath11)
			print(str(index1) + " is done!")
			del data_3d

def main():
	# # ѡ?վ?????ļ?
	# dirPath1 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\2select"
	# for index in range(2016, 2020):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)
	# filePath1 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\0base\\stations_Dhaka.csv"
	# dirPath2 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\1download"
	# SelectFiles(filePath1, dirPath2)

	# # ??????
	# dirPath1 = "F:\\1_paper_heat wave\\data\\3unpack"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)

	# ??վ?????ļ?ת??Ϊexcel???
	# dirPath1 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\4XLS"
	# dirPath2 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\5CSV"
	# for index in range(2016, 2020):
	# 	dirPath3 = os.path.join(dirPath1, str(index))
	# 	dirPath4 = os.path.join(dirPath2, str(index))
	# 	CreateDir(dirPath3)
	# 	CreateDir(dirPath4)
	# dirPath5 = "G:\\1_任务\\1_高温热浪_高温热浪和极端干旱对关键节点区域影响的风险评估和典型节点区域环境问题综合应对方案\\数据提交20200116\\气象站点监测数据\\3unpack"
	# TxtToCSV(dirPath5)

	# ȱʧֵ????
	# dirPath1 = "F:\\1_paper_heat wave\\data\\6null"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)
	# dirPath2 = "F:\\1_paper_heat wave\\data\\5CSV"
	# RMissingPro(dirPath2)
	# dirPath3 = "F:\\1_paper_heat wave\\data\\7null"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath3, str(index))
	# 	CreateDir(dirPath2)	

	# # ??????ȣ?ƥ???γ??
	# dirPath1 = "F:\\1_paper_heat wave\\data\\8AT"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)	
	# filePath1 = "F:\\1_paper_heat wave\\data\\Stations.csv"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\7null"
	# Calculate(filePath1, dirPath2)

	# # ?????
	# dirPath1 = "F:\\1_paper_heat wave\\data\\9XT"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)	
	# dirPath2 = "F:\\1_paper_heat wave\\data\\8AT"
	# Correct(dirPath2)

	# # ?ϲ?excel???
	# dirPath = "F:\\1_paper_heat wave\\data\\9XT"
	# MergeFile(dirPath)

	# # ?ȡÿ????
	# dirPath1 = "F:\\1_paper_heat wave\\data\\11daily"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)		
	# dirPath3 = "F:\\1_paper_heat wave\\data\\10merge"
	# DailyData(dirPath3)

	# # 文本数据空间化
	# dirPath1 = "F:\\1_paper_heat wave\\data\\13Layer"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)		
	# dirPath3 = "F:\\1_paper_heat wave\\data\\11daily"
	# CsvToLayer(dirPath3)

	# 插值
	# field1 = "HTEMPX"
	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# dirPath2 = os.path.join(dirPath1, "14" + field1 + "_1")
	# dirPath3 = os.path.join(dirPath1, "14" + field1 + "_2")
	# CreateDir(dirPath2)
	# CreateDir(dirPath3)
	# for index in range(1989, 2019):
	# 	dirPath4 = os.path.join(dirPath2, str(index))
	# 	dirPath5 = os.path.join(dirPath3, str(index))
	# 	CreateDir(dirPath4)
	# 	CreateDir(dirPath5)
	# dirPath6 = "F:\\1_paper_heat wave\\data\\13layer"
	# PointToRaster(dirPath6, field1)

	field1 = "HTEMPX"
	# dirPath1 = "F:\\1_paper_heat wave\\data\\26variance"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\25HTEMPX"
	# for index in range(2015, 2016):
	# 	dirPath3 = os.path.join(dirPath1, str(index))
	# 	dirPath4 = os.path.join(dirPath2, str(index))
	# 	CreateDir(dirPath3)
	# 	CreateDir(dirPath4)		
	dirPath5 = "F:\\1_paper_heat wave\\data\\13layer"
	PointToRaster(dirPath5, field1)

	# dirPath1 = "F:\\1_paper_heat wave\\data\\18daily_check"
	# for index in range(1989, 2019):
	# 	dirPath2 = os.path.join(dirPath1, str(index))
	# 	CreateDir(dirPath2)	
	# dirPath3 = "F:\\1_paper_heat wave\\data\\11daily"
	# field1 = "HTEMP"
	# CheckInterpolate(dirPath3, field1)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "15HW_HTEMPX_1"
	# dirPath2 = os.path.join(dirPath1, field1)			
	# HeatWave1(dirPath2, field1, field2, 29, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "17statistics_heatwave"
	# dirPath2 = os.path.join(dirPath1, field1)			
	# HeatWave1(dirPath2, field1, field2, 35, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14ATEMPX"
	# field2 = "15HW_FT_ATEMPX"
	# dirPath2 = os.path.join(dirPath1, field1)			
	# HeatWave1(dirPath2, field1, field2, 29, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "16MEAN_HTEMPX"
	# dirPath2 = os.path.join(dirPath1, field1)
	# CalculateTemp1(dirPath2, field1, field2)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "17HW_HTEMPX"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\16MEAN_HTEMPX"
	# dirPath3 = os.path.join(dirPath1, field1)			
	# HeatWave2(dirPath2, dirPath3, field1, field2, 95, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "17MFAT_HTEMPX_1"
	# dirPath2 = os.path.join(dirPath1, field1)
	# CalculateTemp2(dirPath2, field1, field2)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "14PERC_90_HTEMPX"
	# dirPath2 = os.path.join(dirPath1, field1)
	# CalculateTemp3(dirPath2, 90, field1, field2)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "15HW_PT_HTEMPX_90_75"
	# dirPath2 = "F:\\1_paper_heat wave\\data\\14PERC_90_HTEMPX"	
	# dirPath3 = os.path.join(dirPath1, field1)	
	# HeatWave3(dirPath2, dirPath3, field1, field2, 75, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "15HW_YPT_HTEMPX_85_29"
	# dirPath3 = os.path.join(dirPath1, field1)
	# HeatWave4(dirPath3, field1, field2, 85, 3)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "14ARTT_80"
	# dirPath3 = os.path.join(dirPath1, field1)
	# CalARTT(dirPath3, field1, field2, 80)

	# dirPath1 = "F:\\1_paper_heat wave\\data"
	# field1 = "14HTEMPX"
	# field2 = "15HW_MYPT_HTEMPX_80_29"
	# filePath1 = "F:\\1_paper_heat wave\\data\\14ARTT_80\\ARTT_mean.tif"
	# dirPath3 = os.path.join(dirPath1, field1)
	# HeatWave5(dirPath3, field1, field2, filePath1, 3)

main()
