from kuwahara import kuwahara
from encoder import encode, decode
from image_util import combine
# from random import randint # testing
import cv2
import os

folder = './img'
os.makedirs(folder, exist_ok=True)

img_path = "noisy_img.png"
image = cv2.imread(img_path)

message = 'hello world'
encoding = encode(message)

method = 'gaussian'
radius = 9

offset  = kuwahara(image, method=method, radius=radius, offsets=encoding)
diff = cv2.subtract(offset, image)  # seeing the difference is epic
# avg, rand, vert, hori
c_avg  = combine(offset, image, "avg")
c_rand = combine(offset, image, "rand")
c_vert = combine(offset, image, "vert")
c_hori = combine(offset, image, "hori")

cv2.imwrite(folder + '/offset.jpg', offset)
cv2.imwrite(folder + '/image.jpg', image)
cv2.imwrite(folder + '/diff.jpg', diff)

cv2.imwrite(folder + '/avg_combined.jpg', c_avg)
cv2.imwrite(folder + '/rand_combined.jpg', c_rand)
cv2.imwrite(folder + '/vert_combined.jpg', c_vert)
cv2.imwrite(folder + '/hori_combined.jpg', c_hori)