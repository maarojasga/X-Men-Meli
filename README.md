# Mutant Detector API

This project provides a RESTful API to detect mutant DNA sequences and record their statistics. The API allows for analysis of DNA sequences to determine if they belong to mutants, stores the results in a database, and provides statistical data on mutant and human records.

## Installation
#### Clone the repository:
``` bash
git clone https://github.com/maarojasga/X-Men-Meli.git
cd mutant-detector
```

#### Install dependencies:
```  bash
pip install -r requirements.txt
``` 

#### Set up environment variables:
The database credentials and configurations are stored in a .env file. Create a .env file in the project root and add the following variables:

``` 
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
DB_NAME=postgres
``` 

#### Initialize the Database:
The database will be initialized automatically when the application starts. It will create the necessary tables if they do not already exist.

## Configuration
The application uses FastAPI as the web framework and psycopg2 to connect to a PostgreSQL database. Ensure you have a PostgreSQL database set up and that the credentials in your .env file match your database configuration.

## Usage
To start the FastAPI application, run:

``` bash
uvicorn main:app --reload
``` 

##### The API will be available at http://127.0.0.1:8000.

## Endpoints

##### POST /api/mutant
Detects whether a DNA sequence belongs to a mutant. A sequence is considered mutant if it contains at least two sequences of four identical letters (A, T, C, G) arranged horizontally, vertically, or diagonally.

Request Body:
``` json
{
  "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
}
```

Response:
```
200 OK: If the sequence belongs to a mutant.
403 Forbidden: If the sequence does not belong to a mutant.
```
Response Example:
``` json
{
  "status": "mutant",
  "record_id": "1234-5678-9012",
  "detail": "The DNA sequence is identified as a new mutant."
}
```

##### GET /api/stats
Returns statistics on the recorded DNA sequences, including the total count of mutants and humans, the ratio of mutants, and the dates with the most mutants and humans recorded.

Response:
``` json
{
  "count_mutant_dna": 40,
  "count_human_dna": 100,
  "ratio": 40.0,
  "most_mutants_day": "2024-01-10",
  "most_humans_day": "2024-01-12"
}
```

## Database Schema
The dna_records table stores the DNA sequence records with the following schema:

```
id (TEXT): Primary key, unique identifier for each record.
dna_sequence (TEXT): DNA sequence as a single string.
is_mutant (BOOLEAN): True if the DNA is identified as mutant, False otherwise.
date (TIMESTAMP): Date when the record was created (default: current date).
```

## Bonus
### If you want to run it with docker
``` bash
docker build -t x-men-meli .
docker run -p 8000:80 x-men-meli
```

#### Note
In utils/compare_mutant_detector.py, two algorithms are evaluated for performance and accuracy. The superior algorithm is then selected and integrated into mutant_service.py.

## Production links
### [Documentation] (https://x-men-meli.azurewebsites.net/docs)

### POST https://x-men-meli.azurewebsites.net/api/mutant

### GET https://x-men-meli.azurewebsites.net/api/stats


