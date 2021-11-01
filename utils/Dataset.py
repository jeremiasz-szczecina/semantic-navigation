import os
import cv2 as cv
from shutil import copyfile
from tqdm import tqdm

class Dataset:
    def __init__(self, img_path, save_path=None, backup=True):
        self.backup = backup
        
        self.img_path = img_path + "\\"
        assert os.path.isdir(self.img_path), "This is not a valid directory, check the path you've passed."
        if save_path is None and self.backup is True:
            default_path = self.img_path + "saved_imgs" + "\\"
            if not os.path.exists(default_path):
                os.makedirs(default_path)
            self.save_path = default_path
        elif save_path is None and not self.backup:
            self.save_path = self.img_path
        else:
            self.save_path = save_path + "\\"
            assert os.path.isdir(self.save_path), "This is not a valid directory, check the path you've passed."

        print(f"IMAGES DIR:     {self.img_path}")
        print(f"SAVE DIR:       {self.save_path}")


    def get_file_list(self, img_path=None):
        filepaths = [] # filepaths -> absolute paths for images
        if img_path is None:
            img_path = self.img_path

        img_ids = next(os.walk(img_path))
        for img_name in img_ids[2]: # img_ids[2] -> container for only image names, eg. '0001.png'
            filepaths.append(img_path + img_name)   
        return filepaths, img_ids[2]
        

    def rename(self):
        num = 1
        filepaths, _ = self.get_file_list()
        print("Making backup, renaming files:" if self.backup else "Renaming files:")
        for filepath in tqdm(filepaths):
            if num >= 1 and num <= 9:
                _NEW_PATH = self.save_path + "000" + str(num) + ".png"
            elif num >= 10 and num <= 99:
                _NEW_PATH = self.save_path + "00" + str(num) + ".png"
            elif num >= 100 and num <= 999:
                _NEW_PATH = self.save_path + "0" + str(num) + ".png"
            else:
                _NEW_PATH = self.save_path + str(num) + ".png"

            copyfile(filepath, _NEW_PATH) if self.backup else os.rename(filepath, _NEW_PATH)
            num += 1


    def crop_resize(self):
        num = 0
        filepaths, img_ids = self.get_file_list(self.save_path)
        print("Cropping and resizing:")
        for file in tqdm(filepaths):
            image = cv.imread(file)
            cropped = image[139:1046, 82:1288]
            cropped_resized = cv.resize(cropped, dsize=(640, 480), interpolation=cv.INTER_AREA)
            cv.imwrite(self.save_path + img_ids[num], cropped_resized)
            num += 1       


    def preprocess(self):
        self.rename()
        self.crop_resize()
