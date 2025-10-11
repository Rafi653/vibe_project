# Booking API Reference

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints Summary

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/api/v1/bookings/coaches` | GET | Client, Coach, Admin | List all coaches with availability |
| `/api/v1/bookings/coaches/{coach_id}` | GET | Client, Coach, Admin | Get specific coach details |
| `/api/v1/bookings/book` | POST | Client | Book a training slot |
| `/api/v1/bookings/my-bookings` | GET | Client, Coach | Get user's bookings |
| `/api/v1/bookings/bookings/{booking_id}` | PUT | Client, Coach | Update booking |
| `/api/v1/bookings/coach/bookings` | GET | Coach | Get coach's bookings |
| `/api/v1/bookings/admin/bookings` | GET | Admin | Get all bookings |
| `/api/v1/bookings/admin/coaches/{coach_id}/bookings` | GET | Admin | Get coach's calendar |

---

## Client Endpoints

### List Available Coaches

Get a list of all coaches with their profiles and availability.

**Endpoint:** `GET /api/v1/bookings/coaches`

**Access:** Client, Coach, Admin

**Response:**
```json
[
  {
    "coach_id": 1,
    "coach_name": "Coach A",
    "strengths": "Strength Training, Powerlifting, Olympic Lifts",
    "specialties": "Powerlifting, Bodybuilding",
    "experience": "10 years of professional coaching experience",
    "available_slots": 7,
    "total_slots": 10,
    "booked_slots": 3
  }
]
```

---

### Get Coach Details

Get detailed profile and availability for a specific coach.

**Endpoint:** `GET /api/v1/bookings/coaches/{coach_id}`

**Access:** Client, Coach, Admin

**Parameters:**
- `coach_id` (path): Coach user ID

**Response:**
```json
{
  "coach_id": 1,
  "coach_name": "Coach A",
  "strengths": "Strength Training, Powerlifting, Olympic Lifts",
  "specialties": "Powerlifting, Bodybuilding",
  "experience": "10 years of professional coaching experience",
  "available_slots": 7,
  "total_slots": 10,
  "booked_slots": 3
}
```

---

### Book Training Slot

Book a training slot with a coach.

**Endpoint:** `POST /api/v1/bookings/book`

**Access:** Client only

**Request Body:**
```json
{
  "coach_id": 1,
  "slot_number": 1,
  "scheduled_at": "2025-10-18T10:00:00Z",  // optional
  "notes": "First training session"         // optional
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "coach_id": 1,
  "client_id": 5,
  "slot_number": 1,
  "scheduled_at": "2025-10-18T10:00:00Z",
  "status": "pending",
  "notes": "First training session",
  "created_at": "2025-10-11T10:50:00Z",
  "updated_at": "2025-10-11T10:50:00Z"
}
```

**Errors:**
- `400 Bad Request`: Coach has no available slots or duplicate booking
- `404 Not Found`: Coach not found

---

### Get My Bookings

Get all bookings for the current user (client or coach view).

**Endpoint:** `GET /api/v1/bookings/my-bookings`

**Access:** Client, Coach

**Response:**
```json
[
  {
    "id": 1,
    "coach_id": 1,
    "client_id": 5,
    "slot_number": 1,
    "scheduled_at": "2025-10-18T10:00:00Z",
    "status": "pending",
    "notes": "First training session",
    "created_at": "2025-10-11T10:50:00Z",
    "updated_at": "2025-10-11T10:50:00Z",
    "coach_name": "Coach A",
    "client_name": "Client E"
  }
]
```

---

### Cancel Booking

Cancel a booking (clients can only cancel, coaches can confirm/complete).

**Endpoint:** `PUT /api/v1/bookings/bookings/{booking_id}`

**Access:** Client (cancel only), Coach (all status changes)

**Parameters:**
- `booking_id` (path): Booking ID

**Request Body (Client):**
```json
{
  "status": "cancelled"
}
```

**Request Body (Coach):**
```json
{
  "status": "confirmed",  // or "completed"
  "scheduled_at": "2025-10-18T14:00:00Z",  // optional
  "notes": "Updated session time"           // optional
}
```

**Response:**
```json
{
  "id": 1,
  "coach_id": 1,
  "client_id": 5,
  "slot_number": 1,
  "scheduled_at": "2025-10-18T14:00:00Z",
  "status": "confirmed",
  "notes": "Updated session time",
  "created_at": "2025-10-11T10:50:00Z",
  "updated_at": "2025-10-11T11:00:00Z"
}
```

---

## Coach Endpoints

### Get Coach's Bookings

Get all bookings for the current coach.

**Endpoint:** `GET /api/v1/bookings/coach/bookings`

**Access:** Coach

**Response:**
```json
[
  {
    "id": 1,
    "coach_id": 1,
    "client_id": 5,
    "slot_number": 1,
    "scheduled_at": "2025-10-18T10:00:00Z",
    "status": "confirmed",
    "notes": "First training session",
    "created_at": "2025-10-11T10:50:00Z",
    "updated_at": "2025-10-11T11:00:00Z",
    "coach_name": "Coach A",
    "client_name": "Client E"
  }
]
```

---

### Get Connected Clients

Get list of clients connected through bookings.

**Endpoint:** `GET /api/v1/coach/clients`

**Access:** Coach

**Response:**
```json
[
  {
    "id": 5,
    "email": "client5@vibe.com",
    "full_name": "Client E",
    "role": "client",
    "age": 30,
    "height": 175.0,
    "weight": 80.0,
    "target_goals": "Build muscle mass and strength"
  }
]
```

---

### Get Client Profile

Get detailed profile of a connected client.

**Endpoint:** `GET /api/v1/coach/clients/{client_id}`

**Access:** Coach (only for connected clients)

**Parameters:**
- `client_id` (path): Client user ID

**Response:**
```json
{
  "id": 5,
  "email": "client5@vibe.com",
  "full_name": "Client E",
  "role": "client",
  "age": 30,
  "gender": "Male",
  "height": 175.0,
  "weight": 80.0,
  "bicep_size": 38.5,
  "waist": 82.0,
  "target_goals": "Build muscle mass and strength",
  "dietary_restrictions": "Vegetarian",
  "health_complications": null,
  "injuries": "Previous knee injury",
  "gym_access": "Commercial Gym"
}
```

**Errors:**
- `403 Forbidden`: Coach not connected to this client through bookings
- `404 Not Found`: Client not found

---

### Get Client Workout Logs

Get day-wise workout logs for a connected client.

**Endpoint:** `GET /api/v1/coach/clients/{client_id}/workout-logs`

**Access:** Coach (only for connected clients)

**Parameters:**
- `client_id` (path): Client user ID
- `start_date` (query, optional): Filter by start date (YYYY-MM-DD)
- `end_date` (query, optional): Filter by end date (YYYY-MM-DD)

**Example:** `GET /api/v1/coach/clients/5/workout-logs?start_date=2025-10-01&end_date=2025-10-11`

**Response:**
```json
[
  {
    "id": 123,
    "user_id": 5,
    "workout_date": "2025-10-11",
    "exercise_name": "Bench Press",
    "sets": 3,
    "reps": 10,
    "weight": 60.0,
    "duration_minutes": 30,
    "notes": "Felt good",
    "created_at": "2025-10-11T08:00:00Z",
    "updated_at": "2025-10-11T08:00:00Z"
  }
]
```

---

### Get Client Diet Logs

Get day-wise diet logs for a connected client.

**Endpoint:** `GET /api/v1/coach/clients/{client_id}/diet-logs`

**Access:** Coach (only for connected clients)

**Parameters:**
- `client_id` (path): Client user ID
- `start_date` (query, optional): Filter by start date (YYYY-MM-DD)
- `end_date` (query, optional): Filter by end date (YYYY-MM-DD)

**Example:** `GET /api/v1/coach/clients/5/diet-logs?start_date=2025-10-01&end_date=2025-10-11`

**Response:**
```json
[
  {
    "id": 456,
    "user_id": 5,
    "meal_date": "2025-10-11",
    "meal_type": "lunch",
    "food_name": "Chicken breast with rice and vegetables",
    "calories": 520.0,
    "protein_grams": 45.0,
    "carbs_grams": 55.0,
    "fat_grams": 10.0,
    "notes": "Delicious",
    "created_at": "2025-10-11T12:00:00Z",
    "updated_at": "2025-10-11T12:00:00Z"
  }
]
```

---

## Admin Endpoints

### Get All Bookings

Get all bookings across all coaches and clients.

**Endpoint:** `GET /api/v1/bookings/admin/bookings`

**Access:** Admin

**Response:**
```json
[
  {
    "id": 1,
    "coach_id": 1,
    "client_id": 5,
    "slot_number": 1,
    "scheduled_at": "2025-10-18T10:00:00Z",
    "status": "confirmed",
    "notes": "First training session",
    "created_at": "2025-10-11T10:50:00Z",
    "updated_at": "2025-10-11T11:00:00Z",
    "coach_name": "Coach A",
    "client_name": "Client E"
  }
]
```

---

### Get Coach Calendar

Get all bookings for a specific coach.

**Endpoint:** `GET /api/v1/bookings/admin/coaches/{coach_id}/bookings`

**Access:** Admin

**Parameters:**
- `coach_id` (path): Coach user ID

**Response:**
```json
[
  {
    "id": 1,
    "coach_id": 1,
    "client_id": 5,
    "slot_number": 1,
    "scheduled_at": "2025-10-18T10:00:00Z",
    "status": "confirmed",
    "notes": "First training session",
    "created_at": "2025-10-11T10:50:00Z",
    "updated_at": "2025-10-11T11:00:00Z",
    "coach_name": "Coach A",
    "client_name": "Client E"
  }
]
```

---

## Booking Status Flow

```
pending → confirmed → completed
   ↓
cancelled
```

**Status Descriptions:**
- `pending`: Booking created by client, awaiting coach confirmation
- `confirmed`: Coach has confirmed the booking
- `completed`: Training session has been completed
- `cancelled`: Booking has been cancelled (by client or coach)

---

## Error Responses

All endpoints may return the following error responses:

**401 Unauthorized**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden**
```json
{
  "detail": "You don't have permission to access this resource"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**400 Bad Request**
```json
{
  "detail": "Invalid request parameters"
}
```
