# Phase-3-Code-Challenge-Articles---without-SQLAlchemy
## project overview
This project it focuss on the models of the relationship between Authors, Artcle and also magazine  using Python and raw SQL queries. It demonstrates how to manage many-to-many relationships and transactions in a relational database, simulating a real-world scenario where authors write articles for various magazines.

## problem statement 

An Author can write many Articles.

A Magazine can publish many Articles.

Each Article belongs to both an Author and a Magazine.

The relationship between Authors and Magazines is many-to-many.


## The project guidlines

Project Setup and Environment
Created a Python virtual environment using venv.

Installed necessary dependencies like pytest for testing and sqlite3 for database management.

Structured the project with clear separation between models, database connection, seed data, and tests.

## Data schema


Designed SQL tables for authors, magazines, and articles with appropriate foreign keys to represent relationships.

Used SQLite for simplicity and easy setup.

Created the schema in lib/db/schema.sql and applied it through a setup script.


## model classes 
implemented python classes Author, Article and magazine in the ib/models/ directory.

Each class includes methods to:

Save instances to the database.

Query records by various attributes.

Retrieve associated objects (e.g., an author’s articles, magazines an author contributed to).


## Relationship methods
For the Author class:

articles(): Returns all articles authored by this individual.

magazines(): Provides a list of distinct magazines to which the author has contributed.

add_article(magazine, title): Creates a new article linked to this author and the specified magazine.

topic_areas(): Lists the unique categories or genres of magazines the author has written for.

## magazine class

articles(): Retrieves all articles published within the magazine.

contributors(): Lists all authors who have contributed articles to the magazine.

article_titles(): Provides the titles of every article featured in the magazine.

contributing_authors(): Identifies authors who have written more than two articles for the magazine.

## Testing

Wrote unit tests for each model in the tests/ directory.

## usage

Run python scripts/setup_db.py to create and seed the database.

Run tests using  
pytest

## Author
Ibrahim Abdullahi





