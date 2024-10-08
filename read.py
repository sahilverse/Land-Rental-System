# This Module contains the functions to read data from the file.

# reads the data from lands.txt file and stores it in a list of dictionaries.
# file data sample: 1, Kathmandu, East, 5, 10000, Available
def read_lands_data(file_path) -> list[dict]:
    lands_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() == '':
                    continue
                kitta_number, city, direction, area, price, availability = line.strip().split(", ")

                lands_data.append({
                    "kitta_number": int(kitta_number),
                    "city": city,
                    "direction": direction,
                    "area": int(area),
                    "price": int(price),
                    "availability": availability
                })
        return lands_data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return []
