import cv2
import numpy as np

# Load the images
img1 = cv2.imread('/content/Corrosaov5/LSM/5_03_01_png.rf.1649f6b5935f5e1b870a7d5032ec8273.jpg')
img2 = cv2.imread('/content/Corrosaov5/LSM/5_03_01_png.rf.1649f6b5935f5e1b870a7d5032ec8273(1).jpg')

# calculate the mean squared error
mse = ((img1 - img2) ** 2).mean()
#mean squared error (MSE) or the mean absolute error (MAE) of the result.
print(f'mean squared error: {mse}')
mae = np.mean(np.abs(img1-img2))
print(f'mean absolute error: {mae}')
# merge the two images together with an opacity of 0.5
merged_img = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

# Create ORB object
orb = cv2.ORB_create()

# Detect keypoints and compute descriptors for the first image
kp1, des1 = orb.detectAndCompute(img1, None)

# Detect keypoints and compute descriptors for the second image
kp2, des2 = orb.detectAndCompute(img2, None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

# Draw matches
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imwrite('image3.jpg', img3)
cv2.imwrite('image4.jpg',merged_img)