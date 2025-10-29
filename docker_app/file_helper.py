def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError as exp:
        err = "Error: file not found"
        print(f"{err} {exp}")
    except Exception as exp:
        err = "Error: Other error while file read"
        print(f"{err} {exp}")
    return None

def write_to_file(file_path, value):
    with open(file_path, "w") as file:
        file.write(value)