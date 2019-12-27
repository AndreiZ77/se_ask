Task for the company BFG
==========================
Search for a given string using API StackExchange

Designed using Python 3.7 + AIOHTTP (09/2019)


Setup
=====


Clone the repository, create virtualenv if necessary.

Install the packages necessary for work: look requirements.txt
    
To start the application you need running Postgres & Redis servers.

Create db with tables and sample data::

    $ python init_db.py

Run server::

    $ python se_app/main.py

