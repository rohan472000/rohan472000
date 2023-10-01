# add_email.py
def add_email(email):
    # Validate the email address
    if not is_valid_email(email):
        print("Invalid email format. Please provide a valid email address.")
        return

    # Check if the email is already subscribed
    if is_email_subscribed(email):
        print("This email address is already subscribed.")
        return

    # Add the email to the list of subscribed emails
    with open('subscribed_emails.txt', 'a') as file:
        file.write(email + '\n')
    print(f'Thank you! You have subscribed with the email: {email}')

def is_valid_email(email):
    return '@' in email and '.' in email

def is_email_subscribed(email):
    # Check if the email is already in the list of subscribed emails
    with open('subscribed_emails.txt', 'r') as file:
        subscribed_emails = [line.strip() for line in file]
        return email in subscribed_emails

if __name__ == '__main__':
    user_email = input('Enter your email: ')
    add_email(user_email)
