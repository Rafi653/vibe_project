# Coach Availability and Booking Feature

## Overview

This document describes the implementation of the coach availability and booking feature for the Vibe Fitness Coaching Platform. This feature allows clients to view coach profiles, see their availability, and book personal training slots. Coaches can view their bookings and connected clients, while admins have full oversight of all bookings and schedules.

## Database Schema Changes

### 1. User Model Updates

Added new fields to the `users` table:
- `strengths` (Text): Coach's areas of strength (e.g., "Strength Training, Weight Loss")
- `available_slots` (Integer): Number of available training slots (default: 10)

### 2. New Booking Table

Created `bookings` table with the following structure:
- `id` (Integer, Primary Key)
- `coach_id` (Integer, Foreign Key to users)
- `client_id` (Integer, Foreign Key to users)
- `slot_number` (Integer): The slot number (1-10)
- `scheduled_at` (DateTime): Scheduled time for the session
- `status` (Enum): pending, confirmed, completed, cancelled
- `notes` (Text): Additional notes
- `created_at` (DateTime)
- `updated_at` (DateTime)

## API Endpoints

### Client Endpoints

#### View Available Coaches
```
GET /api/v1/bookings/coaches
```
Returns list of all coaches with their:
- Profile information (name, strengths, specialties, experience)
- Available slots
- Total slots
- Booked slots

#### View Specific Coach
```
GET /api/v1/bookings/coaches/{coach_id}
```
Returns detailed profile and availability for a specific coach.

#### Book Training Slot
```
POST /api/v1/bookings/book
Body: {
  "coach_id": int,
  "slot_number": int,
  "scheduled_at": datetime (optional),
  "notes": string (optional)
}
```
Books a training slot with a coach. Automatically:
- Creates booking with "pending" status
- Decrements coach's available_slots
- Prevents duplicate bookings

#### View My Bookings
```
GET /api/v1/bookings/my-bookings
```
Returns all bookings for the current user (client or coach).

#### Cancel Booking
```
PUT /api/v1/bookings/bookings/{booking_id}
Body: {
  "status": "cancelled"
}
```
Allows clients to cancel their bookings. Automatically restores the coach's available slot.

### Coach Endpoints

#### View Connected Clients
```
GET /api/v1/coach/clients
```
Returns list of clients connected through bookings. Coaches can only see clients they have bookings with.

#### View Client Profile
```
GET /api/v1/coach/clients/{client_id}
```
View detailed profile of a connected client. Access restricted to clients with whom the coach has bookings.

#### View Client Workout Logs
```
GET /api/v1/coach/clients/{client_id}/workout-logs?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
View day-wise workout logs for connected clients. Supports date filtering.

#### View Client Diet Logs
```
GET /api/v1/coach/clients/{client_id}/diet-logs?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
View day-wise diet logs for connected clients. Supports date filtering.

#### View Client Progress
```
GET /api/v1/coach/clients/{client_id}/progress
```
View progress metrics for connected clients.

#### Manage Bookings
```
GET /api/v1/bookings/coach/bookings
```
View all bookings for the current coach.

```
PUT /api/v1/bookings/bookings/{booking_id}
Body: {
  "status": "confirmed" | "completed",
  "scheduled_at": datetime (optional),
  "notes": string (optional)
}
```
Update booking status (confirm, complete).

### Admin Endpoints

#### View All Bookings
```
GET /api/v1/bookings/admin/bookings
```
View all bookings across all coaches and clients.

#### View Coach Calendar
```
GET /api/v1/bookings/admin/coaches/{coach_id}/bookings
```
View all bookings for a specific coach.

#### View All Users
```
GET /api/v1/admin/users?role=coach|client|admin
```
View all users with optional role filtering.

#### View User Profile
```
GET /api/v1/admin/users/{user_id}
```
View detailed profile of any user (coach, client, or admin).

## Access Control

### Client Access
- Can view all coaches and their availability
- Can book available slots with any coach
- Can view and cancel their own bookings
- Cannot access other clients' information

### Coach Access
- Can view profiles and logs ONLY of clients they're connected with through bookings
- Can view and manage their own bookings
- Can confirm/complete bookings
- Cannot access other coaches' information

### Admin Access
- Can view all users (coaches, clients, admins)
- Can view all bookings
- Can view any coach's calendar
- Full oversight of the platform

## Seeded Data

The `seed_charts.py` script creates comprehensive demo data:

### 3 Coaches with detailed profiles:
1. **Coach A**: Strength Training, Powerlifting, Olympic Lifts
   - 10 years experience
   - NASM-CPT, CSCS, USA Weightlifting Level 1

2. **Coach B**: Weight Loss, Cardio Training, HIIT
   - 8 years experience
   - ACE-CPT, Precision Nutrition Level 1

3. **Coach C**: Functional Training, CrossFit, Athletic Performance
   - 12 years experience
   - CrossFit Level 2, FMS Level 1

### 10 Clients with varied profiles:
- Demographics (age, gender, height, weight, measurements)
- Fitness goals
- Gym access
- Dietary restrictions
- Health complications
- Injuries

### Initial Bookings:
- 3-5 bookings per coach
- Various statuses (pending, confirmed, completed)
- Scheduled times (past and future)

## Testing

Comprehensive test suite with 18 booking-specific tests covering:

1. **Coach Availability Tests**
   - Get list of available coaches
   - Get specific coach details
   - Authentication requirements

2. **Booking Tests**
   - Successful slot booking
   - Duplicate booking prevention
   - Coach availability validation
   - Role-based access control

3. **Booking Management Tests**
   - View user's bookings
   - Coach confirmation
   - Client cancellation
   - Slot restoration on cancellation

4. **Admin Tests**
   - View all bookings
   - View coach calendars
   - Access control enforcement

**All 109 tests passing, 2 skipped**

## Migration

Database migration file: `backend/alembic/versions/004_add_booking_and_coach_slots.py`

To apply the migration:
```bash
cd backend
alembic upgrade head
```

## Usage Examples

### Client Booking Flow
1. Client views available coaches: `GET /api/v1/bookings/coaches`
2. Client selects a coach and views details: `GET /api/v1/bookings/coaches/1`
3. Client books a slot: `POST /api/v1/bookings/book`
4. Coach confirms booking: `PUT /api/v1/bookings/bookings/1` (status: confirmed)
5. Client and coach are now connected
6. Coach can view client profile: `GET /api/v1/coach/clients/5`
7. Coach can view client logs: `GET /api/v1/coach/clients/5/workout-logs`

### Admin Oversight Flow
1. Admin views all bookings: `GET /api/v1/bookings/admin/bookings`
2. Admin views specific coach's calendar: `GET /api/v1/bookings/admin/coaches/1/bookings`
3. Admin views coach profile: `GET /api/v1/admin/users/1`
4. Admin views client profile: `GET /api/v1/admin/users/5`

## Security Features

1. **Authentication**: All endpoints require valid JWT tokens
2. **Authorization**: Role-based access control (client, coach, admin)
3. **Data Isolation**: Coaches can only access data for connected clients
4. **Booking Validation**: Prevents duplicate bookings and overbooking
5. **Slot Management**: Automatic slot tracking and restoration

## Future Enhancements

Potential improvements for future iterations:
- Email notifications for booking confirmations
- Calendar integration (Google Calendar, iCal)
- Recurring bookings
- Waitlist for fully booked coaches
- Coach rating and review system
- Advanced scheduling with time slots
- Payment integration
- Video session integration
