import os
import random
from fastapi import FastAPI, Query

app = FastAPI()
mult = os.environ.get('MULTIPLIER', 1)


"""
Generates and returns a random number within a specified range.

This endpoint accepts optional query parameters 'min' and 'max' to define the range for the random number generation.
If not provided, 'min' defaults to 1 and 'max' defaults to 100. Both parameters must be greater than or equal to 1.

Args:
    min (int, optional): The minimum value for the random number (inclusive). Defaults to 1. Must be >= 1.
    max (int, optional): The maximum value for the random number (inclusive). Defaults to 100. Must be >= 1.

Returns:
    dict: A dictionary containing the min, max, generated random number, and a descriptive message.
"""
@app.get('/')
def give_a_num(min: int = Query(1, ge=1), max: int = Query(100, ge=1)):
  rand = random.randint(int(min), int(max)) * int(mult)
  return {
    'min': min,
    'max': max,
    'mult': mult,
    'rand': rand,
    'message': f"Here is a random number {rand} between {min} and {max}, multiplied by {mult}"
  }
