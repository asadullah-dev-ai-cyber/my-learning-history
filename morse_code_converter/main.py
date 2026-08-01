from morse_dict import MORSE_CODE_DICT


def text_to_morse(user_text):
    morse_text = []
    for char in user_text:
        if char == " ":
            # Represent word breaks with a slash
            morse_text.append("/")
        elif char in MORSE_CODE_DICT:
            morse_text.append(MORSE_CODE_DICT[char])
        # morse_text.append(MORSE_CODE_DICT.get(char, "/"))

    return " ".join(morse_text)


def morse_to_text(morse_string):
    reversed_morse_code_dict = {value: key for key, value in MORSE_CODE_DICT.items()}

    normalized_input = morse_string.replace("   ", " / ")

    morse_words = normalized_input.split(" / ")
    decoded_words = []

    for word in morse_words:
        morse_letters = word.split(" ")
        decoded_letters = []

        for char in morse_letters:
            if char in reversed_morse_code_dict:
                decoded_letters.append(reversed_morse_code_dict[char])

        decoded_words.append("".join(decoded_letters))


    return " ".join(decoded_words)

# --- USER MENU INTERFACE ---
if __name__ == "__main__":

    is_morse_generating = True

    print("\n====================================")
    print("Welcome to the Morse Code Converter!")
    print("====================================")

    while is_morse_generating:
        user_input = input("\nDo you want to (E)ncrypt text, (D)ecrypt Morse, or (Q)uit? ").upper()

        if user_input == "E":
            text = input("Enter your text to encrypt: ").upper()
            output = text_to_morse(text)
            print(f"Encrypted Morse: {output}")

        elif user_input == "D":
            morse_string = input("Enter Morse code (use spaces between letters and / or 3 spaces between words): ")
            output = morse_to_text(morse_string)
            print(f"Decrypted Text: {output}")

        elif user_input == "Q":
            print("Goodbye!")
            is_morse_generating = False

        else:
            print("Invalid choice, please select E, D, or Q.")

