import yaml
import logging
import pathlib
from datetime import datetime
import os


cwd = pathlib.Path.cwd()
logs_folder = cwd.joinpath("Logs")
output_folder = cwd.joinpath("Output")


def fibonacci_generator():
    """
    Create a generator for fabonacci series which will be produced lazily, one at a time
    and wont return all at once
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_yaml(file_path: str) -> dict:
    with open(file_path, "r") as ymlfile:
        logging.info(f"Reading {file_path}")
        return yaml.load(ymlfile, Loader=yaml.CLoader)


def dump_yaml(parameters: dict, file_path: str) -> bool:
    with open(file_path, "w") as ymlfile:
        logging.info(f"Dumping {file_path}")
        yaml.dump(parameters, ymlfile)
    return True


def setup_logging():
    if not logs_folder.exists():
        print("Creating logs folder")
        logs_folder.mkdir()

    if not output_folder.exists():
        print("Creating output folder")
        output_folder.mkdir()

    now = datetime.today().strftime("%d%m%Y")
    log_file = logs_folder.joinpath(f"{now}.log")

    if not log_file.exists():
        print(f"Creating {now}.log")
        with open(log_file, "w") as f:
            os.utime(log_file, None)
            f.close()

    logging.basicConfig(
        filename=f"Logs/{now}.log",
        format="%(asctime)s\t|\t%(levelname)s\t|\t%(message)s",
        level=logging.INFO,
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    logging.info("tool started")
