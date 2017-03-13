import sqlite3

conn = sqlite3.connect("profiles.db")
c = conn.cursor()

# create table if it doesn't already exist
try:
    c.execute('''CREATE TABLE profiles
                 (firstname, lastname, age);''')
except sqlite3.OperationalError:
    pass

# take user input
selection = int(input("Enter 1 to add a new profile, 2 to remove one, 3 to look one up, 4 to display all: "))

# check selection and execute code accordingly
try:
    if selection == 1:
        name = input("Enter first and last name: ").split()
        age = int(input("Enter age: "))
        c.execute(f'INSERT INTO profiles VALUES ("{name[0]}", "{name[1]}", {age});')
        print("Done.")
        
    elif selection == 2:
        name = input("Enter first and last name: ").split()
        age = int(input("Enter age: "))
        
        profiles = c.execute(f'SELECT * FROM profiles WHERE firstname = "{name[0]}" AND lastname = "{name[1]}" AND age = {age};')
        found = False
        for row in profiles:
            found = True
            break
            
        if not found:
            print("Profile not found.")
        else: 
            c.execute(f'DELETE FROM profiles WHERE firstname = "{name[0]}" AND lastname = "{name[1]}" AND age = {age};')
            print("Done.")
    
    elif selection == 3:
        query = input("Enter search query: ")
        search = c.execute(f'SELECT * FROM profiles WHERE firstname LIKE "%{query}%" OR lastname LIKE "%{query}%";')
        profile_list = search.fetchall()
        
        if len(profile_list) == 0:
            print("No results found.")
        for row in profile_list:
            print(row)
            
    elif selection == 4:
        profiles = c.execute('SELECT * FROM profiles;')
        profile_list = profiles.fetchall()
        
        if len(profile_list) == 0:
            print("Table is empty.")
        for row in profile_list:
            print(row)
except ValueError:
    print("Invalid age.")
except IndexError:
    print("Please separate first and last name with a space.")

conn.commit()
conn.close()