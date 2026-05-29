# Flasky Web Application - REST API Enhancement (Categories Feature)

This repository is my official submission for the IT6 Final Drill assessment. The project extends Miguel Grinberg's baseline modular Flask application by adding a new Categories endpoint group under the core API blueprint.

## Added Feature and Business Value

To improve the application's unorganized blog feed, this enhancement allows users and administrative clients to classify blog posts into specific topics. 

First, we established a One-to-Many Relationship where a single category can contain multiple blog posts, but each post is tied strictly to one category. Second, we integrated a Full CRUD Lifecycle which provides explicit API routes to Create, Read, Update, and Delete categories dynamically using JSON payloads.

## Architecture and Code Changes

The modifications were implemented across the following project files:

app/models.py: Created the new Category database model, added the to_json and from_json helper methods, and updated the existing Post model to include a category_id foreign key constraint.

app/api/categories.py: Developed the REST API route handlers handles the CRUD endpoints, input data validation, and appropriate HTTP status responses like 201 Created and 400 Bad Request.

app/api/__init__.py: Registered the new categories API endpoint module inside the native Flask Blueprint framework.

openapi.json: Wrote the structural API documentation mapping the endpoints and sample payloads.

## Local Test Execution Instructions

To run the complete automated unit test suite and verify the code coverage, execute the following command in your terminal:

flask test