import cv2
import numpy as np

def control_brightness(img,beta):
	top_layer = img.copy()
	top_layer.fill(beta)
	img = cv2.add(img, top_layer)
	img = np.clip(img,0,255)
	cv2.imwrite('Out.jpg',img)
	return img

def control_contrast(img,alpha):
	img = img*alpha
	img = np.clip(img,0,255)
	cv2.imwrite('Out.jpg',img)
	return img

def control_clahe(img,clip,gridSize):
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(gridSize,gridSize))
	img = clahe.apply(img)
	return img

def control_noise_removal(img):
	blur = cv2.bilateralFilter(img,9,75,75)
	cv2.imwrite('Out.jpg',blur)
	return blur

def hist_eqn(img):
	img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
	img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
	img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
	cv2.imwrite('Out.jpg',img_output)
	return img_output

# img = cv2.imread('images/test.jpg')
# img = control_brightness(img,100)
# img = control_contrast(img,0)
# # img = control_clahe(img,10,8)
# # img = hist_eqn(img)
# cv2.imwrite('Out1.jpg',img)
