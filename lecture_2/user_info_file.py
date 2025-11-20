
# The function that determines the user's life stage
def generate_profile(age):
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"

# We collect user data
user_name = input("Enter your full name: ")
birth_year_str = input("Enter your birth year: ")
birth_year = int(birth_year_str)
current_age = 2025 - birth_year

hobbies = []


# Learn about the user's hobbies using a loop
while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    else:
        hobbies.append(hobby)


life_stage = generate_profile(current_age)


# We pack all variables into a dictionary.
user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}


# Display a user profile summary
print()
print("---")
print("Profile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")


# We check if the user has a hobby and display the data if so.
if len(user_profile["hobbies"]) == 0:
    print("You didn't mention any hobbies.")
else:
   print(f"Favorite Hobbies ({len(user_profile['hobbies'])}):")
   for i in user_profile["hobbies"]:
       print(f"- {i}")

print("---")

