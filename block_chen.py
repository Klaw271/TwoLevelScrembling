import random
import pickle
from encryption import *
import imageio.v2 as imageio


# Блочное скремблирование
def block_encrypt_image(image_path, block_size, output_path):
    # Открываем изображение
    image = Image.open(image_path)
    image = image.convert('RGB')  # Убедимся, что изображение в формате RGB

    # Преобразуем изображение в массив numpy
    img_array = np.array(image)
    height, width, channels = img_array.shape

    # Проверяем, чтобы размеры изображения делились на размер блока
    if height % block_size != 0 or width % block_size != 0:
        raise ValueError("Размеры изображения должны быть кратны размеру блока.")

    # Разбиваем изображение на блоки
    blocks = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = img_array[y:y + block_size, x:x + block_size]
            blocks.append(block)

    # Создаем список индексов и перемешиваем их
    indices = list(range(len(blocks)))
    random.shuffle(indices)

    # Сохраняем ключ (порядок блоков) в файл
    with open("key1.txt", 'wb') as key_file:
        pickle.dump(indices, key_file)

    # Перемешиваем блоки в соответствии с индексами
    scrambled_blocks = [blocks[i] for i in indices]

    # Создаем новое изображение из перемешанных блоков
    scrambled_array = np.zeros_like(img_array)
    idx = 0
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            scrambled_array[y:y + block_size, x:x + block_size] = scrambled_blocks[idx]
            idx += 1

    # Преобразуем массив обратно в изображение
    scrambled_image = Image.fromarray(scrambled_array)

    # Сохраняем новое изображение
    scrambled_image.save(output_path)

def block_decrypt_image(image_path, block_size, encoded_key, output_path):
    # Открываем скрэмблированное изображение
    scrambled_image = Image.open(image_path)
    scrambled_image = scrambled_image.convert('RGB')

    # Преобразуем изображение в массив numpy
    scrambled_array = np.array(scrambled_image)
    height, width, channels = scrambled_array.shape

    # Загружаем ключ (порядок блоков)
    with open(f"key{encoded_key}.txt", 'rb') as key_file:
        indices = pickle.load(key_file)

    # Разбиваем скрэмблированное изображение на блоки
    scrambled_blocks = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = scrambled_array[y:y + block_size, x:x + block_size]
            scrambled_blocks.append(block)

    # Восстанавливаем исходный порядок блоков
    blocks = [None] * len(scrambled_blocks)
    for original_idx, scrambled_idx in enumerate(indices):
        blocks[scrambled_idx] = scrambled_blocks[original_idx]

    # Создаем восстановленное изображение
    descrambled_array = np.zeros_like(scrambled_array)
    idx = 0
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            descrambled_array[y:y + block_size, x:x + block_size] = blocks[idx]
            idx += 1

    # Преобразуем массив обратно в изображение
    descrambled_image = Image.fromarray(descrambled_array)

    # Сохраняем восстановленное изображение
    descrambled_image.save(output_path)

# Основная функция
def main():
    # Шаг 1. Вводим путь до изображения
    image_input = input("Введите путь/название картинки с его расширением: ")
    block_size = int(input("Введите размер блока: "))
    original_image = imageio.imread(image_input)

    # Шаг 2. Скремблирование методами блоков и Чена
    block_encrypt_image(image_input, block_size, "encrypted_first.png")
    encrypted_image, permutation = Encrypt_chen_system("encrypted_first.png", "encrypted_final.png", a=35, b=3, c=28, initial_state=[1.0, 1.0, 1.0],
                                                       t=np.linspace(0, 100,
                                                                        original_image.shape[0] * original_image.shape[1]))

    # Шаг 3. Дескремблирование методами Чена и блоков
    Decrypt_chen_system("encrypted_final.png","decrypted_first.png", permutation)
    block_decrypt_image("decrypted_first.png", block_size, 1, "decrypted_final.png")

    Display_images(original_image, "encrypted_first.png", "encrypted_final.png","decrypted_first.png","decrypted_final.png", 'Hyper chaotic chen system scrambling')




if __name__ == "__main__":
    main()