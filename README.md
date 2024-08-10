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

![image](https://github.com/user-attachments/assets/bce135f6-8dde-4545-a48c-f97695bedd26)


## Key Endpoints

### Accounts

- **List and Create Accounts**: `GET /accounts/` and `POST /accounts/`
- **Account Details**: `GET /accounts/{id}/`

![image](https://github.com/user-attachments/assets/7c51bc53-2133-483d-b387-7be1a8533887)


### Transactions

- **List and Create Transactions**: `GET /transactions/` and `POST /transactions/`
  - **Available Filters**:
    - `type`: Filter by transaction type (`deposit`, `withdrawal`, `transfer`).
    - `start_date` and `end_date`: Filter by date range.
    - `ordering`: Sort transactions by date (`date` or `-date`).
- **Transaction Details**: `GET /transactions/{id}/`
![image](https://github.com/user-attachments/assets/5c3ad5ab-bddc-49c8-bc85-99110170fd61)


## Use Cases using Swagger

### 1. **Create a New Account**

Users can create a new account by providing a unique IBAN and an optional initial balance.

**Request Example :**

![image](https://github.com/user-attachments/assets/068f1c98-c63f-4439-a337-a8524660f3f0)


**Response  Example :**
![image](https://github.com/user-attachments/assets/cf130b6c-7381-401f-8d2c-60e7f2f28c44)


### 2. **Make a Transaction**
Users can make a transaction to a specific type (deposit, withdrawal, transfer).
Account field is The account related to the transaction
**Request Example :**
![image](https://github.com/user-attachments/assets/ebcc2516-c18e-416e-aa60-3cca8735cdb0)


**Response  Example :**
![image](https://github.com/user-attachments/assets/9830b1fc-ef42-4c4e-bcff-816a4b7fec98)


### 3. **Make a Failed Transaction**
Validates that sufficient funds are available for withdrawal or transfer transactions
**Request Example :**
![image](https://github.com/user-attachments/assets/03778145-68d8-4a9d-b8f6-c6162a03a197)


**Response  Example :**
![image](https://github.com/user-attachments/assets/f6026b2a-202c-4eb9-afdd-ff98b6e75d49)


### 4. **Make a Query Transaction History**
Users can query the transaction history, sort by date (in ascending and descending order), filtering by transaction type and date range.
![image](https://github.com/user-attachments/assets/14e9a4b4-a7a7-4747-85ed-bb9388e2753c)


**Request Example :**
http://127.0.0.1:8000/api/transactions/?type=transfer&type=withdrawal&start_date=2024-08-09&end_date=2024-08-11&ordering=-date&page=1

![image](https://github.com/user-attachments/assets/b3ea1911-935d-4031-862a-27ba39771ecb)


**Response  Example :**
![image](https://github.com/user-attachments/assets/e44a1f5d-820b-42ea-8a43-b99b2082468a)


***Nicolas Hurtado C***
