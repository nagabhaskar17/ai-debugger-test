from fastapi import APIRouter
from services.example_service import ExampleService

router = APIRouter()

@router.get("/example")
def example_endpoint():
    return ExampleService.get_example_data()

@router.get("/greet/{name}")
def greet_user(name: str):
    return {"greeting": f"Hello, {name}!"}

@router.get("/status")
def get_status():
    return {"status": "Application is running smoothly."}

@router.get("/error/divide-by-zero")
def trigger_divide_by_zero_error():
    return ExampleService.simulate_divide_by_zero_error()

@router.get("/error/conversion")
def trigger_conversion_error():
    return ExampleService.simulate_conversion_error()
