import argparse
from piwardrive import vector_tile_customizer as vtc


def main(argv: list[str] | None = None) -> None:
    """Generate or style MBTiles files."""
    parser = argparse.ArgumentParser(description="Customize vector tile sets")
    sub = parser.add_subparsers(dest="cmd")

    gen = sub.add_parser("build", help="create MBTiles from a tile folder")
    gen.add_argument("folder", help="source directory of XYZ PBF tiles")
    gen.add_argument("output", help="destination MBTiles file")

    style = sub.add_parser("style", help="apply style metadata to an MBTiles file")
    style.add_argument("mbtiles", help="MBTiles file to modify")
    style.add_argument("--style", dest="style_path", help="path to style JSON")
    style.add_argument("--name", help="dataset name")
    style.add_argument("--description", help="dataset description")

    args = parser.parse_args(argv)
    if args.cmd == "build":
        vtc.build_mbtiles(args.folder, args.output)
    elif args.cmd == "style":
        vtc.apply_style(
            args.mbtiles,
            style_path=args.style_path,
            name=args.name,
            description=args.description,
        )
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
