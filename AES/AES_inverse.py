import numpy as np
import AES_box as box

def InvShiftRows(state):
    tempstate = np.array(state)
    for i in range(4):
        tempstate[i] = np.roll(tempstate[i], i)
    state = tempstate
    return state

def InvSubBytes(state):
    x = np.array(state / 16, dtype=int)
    y = np.array(state % 16, dtype=int)
    for i in range(4):
        for j in range(4):
            state[i][j] = box.Inverse_Sbox[x[i][j]][y[i][j]]
    return state

def galois(n,state):
    result = 0
    for _ in range(8):
        if state & 1:
            result ^= n
        highest_bit = n & 0x80
        n = (n << 1) & 0xFF         
        if highest_bit:
            n ^= 0x1b
        state >>= 1
    return result

def InvMixColumns(state):
    tempstate = np.zeros((4,4))
    for j in range(4):
        tempstate[0][j] = galois(0x0e,state[0][j]) ^ galois(0x0b,state[1][j]) ^ galois(0x0d,state[2][j]) ^ galois(0x09,state[3][j])
        tempstate[1][j] = galois(0x09,state[0][j]) ^ galois(0x0e,state[1][j]) ^ galois(0x0b,state[2][j]) ^ galois(0x0d,state[3][j])
        tempstate[2][j] = galois(0x0d,state[0][j]) ^ galois(0x09,state[1][j]) ^ galois(0x0e,state[2][j]) ^ galois(0x0b,state[3][j])
        tempstate[3][j] = galois(0x0b,state[0][j]) ^ galois(0x0d,state[1][j]) ^ galois(0x09,state[2][j]) ^ galois(0x0e,state[3][j])
        
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = int(tempstate[i][j])
    return state