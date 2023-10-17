def print_strength(input_str):
    n = len(input_str)
    has_lower = False
    has_upper = False
    has_digit = False
    special_char = False

    normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "

    for char in input_str:
        if char.islower():
            has_lower = True
        if char.isupper():
            has_upper = True
        if char.isdigit():
            has_digit = True
        if char not in normal_chars:
            special_char = True

    print("Strength of your password:", end=" ")
    if has_lower and has_upper and has_digit and special_char and (n >= 8):
        print("Strong")
    elif (has_lower or has_upper) and special_char and (n >= 6):
        print("Moderate")
    else:
        print("Weak")

if __name__ == "__main__":
    input_str = input("Enter your password: ")
    print_strength(input_str)
