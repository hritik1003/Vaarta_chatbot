from fastapi import FastAPI
import random

app = FastAPI()

# A list of jokes to choose from
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't some couples go to the gym? Because some relationships don't work out!",
    "Why don't skeletons fight each other?They don't have the guts.",
    "Why couldn't the bicycle stand up by itself?It was two-tired.",
    "What do you call cheese that isn't yours?Nacho cheese!",
    "Why did the math book look sad?Because it had too many problems.",
    "What's orange and sounds like a parrot?A carrot!"
    "Why did the tomato turn red?Because it saw the salad dressing!",
    "What do you call fake spaghetti?An impasta!",
    "Why did the coffee file a police report?It got mugged!",
    "What did one hat say to the other?You stay here, I'll go on ahead!",
    "What do you call a belt made out of watches?A waist of time!",
    "Why did the golfer bring two pairs of pants?In case he got a hole in one!"
]



async def get_joke():
    """Returns a random joke as fulfillment text."""
    joke = random.choice(jokes)
    return {"fulfillmentText": joke}

