import logging
import os
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

config_ = config["logging"]


def create_log_file():
    # Check if the log file exists
    if not os.path.exists(config_["file_path"]):
        # If it doesn't exist, create a new file
        with open(config_["file_path"], "w") as f:
            f.write("")  # it just doesn't work without this line
            # Configure the logging module
            write_log("Log file created", 200)


def write_log(message:str, code:int) -> None:
    """
    Writes a message to the log file.

    Args:
        message (str): message to write
        code (int): code of the message
    """
    
    code = str(code)
    # Configure the logging module
    logging.basicConfig(
                filename=config_["file_path"],
                format=config_["format"],
                level=config_["level"]
            )
    if code[0] == "2" or code[0] == "1":
        logging.info(f'{code} - {message}')
    elif code[0] == "3":
        logging.warning(f'{code} - {message}')
    elif code[0] == "4":
        logging.error(f'{code} - {message}')
    elif code[0] == "5":
        logging.critical(f'{code} - {message}')
        
        
if __name__ == "__main__":
    create_log_file()
    write_log("Test", 100)
    write_log("Test", 200)
    write_log("Test", 300)
    write_log("Test", 400)
    write_log("Test", 500)