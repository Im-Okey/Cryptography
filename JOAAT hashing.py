
def encrypt(bytearray_phrase: bytearray) -> str:
    hashing: int = 0
    for i in range(len(bytearray_phrase)):
        hashing += bytearray_phrase[i]
        hashing &= 0xFFFFFFFF

        hashing += hashing << 10
        hashing &= 0xFFFFFFFF

        hashing ^= hashing >> 6
        hashing &= 0xFFFFFFFF

    hashing += hashing << 3
    hashing &= 0xFFFFFFFF

    hashing ^= hashing >> 11
    hashing &= 0xFFFFFFFF

    hashing += hashing << 15
    hashing &= 0xFFFFFFFF

    return hex(hashing).upper().replace('X', 'x')


if __name__ == '__main__':
    print(encrypt(bytearray(b'BSUIR')))
