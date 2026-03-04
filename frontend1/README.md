# RoadCare Frontend - React Application

This is the React-based frontend for the RoadCare AI-Based Road Detection System, converted from vanilla HTML/CSS/JavaScript to a modern React application using Vite.

## Features

- ✨ Modern React 18 with Hooks
- ⚡ Vite for blazing fast development
- 🎨 Tailwind CSS for styling
- 🌓 Dark mode support
- 🔐 JWT Authentication
- 📱 Responsive design
- 🚀 Client-side routing with React Router
- 🎯 Context API for state management
- 📡 Axios for API calls

## Project Structure

```
frontend1/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── Toast.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ProtectedRoute.jsx
│   ├── context/          # React Context providers
│   │   ├── AuthContext.jsx
│   │   └── ThemeContext.jsx
│   ├── pages/            # Page components
│   │   ├── HomePage.jsx
│   │   ├── ReportPotholePage.jsx
│   │   ├── AuthorityLoginPage.jsx
│   │   ├── AuthorityDashboardPage.jsx
│   │   └── ComplaintDetailPage.jsx
│   ├── services/         # API service layer
│   │   └── apiService.js
│   ├── utils/            # Utility functions
│   │   └── storageUtils.js
│   ├── config/           # Configuration
│   │   └── config.js
│   ├── App.jsx           # Main App component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── public/               # Static assets
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── postcss.config.js     # PostCSS configuration
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend1
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Pages

### Public Pages
- **Home Page** (`/`) - Landing page with features and information
- **Report Pothole** (`/report-pothole`) - Form to submit pothole reports
- **Authority Login** (`/authority-login`) - Login page for authorities

### Protected Pages (Require Authentication)
- **Authority Dashboard** (`/authority-dashboard`) - Dashboard for managing reports
- **Complaint Detail** (`/complaint/:id`) - Detailed view of a specific report

## Key Features

### Authentication
- JWT-based authentication
- Protected routes with automatic redirect
- Token storage in localStorage
- Auto-logout on token expiration

### Dark Mode
- System preference detection
- Manual toggle
- Persistent preference storage

### API Integration
- Axios interceptors for token injection
- Automatic error handling
- Centralized API service

### Responsive Design
- Mobile-first approach
- Tailwind CSS breakpoints
- Optimized for all screen sizes

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: `http://localhost:8000`)

## Technologies Used

- **React** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Google Fonts** - Libre Caslon Text font
- **Material Symbols** - Icons

## Migration from Vanilla JS

This application was converted from vanilla HTML/CSS/JavaScript to React. Key changes:

1. **Component-based architecture** - Modular, reusable components
2. **State management** - React Context API instead of global variables
3. **Routing** - React Router instead of multi-page HTML
4. **Build process** - Vite for optimized bundling
5. **Modern JavaScript** - ES6+ features, async/await
6. **Type safety ready** - Easy to migrate to TypeScript

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api/v1`. Ensure the backend is running before using the application.

## Contributing

1. Follow the existing code structure
2. Use functional components with hooks
3. Maintain consistent styling with Tailwind
4. Add comments for complex logic
5. Test all features before committing

## License

This project is part of the RoadCare AI-Based Road Detection System.
