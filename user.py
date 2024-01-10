from kuwahara import kuwahara
from random import randint
import cv2

img_path = "noisy_img.png"
image = cv2.imread(img_path)

offset  = kuwahara(image, offsets=[randint(0, 3) for _ in range(100)], method='gaussian', radius=5)
noffset = kuwahara(image, offsets=[0]*100, method='gaussian', radius=5)
diff = cv2.subtract(offset, noffset)  # seeing the difference is epic

cv2.imwrite('offset.jpg', offset)
cv2.imwrite('noffset.jpg', noffset)
cv2.imwrite('diff.jpg', diff)