# The Wall

This project contains the back end source code for the Full-Stack: Wall App Assignment.

# Pre-Requisites

In order to run The Wall app, you will need:

1. Docker-compose
2. Sendgrid account. 

# Running The Wall

1. cd into the_wall_api
2. Create a file called varsettings.env to tell Docker the environment variables we need.
3. Create a Sendgrid account.
4. Do docker-compose up

# Sendgrid Account
1. Create a sendgrid account.
2. Settings -> Sender Authentication -> Create a Sender , using a valid email.
3. Settings -> Api Key -> Create Api Key -> Set a name for the Api Key -> Select Restricted Access -> In access details, select mail send and give it full access.
4. Copy the Api Key you have created, because send grid will only  show it once.
5. Set a variable with the name 'SG_KEY' in the varsettings.env and use the api key you obtain in step 4.
6. Set a variable name 'SG_FROM' in the varsettings.env with the email you put as the sender in step 2.

# varsettings.env format:
	SG_KEY=<API_KEY>
	SG_FROM=<EMAIL_SENDER>

