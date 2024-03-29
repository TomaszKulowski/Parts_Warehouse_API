# Table of Contents
   1. [Task overview](#task-overview)
      1. [Parts - Model Description](#1-parts---model-description)
      2. [Categories - Model Description](#2-categories---model-description)
      3. [CRUD Operations](#3-crud-operations)
      4. [Search Endpoints](#4-search-endpoints)
      5. [Input Validation](#5-input-validation)
      6. [Dockerization](#6-dockerization)
      7. [JSON Format](#7-json-format)
   2. [About implementation](#about-implementation)
   3. [Setup](#setup)
      1. [Project Requirements](#project-requirements)
      2. [Docker](#docker)
      3. [Local Setup](#local-setup)
   4. [API Endpoints](#api-endpoints)
      1. [Categories](#categories)
         1. [List All Categories](#list-all-categories)
         2. [Add New Category](#add-new-category)
         3. [Retrieve Category Details](#retrieve-category-details)
         4. [Update Category](#update-category)
         5. [Delete Category](#delete-category)
      2. [Parts](#parts)
         1. [List All Parts](#list-all-parts)
         2. [Search Parts](#search-parts)
         3. [Add New Part](#add-new-part)
         4. [Retrieve Part Details](#retrieve-part-details)
         5. [Update Part](#update-part)
         6. [Delete Part](#delete-part)
   5. [Tests](#tests)

# Task overview:
Create a simple RestAPI for a Parts Warehouse. The warehouse contains small parts used in electronic repair workshops.
The API will be connected to a MongoDB database,
and the developer is expected to create his workspace, with some mockup data.
The dataset should include two collections: 'parts' and 'categories'.
The task involves implementing simple CRUD functionality for both collections and adding one additional endpoint for search in a parts collection.
The application should be containerized using Docker.
Input validation for both collections must be implemented using object models created by the candidate.
The API should return results in JSON format.

### 1. Parts - Model Description:
The 'Part' object model represents each part in the warehouse. The mandatory fields are as follows:
- serial_number (str): A unique serial number assigned to each part.
- name (str): The name or model of the part.
- description (str): A brief description of the part.
- category (str): The category to which the part belongs (e.g., resistor, capacitor, IC).
- quantity (int): The quanƟty of the part available in the warehouse.
- price (float): The price of a single unit of the part.
- location (dict): A dictionary specifying the exact location of the part in the warehouse, including
sections such as room, bookcase, shelf, cuvette, column, row.

### 2. Categories - Model Description:
The 'Category' object model represents the categories to which parts belong. The mandatory fields are as follows:
- name (str): The name of the category.
- parent_name (str): If empty, this is a base category. This will be used to create a category tree.

### 3. CRUD Operations:
- Parts collection:
   - Implement CRUD operations (Create, Read, Update, Delete) for the 'parts' collection.
   - Ensure that a part cannot be assigned to a base category.
- Categories collection:
   - Implement CRUD operations for the 'categories' collection.
   - Ensure that a category cannot be removed if there are parts assigned to it.
   - Ensure that a parent category cannot be removed if it has child categories.

### 4. Search Endpoints:
Create one additional endpoint:
- Search for parts based on all mandatory fields – your own implementation.

### 5. Input Validation:
- Implement input validation for both collections.
- Pay special attention to the 'location' field in the 'parts' dataset, which includes sections such as
room, bookcase, shelf, cuvette, column, row.
- Ensure that each part belongs to a category and that a part cannot be in a base category.

### 6. Dockerization:
 - Dockerize the application, ensuring that it can be easily deployed and run in a containerized environment.

### 7. JSON Format:
- Ensure that the API returns results in JSON format and can be consumed with Postman.


## About implementation
In the 'category' field of the Parts model, I decided to store 'category_id (id)' instead of 'category (str)'.
I made this change for easier database maintenance.
Category names may repeat in the case of electronic parts,
for example, the subcategory 'capacitors' may exist in both the SMD and THT categories,
indicating a completely different category. By storing 'category_id',
we won't have a problem locating the parent category.
Additionally, it will be easier to make any changes.

In the Categories model,
I replaced the 'parent_name (str)'field with 'parent_id (id)' for similar reasons as mentioned above.
This change makes it easier to maintain the database,
and we won't have to worry about errors in the case of two identical categories with different parents.

To implement the requested API,
I used the Django Rest Framework because,
based on the initial requirements,
I concluded that such an application would require features like authentication in the future,
which is built into the framework I chose. Additionally, it is simple and quick to develop.

## Setup

### Project Requirements
This project requires Python 3.11 or higher.

Please make sure you have Python 3.11 installed on your system before running any scripts or executing the project.
You can download Python 3.11 from the official Python website.

### Docker
Ensure that Docker is installed on your machine. You can download and install Docker from the official Docker website.
Getting Started
Follow these steps to set up and run the Dockerized application:

1. #### Clone the Repository
    ```bash
    git clone https://github.com/TomaszKulowski/Parts_Warehouse_API.git
    cd Parts-Warehouse-API
    ```

2. #### Set environment
   Adjust the Dockerfile to either set environment variables directly
   or utilize a .env file for managing environment configurations:
   ```
   ENV SECRET_KEY = 'Django secret key'
   ENV MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
   ENV DATABASE_NAME = 'Database name'

   ENV TEST_MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
   ENV TEST_DATABASE_NAME = 'Test database name'
   ```

3. #### Build and Run the Docker Container
   Build and run the Docker container for the Parts Warehouse API:

   ```bash
   docker build -t parts-warehouse-api .
   docker run -p 8000:8000 parts-warehouse-api
   ```

4. #### Access the API
   The API will be accessible at http://localhost:8000.


### Local Setup
Follow these steps to set up the application without using Docker:

1. #### Prerequisites

   Make sure you have the following prerequisites installed before setting up the project:
      - Python 3.11

2. #### Clone the Repository
    ```bash
    git clone https://github.com/TomaszKulowski/Parts_Warehouse_API.git
    cd Parts-Warehouse-API
   ```

3. #### Set Environment
   Set up the required environment variables by creating a .env file in the project root. Adjust the values accordingly.
   ```
   SECRET_KEY = 'Django secret key'
   MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
   DATABASE_NAME = 'Database name'

   TEST_MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
   TEST_DATABASE_NAME = 'Test database name'
   ```

4. #### Install Dependencies
   Install the necessary dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```

5. #### Run Development Server
   Run the development server with:
   ```
   python manage.py runserver
   ```

6. #### Access the API
    The API will be accessible at http://localhost:8000.



## API Endpoints:

The Parts Warehouse API provides the following endpoints for managing parts and categories.

### Categories

#### List All Categories
- URL: /categories/
- Method: GET
- Description: Retrieve a list of all categories.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        [
          {
            "_id": "65bbdd1ecd883f798be3f291",
            "name": "Category A",
            "parent_id": null,
          },
          {
            "_id": "65bbdd1ecd883f798be3f292",
            "name": "Category B",
            "parent_id": "65bbdd1ecd883f798be3f291",
          },
           // ... additional categories
        ]
      ```


#### Add New Category
- URL: /categories/
- Method: POST
- Description: Create a new category.
- Data Params:
  - Required:
    - name=[string]: The name of the category.
  - Optional:
    - parent_id=[string]: The ID of the parent category, if applicable.
- Responses:
  - Status: 201 CREATED
    - Content:
      ```
        {
          "_id": "65bbdd1ecd883f798be3f291",
          "name": "Category B",
          "parent_id": "65bbdd1ecd883f798be3f292",
         }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If a Category with the same 'name' and 'parent_id' already exists.
    - Content:
      ```
      {
        "error": [
          "Category with the same name and parent_id already exists."
        ]
      }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the parent_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65b9295a1835868ddb749' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```


#### Retrieve Category Details
- URL: /categories/<str:object_id>/
- Method: GET
- Description: Retrieve details of a specific category.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65bbdd1ecd883f798be3f291",
          "name": "Category A",
          "parent_id": null,
        }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the parent_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65bbdd1ecd883f798be3f291' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```


#### Update Category
- URL: /categories/<str:object_id>/
- Method: PUT
- Description: Update details of a specific category.
- Data Params:
  - Optional:
    - name=[string]: The name of the category.
    - parent_id=[string]: The ID of the parent category.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65bbdd1ecd883f798be3f291",
          "name": "Category A",
          "parent_id": null,
        }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the parent_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65bbdd1ecd88' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```


#### Delete Category
- URL: /categories/<str:object_id>/
- Method: DELETE
- Description: Delete a specific category.
- Responses:
  - Status: 204 NO CONTENT
    - Reason: If the category is deleted.
    - Content:
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the category is referenced by other objects.
    - Content:
      ```
        {
          "error": "This category cannot be deleted because it is referenced by other objects."
        }
      ```


### Parts


#### List All Parts
- URL: /parts/
- Method: GET
- Description: Retrieve a list of all parts.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        [
          {
            "_id": "65b929a773cd8210b1eb9078",
            "serial_number": "sblnZSkaaMdcEhh",
            "name": "Power Supply",
            "description": "Description.",
            "quantity": 7777777,
            "price": 46.76,
            "location": {
              "room": "R",
              "bookcase": "k",
              "shelf": "A",
              "cuvette": "14",
              "column": "g",
              "row": "14"
            },
            "category_id": "65b9295a1835868ddb749ed4"
            },
            // ... additional parts
        ]
      ```


#### Search Parts
- URL: /parts/search/
- Method: GET
- Description: Search for parts based on specified criteria.
- Data Params:
  - Optional:
    - serial_number=[string]: The unique serial number assigned to the part.
    - name=[string]: The name or title of the part.
    - description=[string]: A detailed description of the part.
    - quantity=[integer]: The quantity of the part available in stock.
    - price=[float]: The price of the part.
    - category_id=[string]: The ID of the category to which the part belongs.
    - room=[string]: The room where the part is located.
    - bookcase=[string]: The bookcase or storage unit within the room.
    - shelf=[string]: The specific shelf on the bookcase.
    - cuvette=[string]: The cuvette or compartment on the shelf.
    - column=[string]: The column or section in the cuvette.
    - row=[string]: The row or position within the column.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65b929a773cd8210b1eb907b",
          "serial_number": "sOwLuPSPUb",
          "name": "Integrated Circuit",
          "description": "Break white management card risk say ten project.",
          "quantity": 777777733,
          "price": 37.32,
          "location": {
            "room": "12",
            "bookcase": "k",
            "shelf": "A",
            "cuvette": "14",
            "column": "g",
            "row": "54"
            },
          "category_id": "65b929a773cd8210b1eb907a"
         }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the category_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65bbdd1ecd88' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```

#### Add New Part
- URL: /parts/
- Method: POST
- Description: Create a new part.
- Data Params:
  - Required:
    - serial_number=[string]: The unique serial number assigned to the part.
    - name=[string]: The name or title of the part.
    - description=[string]: A detailed description of the part.
    - quantity=[integer]: The quantity of the part available in stock.
    - price=[float]: The price of the part.
    - category_id=[string]: The ID of the category to which the part belongs.
    - room=[string]: The room where the part is located.
    - bookcase=[string]: The bookcase or storage unit within the room.
    - shelf=[string]: The specific shelf on the bookcase.
    - cuvette=[string]: The cuvette or compartment on the shelf.
    - column=[string]: The column or section in the cuvette.
    - row=[string]: The row or position within the column.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65b929a773cd8210b1eb907b",
          "serial_number": "sOwLuPSPUb",
          "name": "Integrated Circuit",
          "description": "Break white management card risk say ten project.",
          "quantity": 777777733,
          "price": 37.32,
          "location": {
            "room": "12",
            "bookcase": "k",
            "shelf": "A",
            "cuvette": "14",
            "column": "g",
            "row": "54"
            },
          "category_id": "65b929a773cd8210b1eb907a"
         }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the category_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65bbdd1ecd88' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```

#### Retrieve Part Details
- URL: /parts/<str:object_id>/
- Method: GET
- Description: Retrieve details of a specific part.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65b929a773cd8210b1eb907b",
          "serial_number": "sOwLuPSPUb",
          "name": "Integrated Circuit",
          "description": "Break white management card risk say ten project.",
          "quantity": 777777733,
          "price": 37.32,
          "location": {
            "room": "12",
            "bookcase": "k",
            "shelf": "A",
            "cuvette": "14",
            "column": "g",
            "row": "54"
            },
          "category_id": "65b929a773cd8210b1eb907a"
         }
      ```

#### Update Part
- URL: /parts/<str:object_id>/
- Method: PUT
- Description: Update details of a specific part.
- Responses:
  - Status: 200 OK
    - Content:
      ```
        {
          "_id": "65b929a773cd8210b1eb907b",
          "serial_number": "sOwLuPSPUb",
          "name": "Integrated Circuit",
          "description": "Break white management card risk say ten project.",
          "quantity": 777777733,
          "price": 37.32,
          "location": {
            "room": "12",
            "bookcase": "k",
            "shelf": "A",
            "cuvette": "14",
            "column": "g",
            "row": "54"
            },
          "category_id": "65b929a773cd8210b1eb907a"
         }
      ```
  - Status: 400 BAD REQUEST
    - Reason: If the category_id is not a valid ObjectId.
    - Content:
      ```
        {
          "error": "'65bbdd1ecd88' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
        }
      ```

#### Delete Part
- URL: /parts/<str:object_id>/
- Method: DELETE
- Description: Delete a specific part.
- Responses:
  - Status: 204 NO CONTENT
    - Reason: If the part is deleted.
    - Content:
      ```

Explore the API endpoints by navigating to http://localhost:8000/categories and http://localhost:8000/parts.


### Tests
This repository contains tests for the project. Below are instructions on how to run the tests.

To run the tests, follow these steps:

#### Running Tests

Navigate to the root directory of the project in your terminal.
Run the following command:

   ```
   python manage.py test
   ```

This command will execute all the tests defined within the project.
After running the command, you will see the test results displayed in the terminal.

Make sure all tests pass before pushing changes to the repository or deploying the project.
If any tests fail, review the output to identify and fix the issues before proceeding.

#### Additional testing commands
For testing purposes, you can use the following commands to add fake categories:
```
python manage.py add_fake_categories -n 10
```
or to add fake parts and the categories:
```
python manage.py add_fake_parts -n 10
```
