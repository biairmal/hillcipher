# Kelompok : 025, 042, 045
# Prak Kriptografi - Hill Cipher

import numpy as np
from egcd import egcd

alphabet = "abcdefghijklmnopqrstuvwxyz"
letterToIndex = dict(zip(alphabet,range(len(alphabet))))
indexToLetter = dict(zip(range(len(alphabet)),alphabet))

#fungsi untuk bikin string jadi matrix
def createMatrix(text, Matrix, kolom):
    #buat list kosong
    textNumber = []

    #convert dari text ke index agar nanti matrixnya angka, ya masa huruf :)
    for letter in text:
        textNumber.append(letterToIndex[letter])
    
    #hasil convert angka tadi di bentuk menjadi matrix
    index = 0
    for j in range(kolom):
        for i in range(2):
            Matrix[i][j] = textNumber[index]
            index += 1
    
    return Matrix

#fungsi untuk bikin matrix jadi string
def translateMatrix(text, Matrix, kolom):
    #buat string kosong
    text = ""
    
    #matrix angka diconvert ke huruf dan langsung ditambahin tiap elemennya ke string kosong tadi
    for i in range(kolom):
        for j in range(2):
            number = int(Matrix[j][i])
            text += indexToLetter[number]
    
    return text

#fungsi inv matrix modular
def invMatrixMod(matrix, modulo):
    det = int(np.round(np.linalg.det(matrix)))
    detInv = egcd(det, modulo)[1] % modulo
    inversedMatrixMod = detInv*np.round(det*np.linalg.inv(matrix)).astype(int) % modulo
    return inversedMatrixMod

#fungsi enkripsi dari plain jadi cipher
def encrypt(plain, keyMatrix):
    # C = K.P

    kolom = int(len(plain)/2)
    encrypted = ""
    plainMatrix = np.zeros((2,kolom)) 
    cipherMatrix = np.zeros((2,kolom))
           
    createMatrix(plain, plainMatrix,kolom)

    #mengalikan matrix key dan matrix plain
    for i in range(2):
        for j in range(kolom):
            cipherMatrix[i][j] = 0
            for x in range(2):
                #print ("i:",i," j:",j," x:",x) #cek ricek
                #print("cek :",keyMatrix[i][x])    
                cipherMatrix[i][j] += ((keyMatrix[i][x] * plainMatrix[x][j]))
            cipherMatrix[i][j] = cipherMatrix[i][j] % 26
    #print(cipherMatrix) #cek ricek

    encrypted = translateMatrix(encrypted, cipherMatrix, kolom)
    print("\n\tEncrypted Text : ",encrypted)

#fungsi dekripsi dari cipher jadi plain   
def decrypt(text, keyMatrix):
    # P = K^-1.C

    kolom = int(len(text)/2)
    decrypted = ""
    plainMatrix = np.zeros((2,kolom))
    cipherMatrix = np.zeros((2,kolom))
    keyMatrixInv = invMatrixMod(keyMatrix, len(alphabet))
    
    createMatrix(text, cipherMatrix, kolom)

    #mengalikan matrix key inverse modular dan matrix cipher
    for i in range(2):
        for j in range(kolom):
            plainMatrix[i][j] = 0
            for x in range(2):
                #print ("i:",i," j:",j," x:",x) #cek ricek
                #print("cek :",keyMatrix[i][x])    
                plainMatrix[i][j] += ((keyMatrixInv[i][x] * cipherMatrix[x][j]))
            plainMatrix[i][j] = plainMatrix[i][j] % 26
    #print(plainMatrix) #cek ricek

    decrypted = translateMatrix(decrypted, plainMatrix, kolom)
    print("\n\tDecrypted Text : ",decrypted)

#fungsi mencari K dari cipher dan plain
def findkey(plain,cipher):
    # K = C.P^-1
    keyMatrix = np.zeros((2,2))

    kolom = 2
    plainMatrix = np.zeros((2,kolom))
    cipherMatrix = np.zeros((2,kolom))

    createMatrix(plain,plainMatrix,kolom)
    createMatrix(cipher,cipherMatrix,kolom)
    plainMatrixInv = invMatrixMod(plainMatrix, len(alphabet))

    #print("plain\n",plainMatrix) #cek ricek
    #print("cipher\n",cipherMatrix) #cek ricek

    #mengalikan matrix cipher dan matrix plain inverse modular
    for i in range(2):
        for j in range(kolom):
            keyMatrix[i][j] = 0
            for x in range(2):
                #print ("i:",i," j:",j," x:",x) #cek ricek
                #print("cek :",kplainMatrix[i][x])    
                keyMatrix[i][j] += ((cipherMatrix[i][x] * plainMatrixInv[x][j]))
            keyMatrix[i][j] = keyMatrix[i][j] % 26
    print("\n\tKey Matrix : \n",keyMatrix) #cek ricek
         
def main():

    #keyMatrix = np.array([[4,5],[3,4]])
    keyMatrix = np.zeros((2,2))

    ans=True
    while ans:
        print("""\nWelcome to Hill Cipher Program!\n1. Encrypt\n2. Decrypt\n3. Find Key Matrix\n4. Exit""")
        ans=input("Please select :  ")
        if ans=="1":
            keyText = input("Input Key Text : ")
            createMatrix(keyText,keyMatrix,2)
            plaintext = input("Input your plain text : ")
            encrypt(plaintext,keyMatrix)
        elif ans=="2":
            keyText = input("Input Key Text : ")
            createMatrix(keyText,keyMatrix,2)
            ciphertext = input("Input yo1ur cipher text : ")
            decrypt(ciphertext,keyMatrix)
        elif ans=="3":
            text1 = input("Input your plain text : ")
            text2 = input("Input your cipher text : ")
            findkey(text1,text2)
        elif ans=="4":
            print("\nGoodbye...") 
            ans = None
        else:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":
    main()
