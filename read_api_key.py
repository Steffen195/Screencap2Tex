def read_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key
