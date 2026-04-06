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

        for i, res in enumerate(results):
            if i % 500 == 0:
                print(f"[+] Tried {i} passwords...")

            if res:
                print(f"\n[+] Password FOUND: {res}")
                return res

    print("[-] Password not found")
    return None
