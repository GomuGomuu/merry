from config.settings import BASE_DIR

with open(f"{BASE_DIR.parent}/initialdata/OP01-025.png", "rb") as f:
    print(f.read())
