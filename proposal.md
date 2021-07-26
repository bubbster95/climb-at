# Climb@

1. What goal will your website be designed to achieve?
	To list all of the recorded climbs in a local area by accessing a climbing API

2. What kind of users will visit your site? In other words, what is the demographic of
your users?
	Climbers In the US who like bouldering, Trad and Free climbing outdoors.

3. What data do you plan on using? You may have not picked your actual API yet,
which is fine, just outline what kind of data you would like it to contain.
	The Open Beta api, is compiled by my target demographic https://openbeta.io/api

4. In brief, outline your approach to creating your project (knowing that you may not
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:

    A. What does your database schema look like?
	>Isn’t that decided by the API? It should be something like:
    - Id
    - Title
    - Location
    - Description
    - Latitude
    - Longitude
    - Notes


    B. What kinds of issues might you run into with your API?

	>The API might not have complete data, it was compiled by climbers afterall
	Writing the filter feature might prove to be tough
	
    C. Is there any sensitive information you need to secure?

	>If I choose to build a User feature then I’d have to encrypt passwords
	And the API uses a key but that's not really sensitive.

    D. What functionality will your app include?

	>You can search the database for local climbs,
	Climbs in other areas
	Search by climb name?
	Search by climb level and type

    E. What will the user flow look like?

	> Enter the site
	Filter search
	Show results
	Pick a result to look at
	Mark that climb?

    F. What features make your site more than CRUD? Do you have any stretch goals?

	> If i choose to make a user profile then there will be an extra database to track user progress
	Users will be able to track what climbs they have visited, if they finished it.
	But a stretch goal I’d really like to meat is to pair each climb with a weather forecast using a second API. the climbs have a location which means i can sync it with a weather forecast for the LAT and LONG.
	
