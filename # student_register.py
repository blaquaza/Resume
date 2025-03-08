# student_register.py

def register_students():
    # Ask the user how many students are registering
  
    try:
        num_students = int(input("Enter the number of students registering: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Open the file reg_form.txt in write mode
  
    with open("reg_form.txt", "w") as file:
        # Loop to collect student IDs
      
        for i in range(num_students):
            student_id = input(f"Enter student ID for student {i + 1}: ")
            # Write the student ID and a dotted line to the file
          
            file.write(f"{student_id}\n{'-' * 40}\n")

    print(f"{num_students} students have been registered. Check 'reg_form.txt' for the register.")

# Run the program
if __name__ == "__main__":
    register_students()