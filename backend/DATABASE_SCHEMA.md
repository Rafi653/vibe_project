# Database Schema Documentation

This document describes the database schema for the Vibe Fitness Platform.

## Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│       USERS         │
├─────────────────────┤
│ id (PK)             │
│ email               │
│ hashed_password     │
│ full_name           │
│ role                │ (client/coach/admin)
│ is_active           │
│ is_verified         │
│ created_at          │
│ updated_at          │
└─────────────────────┘
         │
         │ 1:N
         ├──────────────────────┐
         │                      │
         │                      │
┌────────▼──────────┐  ┌────────▼──────────┐
│   WORKOUT_LOGS    │  │    DIET_LOGS      │
├───────────────────┤  ├───────────────────┤
│ id (PK)           │  │ id (PK)           │
│ user_id (FK)      │  │ user_id (FK)      │
│ workout_date      │  │ meal_date         │
│ exercise_name     │  │ meal_type         │
│ sets              │  │ food_name         │
│ reps              │  │ calories          │
│ weight            │  │ protein_grams     │
│ duration_minutes  │  │ carbs_grams       │
│ notes             │  │ fat_grams         │
│ created_at        │  │ notes             │
│ updated_at        │  │ created_at        │
└───────────────────┘  │ updated_at        │
                       └───────────────────┘
         │
         │ 1:N
         ├──────────────────────┐
         │                      │
         │                      │
┌────────▼──────────┐  ┌────────▼──────────┐
│  WORKOUT_PLANS    │  │   DIET_PLANS      │
├───────────────────┤  ├───────────────────┤
│ id (PK)           │  │ id (PK)           │
│ user_id (FK)      │  │ user_id (FK)      │
│ name              │  │ name              │
│ description       │  │ description       │
│ start_date        │  │ start_date        │
│ end_date          │  │ end_date          │
│ status            │  │ status            │
│ duration_weeks    │  │ target_calories   │
│ workout_details   │  │ target_protein_g  │
│ created_at        │  │ target_carbs_g    │
│ updated_at        │  │ target_fat_g      │
└───────────────────┘  │ meal_plan_details │
                       │ created_at        │
                       │ updated_at        │
                       └───────────────────┘
```

## Table Definitions

### Users Table

Stores user accounts with authentication and profile information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | User's email address |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| full_name | VARCHAR(255) | NOT NULL | User's full name |
| role | ENUM | NOT NULL | User role: client, coach, or admin |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| is_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | Email verification status |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `email`

**Relationships:**
- One-to-Many with `workout_logs`
- One-to-Many with `diet_logs`
- One-to-Many with `workout_plans`
- One-to-Many with `diet_plans`

---

### WorkoutLog Table

Tracks individual workout sessions and exercises.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| workout_date | DATE | NOT NULL, INDEXED | Date of workout |
| exercise_name | VARCHAR(255) | NOT NULL | Name of exercise performed |
| sets | INTEGER | NULL | Number of sets |
| reps | INTEGER | NULL | Number of repetitions |
| weight | FLOAT | NULL | Weight used (kg or lbs) |
| duration_minutes | INTEGER | NULL | Duration of workout |
| notes | TEXT | NULL | Additional notes |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `user_id`
- Index on `workout_date`

**Relationships:**
- Many-to-One with `users`

---

### DietLog Table

Tracks daily meals and nutritional information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| meal_date | DATE | NOT NULL, INDEXED | Date of meal |
| meal_type | ENUM | NOT NULL | Type: breakfast, lunch, dinner, snack |
| food_name | VARCHAR(255) | NOT NULL | Name of food consumed |
| calories | FLOAT | NULL | Calories consumed |
| protein_grams | FLOAT | NULL | Protein in grams |
| carbs_grams | FLOAT | NULL | Carbohydrates in grams |
| fat_grams | FLOAT | NULL | Fat in grams |
| notes | TEXT | NULL | Additional notes |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `user_id`
- Index on `meal_date`

**Relationships:**
- Many-to-One with `users`

---

### WorkoutPlan Table

Defines structured workout programs for users.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique plan identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| name | VARCHAR(255) | NOT NULL | Plan name |
| description | TEXT | NULL | Plan description |
| start_date | DATE | NOT NULL | Plan start date |
| end_date | DATE | NULL | Plan end date (if applicable) |
| status | ENUM | NOT NULL | Status: active, completed, paused, cancelled |
| duration_weeks | INTEGER | NULL | Plan duration in weeks |
| workout_details | JSON | NULL | Structured workout information |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `user_id`

**Relationships:**
- Many-to-One with `users`

**JSON Structure (workout_details):**
```json
{
  "days_per_week": 3,
  "focus": "Strength",
  "exercises": [
    {
      "name": "Squats",
      "sets": 3,
      "reps": 10,
      "rest_seconds": 90
    }
  ]
}
```

---

### DietPlan Table

Defines structured diet programs with nutritional targets.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique plan identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| name | VARCHAR(255) | NOT NULL | Plan name |
| description | TEXT | NULL | Plan description |
| start_date | DATE | NOT NULL | Plan start date |
| end_date | DATE | NULL | Plan end date (if applicable) |
| status | ENUM | NOT NULL | Status: active, completed, paused, cancelled |
| target_calories | FLOAT | NULL | Daily calorie target |
| target_protein_grams | FLOAT | NULL | Daily protein target in grams |
| target_carbs_grams | FLOAT | NULL | Daily carbs target in grams |
| target_fat_grams | FLOAT | NULL | Daily fat target in grams |
| meal_plan_details | JSON | NULL | Structured meal plan information |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Record creation timestamp |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `user_id`

**Relationships:**
- Many-to-One with `users`

**JSON Structure (meal_plan_details):**
```json
{
  "meals_per_day": 5,
  "meal_timing": ["7:00", "10:00", "13:00", "16:00", "19:00"],
  "restrictions": ["gluten-free"],
  "preferences": ["high-protein"]
}
```

---

## Enumerations

### UserRole
- `client` - Regular user/client
- `coach` - Fitness coach
- `admin` - System administrator

### MealType
- `breakfast` - Morning meal
- `lunch` - Midday meal
- `dinner` - Evening meal
- `snack` - Snack or small meal

### PlanStatus
- `active` - Currently active plan
- `completed` - Successfully completed plan
- `paused` - Temporarily paused
- `cancelled` - Cancelled/abandoned plan

---

## Database Constraints

### Foreign Key Constraints
All foreign key relationships enforce referential integrity with CASCADE on delete:
- `workout_logs.user_id` → `users.id`
- `diet_logs.user_id` → `users.id`
- `workout_plans.user_id` → `users.id`
- `diet_plans.user_id` → `users.id`

### Check Constraints
- Email addresses follow standard email format
- Numeric values (weight, calories, etc.) are non-negative
- Dates are valid and consistent (end_date >= start_date)

---

## Common Queries

### Get User's Recent Workouts
```sql
SELECT * FROM workout_logs
WHERE user_id = :user_id
ORDER BY workout_date DESC, created_at DESC
LIMIT 10;
```

### Get Daily Nutrition Summary
```sql
SELECT
    meal_date,
    SUM(calories) as total_calories,
    SUM(protein_grams) as total_protein,
    SUM(carbs_grams) as total_carbs,
    SUM(fat_grams) as total_fat
FROM diet_logs
WHERE user_id = :user_id
    AND meal_date = :date
GROUP BY meal_date;
```

### Get Active Plans for User
```sql
SELECT * FROM workout_plans
WHERE user_id = :user_id
    AND status = 'active'
ORDER BY start_date DESC;

SELECT * FROM diet_plans
WHERE user_id = :user_id
    AND status = 'active'
ORDER BY start_date DESC;
```

### Get User Statistics
```sql
-- Total workout sessions
SELECT COUNT(*) as total_workouts
FROM workout_logs
WHERE user_id = :user_id;

-- Average calories per day
SELECT AVG(daily_calories) as avg_daily_calories
FROM (
    SELECT meal_date, SUM(calories) as daily_calories
    FROM diet_logs
    WHERE user_id = :user_id
    GROUP BY meal_date
) subquery;
```

---

## Migration History

| Version | Description | Date |
|---------|-------------|------|
| 001 | Initial migration with all core tables | 2025-10-11 |

---

## Future Schema Considerations

Potential enhancements for future versions:

1. **Exercise Library Table**
   - Pre-defined exercises with instructions
   - Muscle groups targeted
   - Equipment required

2. **User Metrics Table**
   - Body measurements
   - Progress photos
   - Weight tracking over time

3. **Social Features**
   - User followers/following
   - Workout sharing
   - Comments and likes

4. **Notifications Table**
   - Reminders
   - Achievements
   - Coach messages

5. **Payment/Subscription Table**
   - Subscription plans
   - Payment history
   - Billing information

---

## Performance Considerations

### Current Optimizations
- Indexes on frequently queried columns (user_id, dates)
- Timestamp fields for all records
- Appropriate data types to minimize storage

### Recommended for Scale
- Partitioning large tables by date (workout_logs, diet_logs)
- Materialized views for analytics
- Read replicas for reporting
- Connection pooling
- Query result caching

---

## Backup and Recovery

### Backup Strategy
- Daily full backups
- Hourly incremental backups
- Transaction log backups
- Off-site backup storage

### Recovery Procedures
See [DATABASE_SETUP.md](DATABASE_SETUP.md#database-backup) for backup and restore procedures.

---

*Last Updated: 2025-10-11*
