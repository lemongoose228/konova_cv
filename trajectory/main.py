import numpy as np
import os
import matplotlib.pyplot as plt
import cv2

# Функция для вычисления евклидова расстояния между двумя точками p1 и p2
def compute_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def load_images_from_directory(directory):
    files = os.listdir(directory)
    # Сортируем файлы по числовой части имени 
    files = sorted(files, key=lambda x: int(x.split('_')[1].split('.')[0]))

    images = []
    for file in files:
        if file.endswith('.npy'):
            file_path = os.path.join(directory, file)
            img = np.load(file_path).astype('uint8')
            images.append(img)
    return images

def extract_contour_coordinates(files):
    # Функция для извлечения координат контуров из списка изображений
    trajectories = {"obj1": [], "obj2": [], "obj3": []}

    for i, image in enumerate(files):
        cnts, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        coords = []

        for cnt in cnts:
            (x, y), r = cv2.minEnclosingCircle(cnt)
            coords.append([x, y])

        if i == 0 and len(coords) >= 3:
            trajectories["obj1"].append(coords[0])
            trajectories["obj2"].append(coords[1])
            trajectories["obj3"].append(coords[2])

        else:
            for key in trajectories.keys():
                trajectory = trajectories[key]

                if trajectory:
                    last_point = trajectory[-1] # Получаем последнюю точку траектории
                    # Находим ближайшую точку из текущих координат к последней точке траектории
                    next_point = min(coords, key=lambda p2: compute_distance(last_point, p2), default=None)

                    
                    # Если найдена ближайшая точка то добавляем её в траекторию и удаляем из списка доступных кординат
                    if next_point is not None:
                        trajectory.append(next_point)
                        coords.remove(next_point)

    return trajectories


def plot_trajectories(trajectories):
    for key, trajectory in trajectories.items():
        x_points = [point[0] for point in trajectory]
        y_points = [point[1] for point in trajectory]

        plt.plot(x_points, y_points, marker='o', label=key)

    plt.legend()
    plt.title('Trajectories')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


directory = "./out/"
files = load_images_from_directory(directory)
res = extract_contour_coordinates(files)
plot_trajectories(res)
