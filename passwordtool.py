import itertools
import random

common_special_chars = ["!", "@", "#", "_", "-", ".", "$"]

leet_dict = {
    "a": ["4", "@"], "e": ["3"], "i": ["1", "!"], "o": ["0"], 
    "s": ["5", "$"], "l": ["1"], "t": ["7"]
}

def leet_transform(word):
    variations = {word}
    for key, values in leet_dict.items():
        for value in values:
            new_variations = set()
            for w in variations:
                new_variations.add(w.replace(key, value))
            variations.update(new_variations)
    return list(variations)

def case_variations(word):
    return [word.lower(), word.capitalize(), word.upper()]

def add_special_char_at_end(word):
    return word + random.choice(common_special_chars)

def insert_special_chars_randomly(word):
    word_list = list(word)
    num_specials = random.randint(1, 2)
    for _ in range(num_specials):
        pos = random.randint(1, len(word_list) - 1)
        word_list.insert(pos, random.choice(common_special_chars))
    return "".join(word_list)

def generate_passwords(words, max_passwords=10000, output_file="password_list.txt"):
    total_passwords = 0
    with open(output_file, "w") as f:
        all_variations = []

        for word in words:
            variations = case_variations(word) + leet_transform(word)
            all_variations.extend(variations)

        for word1 in words:
            for word2 in words:
                if word1 != word2:
                    base_password = word1 + word2
                    f.write(base_password + "\n")
                    f.write(add_special_char_at_end(base_password) + "\n")
                    total_passwords += 2
                    if total_passwords >= max_passwords:
                        return total_passwords

        for word1 in all_variations:
            for word2 in all_variations:
                if word1 != word2:
                    mixed_password = word1 + word2
                    f.write(mixed_password + "\n")
                    f.write(add_special_char_at_end(mixed_password) + "\n")
                    f.write(insert_special_chars_randomly(mixed_password) + "\n")
                    total_passwords += 3
                    if total_passwords >= max_passwords:
                        return total_passwords

        for r in range(2, min(5, len(all_variations) + 1)):  
            for combo in itertools.permutations(all_variations, r):
                if total_passwords >= max_passwords:
                    return total_passwords

                base = ''.join(combo)
                f.write(base + "\n")
                f.write(add_special_char_at_end(base) + "\n")
                f.write(insert_special_chars_randomly(base) + "\n")
                total_passwords += 3

                if total_passwords >= max_passwords:
                    return total_passwords

    return total_passwords

user_input = input("Inserisci parole chiave: ")
words_list = user_input.split()
total_passwords = generate_passwords(words_list)

print(f"\n✅ Password salvate in: password_list.txt ({total_passwords} generate)")
