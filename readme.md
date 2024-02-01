# Table of Contents
  1. [About implementation](#about-implementation)
  2. [Setup](#setup)
     1. [Docker](#docker)
     2. [Local Setup](#local-setup)
   3. [API Endpoints](#api-endpoints)
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

# Parts Warehouse API
This repository contains the source code for the Parts Warehouse API, a Django-based application for managing parts and categories.
This application is designed and prepared to seamlessly integrate with MongoDB, a NoSQL database.

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
which is built into the framework I chose. Additionally,
it is simple and quick to develop.

## Setup

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
   SECRET_KEY = 'Django secret key'
   MONGO_CONNECTION_STR = 'mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<database_name>?retryWrites=true&w=majority'
   DATABASE_NAME = 'Database name'
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