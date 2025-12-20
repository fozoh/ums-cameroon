# UMS API Documentation

Base URL: `http://localhost:8000/api/`

## Authentication

Most endpoints require authentication via Django session or token. Include the authentication token in request headers:

```
Authorization: Bearer <your-token>
```

## Endpoints

### Health Check
```
GET /health/
```
Returns server health status. No authentication required.

**Response:** `200 OK`
```
OK
```

---

### Authentication

#### Login
```
POST /login/
Content-Type: application/json

{
  "username": "student@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "student@example.com",
  "role": "student",
  "token": "mock-jwt-token"
}
```

**Response (Invalid):** `401 Unauthorized`
```json
{
  "error": "Invalid credentials"
}
```

---

### Student Data

#### Get Continuous Assessment Marks
```
GET /ca/
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "student": 1,
    "course": "CSC3101",
    "ca_score": 18,
    "total_possible": 30,
    "recorded_at": "2025-01-15T10:30:00Z"
  }
]
```

#### Get Exam Results
```
GET /results/
Authorization: Bearer <token>
```

**Note:** Requires payment verification for "result" payment type.

**Response:** `200 OK`
```json
[
  {
    "course": "CSC3101",
    "title": "Data Structures",
    "ca": 18,
    "exam": 32,
    "total": 70,
    "grade": "B"
  }
]
```

**Response (No Payment):** `402 Payment Required`
```json
{
  "error": "Payment required"
}
```

---

### Downloads

#### Download Result Slip (PDF)
```
GET /results/slip/
Authorization: Bearer <token>
```

**Response:** `200 OK` (PDF file)

---

### Lecturer Endpoints

#### Upload Continuous Assessment Marks
```
POST /lecturer/upload-ca/
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_id": 1,
  "course_id": 2,
  "ca_score": 25
}
```

**Response:** `200 OK`
```json
{
  "status": "success",
  "created": true
}
```

---

### Finance Endpoints

#### Verify Payment
```
POST /finance/verify-payment/
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_id": 5
}
```

**Response:** `200 OK`
```json
{
  "status": "verified"
}
```

---

### Payments

#### Initiate Flutterwave Payment
```
POST /payments/initiate/
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 2000,
  "payment_type": "resit"
}
```

**Response:** `200 OK`
```json
{
  "status": "initiated",
  "payment_link": "https://checkout.flutterwave.com/..."
}
```

#### Payment Callback
```
POST /payments/callback/
Content-Type: application/json

{
  "data": {
    "id": "txn_12345",
    "status": "successful",
    "amount": 2000
  }
}
```

**Response:** `200 OK`

---

### Resit Registration

#### Get Resit Timetable
```
GET /resit-timetable/
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "course": "CSC3101",
    "date": "2025-02-10",
    "start_time": "09:00:00",
    "end_time": "11:00:00",
    "venue": "Hall A"
  }
]
```

#### Register for Resit
```
POST /resit/register/
Authorization: Bearer <token>
Content-Type: application/json

{
  "course_id": 2,
  "exam_id": 5
}
```

**Response:** `201 Created`
```json
{
  "status": "registered",
  "resit_id": 10
}
```

---

### Academic Programs

#### Create Program
```
POST /programs/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Computer Science (BSc)",
  "code": "CS100",
  "department_id": 1,
  "program_type_id": 2,
  "total_credits": 120
}
```

**Response:** `201 Created`
```json
{
  "id": 5,
  "name": "Computer Science (BSc)",
  "code": "CS100"
}
```

---

### SMS

#### Send Bulk SMS
```
POST /sms/send/
Authorization: Bearer <token>
Content-Type: application/json

{
  "recipients": ["+237670000001", "+237670000002"],
  "message": "Your results are ready. Visit the portal to download."
}
```

**Response:** `200 OK`
```json
{
  "status": "sent",
  "count": 2
}
```

#### SMS History
```
GET /sms/history/
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "recipient": "+237670000001",
    "message": "Your results are ready...",
    "status": "sent",
    "sent_at": "2025-01-15T10:30:00Z"
  }
]
```

---

### At-Risk Student Prediction

#### Predict At-Risk Students
```
GET /at-risk/
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "at_risk_students": [
    {
      "matric_number": "CS2023001",
      "name": "John Doe",
      "cgpa": 1.8,
      "risk_score": 0.85,
      "factors": ["low_cgpa", "failed_courses", "low_attendance"]
    }
  ]
}
```

---

### Thesis

#### Submit Thesis
```
POST /thesis/submit/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "title": "Machine Learning in Healthcare",
  "abstract": "This thesis explores...",
  "supervisor_id": 3,
  "file": <thesis.pdf>
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "status": "draft",
  "submission_date": "2025-01-15"
}
```

---

### Reports

#### Generate NUC Report
```
GET /reports/nuc/
Authorization: Bearer <token>
```

**Response:** `200 OK` (PDF)

---

### Data Import

#### Import Students from Excel
```
POST /students/import/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
  "file": <students.xlsx>
}
```

**Response:** `200 OK`
```json
{
  "imported": 150,
  "errors": 2,
  "message": "Import completed"
}
```

---

### License Management

#### Renew License
```
POST /license/renew/
Authorization: Bearer <token>
Content-Type: application/json

{
  "license_key": "existing-key",
  "new_valid_until": "2026-12-31"
}
```

**Response:** `200 OK`
```json
{
  "status": "renewed",
  "valid_until": "2026-12-31"
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 402 | Payment Required |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 500 | Server Error |

---

## Rate Limiting

Currently no rate limiting. Production deployment should implement:
- 100 requests/min per user
- 1000 requests/min per IP

---

## Pagination

List endpoints support pagination:
```
GET /ca/?page=1&page_size=20
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/ca/?page=2",
  "previous": null,
  "results": [...]
}
```
