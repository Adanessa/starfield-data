#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import Counter
from typing import Dict
import json
import os
import pathlib
import sqlite3
import sys


def main():
    args = parse_arguments(sys.argv[1:])
    if not args_are_valid(args):
        sys.exit(1)
    else:
        con = connect_to_db(args.data_dir)
        install_schema(args.data_dir, con)
        shortname_map = insert_resources(args.data_dir, con)
        insert_galaxy(args.data_dir, con, shortname_map)
        con.close()


def parse_arguments(args):
    """
    Parses command-line arguments for the 'create_db.py' script.

    This function sets up an argument parser to handle command-line arguments
    for data validation and database creation. It defines a single required
    argument, `--data-dir`, which specifies the path to the data directory.

    Args:
        args (list, optional):
            A list of command-line arguments. If not provided, `sys.argv[1:]`
            (the arguments passed to the script) will be used.

    Returns:
        argparse.Namespace:
            An object containing the parsed arguments as attributes
            (e.g., `args.data_dir`).

    Raises:
        SystemExit:
            If there are errors during argument parsing (e.g., invalid arguments or missing required ones),
            the script will exit with a relevant error message.
    """
    parser = ArgumentParser(
        prog="create_db.py",
        description="Validate the JSON data and organize it into an SQLite database.",
        epilog="https://github.com/Adanessa/starfield-data",
    )

    parser.add_argument(
        "--data-dir",
        help="Path to where the data is stored",
        type=pathlib.Path,
        required=True,
    )
    return parser.parse_args(args)


def args_are_valid(args):
    """
    Validates command-line arguments.

    This function checks the validity of the provided arguments.
    Currently, it specifically verifies the existence of the data directory.

    Args:
    args (argparse.Namespace): A namespace object containing parsed command-line arguments.
    This is typically obtained from argparse.ArgumentParser.parse_args().

    Returns:
    bool: True if all checked arguments are valid, False otherwise.
    """
    valid = True
    if not args.data_dir.exists():
        print("Invalid data directory, may not exist")
        valid = False
    return valid


def connect_to_db(data_dir: pathlib.Path) -> sqlite3.Connection:
    """
    Establishes a connection to an SQLite database file named
    "sf.db" within the specified directory.  If the database file
    already exists, it is deleted and a new connection is created to a
    fresh database.

    Args:
        data_dir (pathlib.Path): The directory path where the "sf.db" file should be located.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.

    Raises:
        sqlite3.Error: If there's an issue connecting to or creating the database.

    """
    db_path: pathlib.Path = data_dir.joinpath("sf.db")
    if db_path.is_file():
        os.remove(db_path)
    return sqlite3.connect(db_path)


def install_schema(data_dir: pathlib.Path, con: sqlite3.Connection) -> None:
    """
    Installs a database schema into an SQLite database.

    This function reads a SQL schema file named "sf.sql" from the specified
    data directory and executes the SQL statements within it to create the
    tables, indexes, and other database objects defined in the schema.

    Args:
        data_dir (pathlib.Path):
            The directory containing the "sf.sql" schema file.
        con (sqlite3.Connection):
            An open connection to the SQLite database where the schema will be installed.

    Raises:
        FileNotFoundError: If the "sf.sql" file is not found in the specified directory.
        sqlite3.Error: If there is an error executing the SQL schema.
    """
    schema_file = data_dir.joinpath("sf.sql")
    with open(schema_file, "r") as fob:
        schema = fob.read()
        cur = con.cursor()
        cur.executescript(schema)
        con.commit()
        cur.close()


def insert_resources(data_dir: pathlib.Path, con: sqlite3.Connection) -> Dict[str, str]:
    """
    Inserts resource data from a JSON file into an SQLite database and creates a shortname mapping.

    This function performs the following steps:
    1. Loads resource data from a JSON file named "resources.json" located in the `data_dir`.
    2. Inserts each resource's data into the "resources" table in the SQLite database.
    3. Creates a dictionary (`shortname_map`) mapping both the lowercase short names and full names
       of the resources to their corresponding full names and short names, respectively.
    4. Commits the changes to the database and closes the cursor.
    5. Returns the `shortname_map` dictionary.

    Args:
        data_dir (pathlib.Path): The directory containing the "resources.json" file.
        con (sqlite3.Connection): An open connection to the SQLite database.

    Returns:
        Dict[str, str]: A dictionary mapping lowercase short names and full names of resources
            to their corresponding full names and short names.

    Raises:
        FileNotFoundError: If the "resources.json" file is not found.
        json.JSONDecodeError: If there's an error parsing the JSON data.
        sqlite3.Error: If there's an error inserting data into the database.
    """
    shortname_map = dict()
    cur = con.cursor()
    with open(data_dir.joinpath("resources.json"), "r") as fob:
        data = json.load(fob)

    for resource in data:
        row = (
            resource["resource"],
            resource["shortName"],
            resource["rarity"],
            resource["type"],
            resource["mass"],
            resource["value"],
            resource["valueToMass"],
        )
        cur.execute("INSERT INTO resources VALUES (?, ?, ?, ?, ?, ?, ?);", row)
        shortname_map[resource["shortName"].lower()] = resource["resource"]
        shortname_map[resource["resource"].lower()] = resource["shortName"]
    con.commit()
    cur.close()
    return shortname_map


def insert_galaxy(
    data_dir: pathlib.Path, con: sqlite3.Connection, shortname_map: Dict[str, str]
) -> None:
    """
    Inserts galaxy and celestial body data from a JSON file into an SQLite database.

    This function performs the following steps:
    1. Loads galaxy data from a JSON file named "galaxy.json" located in the `data_dir`.
    2. Calculates the number of celestial bodies (`counts`) per star system.
    3. Inserts each unique star system and its body count into the "systems" table.
    4. Iterates through each celestial body in the `galaxy` data:
        - Inserts the body's details (name, system, type, gravity, etc.) into the "bodies" table.
        - Handles potential `sqlite3.IntegrityError` if there's duplicate data.
        - Inserts associated traits into the "traits" table.
        - Uses the `shortname_map` to insert resource references into the "body_resources" table.
        - Inserts domesticable and gatherable organics into the "body_organics" table.
        - Inserts biome data (name and coverage) into the "biomes" table.
    5. Commits all changes to the database after processing each body to ensure data integrity.

    Args:
        data_dir (pathlib.Path): The directory containing the "galaxy.json" file.
        con (sqlite3.Connection): An open connection to the SQLite database.
        shortname_map (Dict[str, str]): A dictionary mapping resource short names to their full names.

    Raises:
        FileNotFoundError: If the "galaxy.json" file is not found.
        json.JSONDecodeError: If there's an error parsing the JSON data.
        sqlite3.Error: If there are general database errors (excluding `IntegrityError`).
    """

    cur = con.cursor()
    with open(data_dir.joinpath("galaxy.json"), "r") as fob:
        galaxy = json.load(fob)

    # obtain both the distinct set of system names, as well as the
    # number of bodies in each
    counts = Counter([body["system"] for body in galaxy])
    cur.executemany("INSERT INTO systems VALUES(?, ?);", counts.items())
    con.commit()

    for body in galaxy:
        row = (
            body["name"],
            body["system"],
            body["type"],
            body["gravity"],
            body["temperature"],
            body["atmosphere"],
            body["magnetosphere"],
            body["water"],
            body["fauna"],
            body["flora"],
            body["hab_rank"],
            body["planet_length"],
        )
        try:
            cur.execute(
                "INSERT INTO bodies VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                row,
            )

        except sqlite3.IntegrityError:
            print(f"Bad data in {row}")

        for trait in body["traits"]:
            cur.execute(
                "INSERT INTO traits VALUES (?, ?, ?);",
                (body["system"], body["name"], trait),
            )

        for resource in body["resources"]:
            cur.execute(
                "INSERT INTO body_resources VALUES (?, ?, ?);",
                (body["system"], body["name"], shortname_map[resource.lower()]),
            )

        for org in body["domesticable"]:
            cur.execute(
                "INSERT INTO body_organics VALUES (?, ?, ?, ?, ?);",
                (body["system"], body["name"], org["name"], org["resource"], True),
            )

        for org in body["gatherable"]:
            cur.execute(
                "INSERT INTO body_organics VALUES (?, ?, ?, ?, ?);",
                (body["system"], body["name"], org["name"], org["resource"], False),
            )

        for biome in body["biomes"]:
            cur.execute(
                "INSERT INTO biomes VALUES (?, ?, ?, ?);",
                (body["system"], body["name"], biome["name"], biome["coverage"]),
            )
        con.commit()


if __name__ == "__main__":
    main()
