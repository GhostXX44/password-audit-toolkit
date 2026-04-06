import hashlib

def hash_password(password, algo="sha256"):
    password = password.encode()

    if algo == "md5":
        return hashlib.md5(password).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(password).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(password).hexdigest()
    else:
        raise ValueError("Unsupported algorithm")


def save_hash(hash_value, filename="hash.txt"):
    with open(filename, "w") as f:
        f.write(hash_value)


if __name__ == "__main__":
    pwd = input("Enter password: ")
    algo = input("Algorithm (md5/sha1/sha256): ").lower()

    try:
        hashed = hash_password(pwd, algo)
        print(f"[+] Hash: {hashed}")

        save_hash(hashed)
        print("[+] Saved to hash.txt")

    except ValueError:
        print("[-] Invalid algorithm")
