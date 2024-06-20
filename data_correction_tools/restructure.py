#!/usr/bin/env python3
"""
Starfield Data Restructuring and Validation Script

This script reads Starfield data from 'starfield_data_updated.json', validates and transforms it, 
and outputs a cleaned and structured version to 'galaxy.json'.

It performs the following operations:
1. Loads data from 'starfield_data_updated.json'.
2. Validates and standardizes the data:
    - Parses numeric fields (fauna, flora, hab_rank, planet_length) with error handling.
    - Converts atmosphere, temperature, and water data to lowercase.
    - Cleans and parses biome information.
    - Parses and sorts resource and organic resource data.
3. Creates dataclass instances (`Body`, `Biome`, `OrganicResource`) to represent the structured data.
4. Outputs the validated and structured data to 'galaxy.json' in a readable format.

Usage:
    python restructure.py --data-dir <path_to_data_directory>

Dependencies:
    - argparse
    - dataclasses
    - json
    - pathlib
    - sys

Author: wkmanire
GitHub: https://github.com/Adanessa/starfield-data
"""

from argparse import ArgumentParser
from dataclasses import dataclass, field, is_dataclass, asdict
from operator import attrgetter
from typing import List
import json
import pathlib
import sys


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class Biome:
    name: str = ""
    coverage: float = 0.0


@dataclass
class OrganicResource:
    name: str = ""
    resource: str = ""


@dataclass
class Body:
    system: str = ""
    name: str = ""
    atmosphere: str = ""
    fauna: int = 0
    flora: int = 0
    gravity: float = 1.0
    hab_rank: int = 0
    magnetosphere: str = ""
    planet_length: int = 0
    temperature: str = ""
    type: str = ""
    water: str = ""
    biomes: List[Biome] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    domesticable: List[OrganicResource] = field(default_factory=list)
    gatherable: List[OrganicResource] = field(default_factory=list)


def main():
    # TODO: This could be cleaned up and refactored, but it's possible
    # that the old format would be abandoned, in which case this
    # module would be removed the repository so for now I'm not
    # bothering. (- wkmanire 2024-06-19)

    parser = ArgumentParser(
        prog="restructure.py",
        description="Refactors, validate, and clean the starfield_updated_data.json file into galaxy.json.",
        epilog="https://github.com/Adanessa/starfield-data",
    )
    parser.add_argument(
        "--data-dir",
        help="Path to where the data is stored",
        type=pathlib.Path,
        required=True,
    )

    args = parser.parse_args()

    data_dir = pathlib.Path(args.data_dir)
    raw_original_data = json.loads(
        data_dir.joinpath("starfield_data_updated.json").read_text()
    )

    galaxy = []

    for system_name, body_data in raw_original_data.items():
        for body_name, body_data in body_data.items():
            body = Body()
            body.system = system_name
            body.name = body_name
            body.atmosphere = body_data["atmosphere"].lower()

            try:
                body.fauna = int(body_data["fauna"])
            except ValueError:
                print(
                    f"invalid fauna count ('{body_data['fauna']}') for {system_name} -> {body_name}', defaulting to 0"
                )
                body.fauna = 0

            try:
                body.flora = int(body_data["flora"])
            except ValueError:
                print(
                    f"invalid flora count ('{body_data['flora']}') for {system_name} -> {body_name}', defaulting to 0"
                )
                body.flora = 0

            body.gravity = float(body_data["gravity"].replace("g", "").strip())

            try:
                body.hab_rank = int(body_data["hab_rank"])
            except ValueError:
                print(
                    f"invalid hab rank ('{body_data['hab_rank']}') for {system_name} -> {body_name}', defaulting to 0"
                )
                body.hab_rank = 0

            body.magnetosphere = body_data["magnetosphere"].lower()
            try:
                pl = body_data["planet_length"]
                parts = pl.split(" ")
                body.planet_length = int(parts[0])
            except (ValueError, AttributeError):
                print(
                    f"invalid planet length ('{body_data['planet_length']}') for {system_name} -> {body_name}', defaulting to 24"
                )
                body.planet_length = 24

            body.temperature = body_data["temperature"].lower()
            body.type = body_data["type"]
            body.water = body_data["water"].lower()

            for biome_str in body_data["biomes"]:
                try:
                    biome = Biome()
                    if "%" in biome_str:
                        parts = biome_str.split(" ")
                        biome.name = " ".join(parts[0:-1])
                        biome.coverage = float(parts[-1].replace("%", "")) / 100.0
                    else:
                        biome.name = biome_str
                        biome.coverage = 0.0
                    body.biomes.append(biome)
                except ValueError:
                    print(
                        f"invalid biome ('{biome_str}') for {system_name} -> {body_name}', skipping"
                    )

            body.biomes.sort(key=attrgetter("name"))

            body.traits.extend(body_data["traits"])
            body.traits.sort()

            body.resources.extend(body_data["resources"])
            body.traits.sort()

            for dom in body_data["domesticable"]:
                o = OrganicResource()
                parts = dom.split("(")
                o.name = parts[0].strip()
                o.resource = parts[-1].replace(")", "").strip()
                body.domesticable.append(o)

            body.domesticable.sort(key=attrgetter("name"))

            for dom in body_data["gatherable"]:
                o = OrganicResource()
                parts = dom.split("(")
                o.name = parts[0].strip()
                o.resource = parts[-1].replace(")", "").strip()
                body.gatherable.append(o)

            body.gatherable.sort(key=attrgetter("name"))

            galaxy.append(body)
    galaxy.sort(key=attrgetter("system", "name"))

    with open(data_dir.joinpath("galaxy.json"), "w") as fob:
        json.dump(galaxy, fob, indent=2, cls=EnhancedJSONEncoder)


if __name__ == "__main__":
    main()
