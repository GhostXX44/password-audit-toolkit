import os

def leet_transform(word):
    replacements = {
        'a': '@',
        's': '$',
        'o': '0',
        'i': '1',
        'e': '3'
    }
    for k, v in replacements.items():
        word = word.replace(k, v)
    return word


def generate_dictionary(base_words, append_numbers=True, max_num=100):
    wordlist = set()

    for word in base_words:
        variations = {
            word,
            word.lower(),
            word.upper(),
            word.capitalize(),
            leet_transform(word)
        }

        for v in variations:
            wordlist.add(v)

            if append_numbers:
                for i in range(max_num):
                    wordlist.add(f"{v}{i}")

    return sorted(wordlist)


def save_to_file(words, filename="wordlist.txt"):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)

    with open(file_path, "w") as f:
        for word in words:
            f.write(word + "\n")


if __name__ == "__main__":
    base = ["admin", "password", "ganesh"]

    words = generate_dictionary(base)

    print(f"[+] Generated {len(words)} words")
    print("[+] Sample:", words[:10])

    save_to_file(words)
    print("[+] Saved to wordlist.txt")
