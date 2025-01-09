import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from PIL import Image

def chen_system(state, t, a, b, c):
    x, y, z = state
    return [a * (y - x), (c - a) * x - x * z + c * y, x * y - b * z]


def Encrypt_chen_system(imagex,output_path, a, b, c, initial_state, t):
    image = np.copy(Image.open(imagex).convert('RGB'))
    if len((np.asarray(image)).shape) == 3:
        long = 3
    else:
        long = 1

    for channel in range(long):
        if long == 3:
            img = image[:, :, channel]
        else:
            img = image
        flat_image = img.flatten()
        solution = odeint(chen_system, initial_state, t, args=(a, b, c))
        permutation = np.argsort(solution[:, 0] % len(flat_image))
        scrambled_image = flat_image[permutation]
        scrambled_image = scrambled_image.reshape(img.shape)
        if long == 3:
            image[:, :, channel] = np.copy(scrambled_image)
        else:
            image = scrambled_image
        scrambled_image = Image.fromarray(image)
        scrambled_image.save(output_path)
    return image, permutation


def Decrypt_chen_system(imagex, output_path, permutation):
    image = np.copy(Image.open(imagex).convert('RGB'))
    if len((np.asarray(image)).shape) == 3:
        long = 3
    else:
        long = 1

    for channel in range(long):
        if long == 3:
            img = image[:, :, channel]
        else:
            img = image
        flat_image = img.flatten()
        inverse_permutation = np.argsort(permutation)
        descrambled_image = flat_image[inverse_permutation]
        descrambled_image = descrambled_image.reshape(img.shape)
        if long == 3:
            image[:, :, channel] = np.copy(descrambled_image)
        else:
            image = descrambled_image
        descrambled_image1 = Image.fromarray(image)
        descrambled_image1.save(output_path)
    return image


def Display_images(original_image, encrypted_image_1, encrypted_image_2, decrypted_image_1, decrypted_image_2, Title):
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5)
    ax1.imshow(original_image, cmap='gray')
    ax1.set_title('Original image', fontsize=7)
    ax2.imshow(Image.open(encrypted_image_1), cmap='gray')
    ax2.set_title('Block scrambling', fontsize=7)
    ax3.imshow(Image.open(encrypted_image_2), cmap='gray')
    ax3.set_title('Hyperchaotic Chen scrambling', fontsize=7)
    ax4.imshow(Image.open(decrypted_image_1), cmap='gray')
    ax4.set_title('Hyperchaotic Chen decryptinon', fontsize=7)
    ax5.imshow(Image.open(decrypted_image_2), cmap='gray')
    ax5.set_title('Block decryption', fontsize=7)
    fig.suptitle(Title, fontsize=16, y=0.88)
    fig.tight_layout()
    plt.show()