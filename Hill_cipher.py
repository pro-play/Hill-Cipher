import numpy as np
import string
import math
import re
import time
#use pip install egcd
from egcd import egcd


#creating an index for char to int
index_ctoi = dict()
list_of_alphabets = list(string.ascii_lowercase)
for i in range(0,26):
    index_ctoi[list_of_alphabets[i]] = i
    
#creating an index for int to char
index_itoc = dict()
list_of_alphabets = list(string.ascii_lowercase)
for i in range(0,26):
    index_itoc[i] = list_of_alphabets[i]


#Check if matrix is invertible or not
def check(key):
    if(np.linalg.det(key)):
        return True
    
    else:
        return False
 
#To generate the key matrix with integers
def get_key_matrix(key):
    size = len(key)
    n = int(math.sqrt(size))
    key = list(key)
    key_matrix = np.ones([n,n])
    k = 0
    for i in range(0,n):
        for j in range(0,n):
            key_matrix[i][j] = int(index_ctoi[key[k]])
            k+=1
    return key_matrix

#to generate integer matrix for plain text  
def get_matrix(mat):
    num_mat = np.ones([1,len(mat)])
    for i in range(0,len(mat)):
        num_mat[0][i] = index_ctoi[mat[i]]
    return num_mat

#To get text from integer matrix   
def get_text(cipher_matrix):
    text = ""
    cipher_text = cipher_matrix.tolist()
    for i in cipher_text[0]:
        text += index_itoc[i]
    return text

#padding message for matrix multiplication
def pad(message,n):
    
    if(len(message)%n == 0):
        return message
    
    else:
        pad_len = n-(len(message)%n)
        
        for i in range(0,pad_len):
            message+='x'
            
        return message
   
def get_adj_of_key(key):
    det = int(np.round(np.linalg.det(key)))
    return np.round(det * np.linalg.inv(key)).astype(int)

def get_mod_inv(value):
    return egcd(value,26)[1]%26

#encrypting the message into cipher text
def encrypt(message,key):
    size = len(key)
    ciphertext = ""
    key = get_key_matrix(key)
    n = int(math.sqrt(size)) # n*n matrix 
    message = pad(message,n)
    
    if(check(key)):
        for i in range(0,len(message),n):
            mat = message[i : (n+i)]
            mat = list(mat)
            mat = get_matrix(mat)
            cipher_matrix = np.dot(mat,key)%26
            ciphertext += get_text(cipher_matrix)
        return ciphertext
    
    else:
        print("Key doesn't have an inverse")
        

def decrypt(ciphertext,key):
    plaintext =""
    size = len(key)
    key = get_key_matrix(key)
    key_adj = get_adj_of_key(key).astype(int)
    # print(key_adj)
    
    n = int(math.sqrt(size))
    for i in range(0,len(ciphertext),n):
        mat = ciphertext[i:(n+i)]
        mat = list(mat)
        mat = get_matrix(mat).astype(int)
        det = int(round(np.round(np.linalg.det(key))))
        mod_inv = get_mod_inv(det)
        res =(np.dot(mat,key_adj))
        plain_matrix =( mod_inv * res)%26
        plaintext += get_text(plain_matrix)
    return plaintext


if __name__ == "__main__":
    message  = input("Enter the plain text : ")
    message = message.replace(" ", "")
    message = message.lower()
    message = re.sub(r'[^\w]', '', message)
    key = input("Enter a key who's size is a 'perfect square number' : ")
    
    while(math.gcd(round(np.linalg.det(get_key_matrix(key))).astype(int),26) != 1):
        key = input("Enter a key who's det is a coprime with 26 :")
        
    initial_message_lenght = len(message)
    key = key.lower()
    
    #encrypting message
    ciphertext = encrypt(message,key)
    cipher_text = ciphertext[0:initial_message_lenght]
    print("\nCiphertext is : ",cipher_text)
    
    #decrypting message
    plaintext = decrypt(ciphertext,key)
    plaintext = plaintext[0:initial_message_lenght]
    print("Plaintext is  : ",plaintext)
    print("\nTo kill the program press 'ctrl+c' :")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
            
