import re

def deterministic_unshuffle(chunk):
    permutation_order = [8,6,9,5,7,3,1,4,0,2]

    unshuffled_chunk = [chunk[i] for i in permutation_order if i < len(chunk)]

    return ''.join(unshuffled_chunk)


def unjumble_hex(hex_string):
    hex_string = hex_string.replace(' ', '')
    hex_chunks = re.findall('.{2}', hex_string)
    hex_chunks = [hex_chunks[i:i+17] for i in range(0, len(hex_chunks), 10)]

    for i, chunk in enumerate(hex_chunks):
        hex_chunks[i] = deterministic_unshuffle(chunk)
    
    unshuffled_hex = ''.join([''.join(chunk) for chunk in hex_chunks])
    unshuffled_hex = ' '.join(unshuffled_hex[i:i+2] for i in range(0, len(unshuffled_hex), 2))
    return unshuffled_hex


def main():
    with open('private', 'r') as file:
        hex_string = file.read()

    unshuffled_hex = unjumble_hex(hex_string)

    print("Unshuffled Hex:")
    print(unshuffled_hex)

    with open('private_unshuffled', 'w') as file:
        file.write(unshuffled_hex)


if __name__ == "__main__":
    main()