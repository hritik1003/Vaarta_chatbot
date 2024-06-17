## VAARTA: THE PERSONAL AI CHATBOT


## Description
Vaarta is a chatbot that responds to the user's query using the concept of natural language processing. In this, it responds to the human language. It is connected to Google Calendar for retrieving events and creating events to get reminders to the e-mail. We can do the following tasks using it:
 1. Scheduling an event (e.g. Remind me to sleep at 10 pm)
 2. Deleting an event (e.g. Delete sleep at 10 pm)
 3. Getting the upcoming events (e.g Show my schedule)
 4. Getting the weather of a location (e.g. What is the weather of Delhi)
 5. Getting the headlines (e.g. Show me the headlines)
 6. Getting a random funny joke (e.g. Get me a joke)


## Installation instructions:
#RUN THESE COMMANDS ON THE TERMINAL:
 1. pip install fastapi
 2. pip install google-auth-OAuth lib
 3. pip install google-api-python-client
 4. pip install pytz
 5. pip install uvicorn
 6. pip install requests
 7. pip install pydantic


## Setup and Usage:
 1. Unzip the agent Calendar-bot and upload it on your Dialogflow console
 2. Go to the google cloud console and generate a 'credentials.json' file by creating a service account and OAuth 2.0 Client ID download the client ID and rename it as 'credentials.json'.
 3. Don't forget to add the Google Calendar scope and the indirect URI in the OAuth verification.
 4. Run the file main.py and grant permission to use your Google calendar.
 5. Now go to integrations on the Dialogflow and integrate your bot as per your choice like a telegram.
 6. Enjoy your bot.


## Documentation
Python_packages_description.md: to know more about used Python packages.


## Contact
Name: Hritik Agarwal \
Email: hritikagarwal96@gmail.com

