# Refactoring Changes Report

This document outline the major issues  I have identified in the  codebase and the details that refactoring work done to transform it into a secure, maintainable, and robust application.

## 1. Major Issues I  Identified 

The original codebase while functional, suffered from several critical issues that made it unsuitable for a production environment:

*   **Critical Security Vulnerability (SQL Injection):** The application used f-strings to insert user-provided data directly into SQL queries. This is a severe vulnerability that would allow an attacker to gain control over the database.

*   **Plaintext Password Storage:** Passwords were stored and checked as plaintext in the database, a major violation of security best practices that would expose all user accounts in the event of a data breach.

*   **Monolithic Code Structure:** All application logic, web routes, and database code were mixed in a single `app.py` file. This makes the code difficult to read, maintain, and test.

*   **No Standard API Practices:** Endpoints returned inconsistent responses (often plain strings instead of JSON) and did not use standard HTTP status codes, making it difficult for client applications to reliably interpret the results.

*   **Poor Error Handling:** The application lacked proper error handling for common database issues, such as a user trying to register with an email that already exists.

## 2. Changes Made and Why

Our refactoring strategy focused on addressing these critical issues by separating concerns and implementing modern security and API best practices.

### a. Security Improvements

*   **Prevented SQL Injection:** Every SQL query was rewritten to use **parameterized queries** (`?` placeholders). This practice fundamentally separates the SQL command from the data, making SQL injection impossible.

*   **Implemented Password Hashing:** The `bcrypt` library was integrated to securely hash all user passwords before they are stored. When a user logs in, we now hash the provided password and compare it against the stored hash, ensuring plaintext passwords are never stored or transmitted.

### b. Code Organization

*   **Separation of Concerns:** We created a new **`database.py`** module to act as a dedicated "data access layer." All database connection logic, query execution, and password handling functions were moved here. This isolates database logic from the web application logic, making both parts cleaner and easier to manage. If we ever change the database, only `database.py` needs to be modified.

### c. API Best Practices

*   **Standardized JSON Responses:** All API endpoints were modified to return structured JSON objects using Flask's `jsonify` function. This provides a consistent and predictable response format for any client.

*   **Proper HTTP Status Codes:** The API now uses appropriate HTTP status codes to signal the outcome of a request (e.g., `200 OK`, `201 Created` for success; `404 Not Found`, `400 Bad Request`, `401 Unauthorized` for errors).

*   **Robust Error Handling:** We implemented `try...except` blocks in critical sections, such as user creation, to gracefully handle potential database errors (e.g., `IntegrityError` when a duplicate email is used) and return a helpful error message.

## 3. Assumptions or Trade-offs

Given the 3-hour time limit, we made the following pragmatic decisions:

*   **Focus on Critical Impact:** We prioritized fixing the most severe security and structural issues over adding minor features or aiming for 100% test coverage.
*   **Simplicity:** We opted for a clean, straightforward architecture (separating the data layer) without over-engineering the solution with complex design patterns that were not necessary for an application of this scale.

*   **Synchronous Code:** The application remains synchronous for simplicity. In a high-concurrency environment, one might consider an asynchronous framework.

## 4. What I Would Do with More Time

If given more time, the next steps to further improve the project would be:

*   **Write Automated Tests:** Implement a testing suite using a framework like `pytest` to create unit and integration tests. This is crucial for verifying functionality and preventing regressions.

* **Which tool was used?**
I utilized **Google's Gemini** as an AI assistant.Ensuring Best Practices: I leveraged the AI to quickly look up and implement the correct syntax for security best practices, such as creating parameterized SQL queries and properly using the bcrypt library for password hashing. and created a chnages.md file.
