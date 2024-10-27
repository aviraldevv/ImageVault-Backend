# ImageVault Backend

ImageVault is an image search and download web application built with FastAPI and PostgreSQL. The backend provides endpoints for user authentication, image search, download tracking, and API integration with the Pexels image service.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Key Endpoints](#key-endpoints)


## Features

- **User Authentication**: User signup, login, and token-based authentication with JWT.
- **Image Search**: Fetch images using the Pexels API.
- **Download Tracking**: Track and retrieve images downloaded by each user.
- **Protected Routes**: Authenticated routes accessible only with a valid JWT token.

## Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT Authentication
- **API Integration**: Pexels API

## Prerequisites

Before starting, ensure you have:

- Python 3.8+
- PostgreSQL installed and running
- Pexels API Key
- Virtual environment (recommended)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/imagevault-backend.git
    cd imagevault-backend
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate   # For Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Create a `.env` file in the root directory to set up the following environment variables. These variables are essential for the backend's operation:

```plaintext
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost/imagevault_db
PEXELS_API_KEY=your_pexels_api_key
```
- `SECRET KEY`: Key used to sign JWT tokens for secure authentication.
- `DATABASE_URL`: PostgreSQL connection string with credentials.
- `PEXELS_API_KEY`: API key from Pexels for fetching images.

## Running the Application

To start FastAPI server locally, use:

```plaintext
uvicorn main:app --reload
```

The server will run at `http://127.0.0.1:8000`.

## API Documentation

FastAPI provides automatic API documentation at `http://127.0.0.1:8000/docs`. You can explore and test the API endpoints here.

## Key Endpoints

- POST /signup: Register a new user.
- POST /token: User login and JWT token generation.
- GET /protected: Access protected routes with a valid JWT token.
- POST /download: Save a downloaded image link for the authenticated user.
- GET /downloads: Retrieve all downloaded image links for the authenticated user.
  
