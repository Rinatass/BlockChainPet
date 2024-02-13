from hashlib import sha256


def binary_to_256(string):
    string = bin(int(string,16))[2:]
    num_of_zeros = 256-len(string)
    return '0' * num_of_zeros + string


def calculate_hash(hashable, complexity):
    proof = 1
    hash_ = sha256((hashable+str(proof)).encode()).hexdigest()
    bin_hash_ = binary_to_256(hash_)

    while bin_hash_[:complexity] != '0'*complexity:
        hash_ = sha256((hashable + str(proof)).encode()).hexdigest()
        bin_hash_ = binary_to_256(hash_)
        proof += 1
    return hash_, proof
