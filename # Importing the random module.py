# Importing the random module

import random

# List of jokes

jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "What do you call fake spaghetti? An impasta!",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "What do you get if you cross a snowman and a vampire? Frostbite!",
    "Why was the math book sad? It had too many problems.",
    "What did the fish say when it hit the wall? Dam!",
    "Why can't your nose be 12 inches long? Because then it would be a foot!",
    "How do trees access the internet? They log on.",
    "Why did the bicycle fall over? It was two-tired.",
    "What do you call cheese that isn't yours? Nacho cheese!"
]

# Select and display a random joke

random_joke = random.choice(jokes)
print(f"Here's a joke for you:\n{random_joke}")