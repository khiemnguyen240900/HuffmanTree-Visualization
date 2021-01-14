import numpy as np
import cv2
# def show_pic(p):
#         ''' use esc to see the results'''
#         print(type(p))
#         cv2.imshow('Color image', p)
#         while True:
#             k = cv2.waitKey(0) & 0xFF
#             if k == 27: break
#         return
#         cv2.destroyAllWindows()
#
# b = numpy.zeros([200,200,3])
#
# b[:,:,0] = numpy.ones([200,200])*255
# b[:,:,1] = numpy.ones([200,200])*255
# b[:,:,2] = numpy.ones([200,200])*0
# cv2.imwrite('color_img.jpg', b)
#
#
# c = cv2.imread('color_img.jpg', 1)
# c = cv2.cvtColor(c, cv2.COLOR_BGR2RGB)
#
# d = cv2.imread('color_img.jpg', 1)
# d = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
#
# e = cv2.imread('color_img.jpg', -1)
# e = cv2.cvtColor(c, cv2.COLOR_BGR2RGB)
#
# f = cv2.imread('color_img.jpg', -1)
# f = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
#
#
# pictures = [d, c, f, e]
#
# for p in pictures:
#         show_pic(p)
# # show the matrix
# print(c)
# print(c.shape)

float_img = np.random.random((256,256))
print(float_img)
im = np.array(float_img * 255, dtype = np.uint8)
print(im)
threshed = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
cv2.imshow('a',threshed)
cv2.waitKey(0)