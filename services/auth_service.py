import csv
import os
from utils.constants import REGISTRATION_PATH
import hashlib


def user_file_exists():
    return os.path.isfile(REGISTRATION_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_login(email, password):
    if not user_file_exists():
        return False, ""

    with open(REGISTRATION_PATH, mode="r") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]

        for row in reader:
            stored_email = row["Email"].strip()
            stored_password = row["Password"].strip()

            if stored_email == email and stored_password == hash_password(password):    
                return True, row["Name"].strip()

    return False, ""


def email_already_registered(email):
    if not user_file_exists():
        return False

    with open(REGISTRATION_PATH, mode="r") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]

        for row in reader:
            if row["Email"].strip() == email:
                return True

    return False


def register_user(name, email, password):
    file_exists = user_file_exists()

    with open(REGISTRATION_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Email", "Password"])
        writer.writerow([name, email, hash_password(password)])