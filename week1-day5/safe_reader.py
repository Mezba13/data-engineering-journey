import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers = [
                        logging.FileHandler('pipeline.log'),
                        logging.StreamHandler()
                    ]
                    )

def read_safe_file(file_path):
    """
    Reads a file safely, ensuring that the file exists and is readable.
    
    """

    logging.info(f"Attempting to read file: {file_path}")

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path,'r',encoding='utf-8') as file:
            contest=file.read()
        logging.info(f"Success: Read {len(contest)} characters from {file_path}")

    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        return None
    except PermissionError as e:
        logging.error(f"PermissionError: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def divide_numbers(a, b):
    """
    Divides two numbers safely, handling division by zero.
    
    """
    logging.info(f"Attempting to divide {a} by {b}")

    try:
        result = a / b
        logging.info(f"Success: {a} divided by {b} is {result}")
        return result
    except ZeroDivisionError as e:
        logging.error(f"ZeroDivisionError: Cannot divide by zero. {e}")
        return None
    except TypeError as e:
        logging.error(f"TypeError: Invalid types for division. {e}")
        return None

if __name__=='__main__':
    content = read_safe_file(r"C:\Users\Lenovo\Desktop\data-engineering-journey\week1-day3\clean_netflix.csv")
    print(f"\n File read success:{content is not None}")

    content=read_safe_file('fake_file.txt')
    print(f"\n File read success:{content is None}")

    print(f"\n10 / 2 = {divide_numbers(10, 2)}")
    print(f"10 / 0 = {divide_numbers(10, 0)}")
    print(f"'a' / 2 = {divide_numbers('a', 2)}")
    
    print("\nCheck pipeline.log for full logs.")
