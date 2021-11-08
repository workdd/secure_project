import random

# ! @  # $ % ^ & * ( ) < > [ ] { } | _ + - =
# a ~ z
# A ~ Z
# 0 ~ 9
# ascii 65 ~ 122
pwd_list = []
ascii_upper = [chr(alpha) for alpha in range(65, 91)]
ascii_lower = [chr(alpha) for alpha in range(97, 123)]
num_list = [num for num in range(10)]
special_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '[', ']', '{', '}', '|', '_', '+', '-',
                   '=']

pwd_list += ascii_lower
pwd_list += ascii_upper
pwd_list += num_list
pwd_list += special_symbols
print(pwd_list)

pwd_length = 8
password_list = []
with open('passwords.txt', 'w') as f:
    for i in range(100000):
        password = ''
        for j in range(pwd_length):
            password += str(random.choice(pwd_list))
        password_list.append(password)
        f.write(password + '\n')

print(password_list)
