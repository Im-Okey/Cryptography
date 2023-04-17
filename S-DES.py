encrypted_word = []
decoded_word = []


# Функция-меню
def main_menu():
    while True:
        print('1.Зашифровать слово')
        print('2.Расшифровать слово')
        print('3.Закончить выполнение программы')
        print('Ваш выбор: ', end='')
        match choice := int(input()):
            case 1:
                word = input('Введите фразу: ')
                print('Зашифрованное слово: ', *encrypt(word))
            case 2:
                print('Расшифрованное слово: ', *decoding())
            case 3:
                exit(0)


# Функция шифрования слова
def encrypt(word: str):
    first_key, second_key = key_generator()
    word = encode(word)
    for i in word:
        encrypted_word.append(letter_encrypt(list(i), first_key, second_key))
    return [decode([''.join(i)]) for i in encrypted_word]


# Функция расшифровки
def decoding():
    first_key, second_key = key_generator()
    for i in encrypted_word:
        first_decode_permutation = ip_permutation(i)
        decoded_word.append(letter_decode(first_decode_permutation, first_key, second_key))
    return [decode([''.join(i)]) for i in decoded_word]


# Функция расшифровки буквы
def letter_decode(letter: list, first_key: list, second_key: list):
    second_round_letter = encrypt_round(letter, second_key)
    swap_sides = second_round_letter[4:] + second_round_letter[0:4]
    first_round_letter = encrypt_round(swap_sides, first_key)
    result_letter = ip_last_permutation(first_round_letter)
    return result_letter


# функция шифровки буквы в двоичный код
def encode(word):
    return list(map(lambda x: "{0:b}".format(ord(x)).zfill(8), word))


# Функция дешифрлвания двоичного кода в букву
def decode(lst):
    return ''.join(map(lambda x: chr(int(x, 2)), lst))


# Функция шифрования одной буквы
def letter_encrypt(letter: list, first_key: list, second_key: list):
    permutation_letter = ip_permutation(letter)
    first_round_letter = encrypt_round(permutation_letter, first_key)
    swap_sides = first_round_letter[4:] + first_round_letter[0:4]
    second_round_letter = encrypt_round(swap_sides, second_key)
    result_letter = ip_last_permutation(second_round_letter)
    return result_letter


# Функция перестановки правилом IP-1
def ip_last_permutation(second_round_letter: list) -> list:
    ip_last_list = [3, 0, 2, 4, 6, 1, 7, 5]
    permutation_ip_last = [second_round_letter[i] for i in ip_last_list]
    return permutation_ip_last


# Функция шифрования первый раунд
def encrypt_round(permutation_letter, key) -> list:
    expanded_permutation_letter_right_side = expand(permutation_letter)
    permutation_letter_xor = letter_key_xor(expanded_permutation_letter_right_side, key)
    letter_from_s_box_left_side = s_box_left_side(left_side := permutation_letter_xor[0:4])
    letter_from_s_box_right_side = s_box_right_side(right_side := permutation_letter_xor[4:])
    result_box_processing = list(str(letter_from_s_box_left_side) + str(letter_from_s_box_right_side))
    permutation_letter_after_p4 = p4_permutation(result_box_processing)
    result_xor_with_left_side = letter_key_xor(permutation_letter_after_p4, permutation_letter[0:4])
    result_encrypted_letter = result_xor_with_left_side + permutation_letter[4:]
    return result_encrypted_letter


# Функция перестановки правилом P4
def p4_permutation(result_box_processing: list) -> list:
    p4_list = [1, 3, 2, 0]
    permutation_p4 = [result_box_processing[i] for i in p4_list]
    return permutation_p4


# Функция обработки левой части с помощью S-Box
def s_box_left_side(left_side: list) -> str:
    s_box_for_left_side = [['1', '0', '3', '2'], ['3', '2', '1', '0'],
                           ['0', '2', '1', '3'], ['3', '1', '3', '2']]
    row = int(left_side[0] + left_side[-1], 2)
    column = int(left_side[1] + left_side[2], 2)
    return str(bin(int(s_box_for_left_side[row][column]))[2:]).rjust(2, '0')


# Функция обработки правой части с помощью S-Box
def s_box_right_side(right_side: list) -> str:
    s_box_for_left_side = [['0', '1', '2', '3'], ['2', '0', '1', '3'],
                           ['3', '0', '1', '0'], ['2', '1', '0', '3']]
    row = int(right_side[0] + right_side[-1], 2)
    column = int(right_side[1] + right_side[2], 2)
    return str(bin(int(s_box_for_left_side[row][column]))[2:]).rjust(2, '0')


# Функция XOR для расширенной правой части и ключа
def letter_key_xor(expanded_permutation_letter_right_side: list, key: list) -> list:
    permutation_letter_xor = []
    for i in range(len(expanded_permutation_letter_right_side)):
        permutation_letter_xor.append('0' if expanded_permutation_letter_right_side[i] == key[i] else '1')
    return permutation_letter_xor


# Функция расширения
def expand(permutation_letter: list) -> list:
    permutation_right_side = ep_permutation(right_side := permutation_letter[4:])
    return permutation_right_side


# Функция перестановки правилом E/P
def ep_permutation(right_side: list) -> list:
    ep_list = [3, 0, 1, 2, 1, 2, 3, 0]
    permutation_right_side = [right_side[i] for i in ep_list]
    return permutation_right_side


# Функция перестановки правилом IP
def ip_permutation(letter: list) -> list:
    ip_list = [1, 5, 2, 0, 3, 7, 4, 6]
    permutation_letter = [letter[i] for i in ip_list]
    return permutation_letter


# Функция для ввода основного первичного ключа
def key_generator() -> [list, list]:
    first_key = first_key_generator(list(str(1001010011)))
    second_key = second_key_generator(list(str(1001010011)))
    return first_key, second_key


# Функция генерации первого ключа
def first_key_generator(start_key: list) -> list:
    permutation_key = p10_permutation(start_key)
    shifted_key = shift(permutation_key, 1)
    return p8_permutation(shifted_key)


# Функция генерации второго ключа
def second_key_generator(start_key: list) -> list:
    permutation_key = p10_permutation(start_key)
    shifted_key = shift(permutation_key, 3)
    return p8_permutation(shifted_key)


# Функция перестановки правилом P10
def p10_permutation(start_key: list) -> list:
    p10_list = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    permutation_key = [start_key[i] for i in p10_list]
    return permutation_key


# Функция перестановки правилом P8
def p8_permutation(shifted_key: list) -> list:
    p8_list = [5, 2, 6, 3, 7, 4, 9, 8]
    permutation_key = [shifted_key[i] for i in p8_list]
    return permutation_key


# Функция сдвиг на заданное значение
def shift(permutation_key: list, shift_position: int) -> list:
    left_side = permutation_key[0:5][shift_position:] + permutation_key[0:5][:shift_position]
    right_side = permutation_key[5:][shift_position:] + permutation_key[5:][:shift_position]
    return left_side+right_side


if __name__ == '__main__':
    main_menu()
