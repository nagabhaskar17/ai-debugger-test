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
    def calculate_expression(payload: dict):
        text = payload["text"]
        text.replace(" ", "")
        x = payload["x"]
        y = payload["y"]
        z = payload["z"]
        result = x / y + y / z + z / x
        return {"result": result}
