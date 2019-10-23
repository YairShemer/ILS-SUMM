import numpy as np
import cv2
import glob
import os
import re
def extract_features(image_dir_name):
    images = [cv2.imread(file) for file in sorted(glob.glob(os.path.join(image_dir_name, "*.jpg")), key=stringSplitByNumbers)]
    BINS_NUMBER_PER_CHANNEL = 32
    features = np.zeros((images.__len__(), BINS_NUMBER_PER_CHANNEL * 3), dtype=float)
    for i in range(len(images)):
        if i % 50 == 0:
            print("Finished extracting features for %d frames" %i)
        r_values = images[i][:,:,0].flatten()
        g_values= images[i][:, :, 1].flatten()
        b_values = images[i][:, :, 2].flatten()

        r_hist, _ = np.histogram(r_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_r_hist =  r_hist / np.sum(r_hist)
        g_hist, _ = np.histogram(g_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_g_hist =  g_hist / np.sum(g_hist)
        b_hist, _ = np.histogram(b_values, BINS_NUMBER_PER_CHANNEL, [0, 256])
        normalized_b_hist =  b_hist / np.sum(b_hist)

        features[i,:] = np.concatenate((normalized_r_hist, normalized_g_hist, normalized_b_hist))
    return features

def stringSplitByNumbers(x):
    r = re.compile('(\d+)')
    l = r.split(x)
    return [int(y) if y.isdigit() else y for y in l]