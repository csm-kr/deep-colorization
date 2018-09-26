import cv2
import os
import numpy as np


def read_data_set(datadir):
    """
    x_feature 과 y_feature 을 모두 읽어드리고, 내보내는 부분
    :param datadir: 데이터셋이 있는 디렉토리
    :return: x_features : nparray ( N, 227, 227, 1)
              y_labels : nparray ( N, 227, 227, 3)
    """
    # 파일이름으로 읽기
    # 파일이름이 cat 이고 뒤의 숫자로 배열한다.
    # 파일 이름 리스트
    data_list = os.listdir(datadir)
    # 데이타 갯수
    data_length = len(data_list)

    x_list = []
    y_list = []

    # 이름 가져오는 부분
    for i in range(data_length):
        name = data_list[i].split('.')[0]
        if name == 'g_cat':
            x_list.append(data_list[i])
        elif name == 'cat':
            y_list.append(data_list[i])

    # 정렬 하는 부분

    x_list.sort()
    y_list.sort()

    cat_len = len(x_list)
    print(cat_len)

    x_features = np.empty(shape=(cat_len, 256, 256, 1), dtype=np.float32)
    y_labels = np.empty(shape=(cat_len, 256, 256, 3), dtype=np.float32)

    for i in range(cat_len):
        img_g = cv2.imread(os.path.join(data_dir, x_list[i]), cv2.IMREAD_GRAYSCALE)
        img_g = cv2.resize(img_g, dsize=(256, 256), interpolation=cv2.INTER_CUBIC).astype(np.float32)
        img_g = img_g[:, :, np.newaxis]
        x_features[i] = img_g
        img = cv2.imread(os.path.join(data_dir, y_list[i]))
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_CUBIC).astype(np.float32)
        y_labels[i] = img
        if np.mod(i, 1000) == 0:
            print("Loading {}/{} images...".format(i, cat_len))

    print('\nDone')
    print(x_features.shape)
    print(y_labels.shape)

    return x_features, y_labels


if __name__ == "__main__":
    data_dir = r"data/train"
    read_data_set(data_dir)