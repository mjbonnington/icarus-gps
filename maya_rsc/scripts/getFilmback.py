#gets film back from stock cameras. Camera sensor specifications are stored in stockCameras module

import stockCameras
reload(stockCameras)

def get(camera, inches):
	if camera == 'arriAlexa':
		return stockCameras.arriAlexa(inches)
	elif camera == 'canon5D':
		return stockCameras.canon5D(inches)
	elif camera == 'redEpicX':
		return stockCameras.redEpicX(inches)
	elif camera == 'redOne':
		return stockCameras.redOne(inches)
	elif camera == 'sonyF55':
		return stockCameras.sonyF55(inches)
	
	