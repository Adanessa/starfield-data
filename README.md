# Starfield Data Repository

Welcome to the Starfield Data Repository, where you can explore detailed information on systems, planets, and various items within the Starfield universe.

## Introduction

This repository hosts comprehensive data extracted from the game Starfield, including systems, planets, and various items like apparel, armor, weapons, and more.

## Contents

This update includes a significant expansion of data files, including:
- Apparel.json
- Armor_mods.csv and Armor_mods.json
- Bays.csv and Bays.json
- Cockpits.csv and Cockpits.json
- Consumables.csv and Consumables.json
- Dockers.csv and Dockers.json
- Engines.csv and Engines.json
- Fuel_tanks.csv and Fuel_tanks.json
- Grav_drives.csv and Grav_drives.json
- Habs.csv and Habs.json
- Landing_gears.csv and Landing_gears.json
- Materials.csv and Materials.json
- Pistols.csv and Pistols.json
- Powers.csv and Powers.json
- Prefixes.csv and Prefixes.json
- Reactors.csv and Reactors.json
- Research_laboratory.csv and Research_laboratory.json
- Resources.csv and Resources.json
- Shield_generators.csv and Shield_generators.json
- Ship_weapons.csv and Ship_weapons.json
- Shotguns.csv and Shotguns.json
- Skills.csv and Skills.json
- Status_effects.csv and Status_effects.json
- Structural_components.csv and Structural_components.json
- Temples.csv and Temples.json
- Traits.csv and Traits.json
- Weapons.csv and Weapons.json

## Data Field Descriptions

### Planets and Systems

Each planet and system in the dataset includes fields such as:
- **name**: The name of the planet or system.
- **type**: The type of the planet or system (e.g., Rock, Gas Giant).
- **gravity**: The gravitational pull of the planet, measured in g (Earth's gravity).
- **temperature**: General temperature classification (e.g., Cold, Hot).
- **atmosphere**: Type and composition of the atmosphere.
- **magnetosphere**: Presence and type of magnetic field.
- **water**: Information about water presence and safety.
- **biomes**: Types and percentages of biomes.
- **traits**: Unique planetary traits or phenomena.
- **fauna**: Number of animal species.
- **flora**: Number of plant species.
- **resources**: List of available resources.
- **domesticable**: Species that can be domesticated.
- **gatherable**: Items or materials that can be gathered.
- **hab_rank**: Habitability rank.
- **planet_length**: Length of a day on the planet.

### Items

Detailed attributes are provided for items such as apparel, armor, weapons, and more.

## Data Sources

Data is sourced from:
- Game data and in-game observations
- Official Starfield documentation
- Community contributions and fan sites

## SQL Interface Contribution

### By [mindfilleter]

#### Objective:
The primary objective of this contribution is to provide an SQL interface for querying the Starfield data. This enables users to leverage SQL for direct queries or to build applications and tools utilizing this data.

#### Details:
The contributor has added two scripts:
- `create_db.py`: This script inserts data from `galaxy.json` (output of `restructure.py`) into an SQLite database file.
- `restructure.py`: Reads `starfield_data_updated.json`, validates it, and stores the data in a flattened format in `galaxy.json`.

These scripts enhance the usability and accessibility of Starfield data for various applications and analytical purposes.

## How to Use

Feel free to clone this repository and explore the data for your own projects or contributions. Use the files provided to analyze, visualize, or integrate with your applications.

## Contributing

Your contributions are welcome! If you have additional data, improvements, or corrections, please open an issue or submit a pull request.

---

Thank you for exploring the Starfield universe with us!
