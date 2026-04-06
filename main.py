import argparse
from brute_force.bruteforce import brute_force_advanced, brute_force_charset
from analyzer.analyzer import analyze_password
from dictionary.generator import generate_dictionary, save_to_file
from hash_extractor.hash_generator import hash_password, save_hash
from brute_force.bruteforce import brute_force_advanced
from reports.report_manager import (
    init_report,
    finalize_report,
    save_dictionary_info,
    save_generated_hash,
    save_cracked_password,
    log_event,
    log_error
)
import subprocess

WORDLIST = "dictionary/wordlist.txt"


def menu():
    print("\n=== Password Audit Toolkit ===")
    print("1. Generate Dictionary")
    print("2. Generate Hash")
    print("3. Crack Password (John)")
    print("4. Dictionary Attack")
    print("5. Brute Force (Charset)")
    print("6. Analyze Password")
    print("7. Exit")


# ---------------- Dictionary ----------------
def generate_dict_option():
    base = input("Enter base words (comma separated): ").split(",")
    base = [word.strip() for word in base]

    words = generate_dictionary(base)
    save_to_file(words)

    print(f"[+] Generated {len(words)} words")
    print("[+] Saved to dictionary/wordlist.txt")

    save_dictionary_info(len(words))


# ---------------- Hash Generator ----------------
def generate_hash_option():
    password = input("Enter password: ")
    algo = input("Algorithm (md5/sha1/sha256): ").lower()

    try:
        hashed = hash_password(password, algo)
        print(f"[+] Hash: {hashed}")

        save_hash(hashed)
        print("[+] Saved to hash.txt")

        save_generated_hash(password, hashed)

    except ValueError:
        print("[-] Invalid algorithm")
        log_error("Invalid hash algorithm selected")


# ---------------- John Cracking ----------------
def crack_password_option():
    hash_file = input("Enter hash file (e.g., hash.txt): ").strip()

    print("[+] Running John the Ripper...")

    try:
        subprocess.run([
            "john",
            f"--wordlist={WORDLIST}",
            hash_file
        ])

        print("\n[+] Results:")
        subprocess.run(["john", "--show", hash_file])

        log_event("John cracking completed")

    except FileNotFoundError:
        print("[-] John not installed")
        log_error("John the Ripper not found")


# ---------------- Brute Force ----------------
def brute_force_option():
    hash_value = input("Enter hash: ")
    algo = input("Algorithm (md5/sha1/sha256): ").lower()

    result = brute_force_advanced(hash_value, WORDLIST, algo, threads=4)

    if result:
        print(f"[+] Password found: {result}")
        save_cracked_password(hash_value, result, method="Brute Force")
    else:
        print("[-] Password not found")
        log_event("Brute force attempt failed")


#----------------analyzer-----------------
def analyze_password_option():
    password = input("Enter password to analyze: ")

    score, feedback = analyze_password(password)

    print(f"[+] Strength Score: {score}/4")

    if feedback:
        print("Suggestions:")
        for f in feedback:
            print("-", f)
    else:
        print("Strong password!")

    log_event(f"Password analyzed | Score: {score}")


# ---------------clI-----------------
def cli_mode():
    import argparse

    parser = argparse.ArgumentParser(description="Password Audit Toolkit")

    parser.add_argument("--generate-dict", help="Generate dictionary")
    parser.add_argument("--hash", help="Generate hash")
    parser.add_argument("--algo", default="sha256")
    parser.add_argument("--crack", help="Crack hash file")
    parser.add_argument("--brute", help="Brute force hash")

    args = parser.parse_args()

    if not any(vars(args).values()):
        return False

    if args.hash:
        h = hash_password(args.hash, args.algo)
        print("[+] Hash:", h)
        return True

    return False
# ---------------- Main ----------------
if __name__ == "__main__":
    init_report()

    if cli_mode():
        finalize_report()
        exit()

    while True:
        menu()
        choice = input("Select option: ")

        if choice == "1":
            generate_dict_option()

        elif choice == "2":
            generate_hash_option()

        elif choice == "3":
            crack_password_option()

        elif choice == "4":
             brute_force_option()

        elif choice == "5":
             hash_value = input("Enter hash: ")
             algo = input("Algorithm (md5/sha1/sha256): ").lower()

             brute_force_charset(hash_value, algo, max_length=3)

        elif choice == "6":
             analyze_password_option()

        elif choice == "7":
             finalize_report()
             print("Exiting...")
             break

        else:
            print("Invalid choice")

