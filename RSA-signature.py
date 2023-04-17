import math
import random
from sympy import isprime


def prime_generator(start, end):
    while True:
        if isprime(check := random.randint(start, end)):
            return check


def encrypt(bytearray_phrase: bytearray) -> int:
    hashing: int = 0
    for i in range(len(bytearray_phrase)):
        hashing += bytearray_phrase[i]
        hashing &= 0xF

        hashing += hashing << 10
        hashing &= 0xF

        hashing ^= hashing >> 6
        hashing &= 0xF

    hashing += hashing << 3
    hashing &= 0xF

    hashing ^= hashing >> 11
    hashing &= 0xF

    hashing += hashing << 15
    hashing &= 0xF

    return hashing


def public_e_generator(eiler_func):
    e = 65537
    while True:
        if math.gcd(e, eiler_func) == 1:
            return e
        else:
            e += 2


def get_d(e, phi):
    x, y = 0, 1
    last_x, last_y = 1, 0
    while phi != 0:
        quotient = e // phi
        e, phi = phi, e % phi
        last_x, x = x, last_x - quotient * x
        last_y, y = y, last_y - quotient * y
    return last_x % e if e != 1 else None


def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x


def rsa_generations(h, phrase) -> list:

    print(f'Хеш: {h}')
    # Генерация простых случайных чисел
    first_prime, second_prime = 0, 0
    while first_prime == second_prime:
        first_prime = prime_generator(10, 20)
        second_prime = prime_generator(10, 20)
    print(f'1 простое число: {first_prime}, 2 простое число: {second_prime}')

    # Произведение простых чисел
    product_of_primes = first_prime * second_prime
    print(f'Произведение простых чисел: {product_of_primes}')

    # Функция эйлера
    eiler_func = (first_prime - 1) * (second_prime - 1)
    print(f'Функция эйлера: {eiler_func}')

    # Выбираем открытую экспоненту, закрытую экспоненту
    e = public_e_generator(eiler_func)
    d = -1
    while d < 0:
        e = public_e_generator(eiler_func)
        d = gcd_extended(eiler_func, e)[2]
    print(f'Открытая экспонента: {eiler_func}, закрытая экспонента: {d}')

    # Открытый ключ, закрытый ключ
    open_key = [e, product_of_primes]
    private_key = [d, product_of_primes]
    print(f'Открытый ключ: {open_key}, закрытый ключ: {private_key}')

    # Подписываем сообщение
    s1 = (h ** d) % product_of_primes
    print(f'Отправленное сообщение({phrase}, {s1})')
    s2 = (s1 ** e) % product_of_primes
    print(f'Хеш образ переданный отправителем: {s2}')
    # где переданное значение это полученная фраза
    h_final = encrypt(bytearray(b'BSUIR'))
    print(f'Хеш образ полученного сообщения: {h_final}')

    return [h_final, s2]


def signature(bytearray_phrase: bytearray, phrase: str):
    # Хеширование
    h = encrypt(bytearray_phrase)
    # Вычисляем хеш начального сообщения и конечного соответсвенно
    h_final, s2 = rsa_generations(h, phrase)
    print("Подпись действительна" if h_final == s2 else "Подпись недействительна")


if __name__ == '__main__':
    signature(bytearray(b'BSUIR'), 'BSUIR')
