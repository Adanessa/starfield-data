import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def find_case_insensitive_key(d, key):
    key_lower = key.lower()
    for k in d.keys():
        if k.lower() == key_lower:
            return k
    return None

def update_planet(planet_name, planet):
    planet_length_key = find_case_insensitive_key(planet, "planet_length")
    hab_rank_key = find_case_insensitive_key(planet, "hab_rank")

    planet_length = planet.get(planet_length_key, "Unknown")
    hab_rank = planet.get(hab_rank_key, "Unknown")

    print(f"\nPlanet: {planet_name}")
    print(f"Current Planet Length: {planet_length}")
    print(f"Current Habitability Rank: {hab_rank}")

    new_planet_length = input("Enter new planet length (or press Enter to keep current): ")
    new_hab_rank = input("Enter new habitability rank (or press Enter to keep current): ")

    if new_planet_length:
        planet[planet_length_key] = new_planet_length
        print(f"Planet length for {planet_name} updated: {new_planet_length}")
    if new_hab_rank:
        planet[hab_rank_key] = new_hab_rank
        print(f"Hab_rank for {planet_name} updated: {new_hab_rank}")
    print("Values updated successfully.")

def update_system(data, system_name):
    system_key = find_case_insensitive_key(data, system_name)
    if system_key is None:
        print("System not found in the data.")
        return

    system = data[system_key]

    for planet_key in system.keys():
        update_planet(planet_key, system[planet_key])

def main():
    file_path = 'starfield_data_updated.json'
    data = load_data(file_path)
    
    system_name = input("Enter the system name: ")

    update_system(data, system_name)

    save_data(data, file_path)

if __name__ == "__main__":
    main()
