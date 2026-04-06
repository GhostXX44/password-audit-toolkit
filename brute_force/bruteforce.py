import hashlib
from concurrent.futures import ThreadPoolExecutor


def hash_word(word, algo):
    word = word.strip().encode()

    if algo == "md5":
        return hashlib.md5(word).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(word).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(word).hexdigest()
    else:
        return None


def check_password(word, target_hash, algo):
    return word if hash_word(word, algo) == target_hash else None


def brute_force_advanced(hash_value, wordlist, algo="sha256", threads=4):
    print(f"[+] Starting brute force ({threads} threads)...")

    with open(wordlist, "r") as f:
        words = f.readlines()

    found = None

    def worker(word):
        nonlocal found
        if found:
            return None

        result = check_password(word.strip(), hash_value, algo)
        if result:
            found = result
            return result

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(worker, words)

        for result in results:
            if result:
                print("[+] Password Found:", result)
                return result

    print("[-] Password not found")
import itertools
import string
import time

def brute_force_charset(target_hash, algo="sha256", max_length=3):
    print("[+] Starting REAL brute force (charset)...")

    charset = string.ascii_lowercase  # a-z
    attempts = 0
    start_time = time.time()

    for length in range(1, max_length + 1):
        for guess in itertools.product(charset, repeat=length):
            guess = ''.join(guess)
            attempts += 1

            hashed = hash_word(guess, algo)

            if hashed == target_hash:
                end_time = time.time()
                print(f"[+] Found: {guess}")
                print(f"[+] Attempts: {attempts}")
                print(f"[+] Time: {round(end_time - start_time, 2)} sec")
                return guess

    print("[-] Password not found")
    return None
