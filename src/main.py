import random
import string
import rsa
import os

def pass_generation():
    total = string.ascii_letters + string.digits + string.punctuation
    length = 30
    password = "".join(random.sample(total, length))
    return password

def keys_generation():
    (key_public, key_private) = rsa.newkeys(2048) #keysize(bits)
    with open('private_key.pem', mode='wb') as private_file:
        private_file.write(key_private.save_pkcs1()) 
    with open('public_key.pem', mode='wb') as public_file:
        public_file.write(key_public.save_pkcs1())

def load_private_keys():
    with open('private_key.pem', mode='rb') as privatefile:
        privkey = rsa.PrivateKey.load_pkcs1(privatefile.read())
    return privkey


def load_public_keys():
    with open('public_key.pem', mode='rb') as publicfile:
        pubkey = rsa.PublicKey.load_pkcs1(publicfile.read())
    return pubkey


def pass_encryption(filename):
    passw = pass_generation()
    message = passw.encode('utf8')
    crypto = rsa.encrypt(message, load_public_keys())
    with open(filename, mode='wb') as encryptedfile:
        encryptedfile.write(crypto)

def pass_decryption(filename):
    with open(filename, "rb") as f:
        crypto = f.read()
    message = rsa.decrypt(crypto, load_private_keys())
    passw = message.decode('utf8')
    print(passw)


def main():
    #keys_generation()
    if (os.path.isfile("private_key.pem") and os.path.isfile("public_key.pem")) :
        load_private_keys()
        load_public_keys()
        print("you have those passwords:")
        files = os.listdir()
        for file in files:
            if os.path.isfile(file):
                print(file)
        question = input("do you want to add or get a password? add/get: ")
        if question == 'get':
            filename = input("what password do you want to see?: ")
            pass_decryption(filename)
        elif question == 'add':
            filename = input("what password do you want to add?: ")
            pass_encryption(filename)
        else: 
            print("add or get???")
            exit
    
    else:
        q = input("do you want to generate keys? yes/no: ")
        if q == 'yes':
            keys_generation()
        elif q == "no":
            print("please upload the keys!")
        else:
            print("yes or no???")
            exit

if __name__ == "__main__":
    main()