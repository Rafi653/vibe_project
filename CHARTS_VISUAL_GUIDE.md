# Charts and Dashboards - Visual Guide

This document provides a visual description of all charts implemented in the Vibe Fitness Platform.

## Client Dashboard

### 1. Progress Summary (Stats Cards)
```
┌─────────────────────────────────────────────────────────────┐
│  Your Progress (Last 30 Days)                               │
├──────────────┬──────────────┬──────────────┬───────────────┤
│      45      │      38      │      2       │      1        │
│  Workout     │  Diet Logs   │  Active      │  Active       │
│  Sessions    │              │  Workout     │  Diet         │
│              │              │  Plans       │  Plans        │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

### 2. Workout Frequency Chart (Line Chart)
```
Workout Frequency (Last 30 Days)
     
  5 |                    *
  4 |        *    *     * *
  3 |   *   * *  * *   *   *
  2 |  * * *   **   * *     *
  1 | *     *       *        *
  0 |________________________
     Oct 1      Oct 15     Oct 30

Legend: * = Workouts per Day
```
**Visual**: Smooth line chart with filled area below, showing daily workout count over time. Teal color (#61dafb).

### 3. Diet Adherence Chart (Line Chart with Target)
```
Diet Adherence (Last 30 Days)

Calories
3000|                    *
2500|    * *  * *  * *  * * *  (Target: 2500 cal - dotted line)
2000| * *   **   **   **     *
1500|
    |________________________
     Oct 1      Oct 15     Oct 30

Legend: * = Daily Calories, -- = Target
```
**Visual**: Two line charts overlaid - actual calories (solid red line) and target calories (dashed red line).

### 4. Macronutrient Breakdown (Bar Chart)
```
Macronutrient Tracking (Last 30 Days)

Grams
250|  |||  |||  |||  |||  |||
200|  |||  |||  |||  |||  |||
150|  |||  |||  |||  |||  |||
100|  |||  |||  |||  |||  |||
 50|  |||  |||  |||  |||  |||
   |________________________
    Oct 1  Oct 8  Oct 15 Oct 22

Legend: | = Protein (blue), | = Carbs (yellow), | = Fat (teal)
```
**Visual**: Grouped bar chart showing protein, carbs, and fat for each day. Three bars per day in different colors.

### 5. Strength Progress Chart (Line Chart with Exercise Selector)
```
Strength Progress (Last 90 Days)

Select Exercise: [Bench Press ▼]

Weight (kg)
100|                      **
 80|            **  **  **  **
 60|    **  **  **
 40| **
    |________________________
     Jul 1    Aug 1    Sep 1    Oct 1

Legend: ** = Average Weight, ** = Max Weight
```
**Visual**: Two line charts showing average and max weight for selected exercise. Purple and orange colors. Dropdown allows switching exercises.

---

## Coach Dashboard

### 1. Client Summary (Stats Card)
```
┌─────────────────────────────────────────────────────────────┐
│  Your Clients                                                │
├──────────────────────────────────────────────────────────────┤
│                          10                                  │
│                    Total Clients                             │
└──────────────────────────────────────────────────────────────┘
```

### 2. Client Activity Overview (Bar Chart)
```
Client Activity Overview (Last 30 Days)

Count
 60|
 50|  |||  |||  |||  |||  |||
 40|  |||  |||  |||  |||  |||
 30|  |||  |||  |||  |||  |||
 20|  |||  |||  |||  |||  |||
 10|  |||  |||  |||  |||  |||
   |________________________
    Client Client Client Client Client
      A      B      C      D      E

Legend: | = Workouts, | = Diet Logs, | = Active Plans
```
**Visual**: Grouped bar chart with three bars per client. Shows workouts (teal), diet logs (red), and active plans (green) for each client.

### 3. Client Engagement Trends (Line Chart)
```
Client Engagement Trends (Last 30 Days)

Count
 80|                    **
 60|        **  **  ** **
 40|   **  **  **  **    **
 20| **  **            **
    |________________________
     Oct 1      Oct 15     Oct 30

Legend: ** = Daily Workouts (all clients), ** = Daily Diet Logs
```
**Visual**: Two line charts showing total daily workouts (teal) and diet logs (red) across all clients. Filled areas beneath.

### 4. Plan Assignment Status (Doughnut Charts)
```
Workout Plans Status           Diet Plans Status
        
    ╭────────╮                    ╭────────╮
   ╱  Active  ╲                  ╱  Active  ╲
  │   (60%)    │                │   (55%)    │
  │ Completed  │                │ Completed  │
   ╲  (40%)   ╱                  ╲  (45%)   ╱
    ╰────────╯                    ╰────────╯
```
**Visual**: Two doughnut charts side by side. Each shows plan status distribution with color-coded segments.

---

## Admin Dashboard

### 1. Platform Statistics (Stats Cards)
```
┌─────────────────────────────────────────────────────────────┐
│  Platform Statistics                                         │
├──────────────┬──────────────┬──────────────┬───────────────┤
│      14      │      12      │      10      │      3        │
│  Total       │  Active      │  Clients     │  Coaches      │
│  Users       │  Users       │              │               │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

### 2. User Growth Chart (Line Chart)
```
User Growth (Last 90 Days)

Users
 10|                      ***
  8|              ***  ***
  6|      ***  ***  ***
  4|  ***  ***
  2| ***
    |________________________
     Jul 1    Aug 1    Sep 1    Oct 1

Legend: *** = Clients, *** = Coaches, *** = Admins
```
**Visual**: Three line charts showing new user registrations by role over time. Clients (teal), Coaches (orange), Admins (purple).

### 3. Platform Activity Chart (Bar Chart)
```
Platform Activity (Last 30 Days)

Count
150|  ||  ||  ||  ||  ||  ||
120|  ||  ||  ||  ||  ||  ||
 90|  ||  ||  ||  ||  ||  ||
 60|  ||  ||  ||  ||  ||  ||
 30|  ||  ||  ||  ||  ||  ||
   |________________________
    Oct Oct Oct Oct Oct Oct
     5  10  15  20  25  30

Legend: || = Workouts, || = Diet Logs
```
**Visual**: Grouped bar chart showing daily workouts (teal) and diet logs (red) platform-wide.

### 4. System Health (Stats + Line Chart)
```
System Health (Last 7 Days)

┌──────────────┬──────────────┐
│      14      │    85.7%     │
│  Total Users │  Active Rate │
└──────────────┴──────────────┘

Active Users
 12|                      *
 10|              *  *  *
  8|      *  *  *
  6|  *  *
    |________________________
     Mon  Tue  Wed  Thu  Fri  Sat  Sun

Legend: * = Daily Active Users
```
**Visual**: Stats cards showing total users and engagement rate, followed by line chart of daily active users (green).

---

## Chart Interaction Features

### Hover Tooltips
```
┌──────────────────────┐
│  October 15, 2025    │
│  Workouts: 5         │
├──────────────────────┤
│  Diet Logs: 4        │
└──────────────────────┘
```
When hovering over data points, tooltips appear showing exact values and dates.

### Legend Interaction
```
Legend: ☑ Workouts  ☐ Diet Logs  ☑ Active Plans
```
Click legend items to show/hide specific datasets on the chart.

### Export Buttons
```
┌─────────────┐  ┌─────────────┐
│ Export PNG  │  │ Export PDF  │
└─────────────┘  └─────────────┘
```
Buttons appear below each chart for exporting.

---

## Responsive Design

### Desktop View
```
┌────────────────────────────────────────────────────────────────┐
│  Dashboard Header                                               │
├──────────────────────────────────────────────────────────────────┤
│  [Stat 1]  [Stat 2]  [Stat 3]  [Stat 4]                        │
├──────────────────────────────────────────────────────────────────┤
│  [Chart 1: Full Width]                                          │
├──────────────────────────────────────────────────────────────────┤
│  [Chart 2: Full Width]                                          │
└──────────────────────────────────────────────────────────────────┘
```

### Mobile View
```
┌────────────────┐
│  Dashboard     │
│  Header        │
├────────────────┤
│  [Stat 1]      │
├────────────────┤
│  [Stat 2]      │
├────────────────┤
│  [Stat 3]      │
├────────────────┤
│  [Stat 4]      │
├────────────────┤
│  [Chart 1]     │
│  [Full Width]  │
├────────────────┤
│  [Chart 2]     │
│  [Full Width]  │
└────────────────┘
```
Stats stack vertically on mobile, charts remain full width.

---

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Primary (Teal) | ████ | #61dafb |
| Success (Green) | ████ | #4caf50 |
| Danger (Red) | ████ | #ff6384 |
| Warning (Orange) | ████ | #ff9f40 |
| Info (Purple) | ████ | #9966ff |
| Secondary (Yellow) | ████ | #ffce56 |
| Dark Text | ████ | #282c34 |
| Light Text | ████ | #666666 |

---

## Chart Types Summary

| Dashboard | Chart Type | Data | Purpose |
|-----------|-----------|------|---------|
| Client | Line | Workout Frequency | Track consistency |
| Client | Line | Diet Adherence | Monitor calorie intake |
| Client | Bar | Macros | Visualize nutrition |
| Client | Line | Strength | Track progress |
| Coach | Bar | Client Activity | Compare clients |
| Coach | Line | Engagement | Monitor trends |
| Coach | Doughnut | Plan Status | Track completion |
| Admin | Line | User Growth | Monitor growth |
| Admin | Bar | Platform Activity | Track usage |
| Admin | Line | System Health | Monitor engagement |

---

## Data Flow

```
Frontend Dashboard
       ↓
API Service Call (clientService.getWorkoutFrequencyChart)
       ↓
Backend Endpoint (/api/v1/client/charts/workout-frequency)
       ↓
Database Query (PostgreSQL with date filters)
       ↓
Data Aggregation (Group by date, count)
       ↓
JSON Response
       ↓
Chart Component (LineChart with labels and data)
       ↓
Chart.js Rendering
       ↓
Interactive Chart Display
```

---

**This visual guide helps developers and stakeholders understand what the charts look like without running the application.**
