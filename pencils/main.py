import os
import cv2
from skimage.measure import label, regionprops

image_folder = 'pencils'

def count_pencils(image_path):
    im = cv2.imread(image_path)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 110, 1, cv2.THRESH_BINARY_INV)

    labeled = label(binary)
    regions = regionprops(labeled)

    total_pencils = 0

    for region in regions:
        area = region.area
        eccentricity = region.eccentricity
        if area > 210000 and eccentricity > 0.95: # это приблизительная площадь и круглость всех карандашей
            total_pencils += 1

    return total_pencils


def main():
    total_pencils = 0
    image_files = os.listdir(image_folder)

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        count = count_pencils(image_path)
        total_pencils += count
        print(f"Количество карандашей на изображении {image_file}: {count}")

    print(f"Общее количество карандашей: {total_pencils}")

if __name__ == "__main__":
    main()
