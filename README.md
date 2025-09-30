# Bored.com
#### Video Demo:  <https://youtu.be/YOiMQ0F7ZZs>
#### Description:
TODO
Connecting bored people so they can have a fun time doing stuff together!
People located near each other can go for runs together, bike trips, road trips, or just a simple meal together,
instead of feeling bored at home or feeling alone.

Here are all the functions in Bored.com:
Register:
Users need to create username and password, and input their age and sex.
Their password need to be confirmed, and their age must be above 18.
Users can also input their location, email, and phone number voluntarily.
All such user information are stored in the project_db database, in the users table.


Login:
Once registered, users can login using their username and password.


Logout:
Click the logout button on top right corner to logout.


Index:
The default index page of the website shows all the available and upcoming activities, displaying the location, time, type of activity, and the contact info.
Google maps API is also used to visually display the locations with activities.


Find:
Users can find specific activities based on the location and type of activities. The search algorithm is based on keyword similarity instead of verbatim results, which increases convenience and usability. However, further improvements can be made to safeguard against injection attacks.


New Activity:
User can create a new activity by clicking on the "New Activity" button on the navigation toolbar, and type in the activity type that the user has in mind. It can be a sport event, such as a soccer match or casual tennis drop-in, as well as a book study meetup on a Thursday afternoon. It's all up to you! The user then needs to specify the time and date of the event, as well as the location of the activity. The time and date is programed to only allow future date and time. Currently, there are only a few locations available, but improvements can be made to dynamically support users' location inputs.
After the new activity is created, all the information is stored in project_db under the "activity" table.


Supported locations:
Currently, we (the web developer) have to manually update the database if we were to include a new location, for example a new city like Hamilton. All the available locations are stored in the locations table in project_db. However, this is not good design from a software standpoint, and we are trying to dynamically allow users to start activities in new locations without having to update the database and maps manually each time.


Current Developments:
We are currently looking at adding a forget username/password feature, allowing users to add and edit details about each activity, and perhaps giving each activity its own detailed page with a link on the index page

