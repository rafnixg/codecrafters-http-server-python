"""Utility functions for the server."""

import argparse

from app.server.constant import HOST, PORT


def get_directory_path():
    """Get the directory path from the command line arguments.
    args:
        --directory: str: The directory path.
    returns:
        str: The directory path.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    if not args.directory:
        return None
    return args.directory


def print_welcome_message():
    """Print the welcome message."""
    print("Welcome to the HTTP server!")
    print(f"Listening on {HOST}:{PORT}...")
    print("Press Ctrl+C to quit.\n")
    print("HTTP Compression is enabled: gzip\n")
    print("Available endpoints:")
    print("GET /")
    print("GET /echo/<message>")
    print("GET /user-agent")
    print("GET /files/<filename>")
    print("POST /files/<filename>")
