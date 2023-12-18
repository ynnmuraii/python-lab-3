import os
import shutil
import csv


def get_full_paths2(class_name: str) -> list:

    full_path = os.path.abspath('dataset2')
    image_names = os.listdir(full_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_full_paths = list(
        map(lambda name: os.path.join(full_path, name), image_class_names))
    return image_full_paths


def get_rel_paths2(class_name: str) -> list:

    rel_path = os.path.relpath('dataset2')
    image_names = os.listdir(rel_path)
    image_class_names = [name for name in image_names if class_name in name]
    image_rel_paths = list(
        map(lambda name: os.path.join(rel_path, name), image_class_names))
    return image_rel_paths


def replace_images(class_name: str) -> list:
    
    rel_path = os.path.relpath('dataset2')
    class_path = os.path.join(rel_path, class_name)
    image_names = os.listdir(class_path)
    image_rel_paths = list(
        map(lambda name: os.path.join(class_path, name), image_names))
    new_rel_paths = list(
        map(lambda name: os.path.join(rel_path, f'{class_name}_{name}'), image_names))
    for old_name, new_name in zip(image_rel_paths, new_rel_paths):
        os.replace(old_name, new_name)

    os.chdir('dataset2')

    if os.path.isdir(class_name):
        os.rmdir(class_name)

    os.chdir('..')


def main() -> None:

    class1 = 'leopard'
    class2 = 'tiger'

    if os.path.isdir('dataset2'):
        shutil.rmtree('dataset2')

    old = os.path.relpath('dataset')
    new = os.path.relpath('dataset2')
    shutil.copytree(old, new)

    replace_images(class1)
    replace_images(class2)

    leopard_full_paths = get_full_paths2(class1)
    leopard_rel_paths = get_rel_paths2(class1)
    tiger_full_paths = get_full_paths2(class2)
    tiger_rel_paths = get_rel_paths2(class2)
    
    with open('paths2.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\r')
        for full_path, rel_path in zip(leopard_full_paths, leopard_rel_paths):
            writer.writerow([full_path, rel_path, class1])
        for full_path, rel_path in zip(tiger_full_paths, tiger_rel_paths):
            writer.writerow([full_path, rel_path, class2])


if __name__ == "__main__":
    main()