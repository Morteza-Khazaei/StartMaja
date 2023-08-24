import sys
import logging
from StartMaja import StartMaja


if __name__ == "__main__":
    assert sys.version_info >= (3, 5), "Start_maja needs python >= 3.5.\n Run 'python --version' for more info."
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tile", help="Tile number",
                        type=str, required=True)
    parser.add_argument("-s", "--site", help="Site name. If not specified,"
                                                "the tile number is used directly for finding the L1/L2 product directory",
                        type=str, required=False)
    parser.add_argument("-f", "--folder", help="Config/Folder-definition file used for all permanent paths.",
                        type=str, required=True)
    parser.add_argument("-d", "--start", help="Start date for processing in format YYYY-MM-DD. If none is provided,"
                                                "all products until the end date will be processed",
                        type=str, required=False, default="1970-01-01")
    parser.add_argument("-e", "--end", help="Start date for processing in format YYYY-MM-DD. If none is provided,"
                                            "all products from the start date onwards will be processed",
                        type=str, required=False, default="3000-01-01")
    parser.add_argument("-v", "--verbose", help="Provides detailed (DEBUG) logging for Maja. Default is false",
                        default=False, action="store_true")
    parser.add_argument("--nbackward", help="Number of products used to run in backward mode. Default is 8.",
                        type=int, default=int(8))
    parser.add_argument("--overwrite", help="Overwrite existing L2 products. Default is false.",
                        default=False, action="store_true")
    parser.add_argument("--cams", help="Use CAMS during processing."
                                        "The CAMS files have to be available in the repCAMS dir. Default is False.",
                        action="store_true", required=False, default=False)
    parser.add_argument("--type_dem",
                        help="DEM type. If none is given, any will be used", required=False, type=str, default="any",
                        choices=["srtm", "eudem", "any"])
    parser.add_argument("-y", help="Skip workplan confirmation. Default is False",
                        action="store_true", required=False, default=False)
    parser.add_argument("--skip_errors", help="Skip erroneous products without stopping.",
                        action="store_true", required=False, default=False)
    parser.add_argument("--version", action='version', version='%(prog)s ' + str(StartMaja.version))
    parser.add_argument("--platform", help="Manually override which platform to use."
                                            "By default this is deducted by the available input product(s)",
                        choices=["sentinel2", "landsat8", "venus"], type=str, required=False, default=None)
    args = parser.parse_args()

    # TODO Add error skipping
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logger = StartMaja.init_loggers(msg_level=logging_level)

    s = StartMaja(args.folder, args.tile, args.site,
                    args.start, args.end, nbackward=args.nbackward, logger=logger,
                    overwrite=args.overwrite, cams=args.cams,
                    skip_confirm=args.y, platform=args.platform,
                    type_dem=args.type_dem, skip_errors=args.skip_errors)
    s.run()