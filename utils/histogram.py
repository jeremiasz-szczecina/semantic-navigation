import numpy as np
import cv2
import time
import matplotlib.pyplot as plt


img = cv2.imread('/home/jerszc/pyscripts/git update/image_148_1.png', cv2.COLOR_BGR2GRAY)
(h, w) = (img.shape[:2])

# cX, cY: hardcoded img center, base imgs have small pixel offset from the left
(cX, cY) = (331, 249) 

# black arrays, allow to skip calculations when there's no need to do them
h_ref = np.zeros((h, 1))
w_ref = np.zeros((1, w))

# angle step
angle = 3


def histogram():
    h_idxs_min, h_idxs_max, v_idxs_min, v_idxs_max = list(), list(), list(), list()
    time_start = time.perf_counter()
    for i in range(0, 90, angle):
        # IMG ROTATION BY i-SPECIFIED ANGLE AROUND (cX, cY) POINT
        M = cv2.getRotationMatrix2D((cX, cY), i, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))

        # HEIGHT PART, VERTICAL SLICE::
        h_cropped = rotated[:, cX-1:cX]
        h_cropped = np.array(h_cropped)
        if not np.array_equal(h_cropped, h_ref):
            h_idx = np.where(h_cropped[:, 0] == np.amax(h_cropped[:, 0]))
            h_max = abs(249 - np.max(h_idx)) if h_cropped[np.max(h_idx)] == 255 and np.max(h_idx) > 249 else 0
            h_min = abs(249 - np.min(h_idx)) if np.min(h_idx) < 249 else 0
            h_idxs_max.append(h_max)
            h_idxs_min.append(h_min)  
        else:
            h_idxs_max.append(0)
            h_idxs_min.append(0)

        # WIDTH PART, HORIZONTAL SLICE::
        w_cropped = rotated[cY-1:cY, :]
        w_cropped = np.array(w_cropped)
        if not np.array_equal(w_cropped, w_ref):
            v_idx = np.where(w_cropped[0, :] == np.amax(w_cropped[0, :]))
            v_max = abs(331 - np.max(v_idx)) if w_cropped[0, np.max(v_idx)] == 255 and np.max(v_idx) >= 331 else 0
            v_min = abs(331 - np.min(v_idx)) if np.min(v_idx) < 331 else 0   
            v_idxs_max.append(v_max)
            v_idxs_min.append(v_min)
        else:
            v_idxs_max.append(0)
            v_idxs_min.append(0)

    
    distances = np.array(h_idxs_max + v_idxs_min + h_idxs_min + v_idxs_max)
    endtime = time.perf_counter() - time_start
    print(f"Time performance: {endtime}, accuracy: {angle} degrees")
    plt.bar(range(-180, 180, angle), distances[::-1])
    ax = plt.gca()
    ax.set_xlim([-180, 180])
    plt.show()

if __name__ == '__main__':
    histogram() 