
import random
from sympy import isprime
from math import gcd as bltin_gcd


def prime_generator(start, end):
    while True:
        if isprime(check := random.randint(start, end)):
            return check


def prim_roots(modulo):
    required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo)}
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                            for powers in range(1, modulo)}]


def encrypt(m):
    m = ord(m)
    print(f'Сообщение для шифрования: {chr(m)} - {m}')
    p = prime_generator(10, 5000)  # случайное простое число
    print('Случайное простое число: ', p)
    g = prim_roots(p)[0]  # первообразый корень р
    print('Первообразый корень р: ', g)
    x = random.randint(2, p - 2)  # случайное целое число от 1 до р-1
    print('Случайное целое число от 1 до р-1, он же закрытый ключ х: ', x)
    y = pow(g, x) % p  # просто у
    print('Просто у: ', y)
    k = prime_generator(1, p - 1)
    print('Случайное целое число от 1 до р-1, k: ', k)
    a = pow(g, k) % p
    print('а: ', a)
    b = pow(y, k) * m % p
    print('b: ', b)

    print(f'Шифротекст: ("{chr(a)}" - {a}, "{chr(b)}" - {b})')
    return [p, x, a, b]


def decrypt(p, x, a, b):
    m_answer = (b * pow(a, p - 1 - x)) % p
    print(f'Расшифрованное сообщение: {chr(m_answer)} - {m_answer}')


keys_storage = []


def main():
    while True:
        print('1.Зашифровать слово')
        print('2.Расшифровать слово')
        print('3.Закончить выполнение программы')

        match choice := int(input('Ваш выбор: ')):
            case 1:
                letter = input('Введите букву: ')
                keys_storage.append(encrypt(letter))
            case 2:
                decrypt(keys_storage[0][0], keys_storage[0][1], keys_storage[0][2], keys_storage[0][3])
            case 3:
                exit(0)


if __name__ == "__main__":
    main()
