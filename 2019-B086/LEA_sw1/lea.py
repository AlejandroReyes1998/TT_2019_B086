# key
K = '01110111011101110111011101110111011101110111011101110111011101110111011101110111011101110111011101110111011101110111011101110111'
# plaintext
P = '00010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001'

# key schedule constants
delta = ['11000011111011111110100111011011',
         '01000100011000100110101100000010',
         '01111001111000100111110010001010',
         '01111000110111110011000011101100',
         '01110001010111101010010010011110',
         '11000111100001011101101000001010',
         '11100000010011101111001000101010',
         '11100101110001000000100101010111']

# this is defined in the paper
T = [] # round key state
RK = [] # round keys
X = [] # encryption state
C = [] # cipher text (segmented)

# segment K and P (K_s means 'segmented K' and P_s means 'segmented P')
K_s = []
P_s = []

def initialize_errthang():
    for i in range (0, 4):
        K_s.append(K[i*32:32+(i*32)])
        P_s.append(P[i*32:32+(i*32)])

        # set T[i] = K[i]
    for i in range(0, 4):
        T.append(K_s[i])

def ROL(i, x):
    # i is the number of times to rotate, x is the number to be rotated
    return x[i:] + x[:i]

def ROR(i, x):
    return x[-i:] + x[:-i]

def XOR(x, y):
    res = (int(x, 2) ^ int(y, 2))
    res = format(res, 'b').zfill(32)
    return res
    
def mod_add(x, y):
    # addition modulo 2^32
    res = (int(x, 2) + int(y, 2)) % 2**32
    res = format(res, 'b').zfill(32)
    return res

def mod_sub(x, y):
    res = (int(x, 2) - int(y, 2)) % 2**32
    res = format(res, 'b').zfill(32)
    return res

def key_schedule():
    # 128 bit key, 24 round keys. Each round key consists of 6 32 bit chunks, meaning 192 bits total for each round key
    # T's value is modified each round. Each T[i] has a different value each round
    for i in range(0, 24):
        T[0] = ROL(1, mod_add(T[0], ROL(i, delta[i % 4])))
        T[1] = ROL(3, mod_add(T[1], ROL(i+1, delta[i % 4])))
        T[2] = ROL(6, mod_add(T[2], ROL(i+2, delta[i % 4])))
        T[3] = ROL(11, mod_add(T[3], ROL(i+3, delta[i % 4])))
        auxlist = [T[0],T[1],T[2],T[1],T[3],T[1]]
        RK.append(auxlist)

def encrypt():
    # 24 rounds for 128 bit keys
    # set the 128 bit intermediate value X[0] to the plaintext P (segmented P, that is)
    X.append(P_s)
    # run the key schedule to generate 24 round keys
    key_schedule()
    for i in range(0, 24):
        # (implementation-specific) make an aux variable for X[i+1]
        aux_x = []
        aux_x.append(ROL(9, mod_add(XOR(X[i][0], RK[i][0]), XOR(X[i][1], RK[i][1]))))
        aux_x.append(ROR(5, mod_add(XOR(X[i][1], RK[i][2]), XOR(X[i][2], RK[i][3]))))
        aux_x.append(ROR(3, mod_add(XOR(X[i][2], RK[i][4]), XOR(X[i][3], RK[i][5]))))
        aux_x.append(X[i][0])
        X.append(aux_x)
        
    # finalization. set ciphertext to last encryption state (also known as X)
    for i in range(0, 4):
        C.append(X[len(X)-1][i])

def decrypt(C):
    X = []
    X.append(C)
    for i in range(0, 24):
        aux_x = []
        aux_x.append(X[i][3])
        aux_x.append(XOR(mod_sub(ROR(9, X[i][0]), XOR(X[i][3], RK[len(RK)-1-i][0])), RK[len(RK)-1-i][1]))
        aux_x.append(XOR(mod_sub(ROL(5, X[i][1]), XOR(aux_x[1], RK[len(RK)-1-i][2])), RK[len(RK)-1-i][3]))
        aux_x.append(XOR(mod_sub(ROL(3, X[i][2]), XOR(aux_x[2], RK[len(RK)-1-i][4])), RK[len(RK)-1-i][5]))
        X.append(aux_x)

    auxstr = ""
    for i in range(0, 4):
        auxstr += X[len(X)-1][i]

    print("decrypted value is ", auxstr)
    
def main():
    initialize_errthang()
    encrypt()
    print("K's value is ", K)
    print("P's value is ", P)
    print("C's value is ", C)
    decrypt(C)
    
main()
