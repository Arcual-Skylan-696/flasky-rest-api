# Flasky Web Application - REST API Enhancement (Categories Feature)

This repository contains my submission for the IT6 Final Drill. The project extends the baseline modular Flask application by adding a new Categories endpoint group under the core API blueprint.

## Added Feature and Business Value

To organize the blog feed, this enhancement allows users to classify blog posts into specific topics. 

First, a One-to-Many Relationship was established where a single category can contain multiple blog posts, but each post is tied strictly to one category. Second, we integrated a Full CRUD Lifecycle which provides explicit API routes to Create, Read, Update, and Delete categories dynamically using JSON payloads.

## Architecture and Code Changes

The modifications were implemented across the following project files:

app/models.py: Created the new Category database model, added the to_json and from_json helper methods, and updated the existing Post model to include a category_id foreign key constraint.

app/api/categories.py: Developed the REST API route handlers to manage the CRUD endpoints, input data validation, and HTTP status responses like 201 Created and 400 Bad Request.

app/api/__init__.py: Registered the new categories API endpoint module inside the Flask Blueprint framework.

openapi.json: Updated the structural API documentation mapping the endpoints and sample payloads.

## Installation Procedures and Setup

To run this backend REST API project locally, follow these steps:

1. Clone the repository and navigate to the project directory:
   git clone https://github.com/Arcual-Skylan-696/flasky-rest-api.git
   cd flasky-rest-api

2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install all the required packages:
   pip install -r requirements.txt

## Local Test Execution Instructions

To run the complete automated unit test suite and verify that all 44 test cases pass successfully, execute this command in your terminal:

python -m unittest discover -s tests