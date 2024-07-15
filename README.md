# TeleCog 
TeleCog is a telephone cognition screener server. It will ask the caller to perform a simple cognitive test and return the results. 

The service is ran using a webserver connected to twilio. 

## Prerequisite

- have a twilio account + number
- have a way to connect the server to the twilio webhook (e.g. ngrok.com)

## Setup

- create an .env file in `telecog` subfolder and add your twilio credentials `TWILIO_ACCOUNT_SID` and
`TWILIO_AUTH_TOKEN` 
- make sure your twilio webhook for incoming calls is connected to your api gateway that can reach your webserver
- start the webserver with `python manage.py runserver`
