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
    with open('./keys/private_key.pem', mode='wb') as private_file:
        private_file.write(key_private.save_pkcs1()) 
    with open('./keys/public_key.pem', mode='wb') as public_file:
        public_file.write(key_public.save_pkcs1())

def load_private_keys():
    with open('./keys/private_key.pem', mode='rb') as privatefile:
        privkey = rsa.PrivateKey.load_pkcs1(privatefile.read())
    return privkey

def load_public_keys():
    with open('./keys/public_key.pem', mode='rb') as publicfile:
        pubkey = rsa.PublicKey.load_pkcs1(publicfile.read())
    return pubkey

def pass_encryption(filename, passw):
    message = passw.encode('utf8')
    crypto = rsa.encrypt(message, load_public_keys())
    with open(f'./passwords/{filename}', mode='wb') as encryptedfile:
        encryptedfile.write(crypto)

def pass_decryption(filename):
    with open(f'./passwords/{filename}', "rb") as f:
        crypto = f.read()
    message = rsa.decrypt(crypto, load_private_keys())
    passw = message.decode('utf8')
    print(passw)

def list_of_passwords():
    print("you have those passwords:")
    files = os.listdir('./passwords/')
    for file in files:
        print(file)

def main():
    if (os.path.isfile("./keys/private_key.pem") and os.path.isfile("./keys/public_key.pem")) :
        load_private_keys()
        load_public_keys()
        question = input("do you want to add or get a password? add/get: ")
        if question == 'get':
            list_of_passwords()
            filename = input("what password do you want to see?: ")
            files = os.listdir('./passwords/')
            if filename in files:
                pass_decryption(filename)
            else:
                print(f'you dont have password for {filename} ')
                main()
        elif question == 'add':
            filename = input("what password do you want to add?: ")
            passw = pass_generation()
            pass_encryption(filename, passw)
        else: 
            print("add or get???")
            main()
    else:
        q = input("do you want to generate keys? yes/no: ")
        if q == 'yes':
            keys_generation()
            main()
        elif q == "no":
            print("please upload the keys!")
        else:
            print("yes or no???")
            main()

if __name__ == "__main__":
    main()