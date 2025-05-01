import os
import subprocess
import sys


def main():
    # Create Django project
    subprocess.run(["django-admin", "startproject", "config", "."], check=True)

    # Create apps
    apps = ["users", "products", "orders", "customers"]
    for app in apps:
        subprocess.run(["python", "manage.py", "startapp", app], check=True)

    print("Django project setup completed successfully!")


if __name__ == "__main__":
    main()
