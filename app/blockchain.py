from hashlib import sha256


def binary_to_256(string):
    '''Takes hex hash string and turns it into binary 256 string'''
    string = bin(int(string,16))[2:]
    num_of_zeros = 256-len(string)
    return '0' * num_of_zeros + string


def calculate_hash(hashable, complexity):
    '''Server mining func
    While first nums of hash not equal zeros, count hash'''
    proof = 1
    hash_ = sha256((hashable+str(proof)).encode()).hexdigest()
    bin_hash_ = binary_to_256(hash_)

    while bin_hash_[:complexity] != '0'*complexity:
        hash_ = sha256((hashable + str(proof)).encode()).hexdigest()
        bin_hash_ = binary_to_256(hash_)
        proof += 1
    return hash_, proof


def count_balance(blockchain, username):
    '''Get all blocks relative to user and count balance from them'''
    username = username.lower()
    balance = 0
    for block in blockchain:
        if block.transaction['debtor'] == block.transaction['creditor']:
            continue
        elif block.transaction['creditor'] == username:
            balance -= block.transaction['amount']
        elif block.transaction['debtor'] == username:
            balance += block.transaction['amount']
        print(balance)
    return balance
