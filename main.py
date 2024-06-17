from fastapi import FastAPI, HTTPException,Request, Query
from typing import Dict, Any
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime,timedelta,timezone
import json
import pytz
import joke
import news
import weather


app = FastAPI()
SCOPES = "https://www.googleapis.com/auth/calendar"
CLIENT_SECRET_FILE = r"C:\Users\Hritik\Desktop\final\pythonProject\credentials.json"

API_KEY = 'AIzaSyDEiN0ggCtgBdK9T9SA2eZG3fncm8KAWDA'

PUBLIC_CALENDAR_ID = '2ee7be9bbc93259cf56b41118773c2bee72def9d4920b98855c639bab63be940@group.calendar.google.com'

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
creds = flow.run_local_server(port=3000)

# Build the service
service = build('calendar', 'v3', credentials=creds)


#webhook to handle all the upcoming requests
@app.post("/webhook")
async def webhook(request: Request):
    try:
        req_json = await request.json()
        intent = req_json['queryResult']['intent']['displayName']
        if intent == 'GetReminders':
            return await get_upcoming_events()
        elif intent == 'SetReminder':
            return await create_event(req_json)
        elif intent == 'DelReminder':
            return await delete_event(req_json)
        elif intent == "GetWeather":
            return await weather.get_weather(req_json)
        elif intent == "GetJoke":
            return await joke.get_joke()
        elif intent == "GetNews":
            headlines = news.get_news()
            news_text = "\n\n\n".join(headlines)
            return {"fulfillmentText": news_text}
        else:
            return {"fulfillmentText": "Sorry, I didn't understand that."}
    except Exception as e:
        return {"fulfillmentText": "An error occurred."}


@app.get("/")
def print_text(text: str):
    return {"printed_text": "This is my server!"}


@app.get("/events")
async def get_upcoming_events():
    try:
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        displayMessage = ""
        events_result = service.events().list(calendarId=PUBLIC_CALENDAR_ID, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            displayMessage = displayMessage + 'No upcoming events found.'
            return {"fulfillmentText": displayMessage}
        displayMessage = "The Upcoming events are :\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            dt = datetime.fromisoformat(start)
            # Format the datetime object to a readable string
            readable_date_time = dt.strftime("%B %d, %Y, %I:%M %p  ")
            # Adjust the time zone offset format
            readable_date_time = readable_date_time[:-5] + readable_date_time[-5:-2] + readable_date_time[-2:]
            displayMessage = displayMessage+event['summary']+"    "+readable_date_time+"\n"
        return {"fulfillmentText": displayMessage}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch events")


async def create_event(req_json: Dict[str, Any]):
    try:
        event_start = req_json['queryResult']['parameters']['date-time'][0]
        summary = req_json['queryResult']['parameters']['ReminderTask']
        start_time = datetime.fromisoformat(event_start)
        target_tz = pytz.timezone('Asia/Kolkata')
        start_time = start_time.astimezone(target_tz)
        end_time = start_time + timedelta(hours=1)
        time_zone = 'Asia/Kolkata'
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': time_zone
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': time_zone
            }
        }
        try:
            created_event = service.events().insert(calendarId=PUBLIC_CALENDAR_ID, body=event).execute()
            return {"fulfillmentText": f"Event created successfully."}
        except Exception as e:
            if hasattr(e, 'content'):
                error_content = json.loads(e.content)
            return {"fulfillmentText": f"Event created not successful."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")


async def delete_event(req_json: Dict[str, Any]):
    event_start = req_json['queryResult']['parameters']['date-time'][0]
    summary = req_json['queryResult']['parameters']['ReminderTask'][0]
    event_id = await get_event_id(summary, event_start)
    try:
        # Delete the event
        service.events().delete(calendarId=PUBLIC_CALENDAR_ID, eventId=event_id).execute()
        dt = datetime.fromisoformat(event_start)
        readable_date_time = dt.strftime("%B %d, %Y, %I:%M %p")
        readable_date_time = readable_date_time[:-5] + readable_date_time[-5:-2] + ":" + readable_date_time[-2:]
        return {"fulfillmentText": f"Event {summary} at {readable_date_time} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")


async def get_event_id(summary: str, start_time: str):
    try:
        # Get current UTC time
        now_utc = datetime.utcnow().replace(tzinfo=timezone.utc)
        # Convert UTC to Indian Standard Time (IST)
        now_india = now_utc.astimezone(timezone(timedelta(hours=5, minutes=30)))
        # Format datetime object to string in '%Y-%m-%dT%H:%M:%S%z' format
        now_india_str = now_india.strftime('%Y-%m-%dT%H:%M:%S%z')
        # Call Google Calendar API to list events
        events_result = service.events().list(
            calendarId=PUBLIC_CALENDAR_ID,
            timeMin=now_india_str,  # Use 'Asia/Kolkata' time for comparison
            maxResults=100,  # Adjust as needed
            singleEvents=True,
            orderBy='startTime',
            q=summary  # Search by event summary
        ).execute()
        events = events_result.get('items', [])
        # Iterate through events to find the matching event ID
        for event in events:
            event_start = event['start'].get('dateTime', event['start'].get('date'))
            # Compare summary and start time
            if event['summary'] == summary and event_start == start_time:
                return event['id']  # Return the event ID if found

        # If no matching event is found, raise HTTPException with 404 status code
        raise HTTPException(status_code=404, detail=f"Event '{summary}' at '{start_time}' not found.")
    except HTTPException:
        # Re-raise HTTPException to propagate it
        raise
    except Exception as e:
        # Handle other exceptions and raise HTTPException with 500 status cod
        raise HTTPException(status_code=500, detail=f"Failed to retrieve event ID: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
