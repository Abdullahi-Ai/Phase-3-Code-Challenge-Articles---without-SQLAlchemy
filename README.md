## Project Overview
This project focuses on modeling the relationships between Authors, Articles, and Magazines using Python along with raw SQL queries. It showcases how to handle many-to-many relationships and database transactions in a relational database setup, reflecting a real-world scenario where authors contribute articles to various magazines.

## Problem Statement
An Author can write multiple Articles.

A Magazine can publish numerous Articles.

Each Article is associated with both an Author and a Magazine.

The connection between Authors and Magazines is many-to-many.

## Project Guidelines
Set up a Python virtual environment using venv.

Installed necessary packages such as pytest for testing and sqlite3 for managing the database.

Organized the project with a clear separation of concerns: models, database connections, seed data, and tests.

## Data Schema
Designed SQL tables for authors, magazines, and articles, incorporating foreign keys to represent their relationships properly.

Used SQLite for simplicity and easy setup.

Created the database schema inside lib/db/schema.sql and applied it using a setup script.

## Model Classes
Implemented Python classes — Author, Article, and Magazine — within the lib/models/ directory.

Each class contains methods to save instances to the database, query records based on different attributes, and retrieve related objects, such as articles written by an author or magazines they’ve contributed to.

## Relationship Methods
For the Author class:

articles(): Fetches all articles written by the author.

magazines(): Returns a list of unique magazines the author has contributed to.

add_article(magazine, title): Adds a new article for this author under the specified magazine.

topic_areas(): Lists distinct categories or genres of magazines the author has written for.

Article magazine and author it's in the models file

## For the Magazine class:

articles(): Retrieves all articles published in the magazine.

contributors(): Lists all authors who have written articles for the magazine.

article_titles(): Provides the titles of every article in the magazine.

contributing_authors(): Identifies authors who have contributed more than two articles to the magazine.

## Testing
Developed unit tests for each model and placed them in the tests/ directory to ensure functionality.

## Usage
Run python scripts/setup_db.py to create and seed the database.

## Use pytest to run all tests.

## Author
Ibrahim Abdullahi