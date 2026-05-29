# Flasky Web Application - REST API Enhancement (Categories Feature)

This repository is a submission for the IT6 Final Drill assessment. It extends Miguel Grinberg's baseline modular Flask social application by introducing a feature-rich, RESTful **Categories** endpoint group under the core API blueprint.

## Added Feature & Business Value
To move away from an unorganized blog feed, this expansion allows administrative elements and programmatic API actors to classify structural blog data. 
* **One-to-Many Relationship:** Each single category entity maps natively to multiple target Blog Posts.
* **Full CRUD Lifecycle:** Integrates API routes to Create, Read, Update, and Delete categories dynamically via JSON parameters.

## Architecture & Code Modification Locations
* **`app/models.py`**: Declared the standard relational `Category` table entity with transactional JSON schemas (`to_json`/`from_json`) and integrated a restrictive foreign key constraint tracking column (`category_id`) inside the preexisting `Post` schema.
* **`app/api/categories.py`**: Implemented explicit resource route endpoints utilizing custom validation patterns and strict HTTP response tracking status codes (`201 Created`, `400 Bad Request`, etc.).
* **`app/api/__init__.py`**: Registered the extension file natively within the original Flask Blueprint container framework.
* **`openapi.json`**: Created structural OpenAPI documentation mapping data payload paths.

## Local Test Execution Instructions
To execute the newly developed unit test container suite achieving complete code coverage, run the application test environment macro terminal command:
```powershell
flask test