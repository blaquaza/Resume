try:
    # Open the DOB.txt file and read its contents
    with open("DOB.txt", "r") as file:
        lines = file.readlines()

    # Lists to store names and birthdates
    names = []
    birthdates = []

    # Process each line
    for line in lines:
        parts = line.strip().split()  # Split by whitespace
        if len(parts) >= 3:  # Ensure the line contains enough parts
            # Name is the first two parts; birthdate is the rest
            name = " ".join(parts[:2])
            birthdate = " ".join(parts[2:])
            names.append(name)
            birthdates.append(birthdate)
        else:
            print(f"Skipping invalid line: {line.strip()}")

    # Print names section
    print("Name")
    for name in names:
        print(name)

    print("\nBirthdate")
    for birthdate in birthdates:
        print(birthdate)

except FileNotFoundError:
    print("Error: The file 'DOB.txt' was not found. Please ensure it is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")