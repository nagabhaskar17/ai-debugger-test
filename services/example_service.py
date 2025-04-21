import logging
import traceback

class ExampleService:
    @staticmethod
    def get_example_data():
        return {"data": "This is an example response from the service layer."}

    @staticmethod
    def greet_user(name: str):
        return {"greeting": f"Hello, {name}!"}

    @staticmethod
    def get_status():
        return {"status": "Application is running smoothly."}

    @staticmethod
    def simulate_divide_by_zero_error():
        try:
            # Simulate a divide by zero error
            result = 1 / 0
        except ZeroDivisionError as e:
            raise RuntimeError("A division by zero error occurred.") from e

    @staticmethod
    def simulate_conversion_error():
        try:
            # Simulate a conversion error
            invalid_conversion = int("not_a_number")
        except ValueError as e:
            raise RuntimeError("A conversion error occurred.") from e
