 # holiday.py

# Function to calculate the hotel cost
def hotel_cost(num_nights):
    price_per_night = 100  # Adjust this value as needed
    return num_nights * price_per_night

# Function to calculate the flight cost
def plane_cost(city_flight):
    if city_flight.lower() == "paris":
        return 250
    elif city_flight.lower() == "new york":
        return 500
    elif city_flight.lower() == "tokyo":
        return 800
    elif city_flight.lower() == "cape town":
        return 300
    else:
        return 0  # Default for unknown city

# Function to calculate the car rental cost
def car_rental(rental_days):
    price_per_day = 40  # Adjust this value as needed
    return rental_days * price_per_day

# Function to calculate the total holiday cost
def holiday_cost(num_nights, city_flight, rental_days):
    total_hotel_cost = hotel_cost(num_nights)
    total_plane_cost = plane_cost(city_flight)
    total_car_rental_cost = car_rental(rental_days)
    return total_hotel_cost + total_plane_cost + total_car_rental_cost

# Main function to get user inputs and display the results
def main():
    print("Welcome to the Holiday Cost Calculator!")
    
    # Get user inputs
    city_flight = input("Enter the city you will be flying to (Paris, New York, Tokyo, Cape Town): ").strip()
    num_nights = int(input("Enter the number of nights you will be staying at the hotel: "))
    rental_days = int(input("Enter the number of days you will be hiring a car: "))

    # Calculate total cost
    total_cost = holiday_cost(num_nights, city_flight, rental_days)

    # Display the details
    print("\n--- Holiday Details ---")
    print(f"City: {city_flight.capitalize()}")
    print(f"Number of nights: {num_nights}")
    print(f"Number of rental days: {rental_days}")
    print(f"Hotel cost: ${hotel_cost(num_nights):.2f}")
    print(f"Flight cost: ${plane_cost(city_flight):.2f}")
    print(f"Car rental cost: ${car_rental(rental_days):.2f}")
    print(f"Total holiday cost: ${total_cost:.2f}")

# Run the program
if __name__ == "__main__":
    main()