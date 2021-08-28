# Climb@
### A Mountain Project Clone

Thank you for checking out my Climb@ app. This app is a clone of The Montain Project app. It accesses the Open Beta API to bring you real climbing locations near you.

Table of Contents:
* [Features](#features-included)
* [Future Features](#future-features)
* [Run Climb@ locally](#run-app-locally)
* [Links](#links)

#### Features Included:

1. Creating a User Profile
    * Add a Bio
    * Edit account Info
    * Log climbs as Complete or ToDo
2. Search For Climbs
    * Search a region
    * Search by name
    * Search by Lat / Long

#### Future Features:
1. Dryness Index
    * Using a weather API to predict the moisure level of a climb.
    * Allows you to see predicted dryness index for planing trips.
2. User comentary
    * Users will be able to comment on climbs.
    * Users will be able to submit updates about climbs.
    * Users will be able to chat with each other.

---

# Run App Locally

To run this app locally you will need to use a bash terminal and python3 to run the following commands.

You must also have a psql server up and running for this project to work locally.

1. Assuming you have postgres installed run:
    >sudo service postgresql start

2. Create and open VENV in the root folder:
    >python3 -m venv venv
    <br>
    source venv/bin/activate
* Note: 'source venv/bin/activate' needs to be run each time you open the project.

3. Use the requirements.txt file to download all dependencies while VENV is activated.

4. Next run:
    > createdb make-change

5. Now you can run the seed.py file:
    > python3 seed.py

6. Finally to run the site:
    > flask run

Thank you for your time.

# Links

* [Climb@ WebSite][ClimbAtWeb]
* [Wills Portfolio][WSWeb]
* [Open Beta API][OpenBeta]
* [Montain Project][MTNProject]

[ClimbAtWeb]: https://www.william-stiles.com/
[WSWeb]: https://www.william-stiles.com/
[OpenBeta]: https://openbeta.io/api/
[MTNProject]: https://www.mountainproject.com/