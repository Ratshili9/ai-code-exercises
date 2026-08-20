# WeThinkCode_ AI Curriculum: Using GenAI to Support Software Development
## Exercise: API Documentation (`exercise-doc-api`)
**Author:** Talifhani  
**Language Selected:** Python (Flask)  
**Target Endpoint:** `POST /api/users/register` (User Registration Endpoint)  

---

## 1. Executive Summary & Challenge Objectives

In this exercise, we practice using Generative AI prompt workflows to generate, convert, and structure comprehensive API documentation. 

We selected the Python/Flask **User Registration Endpoint** (`/api/users/register`) and applied three prompt strategies:
1. **Prompt 1 (Endpoint Documentation Generation):** Creating structured Markdown API documentation covering request schemas, status codes, validations, and edge cases.
2. **Prompt 2 (API Reference Conversion):** Transforming informal documentation into a standardized, machine-readable **OpenAPI 3.0.0 (Swagger)** YAML specification.
3. **Prompt 3 (API Usage Guide Creation):** Writing a developer-friendly integration guide with error handling patterns and runnable client code examples (`curl` and Python `requests`).

---

## 2. Section 1: Original API Implementation

Below is the Python/Flask endpoint code selected for documentation:

```python
@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': f'{field} is required'
            }), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'error': 'Username taken',
            'message': 'Username is already in use'
        }), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'Email exists',
            'message': 'An account with this email already exists'
        }), 409

    # Validate email format
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data['email']):
        return jsonify({
            'error': 'Invalid email',
            'message': 'Please provide a valid email address'
        }), 400

    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({
            'error': 'Weak password',
            'message': 'Password must be at least 8 characters long'
        }), 400

    # Create new user
    try:
        password_hash = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            email=data['email'].lower(),
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            role='user'
        )

        db.session.add(new_user)
        db.session.commit()

        confirmation_token = generate_confirmation_token(new_user.id)

        try:
            send_confirmation_email(new_user.email, confirmation_token)
        except Exception as e:
            app.logger.error(f"Failed to send confirmation email: {str(e)}")

        user_data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_at': new_user.created_at.isoformat(),
            'role': new_user.role
        }

        return jsonify({
            'message': 'User registered successfully',
            'user': user_data
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error registering user: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'Failed to register user'
        }), 500
```

---

## 3. Section 2: Prompt 1 Output — Comprehensive Markdown API Documentation

# User Registration API Reference

Creates a new user account, securely hashes credentials, creates default role assignments, and dispatches an asynchronous email confirmation token.

## Endpoint Specification

- **HTTP Method:** `POST`
- **Path:** `/api/users/register`
- **Content-Type:** `application/json`
- **Authentication:** None required (Public endpoint)

## Request Headers

| Header | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `Content-Type` | `string` | **Yes** | Must be `application/json` |
| `Accept` | `string` | No | Recommended `application/json` |

## Request Body Parameters

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `username` | `string` | **Yes** | Unique across system | Chosen user handle |
| `email` | `string` | **Yes** | Valid email regex (`^[^@]+@[^@]+\.[^@]+$`) | Contact email (normalized to lowercase) |
| `password` | `string` | **Yes** | Minimum 8 characters | Plaintext password (hashed with scrypt/bcrypt prior to persistence) |

### Request Example
```json
{
  "username": "talifhani_dev",
  "email": "talifhani@example.com",
  "password": "SecurePassword123!"
}
```

---

## Responses & Status Codes

### 201 Created — Successful Registration
Returned when user creation and transaction commit succeed.

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1042,
    "username": "talifhani_dev",
    "email": "talifhani@example.com",
    "created_at": "2026-08-20T19:15:00.000Z",
    "role": "user"
  }
}
```

### 400 Bad Request — Validation Failure
Returned when required fields are missing, email format is invalid, or password is under 8 characters.

```json
{
  "error": "Weak password",
  "message": "Password must be at least 8 characters long"
}
```

### 409 Conflict — Unique Constraint Violation
Returned when `username` or `email` is already registered in the system.

```json
{
  "error": "Email exists",
  "message": "An account with this email already exists"
}
```

### 500 Internal Server Error — Database / System Error
Returned on unexpected database failure (transaction automatically rolled back).

```json
{
  "error": "Server error",
  "message": "Failed to register user"
}
```

---

## 4. Section 3: Prompt 2 Output — Standardized OpenAPI 3.0.0 YAML Specification

```yaml
openapi: 3.0.0
info:
  title: User Management Service API
  description: Authentication and user onboarding API endpoints.
  version: 1.0.0
servers:
  - url: https://api.example.com
    description: Production Server
paths:
  /api/users/register:
    post:
      summary: Register a new user
      description: Creates a user account, hashes passwords, and sends email confirmation.
      operationId: registerUser
      tags:
        - Authentication
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRegistrationRequest'
      responses:
        '201':
          description: User registered successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserRegistrationSuccess'
        '400':
          description: Bad request / validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '409':
          description: Conflict - username or email already in use
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    UserRegistrationRequest:
      type: object
      required:
        - username
        - email
        - password
      properties:
        username:
          type: string
          example: "talifhani_dev"
        email:
          type: string
          format: email
          example: "talifhani@example.com"
        password:
          type: string
          format: password
          minLength: 8
          example: "SecurePassword123!"

    UserRegistrationSuccess:
      type: object
      properties:
        message:
          type: string
          example: "User registered successfully"
        user:
          $ref: '#/components/schemas/UserProfile'

    UserProfile:
      type: object
      properties:
        id:
          type: integer
          example: 1042
        username:
          type: string
          example: "talifhani_dev"
        email:
          type: string
          example: "talifhani@example.com"
        created_at:
          type: string
          format: date-time
          example: "2026-08-20T19:15:00.000Z"
        role:
          type: string
          example: "user"

    ErrorResponse:
      type: object
      properties:
        error:
          type: string
          example: "Missing required field"
        message:
          type: string
          example: "email is required"
```

---

## 5. Section 4: Prompt 3 Output — Developer Quickstart Guide

### 5.1 Overview
The User Registration API enables client applications to onboard new accounts. 

### 5.2 Python Integration Example (`requests`)

```python
import requests

def register_new_account(username, email, password):
    url = "https://api.example.com/api/users/register"
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 201:
            data = response.json()
            print(f"Success! Created User ID: {data['user']['id']}")
            return data['user']
            
        elif response.status_code in (400, 409):
            err = response.json()
            print(f"Registration Error [{err['error']}]: {err['message']}")
            return None
            
        else:
            print(f"Unexpected Server Error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Network / Connection Failure: {e}")
        return None

# Usage:
user = register_new_account("talifhani_dev", "talifhani@example.com", "SecurePassword123!")
```

### 5.3 cURL Integration Example

```bash
curl -X POST https://api.example.com/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "talifhani_dev",
    "email": "talifhani@example.com",
    "password": "SecurePassword123!"
  }'
```

---

## 6. Section 5: Reflection & Learnings

1. **Challenges Encountered:** Identifying implicit business constraints (like the non-blocking email confirmation failure where registration still succeeds with `201` even if SMTP fails).
2. **Prompt Tuning:** Explicitly requesting status code tables with concrete JSON error bodies prevented generic 200/500 responses.
3. **Format Effectiveness:** OpenAPI 3.0.0 is ideal for automated SDK code generation and API testing tools (Postman, Swagger UI), whereas Markdown is optimal for human-readable developer portals.

---

## 7. Submission Summary

```text
================================================================================
                    EXERCISE SUBMISSION: API DOCUMENTATION
================================================================================
Student: Talifhani
Target Endpoint: POST /api/users/register (Python/Flask)

1. DELIVERABLES PRODUCED:
   - Comprehensive Markdown Endpoint Reference (status codes 201, 400, 409, 500).
   - Valid OpenAPI 3.0.0 Swagger specification with JSON Schema references.
   - Developer Quickstart Guide with Python and cURL client code.

2. KEY TAKEAWAYS:
   - AI converts code logic into formal API schemas with zero manual typing.
   - Explicit prompt requirements ensure error models and edge cases are documented.
================================================================================
```
