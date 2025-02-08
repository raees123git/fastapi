import bcrypt

# Hashed password from the database
hashed_password = b"$2b$12$07E7OE.c6pjduwPlZEMcYeOKRWcL1CNVHQM2SN.8IvAMJ.BUWT/ti"

# Password you want to verify
plain_password = "1234"  # Replace with the password you want to test

# Check if the password matches the hash
if bcrypt.checkpw(plain_password.encode(), hashed_password):
    print("Password is correct!")
else:
    print("Incorrect password.")