# PokerStats
#### Video Demo:  [<https://youtu.be/hADV1pMRuHs?si=bo--AK21WjUO0F9g>]
#### Description:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is a web app that allows users to track their performance in poker over time. There are 5 main views: 
1. **Register Page (sign-up.jinja2)**: This page extends base.html, providing inputs for email, password, and password confirmation fields. The user can click the **"Submit"** button to register a new account with the app. Once registered, the user will be redirected to the login page (sign-in.jinja2). In the event that the email is already registered, a flash message will notify the user and provide a redirect link to the sign-in page. Lastly, the user may select the PokerStats icon to be navigated back to the homepage (homepage.htjinja2ml).
<br>
2. **Sign-In Page (sign-in.html)**: This page also extends base.html, providing inputs for email and password as well as the "Sign In" button. This page also has the PokerStats icon which allows the user to navigate back to the homepage. The user has access to a link to Register on this page.
<br>
3. **Homepage (homepage.jinja2)**: This page contains the title of the web app along with the pokerstats icon and an empty-user.png in place of a profile picture. The profile-pic icon is a dropdown which directs the user either to the **"Login"** or **"Register"** pages. After the user logs in, the are automatically redirected from the sign-in page to the homepage. If they've previously recorded any data of past poker performance, they will see plotly plots which showcase those data. If not, they have a couple of options:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. **New Round**:<p style="margin-left: 80px; max-width: 700px;">By clicking the dropdown profile pic icon, the user will see the "New Round" option at the top of the list. Clicking on this button will redirect them to the **"New Round"** Page, which we discuss further in a later bullet.</p>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. **Profile**:<p style="margin-left: 80px; max-width: 700px;">By clicking the dropdown profile pic icon, the user will see the **"Profile"** option at the top of the list. Clicking on this button will redirect them to the **Profile** Page, which we discuss further in a later bullet.</p>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. **Sign Out**:<p style="margin-left: 80px; max-width: 700px;">By clicking the dropdown profile pic icon, the user will see the **"Sign Out"** option at the bottom of the list. Clicking on this button will sign them out and redirect them to the starting point in homepage.jinja2.</p>
<br>
4. **Profile Page (profile.jinja2)**: The first thing the user sees are the column names for the pokwer data they will be tracking. If they are logging in for the first time, they will see that no data has been populated yet. Just above the column headers, on the left, the user will see the **"New Round"** button, which will redirect them to the "New Round" page upon clicking. The user will also see the profile pic empty-user icon in the top right. Hovering over this ico, they will see the option to upload a new profile picture, which will work upon clicking.
<br>
5. **New Round (new_round.jinja2)**: This page provides entries for the following data: date, buy-in, take-home, # of times all-in, # of times standup game lost, additional buy-in, and seat position. Once the user enters data for these fields, they can click the **"Submit"** button to store that data to their profile. Clicking this button will redirect them to the **Homepage** where they will see their data plotted across three different plotly plots.

### Design
**Homepage Plots (homepage.jinja2, app.py)**: I originally started with matplotlib, but the methodology there is to convert the plots to png and then insert the png to the page. This looked tacky, so I decided to go with plotly, which allowed more freedom to design the plots in a way that they appear to match the color scheme of the page.

**PokerStats Logo**: after prompting ChatGPT for a logo for this app, the logo you see on the web page is what ChatGPT came up with.

**Page color schemes**: I got inspiration from the Bootstrap examples for headers and sign-in screens. A lot of the html I user in my pages were borrowed from these examples. This includes the profile pic dropdown.

**Database per profile**: Thanks to the guidance from ChatGPT, I learned the concept of using sessions to manage which data to use for the plots based on the user's sign-in status. The way this works is that when a new session starts (when a new round is started), it will create a new database table with the name being "session_id". This allows me to query the tables in my database, and then use those data for plotting on the web page.


### References:
1. Bootstrap Examples: <https://getbootstrap.com/docs/5.0/examples/>
2. ChatGPT: <https://chatgpt.com/>
