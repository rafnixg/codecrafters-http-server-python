"""Utility functions for the server."""
import argparse


def get_directory_path():
    """Get the directory path from the command line arguments.
        --directory <directory_path>
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    if not args.directory:
        return None
    return args.directory
