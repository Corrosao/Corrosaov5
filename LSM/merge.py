import os
import cv2
import numpy as np
import datetime

now = datetime.datetime.now()

folder_name = f"lsm_{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

# specify the path to the OUTPUT and OUTPUT_DETECT folders
output_folder = '/content/Corrosaov5/output'
output_detect_folder = '/content/Corrosaov5/output_detect'

# create a new folder
save_folder = os.path.join('/content/Corrosaov5/LSM', folder_name)
os.makedirs(save_folder)

# create a text file to save results
txt_file = open(os.path.join(save_folder, 'results.txt'), 'w')

# get a list of all files in the OUTPUT folder
output_files = os.listdir(output_folder)

# get a list of all files in the OUTPUT_DETECT folder
output_detect_files = os.listdir(output_detect_folder)

# iterate through the files in the OUTPUT folder
for file in output_files:
    # construct the full file path
    img1_path = os.path.join(output_folder, file)
    # load the image
    img1 = cv2.imread(img1_path)
    # check if the file also exists in the OUTPUT_DETECT folder
    if file in output_detect_files:
        # construct the full file path
        img2_path = os.path.join(output_detect_folder, file)
        # load the image
        img2 = cv2.imread(img2_path)
        # calculate the mean squared error
        mse = ((img1 - img2) ** 2).mean()
        print(f'mean squared error for {file}: {mse}')
        mae = np.mean(np.abs(img1-img2))
        print(f'mean absolute error for {file}: {mae}')
        # write the image name, mean squared error, and mean absolute error to the text file
        txt_file.write(f'{file}\nmean squared error: {mse}\nmean absolute error: {mae}\n\n')
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
        # save the images
        # cv2.imwrite(os.path.join(save_folder,f'image3_{file}'), img3)
        cv2.imwrite(os.path.join(save_folder,f'lsm_{file}'), merged_img)
# close the text file
txt_file.close()