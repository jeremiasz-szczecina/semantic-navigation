from Dataset import Dataset

images = r"C:\Users\Jeremiasz\Desktop\script_tests\raw_data"
save = r"C:\Users\Jeremiasz\Desktop\script_tests\prepped_data"

dataset = Dataset(images, save, backup=False)
dataset.preprocess()