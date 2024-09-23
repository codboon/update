
# Update Service

This Update Service is a FastAPI-based API that allows users to retrieve and download the latest version of an application. It is designed to manage versioned `.exe` files stored in a structured directory and provide endpoints for accessing the latest updates.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [How to Use](#how-to-use)
- [FAQ](#faq)

## Installation

### Prerequisites
- Python 3.8+
- Pip (Python package manager)
- Git (optional)

### Step-by-Step Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/update-service.git
   ```

2. Navigate to the project directory:
   ```bash
   cd update-service
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```
   The service will be available at `http://localhost:8000`.

## Project Structure

```
update-service/
│
├── app/
│   ├── main.py                 # Main application entry
│   ├── version/
│   │   └── filehandle.py       # File handling logic for managing versioned files
│   └── exe_files/              # Directory containing versioned `.exe` files
│       └── 1.0.0/
│           └── codboon_1.0.0.exe
│
├── tests/
│   └── test_main.py            # Test cases for the API endpoints
│
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Endpoints

### 1. Root Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.
- **Response:**
  ```json
  {
    "message": "Bienvenue sur l'API de mise à jour"
  }
  ```

### 2. Get Latest Version
- **URL:** `/latest-version`
- **Method:** `GET`
- **Description:** Retrieves the latest available version of the application.
- **Response:**
  - Success: `200 OK`
    ```json
    {
      "latest_version": "1.0.0"
    }
    ```
  - Error: `404 Not Found` if no `.exe` files are available.
    ```json
    {
      "detail": "Aucun fichier .exe disponible"
    }
    ```

### 3. Download Latest Version
- **URL:** `/download-latest`
- **Method:** `GET`
- **Description:** Downloads the latest available `.exe` file.
- **Response:**
  - Success: `200 OK` with file download.
  - Error: `404 Not Found` if no `.exe` files are available.
    ```json
    {
      "detail": "Aucun fichier .exe disponible"
    }
    ```

## Testing

You can test the Update Service using `pytest`. The test cases are located in the `tests/test_main.py` file.

### Running the tests
```bash
pytest tests/test_main.py -s
```

Ensure that the `exe_files` directory contains at least one versioned `.exe` file for successful tests.

## How to Use

1. Place the versioned `.exe` files inside the `exe_files` directory following this structure:
   ```
   exe_files/
   └── 1.0.0/
       └── codboon_1.0.0.exe
   ```
2. Start the FastAPI service using `uvicorn`.
3. Access the endpoints using `http://localhost:8000/latest-version` or `http://localhost:8000/download-latest`.

## FAQ

### Q1: How do I add a new version?
- Create a new directory inside `exe_files` named after the version (e.g., `2.0.0`) and place the `.exe` file inside it.

### Q2: What happens if there are no `.exe` files available?
- The endpoints `/latest-version` and `/download-latest` will return a `404 Not Found` error with the message "Aucun fichier .exe disponible".

### Q3: How does the service determine the latest version?
- The service selects the `.exe` file from the directory with the highest version number using a tuple-based comparison.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to improve this project.

## Contact

For any questions or feedback, please contact us at [contact@codboon.com].
