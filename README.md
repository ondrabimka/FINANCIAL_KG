# Financial Knowledge Graph

## Overview
This project aims to create a comprehensive Financial Knowledge Graph. Currently, the Knowledge Graph contains information about companies, their stock prices, and financial metrics from Yahoo Finance, using the yfinance library. The data is translated into a graph database schema and stored in Memgraph.
The Knowledge Graph provides a structured representation of financial data, allowing for efficient querying and analysis.

## Features
- Fetches financial data from Yahoo Finance using the yfinance library.
- Translates the fetched data into a graph database schema.
- Stores the data in Memgraph, a high-performance graph database.
- Provides query capabilities to explore and analyze the financial data.
- Can be easily deployed using Docker.

## Prerequisites
- Docker
- Docker Compose

## Installation
1. Clone the repository: `git clone https://github.com/ondrabimka/FINANCIAL_KG`
2. Change into the project directory: `cd FINANCIAL_KG`
3. Run docker-compose: `docker-compose up -d`

## Usage
Data is fetched automatically from Yahoo Finance and translated into a graph database schema. The Knowledge Graph can be queried using the Memgraph Lab interface.
1. Lab is available at `http://localhost:3000`

## Configuration
- Create .env file in the root directory with the following content:
```
TICKERS=MSFT,AAPL,GOOGL,AMZN,FB,TSLA,INTC,AMD,NVDA,IBM,ORCL,CRM,ADBE,VMW,HPQ,DELL
```

## Contributing
Contributions are welcome! Please follow the code style and structure of the project (to some extent).
