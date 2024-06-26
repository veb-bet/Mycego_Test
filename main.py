import glob
import numpy as np
from PIL import Image

# Создание сетки изображений из массива изображений
def imgrid(imarray, cols=4):
    cols = int(cols)
    assert cols >= 1
    N = len(imarray)
    rows = N // cols + int(N % cols != 0)

    # Нахождение максимальной высоты и ширины изображений
    max_height = max(img.shape[0] for img in imarray)
    max_width = max(img.shape[1] for img in imarray)

    # Создание пустого изображения
    grid = np.zeros((rows * max_height, cols * max_width, 3), dtype=np.uint8)

    # Размещение изображения в сетке
    for i, img in enumerate(imarray):
        row = i // cols
        col = i % cols
        if img.shape[2] == 4:
            img = img[:, :, :3]  # Конвертация RGBA в RGB
        grid[row * max_height:(row + 1) * max_height, col * max_width:(col + 1) * max_width] = img

    return grid


dicts = input("Введите список папок с изображениями из data через запятую: ").split(",")
all_images = []
for i, dicts in enumerate(dicts):
    # Нахождение всех файлов .png
    fnames = glob.glob(f'./Data/{dicts.strip()}/*.png')
    # Загрузка все изображения в массив
    imarray = [np.array(Image.open(fname)) for fname in fnames]
    imarray = [np.array(Image.open(fname).resize((256, 256), resample=Image.LANCZOS)) for fname in fnames]
    # Объединие изображений и сохрание как tiff
    Image.fromarray(imgrid(imarray)).save(f'Result_{i}.tiff')
    all_images.extend(imarray)

# Создание финального изображения
final_image = Image.fromarray(imgrid(all_images))
final_image.save('Result.tiff')