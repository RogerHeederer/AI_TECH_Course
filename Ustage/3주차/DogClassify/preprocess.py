"""
해당 프로그램은 스탠포드 사이트에서 받아온 이미지 데이터를 정제하여
dataset 폴더 밑에 train, test로 분리를 위한 전처리를 담은 코드입니다.
"""

import wget

#url = 'http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar'
#wget.download(url)

import tarfile
import os
import shutil
import glob
import numpy as np

# 압축 풀어 놓을 타겟 폴더명 만들어줌
TARGET_PATH = "Images"
if os.path.exists(TARGET_PATH):
    shutil.rmtree(TARGET_PATH)

#images.tar 파일을 압축 푼다. 그럼 /content/Images 폴더가 생김
fname = "images.tar"
tar = tarfile.open(fname, "r:tar")
tar.extractall()
tar.close()

#폴더 이름을 품종명만 남기기
for dir_name in os.listdir(TARGET_PATH):
    breed_name = dir_name.split("-")[-1].lower()
    source_dir = os.path.join(TARGET_PATH, dir_name)
    target_dir = os.path.join(TARGET_PATH, breed_name)
    shutil.move(source_dir, target_dir)

dataset = []
for filepath in glob.iglob(f'{TARGET_PATH}/**/*.jpg', recursive=True):
    breed_name = filepath.split("/")[1]
    dataset.append([filepath, breed_name])
dataset = np.array(dataset)


from sklearn.model_selection import train_test_split

train_image, test_image, train_target, test_target = train_test_split(dataset[:,0], dataset[:,1], stratify=dataset[:,1])

#train 과 test를 분리하여 폴더 구조를 잡으려고 함
DATA_PATH = "dataset"

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
    os.makedirs(os.path.join(DATA_PATH, "train"))
    os.makedirs(os.path.join(DATA_PATH, "test"))

    for breed_name in set(test_target):
        os.makedirs(os.path.join(DATA_PATH, "train", breed_name))
        os.makedirs(os.path.join(DATA_PATH, "test", breed_name))

#train 하위 폴더에, 각 종 이름에 맞는 폴더 아래에 이미지 사진들 다 복사해주기
for filepath, target_dir in zip(train_image.tolist(), train_target.tolist()):
    filename = filepath.split("/")[-1]
    source_path = filepath
    target_dir = os.path.join(DATA_PATH, "train", target_dir, filename)
    shutil.copy(source_path, target_dir)

for filepath, target_dir in zip(test_image.tolist(), test_target.tolist()):
    filenmae = filepath.split("/")[-1]
    source_path = filepath
    target_dir = os.path.join(DATA_PATH, "test", target_dir, filename)
    shutil.copy(source_path, target_dir)