import re

def deterministic_shuffle(chunk):
    permutation_order = [8,6,9,5,7,3,1,4,0,2]

    shuffled_chunk = [chunk[i] for i in permutation_order if i < len(chunk)]

    return ''.join(shuffled_chunk)


def jumble_hex(hex_string):
    hex_string = hex_string.replace(' ', '')
    hex_chunks = re.findall('.{2}', hex_string)
    hex_chunks = [hex_chunks[i:i+10] for i in range(0, len(hex_chunks), 10)]

    for i, chunk in enumerate(hex_chunks):
        hex_chunks[i] = deterministic_shuffle(chunk)

    shuffled_hex = ''.join([''.join(chunk) for chunk in hex_chunks])
    shuffled_hex = ' '.join(shuffled_hex[i:i+2] for i in range(0, len(shuffled_hex), 2))
    return shuffled_hex


def main():
    with open('private_original', 'r') as file:
        hex_string = file.read().replace('\n', '')

    shuffled_hex = jumble_hex(hex_string)

    print("Shuffled Hex:")
    print(shuffled_hex)

    with open('private', 'w') as file:
        file.write(shuffled_hex)


if __name__ == "__main__":
    main()