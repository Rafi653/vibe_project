# Charts and Dashboards Documentation

## Overview

The Vibe Fitness Platform now includes comprehensive charting and analytics capabilities across all user roles. This document describes the implementation, features, and usage.

## Features

### Client Dashboard Charts

#### 1. Workout Frequency Chart
- **Type**: Line Chart
- **Time Range**: Last 30 days
- **Description**: Shows the number of workouts logged per day
- **Purpose**: Track workout consistency and identify patterns

#### 2. Diet Adherence Chart
- **Type**: Line Chart with Target Line
- **Time Range**: Last 30 days
- **Metrics**: Daily calorie intake vs. target
- **Purpose**: Monitor nutritional adherence to diet plans

#### 3. Macronutrient Breakdown Chart
- **Type**: Bar Chart
- **Time Range**: Last 30 days
- **Metrics**: Protein, Carbs, Fat (grams per day)
- **Purpose**: Visualize macro distribution over time

#### 4. Strength Progress Chart
- **Type**: Line Chart
- **Time Range**: Last 90 days
- **Features**: 
  - Exercise selector dropdown
  - Shows both average and max weight lifted
- **Purpose**: Track progressive overload and strength gains

### Coach Dashboard Charts

#### 1. Client Activity Overview
- **Type**: Bar Chart
- **Time Range**: Last 30 days
- **Metrics**: Workouts, Diet Logs, Active Plans per client
- **Purpose**: Quickly assess client engagement levels

#### 2. Client Engagement Trends
- **Type**: Line Chart
- **Time Range**: Last 30 days
- **Metrics**: Daily workouts and diet logs across all clients
- **Purpose**: Monitor overall client engagement patterns

#### 3. Plan Assignment Status
- **Type**: Doughnut Charts (2)
- **Metrics**: 
  - Workout plans by status (active, completed, etc.)
  - Diet plans by status
- **Purpose**: Track plan management and completion rates

### Admin Dashboard Charts

#### 1. User Growth Chart
- **Type**: Line Chart
- **Time Range**: Last 90 days
- **Metrics**: New clients, coaches, and admins over time
- **Purpose**: Monitor platform growth and user acquisition

#### 2. Platform Activity Chart
- **Type**: Bar Chart
- **Time Range**: Last 30 days
- **Metrics**: Daily workouts and diet logs platform-wide
- **Purpose**: Understand overall platform usage patterns

#### 3. System Health Chart
- **Type**: Line Chart with Stats Cards
- **Time Range**: Last 7 days
- **Metrics**: 
  - Total users
  - Active rate percentage
  - Daily active users
- **Purpose**: Monitor platform health and user engagement

## Technical Implementation

### Frontend Components

#### Chart Components (`frontend/src/components/charts/`)

1. **LineChart.js**
   - Configurable line chart with multi-dataset support
   - Supports filled areas and custom colors
   - Responsive design

2. **BarChart.js**
   - Configurable bar chart with multi-dataset support
   - Horizontal and vertical orientations
   - Responsive design

3. **DoughnutChart.js**
   - Circular chart for categorical data
   - Automatic color generation
   - Responsive design

4. **ChartExport.js**
   - Export charts as PNG
   - Export charts as PDF (via print)
   - Reusable component for any chart

#### Chart.js Configuration

All charts are built using Chart.js v4 with the following registered components:
- CategoryScale, LinearScale (axes)
- PointElement, LineElement (line charts)
- BarElement (bar charts)
- ArcElement (doughnut charts)
- Title, Tooltip, Legend, Filler (plugins)

### Backend API Endpoints

#### Client Endpoints (`/api/v1/client/charts/`)

```
GET /workout-frequency?days=30
Returns: { labels: [], data: [] }

GET /diet-adherence?days=30
Returns: { labels: [], calories: [], protein: [], carbs: [], fat: [], targets: {} }

GET /workout-volume?days=90&exercise=Bench%20Press
Returns: { exercises: [], data: { exercise_name: { dates: [], avg_weights: [], max_weights: [] } } }
```

#### Coach Endpoints (`/api/v1/coach/charts/`)

```
GET /client-overview
Returns: { clients: [{ client_name, client_id, workouts, diet_logs, active_plans }] }

GET /engagement?days=30
Returns: { workouts: { labels: [], data: [] }, diet_logs: { labels: [], data: [] } }

GET /plan-assignments
Returns: { workout_plans: {}, diet_plans: {} }
```

#### Admin Endpoints (`/api/v1/admin/charts/`)

```
GET /user-growth?days=90
Returns: { labels: [], clients: [], coaches: [], admins: [] }

GET /platform-usage?days=30
Returns: { workouts: { labels: [], data: [] }, diet_logs: { labels: [], data: [] } }

GET /coach-performance
Returns: { total_workout_plans, total_diet_plans, total_clients }

GET /system-health?days=7
Returns: { daily_active_users: { labels: [], data: [] }, total_users, active_rate }
```

## Data Seeding

### Comprehensive Seed Script

The `backend/app/db/seed_charts.py` script provides realistic test data:

**Users Created:**
- 1 Admin: `admin@vibe.com` / `admin123`
- 3 Coaches: `coach1-3@vibe.com` / `coach[1-3]123`
- 10 Clients: `client1-10@vibe.com` / `client[1-10]123`

**Data Generated:**
- **90 days** of historical workout logs
- **90 days** of historical diet logs
- **Varied workout frequency**: 2-6 times per week per client
- **Progressive overload**: Weight increases over time
- **Diet adherence**: ~70% logging compliance
- **Multiple plans**: 1-3 workout plans and 1-2 diet plans per client
- **Realistic meals**: Breakfast, lunch, dinner, snacks with proper macros

### Running the Seed Script

```bash
# With Docker
docker-compose exec backend python -m app.db.seed_charts

# Local development
cd backend
source venv/bin/activate
python -m app.db.seed_charts
```

## Responsive Design

All charts are fully responsive:
- Charts resize automatically based on container width
- `maintainAspectRatio: false` for better control
- Mobile-friendly layout with stacked charts
- CSS media queries for smaller screens

### Mobile Optimizations
- Chart cards have reduced padding on mobile
- Stats grids adjust to single column
- Font sizes scale appropriately
- Touch-friendly interactions

## Chart Export Feature

### Export to PNG
1. Click "Export PNG" button below any chart
2. Image downloads automatically
3. High-quality resolution preserved

### Export to PDF
1. Click "Export PDF" button below any chart
2. Opens print dialog with chart
3. Save as PDF or print

**Note:** For production use, consider integrating jsPDF library for better PDF generation.

## Performance Considerations

### Data Fetching
- Charts load asynchronously after dashboard data
- Uses Promise.all() for parallel requests
- Error handling prevents dashboard failure if charts fail

### Rendering
- Charts render only when data is available
- Conditional rendering prevents empty chart errors
- Minimal re-renders with proper React hooks

### Large Datasets
- Backend queries use indexed columns
- Date range filters prevent excessive data
- Frontend limits displayed data points when appropriate

## Future Enhancements

### Planned Features
1. **Real-time Updates**: WebSocket integration for live chart updates
2. **Custom Date Ranges**: User-selectable time periods
3. **Chart Filtering**: Interactive filters for exercises, clients, etc.
4. **Comparison Views**: Side-by-side comparisons
5. **Export to Excel**: CSV/Excel export for data analysis
6. **Annotations**: Add notes/markers to specific dates
7. **Goal Lines**: Visual goal tracking on charts
8. **Sharing**: Share charts with coaches/clients

### Possible Chart Additions
- **Heatmap**: Workout frequency heatmap (calendar view)
- **Pie Charts**: Meal type distribution
- **Scatter Plots**: Weight vs. reps correlation
- **Area Charts**: Cumulative progress over time
- **Gauge Charts**: Goal completion percentage

## Troubleshooting

### Charts Not Displaying
1. Check browser console for errors
2. Verify API endpoints are accessible
3. Ensure data is seeded in database
4. Check authentication token is valid

### Empty Charts
1. Run seed script to generate data
2. Verify date ranges include data
3. Check backend logs for query errors

### Performance Issues
1. Reduce date range for queries
2. Check database indexes
3. Monitor network requests
4. Consider data pagination

## API Testing

Test chart endpoints with curl:

```bash
# Login first
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client1@vibe.com","password":"client1123"}' \
  | jq -r '.access_token')

# Test workout frequency
curl -X GET "http://localhost:8000/api/v1/client/charts/workout-frequency?days=30" \
  -H "Authorization: Bearer $TOKEN"

# Test diet adherence
curl -X GET "http://localhost:8000/api/v1/client/charts/diet-adherence?days=30" \
  -H "Authorization: Bearer $TOKEN"
```

## Browser Compatibility

Charts are tested and working on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Dependencies

### Frontend
- `chart.js`: ^4.4.0 (Core charting library)
- `react-chartjs-2`: ^5.2.0 (React wrapper for Chart.js)

### Backend
- FastAPI for API endpoints
- SQLAlchemy for database queries
- PostgreSQL for data storage

## Support and Maintenance

For issues or questions:
1. Check this documentation
2. Review backend logs
3. Check browser console
4. Review API responses
5. Check database data

---

**Last Updated**: 2025-10-11
**Version**: 1.0.0
