import os
import sys


# Меню
def main_menu():
    while True:
        print('1.Зашифровать слово\n'
              '2.Расшифровать слово\n'
              '3.Закончить выполнение программы\n'
              'Ваш выбор: ', end='')
        match choice := int(input()):
            case 1:
                text = input('Введите фразу: ')
                encrypt(text)
            case 2:
                print('Расшифрованное слово: ', decrypt())
            case 3:
                exit(0)


# Функция для открытия файлов с картинками
def file_open(start_bmp, encoded_bmp, text, degree) -> tuple:
    # Проверка чтобы длинна текста не превышала размер картинки
    text_len = len(text)
    img_len = os.stat(start_bmp).st_size
    return open(start_bmp, 'rb'), open(encoded_bmp, 'wb') if (img_len * degree / 8) - 54 >= text_len else None


def file_close(start_bmp, encoded_bmp):
    start_bmp.close()
    encoded_bmp.close()


def create_masks(degree) -> tuple:
    text_mask, img_mask = 0b11111111, 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


def decrypt() -> str:
    # Вводим глубину шифровки
    degree = int(input("Введите глубину шифровки(количество заменяемых бит): "))
    to_read = int(input('Сколько символов сообщения считать из файла: '))
    # Открываем полученный файл
    encoded_bmp = open('encoded.bmp', 'rb')

    encoded_text = ''

    # Пропускаем первые 54 служебных символа
    encoded_bmp.seek(54)

    # Формируем маски для текста и картинки для дальнейшей замены младших битов
    text_mask, img_mask = create_masks(degree)
    img_mask = ~img_mask

    read = 0
    while read < to_read:
        letter = 0
        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask

            letter <<= degree
            letter |= img_byte
        print('Letter #{0} is {1:c}'.format(read, letter))
        read += 1
        encoded_text += chr(letter)

    encoded_bmp.close()
    return encoded_text


# Функция шифрования
def encrypt(text: str):
    # Выбираем глубину шифровки
    degree = int(input("Введите глубину шифровки(количество заменяемых бит): "))

    # Открываем файлы с картинками на чтение для дальнейшей работы
    start_bmp, encoded_bmp = file_open('start.bmp', 'encoded.bmp', text, degree)

    # Записываем первые 54 символа в зашифрованную картинку
    encoded_bmp.write(start_bmp.read(54))

    # Формируем маски для текста и картинки для дальнейшей замены младших битов
    text_mask, img_mask = create_masks(degree)

    # Проходим циклом по каждой букве сообщения
    for letter in text:
        print('Letter {0}, bin {1:b}'.format(letter, ord(letter)))
        letter = ord(letter)
        # Задаем шаг с которым будем двигаться по битам 1 байта изображения в зависимости
        # от количества заменяемых младших битов
        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(start_bmp.read(1), sys.byteorder) & img_mask
            bits = letter & text_mask
            bits >>= (8 - degree)

            img_byte |= bits

            encoded_bmp.write(img_byte.to_bytes(1, sys.byteorder))
            letter <<= degree
    encoded_bmp.write(start_bmp.read())
    # Закрываем файлы с картинками
    file_close(start_bmp, encoded_bmp)


if __name__ == '__main__':
    main_menu()