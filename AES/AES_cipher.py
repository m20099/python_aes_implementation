import numpy as np
import AES_box as box

def SubBytes(state):
    x = np.array(state / 16, dtype=int)
    y = np.array(state % 16, dtype=int)
    for i in range(4):
        for j in range(4):
            state[i][j] = box.Sbox[x[i][j]][y[i][j]]
    return state

def ShiftRows(state):
    tempstate = np.array(state)
    for i in range(4):
        tempstate[i] = np.roll(tempstate[i], -i)
    state = tempstate
    return state

def Shift(num,state):
    if num == 2:
        state = state<<1
    elif num == 3:
        state = state<<1 ^ state
    if state > 0xff:
        state = state ^ 0x11b
    return state

def MixColumns(state):
    tempstate = np.zeros((4,4))
    for j in range(4):
        tempstate[0][j] = Shift(2,state[0][j]) ^ Shift(3,state[1][j]) ^ state[2][j] ^ state[3][j]
        tempstate[1][j] = state[0][j] ^ Shift(2,state[1][j]) ^ Shift(3,state[2][j]) ^ state[3][j]
        tempstate[2][j] = state[0][j] ^ state[1][j] ^ Shift(2,state[2][j]) ^ Shift(3,state[3][j])
        tempstate[3][j] = Shift(3,state[0][j]) ^ state[1][j] ^ state[2][j] ^ Shift(2,state[3][j])
    for i in range(4):
        for j in range(4):
            state[i][j] = int(tempstate[i][j])
    return state