# Make Change Code Test

You will need to use a bash terminal and python3 to run the following commands to set this project up.

You must also have a psql server up and running for this project to work locally.

1. Assuming you have postgres installed run:
    >$ sudo service postgresql start

2. Create and open VENV in the root folder:
    >$ python3 -m venv venv

    >$ source venv/bin/activate

3. Use the requirements.txt file to download all dependencies into this VENV folder.

4. Next, in your bash terminal run:
    > $ createdb make-change

5. Now you can run the seed.py file:
    > $ python3 seed.py

6. Finally to run the site:
    > $ flask run

Thank you for your time.