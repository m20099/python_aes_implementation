import numpy as np
import AES_subkey as subkey
import AES_cipher as cipher
import AES_inverse as Inverse
np.set_printoptions(formatter={'int': '{:02x}'.format})

def main():
    #from「nist.fips.197.pdf」p33, "AppendixB - Cipher Example"
    #Plain-text = (3243f6a8 885a308d 313198a2 e0370734)
    Input = np.array([
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34]
    ])
    
    #Key = (2b7e1516 28aed2a6 abf71588 09cf4f3c)
    Cipher_Key = np.array([
        [0x2b, 0x28, 0xab, 0x09],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c]
    ])
    
    Rcon = np.array([0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36])  
    
    Output = np.array(Input)
    
    #Cipher
    Output ^= Cipher_Key
    Keep_Key = np.array(Cipher_Key)
    for Round in range(10):
        if Round == 0:
            Round_Key = np.array(subkey.KeyExpansion(Cipher_Key, Rcon[Round]))
        else:
            Round_Key = np.array(subkey.KeyExpansion(Round_Key, Rcon[Round]))
        Keep_Key = np.insert(Keep_Key, 0, Round_Key, axis=0)
        
        Output = cipher.SubBytes(Output)
        Output = cipher.ShiftRows(Output)
        if Round != 9:
            cipher.MixColumns(Output)
        Output ^= Round_Key

    #Inverse_Cipher
    InvOutput = np.array(Output)
    for Round in range(10):
        InvOutput ^= Keep_Key[Round*4:(Round+1)*4]
        if Round != 0:
            InvOutput = Inverse.InvMixColumns(InvOutput)
        InvOutput = Inverse.InvShiftRows(InvOutput)
        InvOutput = Inverse.InvSubBytes(InvOutput)
    InvOutput ^= Keep_Key[(Round+1)*4:(Round+2)*4]
    
    print("Plain-text")
    print(Input)
    print("\nCipher-text")
    print(Output)
    print("\nDecryption")
    print(InvOutput)

main()
