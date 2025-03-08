import math

# Display the menu to the user
print("investment - to calculate the amount of interest you'll earn on your investment")
print("bond       - to calculate the amount you'll have to pay on a home loan")
choice = input("Enter either 'investment' or 'bond' from the menu above to proceed: ").strip().lower()

# Validate the user's choice
if choice not in ["investment", "bond"]:
    print("Error: Invalid choice. Please enter 'investment' or 'bond'.")
else:
    if choice == "investment":
        # Gather input for the investment calculation
        P = float(input("Enter the amount of money you are depositing: "))
        rate = float(input("Enter the interest rate (only the number, e.g., 8 for 8%): "))
        r = rate / 100  # Convert to decimal
        t = int(input("Enter the number of years you plan on investing: "))
        interest = input("Do you want 'simple' or 'compound' interest? ").strip().lower()

        # Calculate and output the result based on the interest type
        if interest == "simple":
            A = P * (1 + r * t)
            print(f"The total amount after {t} years with simple interest is: {A:.2f}")
        elif interest == "compound":
            A = P * math.pow((1 + r), t)
            print(f"The total amount after {t} years with compound interest is: {A:.2f}")
        else:
            print("Error: Invalid interest type. Please enter 'simple' or 'compound'.")
    elif choice == "bond":
        # Gather input for the bond calculation
        P = float(input("Enter the present value of the house: "))
        rate = float(input("Enter the annual interest rate (only the number, e.g., 7 for 7%): "))
        n = int(input("Enter the number of months you plan to take to repay the bond: "))
        i = (rate / 100) / 12  # Convert to monthly interest rate

        # Calculate and output the monthly repayment
        repayment = (i * P) / (1 - (1 + i)**(-n))
        print(f"The amount you will have to repay each month is: {repayment:.2f}")