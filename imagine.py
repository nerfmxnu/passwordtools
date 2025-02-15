import itertools
import random
import os

ascii_art = """
 ██▓ ███▄ ▄███▓ ▄▄▄        ▄████  ██▓ ███▄    █ ▓█████ 
▓██▒▓██▒▀█▀ ██▒▒████▄     ██▒ ▀█▒▓██▒ ██ ▀█   █ ▓█   ▀ 
▒██▒▓██    ▓██░▒██  ▀█▄  ▒██░▄▄▄░▒██▒▓██  ▀█ ██▒▒███   
░██░▒██    ▒██ ░██▄▄▄▄██ ░▓█  ██▓░██░▓██▒  ▐▌██▒▒▓█  ▄ 
░██░▒██▒   ░██▒ ▓█   ▓██▒░▒▓███▀▒░██░▒██░   ▓██░░▒████▒
░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ░▒   ▒ ░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
 ▒ ░░  ░      ░  ▒   ▒▒ ░  ░   ░  ▒ ░░ ░░   ░ ▒░ ░ ░  ░
 ▒ ░░      ░     ░   ▒   ░ ░   ░  ▒ ░   ░   ░ ░    ░   
 ░         ░         ░  ░      ░  ░           ░    ░  ░

                      by @nerfmxnu
"""

common_special_chars = ["!", "@", "#", "_", "-", ".", "$"]

leet_dict = {
    "a": ["4", "@"], "e": ["3"], "i": ["1", "!"], "o": ["0"], 
    "s": ["5", "$"], "l": ["1"], "t": ["7"]
}

config = {
    "words": [],
    "max_passwords": 10000,
    "output_file": "password_list.txt"
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

def show_help():
    print("\nAVAILABLE COMMANDS:")
    print("  set words <word1> <word2> ...   - Set words for password generation")
    print("  set max <num>                   - Set max number of passwords")
    print("  set output <filename>            - Set output file")
    print("  show config                      - Show current settings")
    print("  run                              - Start password generation")
    print("  clear                            - Clear the screen")
    print("  help                             - Show help")
    print("  exit                             - Exit the program\n")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(ascii_art)

    while True:
        cmd = input("Imagine> ").strip().lower()
        parts = cmd.split(" ", 2)

        if len(parts) < 2 and parts[0] not in ["show", "run", "clear", "help", "exit"]:
            print("Invalid command. Type 'help' for commands.")
            continue

        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if command == "set":
            if len(args) < 1:
                print("Usage: set <parameter> <value>")
                continue

            param = args[0]
            value = args[1] if len(args) > 1 else None

            if param == "words" and value:
                config["words"] = value.split()
                print(f"Words set: {', '.join(config['words'])}")
            elif param == "max" and value and value.isdigit():
                config["max_passwords"] = int(value)
                print(f"Max passwords set: {config['max_passwords']}")
            elif param == "output" and value:
                config["output_file"] = value
                print(f"Output file set: {config['output_file']}")
            else:
                print("Unknown parameter. Use 'help' for commands.")

        elif command == "show" and args[0] == "config":
            print("\nCURRENT CONFIGURATION:")
            print(f"  Words: {', '.join(config['words']) if config['words'] else 'None'}")
            print(f"  Max Passwords: {config['max_passwords']}")
            print(f"  Output File: {config['output_file']}\n")

        elif command == "run":
            if not config["words"]:
                print("\nError: No words set. Use 'set words <word1> <word2>' first.")
                continue
            total_passwords = generate_passwords(config["words"], config["max_passwords"], config["output_file"])
            print(f"\nPasswords saved in: {config['output_file']} ({total_passwords} generated)")

        elif command == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            print(ascii_art)

        elif command == "help":
            show_help()

        elif command == "exit":
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
