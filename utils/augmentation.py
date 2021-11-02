import albumentations as A
import os
import random
import cv2
from tqdm import tqdm

SCREEN_PATH = r"C:\Users\Jeremiasz\Documents\pyScripts\dataset_marked_1\JPEGImages" + "\\"
MASK_PATH = r"C:\Users\Jeremiasz\Documents\pyScripts\dataset_marked_1\SegmentationClass" + "\\"
AUG_IMG_PATH = r"C:\Users\Jeremiasz\Documents\pyScripts\augmented\aug_img" + "\\"
AUG_MASKS_PATH = r"C:\Users\Jeremiasz\Documents\pyScripts\augmented\aug_masks" + "\\"

if not os.path.exists(AUG_IMG_PATH):
    os.makedirs(AUG_IMG_PATH)

if not os.path.exists(AUG_MASKS_PATH):
    os.makedirs(AUG_MASKS_PATH)


images = []
masks = []

for im in os.listdir(SCREEN_PATH):   
    images.append(os.path.join(SCREEN_PATH, im))

for msk in os.listdir(MASK_PATH):   
    masks.append(os.path.join(MASK_PATH, msk))

aug = A.Compose([
    A.Blur(blur_limit=9, p=0.7),
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0),
    A.GaussNoise(p=1.0),
    A.CLAHE(clip_limit=3, p=0.4),
    A.OpticalDistortion(p=1.0)
    ]
)


images_to_generate = 500
num = 295
for i in tqdm(range(0, images_to_generate)):
    number = random.randint(0, len(images) - 1)
    image = images[number]
    mask = masks[number]
    original_image = cv2.imread(image, cv2.COLOR_BGR2RGB)
    original_mask = cv2.imread(mask)
        
    augmented = aug(image=original_image, mask=original_mask)
    transformed_image = augmented['image']
    transformed_mask = augmented['mask']

    filename_end = ''
    if num >= 1 and num <= 9:
        filename_end = "000" + str(num) + ".png"
    elif num >= 10 and num <= 99:
        filename_end = "00" + str(num) + ".png"
    elif num >= 100 and num <= 999:
        filename_end = "0" + str(num) + ".png"
    else:
        filename_end = str(num) + ".png"
     
    new_image_path = AUG_IMG_PATH + filename_end
    new_mask_path = AUG_MASKS_PATH + filename_end
    cv2.imwrite(new_image_path, transformed_image)
    cv2.imwrite(new_mask_path, transformed_mask)
    num += 1