# Vibe Fitness - Frontend

This is the frontend application for the Vibe Fitness coaching platform, built with React.js.

## Tech Stack

- **Framework**: React.js 19.2.0
- **Routing**: React Router DOM 7.9.4
- **Build Tool**: Create React App (react-scripts 5.0.1)
- **Testing**: Jest & React Testing Library

## Project Structure

```
frontend/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable UI components
│   │   └── Navigation.js
│   ├── pages/           # Page components
│   │   ├── admin/       # Admin dashboard pages
│   │   ├── client/      # Client dashboard pages
│   │   ├── coach/       # Coach dashboard pages
│   │   └── common/      # Common pages (Home, etc.)
│   ├── App.js           # Main application component with routing
│   ├── App.css          # Global app styles
│   ├── index.js         # Application entry point
│   └── index.css        # Global styles
└── package.json         # Dependencies and scripts
```

## Features

### Role-Based Navigation
The application includes navigation and routing for three user roles:

1. **Client Portal** (`/client`) - For fitness clients to view workouts, track progress, connect with coaches, and access nutrition plans
2. **Coach Portal** (`/coach`) - For fitness coaches to manage clients, create workout plans, monitor progress, and manage schedules
3. **Admin Portal** (`/admin`) - For administrators to manage users, view analytics, moderate content, and configure settings

### Navigation Component
A responsive navigation bar provides easy access to all sections of the application.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
