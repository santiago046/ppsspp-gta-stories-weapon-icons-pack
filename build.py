#!/usr/bin/python3

import argparse
from pathlib import Path
from zipfile import ZipFile

PSP_GAME_CODES = {
    "LCS": [
        "ULES00151",
        "ULES00182",
        "ULKS46157",
        "ULJM05255",
        "ULJM05885",
        "ULUS10041",
    ],
    "VCS": ["ULES00502", "ULES00503", "ULJM05884", "ULJM05297", "ULUS10160"],
}


def create_ini(hash_type, reduce_hash, game):
    codes = "\n".join(
        f"{code} = textures.ini" for code in PSP_GAME_CODES[game.upper()]
    )

    hashes_file = (
        Path("./hashes")
        / f"{game}_{hash_type}{'r' if reduce_hash else ''}.txt"
    )

    textures_ini = f"""[options]
version = 1
hash = {hash_type}
ignoreAddress = true
ignoreMipmap = true
reduceHash = {'true' if reduce_hash else 'false'}

[games]
{codes}

[hashes]
{hashes_file.read_text()}

[hashranges]

[filtering]

[reducehasranges]"""

    return textures_ini


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Build the ZIP texture pack",
    )
    parser.add_argument(
        "-c",
        "--icon-color",
        choices=["blue", "orange", "original", "white"],
        default="original",
        help="choose the icons color. Valid values are: blue, orange, original or white",
        metavar="<color>",
        type=str.lower,
    )
    parser.add_argument(
        "-r",
        "--reduce-hash",
        action="store_true",
        help="enable reducedHash in textures.ini file",
    )
    parser.add_argument(
        "-t",
        "--hash-type",
        choices=["xxh32", "xxh64"],
        default="xxh64",
        help="set the hash type for textures.ini file. Valid values are: xxh32 or xxh64",
        metavar="<type>",
        type=str.lower,
    )
    parser.add_argument(
        "game",
        choices=["lcs", "vcs"],
        help="set the game. Valid values are: LCS or VCS",
        metavar="GAME",
        type=str.lower,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    dest_zip_file = f"{args.game}-{args.hash_type}{'r' if args.reduce_hash else ''}-{args.icon_color}.zip"
    icons_path = Path("./icons") / args.game / args.icon_color

    # Pack into ZIP
    with ZipFile(dest_zip_file, "w") as zip_file:
        zip_file.writestr(
            "textures.ini",
            create_ini(args.hash_type, args.reduce_hash, args.game),
        )

        for file in icons_path.glob("*.png"):
            zip_file.write(file, Path("HUD/weapon_icons") / file.name)


if __name__ == "__main__":
    main()
