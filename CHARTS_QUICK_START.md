# Charts and Dashboards - Quick Start Guide

## Getting Started with Charts

This guide will help you quickly set up and start using the new charts and analytics features.

## Step 1: Install Dependencies

The Chart.js dependencies have already been added to `package.json`. Install them:

```bash
cd frontend
npm install
```

## Step 2: Seed the Database with Chart Data

To see the charts in action, you need historical data. Run the comprehensive seed script:

### Using Docker:
```bash
docker-compose exec backend python -m app.db.seed_charts
```

### Without Docker (Local Development):
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.db.seed_charts
```

This will create:
- 1 Admin user
- 3 Coaches
- 10 Clients
- 90 days of workout logs (varied frequency per client)
- 90 days of diet logs (with realistic meals and macros)
- Multiple workout and diet plans

## Step 3: Start the Application

### Backend:
```bash
# With Docker
docker-compose up backend

# Without Docker
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend:
```bash
cd frontend
npm start
```

## Step 4: Login and View Charts

### Client Dashboard (client1@vibe.com / client1123)
1. Navigate to http://localhost:3000
2. Login with client credentials
3. View your dashboard with:
   - **Workout Frequency Chart**: See your workout consistency
   - **Diet Adherence Chart**: Track calorie intake vs. targets
   - **Macros Breakdown**: View protein, carbs, fat distribution
   - **Strength Progress**: Select exercises to see weight progression

### Coach Dashboard (coach1@vibe.com / coach1123)
1. Login with coach credentials
2. View coach dashboard with:
   - **Client Activity Overview**: Bar chart showing all clients' activity
   - **Engagement Trends**: Line chart of daily workouts and diet logs
   - **Plan Assignments**: Doughnut charts showing plan status distribution

### Admin Dashboard (admin@vibe.com / admin123)
1. Login with admin credentials
2. View admin dashboard with:
   - **User Growth**: Line chart showing new user registrations over time
   - **Platform Activity**: Bar chart of daily platform usage
   - **System Health**: Active users and engagement metrics

## Sample Credentials

After running the seed script, use these credentials:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@vibe.com | admin123 |
| Coach 1 | coach1@vibe.com | coach1123 |
| Coach 2 | coach2@vibe.com | coach2123 |
| Coach 3 | coach3@vibe.com | coach3123 |
| Client 1 | client1@vibe.com | client1123 |
| Client 2 | client2@vibe.com | client2123 |
| ... | ... | ... |
| Client 10 | client10@vibe.com | client10123 |

## Chart Features

### Interactive Elements
- **Hover**: Hover over data points to see exact values
- **Legend**: Click legend items to show/hide datasets
- **Tooltips**: Rich tooltips with formatted data

### Exercise Selection (Client Dashboard)
1. Scroll to "Strength Progress" chart
2. Use dropdown to select different exercises
3. View avg and max weight progression

### Export Charts
- **PNG Export**: Click "Export PNG" to download chart as image
- **PDF Export**: Click "Export PDF" to print or save as PDF

## Customization

### Adjust Time Ranges

You can customize the time ranges by modifying the API calls in the dashboard components:

```javascript
// In ClientDashboard.js
clientService.getWorkoutFrequencyChart(token, 30)  // Change 30 to desired days
clientService.getDietAdherenceChart(token, 30)     // Change 30 to desired days
clientService.getWorkoutVolumeChart(token, 90)     // Change 90 to desired days
```

### Chart Colors

Charts use color schemes defined in the components. To customize:

1. Open the relevant dashboard file (e.g., `ClientDashboard.js`)
2. Find the chart configuration
3. Modify `borderColor` and `backgroundColor` properties

Example:
```javascript
{
  label: 'Workouts per Day',
  data: workoutFrequencyData.data,
  borderColor: 'rgb(97, 218, 251)',        // Line color
  backgroundColor: 'rgba(97, 218, 251, 0.2)', // Fill color
  fill: true,
}
```

## Troubleshooting

### No Charts Appearing?
1. **Check if data exists**: Run the seed script
2. **Open browser console**: Look for JavaScript errors
3. **Check API responses**: Open Network tab in DevTools
4. **Verify backend is running**: Check http://localhost:8000/api/docs

### Charts Show "No Data"?
1. The seed script may not have run successfully
2. Check that you're logged in as the correct user
3. Verify database contains data using a DB client

### Backend Errors?
1. Check backend console for error messages
2. Ensure all migrations are applied: `alembic upgrade head`
3. Verify database connection is working

### Build Errors?
```bash
# Clear cache and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## API Endpoints Reference

### Client Charts
```
GET /api/v1/client/charts/workout-frequency?days=30
GET /api/v1/client/charts/diet-adherence?days=30
GET /api/v1/client/charts/workout-volume?days=90&exercise=Bench%20Press
```

### Coach Charts
```
GET /api/v1/coach/charts/client-overview
GET /api/v1/coach/charts/engagement?days=30
GET /api/v1/coach/charts/plan-assignments
```

### Admin Charts
```
GET /api/v1/admin/charts/user-growth?days=90
GET /api/v1/admin/charts/platform-usage?days=30
GET /api/v1/admin/charts/coach-performance
GET /api/v1/admin/charts/system-health?days=7
```

## Testing with cURL

```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"client1@vibe.com","password":"client1123"}' \
  | jq -r '.access_token')

# Get workout frequency data
curl -X GET "http://localhost:8000/api/v1/client/charts/workout-frequency?days=30" \
  -H "Authorization: Bearer $TOKEN" | jq

# Get diet adherence data
curl -X GET "http://localhost:8000/api/v1/client/charts/diet-adherence?days=30" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## Mobile Responsive

All charts are fully responsive and work on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

The layout automatically adjusts:
- Charts resize to fit screen width
- Stats cards stack vertically on small screens
- Touch-friendly interactions

## Performance Tips

1. **Limit Date Ranges**: Shorter date ranges load faster
2. **Use Pagination**: For very large datasets
3. **Cache Data**: Consider implementing client-side caching
4. **Optimize Queries**: Database indexes are already in place

## Next Steps

1. Explore all three dashboard types (Client, Coach, Admin)
2. Experiment with different time ranges
3. Try exporting charts
4. Review the comprehensive documentation in `CHARTS_DOCUMENTATION.md`

## Support

For detailed technical documentation, see:
- `CHARTS_DOCUMENTATION.md` - Complete technical reference
- `API_REFERENCE.md` - API endpoints documentation
- `CORE_FEATURES.md` - Core platform features

---

**Enjoy visualizing your fitness journey! 💪📊**
