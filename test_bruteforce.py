import hashlib
import itertools

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def brute_force():
    target_hash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    
    charset = "abc"   
    max_length = 3

    attempts = 0

    for length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=length):
            guess = ''.join(guess)
            attempts += 1

            print("Trying:", guess)   

            if hash_password(guess) == target_hash:
                print("\n[+] Found:", guess)
                print("[+] Attempts:", attempts)
                return

    print("[-] Password not found")

brute_force()
