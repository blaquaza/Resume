import hashlib

def calculate_hash(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

file = input("Enter filename: ")
print("SHA-256 Hash:")
print(calculate_hash(file))
