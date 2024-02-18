import numpy as np
import AES_box as box

def SubWord(Key):
    for i in range(len(Key)):
        x = Key[i] / 16
        y = Key[i] % 16
        Key[i] = box.Sbox[int(x)][int(y)]
    return Key

def RotWord(Key):
    keyroll = np.roll(Key,-1)
    Key = keyroll
    return Key

def KeyExpansion(Key,Rcon):
    temp_Key = np.array(Key.T)
    Rcon_XOR_key = np.array(temp_Key[3])
    Rcon_XOR_key = RotWord(Rcon_XOR_key)
    SubWord(Rcon_XOR_key)
    Rcon_XOR_key[0] ^= Rcon
    for j in range(4):
        if j == 0:
            temp_Key[0] ^= Rcon_XOR_key
        else:
            temp_Key[j] ^= temp_Key[j-1]
    Key = temp_Key.T
    return Key