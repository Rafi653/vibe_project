# API Reference - Core Features

Quick reference guide for the new API endpoints implemented in the Vibe Fitness Platform.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints require JWT authentication via Bearer token:

```http
Authorization: Bearer <your_jwt_token>
```

---

## Client Endpoints

Base path: `/api/v1/client`

### Workout Logs

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| POST | `/workout-logs` | Create a new workout log | CLIENT+ |
| GET | `/workout-logs` | Get all workout logs (with optional date filters) | CLIENT+ |
| GET | `/workout-logs/{id}` | Get specific workout log | CLIENT+ |
| PUT | `/workout-logs/{id}` | Update workout log | CLIENT+ |
| DELETE | `/workout-logs/{id}` | Delete workout log | CLIENT+ |

### Diet Logs

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| POST | `/diet-logs` | Create a new diet log | CLIENT+ |
| GET | `/diet-logs` | Get all diet logs (with optional date filters) | CLIENT+ |
| GET | `/diet-logs/{id}` | Get specific diet log | CLIENT+ |
| PUT | `/diet-logs/{id}` | Update diet log | CLIENT+ |
| DELETE | `/diet-logs/{id}` | Delete diet log | CLIENT+ |

### Plans

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/workout-plans` | Get assigned workout plans | CLIENT+ |
| GET | `/workout-plans/{id}` | Get specific workout plan | CLIENT+ |
| GET | `/diet-plans` | Get assigned diet plans | CLIENT+ |
| GET | `/diet-plans/{id}` | Get specific diet plan | CLIENT+ |

### Other

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/progress` | Get progress metrics (30-day stats) | CLIENT+ |
| PUT | `/profile` | Update user profile | CLIENT+ |

---

## Coach Endpoints

Base path: `/api/v1/coach`

### Client Management

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/clients` | Get all clients | COACH+ |
| GET | `/clients/{id}` | Get specific client | COACH+ |
| GET | `/clients/{id}/workout-logs` | Get client's workout logs | COACH+ |
| GET | `/clients/{id}/diet-logs` | Get client's diet logs | COACH+ |
| GET | `/clients/{id}/progress` | Get client progress | COACH+ |

### Workout Plans

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| POST | `/workout-plans` | Create workout plan for client | COACH+ |
| GET | `/workout-plans` | Get all workout plans (optional client filter) | COACH+ |
| PUT | `/workout-plans/{id}` | Update workout plan | COACH+ |
| DELETE | `/workout-plans/{id}` | Delete workout plan | COACH+ |

### Diet Plans

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| POST | `/diet-plans` | Create diet plan for client | COACH+ |
| GET | `/diet-plans` | Get all diet plans (optional client filter) | COACH+ |
| PUT | `/diet-plans/{id}` | Update diet plan | COACH+ |
| DELETE | `/diet-plans/{id}` | Delete diet plan | COACH+ |

---

## Admin Endpoints

Base path: `/api/v1/admin`

### User Management

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/users` | Get all users (optional role filter) | ADMIN |
| GET | `/users/{id}` | Get specific user | ADMIN |
| PUT | `/users/{id}` | Update user | ADMIN |
| DELETE | `/users/{id}` | Delete user | ADMIN |

### Statistics & Reports

| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| GET | `/stats` | Get platform statistics | ADMIN |
| GET | `/reports/usage` | Generate usage report (optional days param) | ADMIN |

---

## Request/Response Examples

### Create Workout Log

**Request:**
```http
POST /api/v1/client/workout-logs
Content-Type: application/json
Authorization: Bearer <token>

{
  "workout_date": "2025-10-11",
  "exercise_name": "Bench Press",
  "sets": 3,
  "reps": 10,
  "weight": 60.0,
  "duration_minutes": 30,
  "notes": "Felt strong today"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 5,
  "workout_date": "2025-10-11",
  "exercise_name": "Bench Press",
  "sets": 3,
  "reps": 10,
  "weight": 60.0,
  "duration_minutes": 30,
  "notes": "Felt strong today"
}
```

### Create Diet Log

**Request:**
```http
POST /api/v1/client/diet-logs
Content-Type: application/json
Authorization: Bearer <token>

{
  "meal_date": "2025-10-11",
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 350.0,
  "protein_grams": 12.0,
  "carbs_grams": 55.0,
  "fat_grams": 8.0,
  "notes": "Added honey"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 5,
  "meal_date": "2025-10-11",
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 350.0,
  "protein_grams": 12.0,
  "carbs_grams": 55.0,
  "fat_grams": 8.0,
  "notes": "Added honey"
}
```

### Create Workout Plan (Coach)

**Request:**
```http
POST /api/v1/coach/workout-plans
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": 5,
  "name": "Beginner Strength Program",
  "description": "12-week program for building foundational strength",
  "start_date": "2025-10-15",
  "duration_weeks": 12,
  "workout_details": {
    "days_per_week": 3,
    "exercises": ["Squat", "Bench Press", "Deadlift"]
  }
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 5,
  "name": "Beginner Strength Program",
  "description": "12-week program for building foundational strength",
  "start_date": "2025-10-15",
  "end_date": null,
  "status": "active",
  "duration_weeks": 12,
  "workout_details": {
    "days_per_week": 3,
    "exercises": ["Squat", "Bench Press", "Deadlift"]
  }
}
```

### Get Platform Stats (Admin)

**Request:**
```http
GET /api/v1/admin/stats
Authorization: Bearer <token>
```

**Response:**
```json
{
  "users": {
    "total": 150,
    "active": 142,
    "clients": 120,
    "coaches": 25,
    "admins": 5
  },
  "activity": {
    "total_workouts": 5420,
    "total_diet_logs": 8340
  },
  "last_30_days": {
    "workouts": 450,
    "diet_logs": 680
  },
  "plans": {
    "active_workout_plans": 85,
    "active_diet_plans": 92
  }
}
```

---

## Query Parameters

### Date Filtering

Available on workout and diet log endpoints:

```http
GET /api/v1/client/workout-logs?start_date=2025-10-01&end_date=2025-10-11
```

### Client Filtering (Coach)

Available on plan listing endpoints:

```http
GET /api/v1/coach/workout-plans?client_id=5
```

### Role Filtering (Admin)

Available on user listing:

```http
GET /api/v1/admin/users?role=client
```

### Report Period (Admin)

Available on usage reports:

```http
GET /api/v1/admin/reports/usage?days=7
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied. Required role: admin"
}
```

### 404 Not Found
```json
{
  "detail": "Workout log not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "workout_date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Role Hierarchy

- **CLIENT+** = CLIENT, COACH, or ADMIN
- **COACH+** = COACH or ADMIN
- **ADMIN** = ADMIN only

---

## Interactive Documentation

For interactive API documentation with request/response examples:

```
http://localhost:8000/api/docs
```

Alternative documentation format:

```
http://localhost:8000/api/redoc
```

---

## Testing with cURL

### Login and Get Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client@vibe.com","password":"client123"}'
```

### Use Token in Requests
```bash
TOKEN="your_jwt_token_here"

curl -X GET http://localhost:8000/api/v1/client/progress \
  -H "Authorization: Bearer $TOKEN"
```

---

## Frontend Integration

See the service files in `frontend/src/services/` for ready-to-use JavaScript API client implementations:

- `clientService.js` - Client operations
- `coachService.js` - Coach operations
- `adminService.js` - Admin operations
