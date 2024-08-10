# Bank Account Management API

## Description

This is an API for managing bank accounts and associated transactions. The application allows users to perform deposits, withdrawals, and transfers between accounts, keeping a record of each transaction and updating the account balance accordingly.

## Features

- **Account Management**: Users can create bank accounts with a unique IBAN and an initial balance.
- **Transaction Management**: Users can create various types of transactions:
  - **Deposits**: Increases the account balance.
  - **Withdrawals**: Decreases the account balance, provided there are sufficient funds.
  - **Transfers**: Transfers funds from one account to another, ensuring the source account has sufficient funds.
- **Transaction Querying**: Users can query the transaction history of an account, with options to filter by transaction type, date range, and ordering by date.
- **Funds Validation**: The application automatically validates that an account has sufficient funds before allowing withdrawals or transfers.

### Requirements

- **Python 3.11.5**
- **Django 5.1**
- **Django Rest Framework**
- **Docker and Docker Compose** (Optional)

## Installation Instructions

1. **Clone this repository**

2. **Create and activate a virtual environment**
    - python3 -m venv env
    - source env/bin/activate  or  env\Scripts\activate

3. **Install dependencies**
    - pip install -r requirements.txt

4. **Apply migrations**
    - python manage.py makemigrations
    - python manage.py migrate

5. **Run the development server**
    - python manage.py runserver

6. **(Optional) Start the application with Docker**
    - docker-compose up --build


### Access the Swagger documentation
Open your web browser and go to: http://localhost:8000/swagger/

![alt text](image-11.png)

## Key Endpoints

### Accounts

- **List and Create Accounts**: `GET /accounts/` and `POST /accounts/`
- **Account Details**: `GET /accounts/{id}/`

![alt text](image-1.png)

### Transactions

- **List and Create Transactions**: `GET /transactions/` and `POST /transactions/`
  - **Available Filters**:
    - `type`: Filter by transaction type (`deposit`, `withdrawal`, `transfer`).
    - `start_date` and `end_date`: Filter by date range.
    - `ordering`: Sort transactions by date (`date` or `-date`).
- **Transaction Details**: `GET /transactions/{id}/`
![alt text](image.png)

## Use Cases using Swagger

### 1. **Create a New Account**

Users can create a new account by providing a unique IBAN and an optional initial balance.

**Request Example :**

![alt text](image-2.png)

**Response  Example :**
![alt text](image-3.png)

### 2. **Make a Transaction**
Users can make a transaction to a specific type (deposit, withdrawal, transfer).
Account field is The account related to the transaction
**Request Example :**
![alt text](image-4.png)

**Response  Example :**
![alt text](image-5.png)

### 3. **Make a Failed Transaction**
Validates that sufficient funds are available for withdrawal or transfer transactions
**Request Example :**
![alt text](image-6.png)

**Response  Example :**
![alt text](image-7.png)

### 4. **Make a Query Transaction History**
Users can query the transaction history, sort by date (in ascending and descending order), filtering by transaction type and date range.
![alt text](image-8.png)

**Request Example :**
http://127.0.0.1:8000/api/transactions/?type=transfer&type=withdrawal&start_date=2024-08-09&end_date=2024-08-11&ordering=-date&page=1

![alt text](image-9.png)

**Response  Example :**
![alt text](image-10.png)

***Nicolas Hurtado C***
