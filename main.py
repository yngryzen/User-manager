import sqlite3
import getpass
import bcrypt

con = sqlite3.connect("database.db")
cur = con.cursor()

userstablequery = """CREATE TABLE IF NOT EXISTS "users" (
	            "id"	INTEGER NOT NULL,
                "username"	TEXT NOT NULL UNIQUE,
                "password"	TEXT NOT NULL,
                "email"	TEXT NOT NULL UNIQUE,
                "first_name"	TEXT NOT NULL,
                "last_name"	TEXT NOT NULL,
                "age"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
                );"""

cur.execute(userstablequery)

accountcheck = input("Type [1] for login, type [2] for registration.")
if accountcheck == "2":
        # Validate username

    ok = False
    while not ok:
        username = input("Username | ")
        if not username.isalnum() or len(username) < 3 or len(username) > 16:
            print("Incorrect Username format.")
        else:
            ok = True

    # Validate email

    ok = False
    while not ok:
        email = input("Email | ")
        if len(email) < 5 or len(email) > 50:
            print("Incorrect Email format.")
        else:
            ok = True
            
    # Validate password

    special_characters = "!@#$%^&*()-+?_=,<>/."
    special_ccounter = 0
    capital_characters = 0

    ok = False
    while not ok:
        password = getpass.getpass("Password ( at least 6 characters, contain more than 1 uppercase character, and more than 1 special character) | ")
        for sc in special_characters:
            if sc in password:
                special_ccounter += 1
        for sc in password:        
            if sc.isupper():
                capital_characters += 1
        if len(password) >= 6 and special_ccounter >= 1 and capital_characters >= 1:
            passwordconfirm = getpass.getpass("Repeat password | ")
            if password != passwordconfirm:
                print("Passwords do not match.")
            else:
                ok = True
        else:
            print("Incorrect Password format.")
    hashedpassword = bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt())
            
    # Validate names

    ok = False
    while not ok:
        firstname = input("What is your first name? | ")
        lastname = input("What is your last name? | ")
        if len(firstname) > 2 and len(lastname) > 2 and len(firstname) < 50 and len(lastname) < 50:
            print("First and last name set.")
            ok = True
        else:
            print("Minimum requirements of between 2 and 50 characters not met")

    # Validate age

    ok = False
    while not ok:
        age = input("What is your age? | ")
        if age.isnumeric() and int(age) > 13 and int(age) < 100:
            print("Age set.")
            ok = True
        else:
            print("Age is invalid")
    print("Everything is ok.")

    sql = ''' INSERT INTO users(username, password, email, first_name, last_name, age)
            VALUES (?, ?, ?, ?, ?, ?) '''

    cur.execute(sql, (
        username,
        hashedpassword,
        email,
        firstname,
        lastname,
        age
    ))
    con.commit()
    print("Account created")
else: # Login
    ok = False
    while not ok:
        email = input("What is your email? | ")
        password = getpass.getpass("What is your password? | ")
        sql = '''SELECT password, first_name, last_name
                 FROM users
                 WHERE email = ?'''
        try:
            cur.execute(sql, (email,))
            row = cur.fetchone()
            if row:
                hashedpassword = row[0]
                firstname = row[1]
                lastname = row[2]
                if bcrypt.checkpw(password.encode(encoding="utf-8"), hashedpassword):
                    print("Logged in successfully")
                    ok = True
                else:
                    print("Wrong email or password")
        except sqlite3.Error as e:
            print(e)
            
    print(f"Welcome back, {firstname} {lastname}!\n1] Info\n2] My friends\n3] My Posts\n4] Log out")
    selection = input(">")
    if selection == "1":
        print(f"Password: {password}")
        print(f"First name: {firstname}")
        print(f"Last name: {lastname}")
    if selection == "2":
        print("You have no friends.")
    if selection == "3":
        print("Yet to make any posts.")
    if selection == "4":
        quit()
    else:
        print("Something went wrong on our side, Sorry about that!")