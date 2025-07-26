# E-commerce Customer Support Chatbot - Frontend

This is the frontend application for the E-commerce Customer Support Chatbot. It provides a modern, responsive chat interface built with React and TypeScript.

## Features

- **Modern Chat Interface**: Clean, responsive design with real-time messaging
- **Quick Suggestions**: Pre-defined query buttons for common questions
- **Loading States**: Visual feedback during API calls
- **Mobile Responsive**: Optimized for both desktop and mobile devices
- **Real-time Updates**: Automatic scrolling and message handling

## Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## Development

The application will be available at `http://localhost:3000` by default.

### Prerequisites

Make sure the backend server is running on `http://localhost:8000` before using the frontend.

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Technology Stack

- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons
- **CSS3** - Modern styling with gradients and animations

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # Application entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── package.json         # Dependencies and scripts
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
└── README.md           # This file
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- **POST** `/chat` - Send chat messages and receive responses
- **GET** `/health` - Check backend health status

## UI Components

### Chat Interface
- Message bubbles with user/bot avatars
- Real-time message updates
- Loading indicators
- Auto-scroll to latest messages

### Input System
- Text input with send button
- Quick suggestion buttons
- Form validation and error handling

### Responsive Design
- Mobile-first approach
- Adaptive layouts for different screen sizes
- Touch-friendly interface elements

## Styling

The application uses modern CSS features:
- CSS Grid and Flexbox for layouts
- CSS Custom Properties for theming
- Smooth animations and transitions
- Glassmorphism effects
- Gradient backgrounds

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Notes

- The application uses React 18's concurrent features
- TypeScript provides type safety throughout the codebase
- Vite provides fast development and build times
- CORS is configured to allow communication with the backend 