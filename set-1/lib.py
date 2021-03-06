decoder_16 = {'1': 1, '0': 0, '3': 3, '2': 2, '5': 5, '4': 4, '7': 7, '6': 6,
              '9': 9, '8': 8, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14,
              'f': 15}

decoder_64 = {'=': 0, '+': 62, '/': 63, '1': 53, '0': 52, '3': 55, '2': 54, '5': 57,
              '4': 56, '7': 59, '6': 58, '9': 61, '8': 60, 'A': 0, 'C': 2,
              'B': 1, 'E': 4, 'D': 3, 'G': 6, 'F': 5, 'I': 8, 'H': 7, 'K': 10,
              'J': 9, 'M': 12, 'L': 11, 'O': 14, 'N': 13, 'Q': 16, 'P': 15,
              'S': 18, 'R': 17, 'U': 20, 'T': 19, 'W': 22, 'V': 21, 'Y': 24,
              'X': 23, 'Z': 25, 'a': 26, 'c': 28, 'b': 27, 'e': 30, 'd': 29,
              'g': 32, 'f': 31, 'i': 34, 'h': 33, 'k': 36, 'j': 35, 'm': 38,
              'l': 37, 'o': 40, 'n': 39, 'q': 42, 'p': 41, 's': 44, 'r': 43,
              'u': 46, 't': 45, 'w': 48, 'v': 47, 'y': 50, 'x': 49, 'z': 51}

encoder_16 = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
              8: '8', 9: '9', 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e',
              15: 'f'}

encoder_64 = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
              8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
              15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V',
              22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'a', 27: 'b', 28: 'c',
              29: 'd', 30: 'e', 31: 'f', 32: 'g', 33: 'h', 34: 'i', 35: 'j',
              36: 'k', 37: 'l', 38: 'm', 39: 'n', 40: 'o', 41: 'p', 42: 'q',
              43: 'r', 44: 's', 45: 't', 46: 'u', 47: 'v', 48: 'w', 49: 'x',
              50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3', 56: '4',
              57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62: '+', 63: '/'}


# Take care of padding problem in special case
def base_64_to_ascii(input_data):
    answer = int_to_ascii(base_64_to_int(input_data))
    while len(answer) < 3 * len(input_data) / 4:
        answer = chr(0) + answer
    return answer


# _          _       _
#| |_ ___   (_)_ __ | |_
#| __/ _ \  | | '_ \| __|
#| || (_) | | | | | | |_
# \__\___/  |_|_| |_|\__|


def base_n_to_int(base_n_input, n, decoder_n):
    output = 0
    for letter in base_n_input:
        output *= n
        output += decoder_n(letter)
    return output


# Special cases


def hex_to_int(hex_input):
    return base_n_to_int(hex_input, 16, lambda x: decoder_16[x])


def base_64_to_int(base_64_input):
    return base_n_to_int(base_64_input, 64, lambda x: decoder_64[x])


def ascii_to_int(ascii_input):
    return base_n_to_int(ascii_input, 256, ord)


#   __                       _       _
#  / _|_ __ ___  _ __ ___   (_)_ __ | |_
# | |_| '__/ _ \| '_ ` _ \  | | '_ \| __|
# |  _| | | (_) | | | | | | | | | | | |_
# |_| |_|  \___/|_| |_| |_| |_|_| |_|\__|


def int_to_base_n(int_input, n, encoder_n):
    output = ""
    while int_input > 0:
        output = encoder_n(int_input % n) + output
        int_input /= n
    return output


# Special cases


def int_to_hex(int_input):
    return int_to_base_n(int_input, 16, lambda x: encoder_16[x])


def int_to_base_64(int_input):
    return int_to_base_n(int_input, 64, lambda x: encoder_64[x])


def int_to_ascii(int_input):
    return int_to_base_n(int_input, 256, chr)


#       _       _
#   ___(_)_ __ | |__   ___ _ __
#  / __| | '_ \| '_ \ / _ \ '__|
# | (__| | |_) | | | |  __/ |
#  \___|_| .__/|_| |_|\___|_|
#        |_|


# Likelihood that a string is cleartext
def score(cleartext):
    answer = 0
    for letter in cleartext:
        code = ord(letter)
        if 64 < code < 91 or code == 32 or 96 < code < 123:
            answer += 1
    return answer


# The bitwise xor of two strings, truncated to length of shortest
def xor_ascii(key, cipher):
    return "".join((chr(ord(a) ^ ord(b)) for (a, b) in zip(key, cipher)))


# Decodes cipher by xoring with key (repeated as necessary)
def xor_ascii_repeated(key_ascii, cipher):
    while len(key_ascii) < len(cipher):
        key_ascii = key_ascii + key_ascii
    return xor_ascii(key_ascii, cipher)


# Return Hamming distance between two ascii strings
def hamming_distance(a, b):
    bits = ascii_to_int(xor_ascii(a, b))
    ans = 0
    while bits > 0:
        ans += 1 if bits % 2 == 1 else 0
        bits /= 2
    return ans


# Return key and cleartext maximizing score
def crack_brute_force(cipher_text, key_set, decrypt_fn, score_fn):
    return max(
        ((k, decrypt_fn(k, cipher_text))
         for k in key_set), key=lambda x: score_fn(x[1])
    )
