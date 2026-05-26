# Prompt

## Context and Role

As a Full Stack AI/ML Developer, your task is to build a modern AI-powered web application called **Mood Analysis**.

The platform should detect human emotions in real-time using the user’s webcam and display live emotion predictions with confidence percentages.

The application should feel smooth, modern, and interactive while maintaining production-level architecture, responsive design, secure APIs, and optimized AI performance.

The final product should resemble a polished AI SaaS platform with immersive UI, real-time processing, and clean user experience.

---

# Objective

Develop a complete full-stack emotion detection application that:

- Detects facial emotions in real-time using webcam input
- Displays live emotion predictions and confidence percentages
- Stores emotion sessions securely in MongoDB
- Provides emotion history and analytics dashboards
- Uses smooth animations and modern UI interactions
- Maintains strong performance, accessibility, and scalability

---

# Technology Stack

## Frontend
Use:
- Next.js
- TypeScript
- Tailwind CSS
- Framer Motion
- React Webcam
- Axios
- Recharts

## Backend
Use:
- Node.js
- Express.js
- MongoDB Atlas
- Mongoose
- Helmet.js
- express-rate-limit
- dotenv

## AI / ML
Use:
- face-api.js
- TensorFlow.js

---

# Core Application Flow

The application should work as follows:

1. User opens the landing page
2. User enters their name
3. User clicks “Start Mood Analysis”
4. Webcam permission is requested
5. Camera initializes successfully
6. Face detection activates automatically
7. Emotion detection begins in real-time
8. Predicted emotions appear live on screen
9. Confidence percentages update dynamically
10. Emotion data is stored in MongoDB
11. User can view emotion history and session summaries

---

# Emotion Detection Requirements

The system should detect the following emotions:

- Happy
- Sad
- Angry
- Neutral
- Fear
- Surprise
- Disgust

The AI system should:
- Detect faces continuously in real-time
- Analyze facial expressions efficiently
- Handle situations where no face is detected
- Handle multiple-face scenarios gracefully
- Maintain smooth real-time performance during webcam analysis

---

# Frontend Requirements

Build a modern futuristic interface featuring:

- Dark theme UI
- Glassmorphism cards
- Neon gradient effects
- Animated backgrounds
- Floating glow effects
- Smooth transitions
- Framer Motion animations
- Fully responsive layouts

The interface should feel clean, immersive, and visually engaging.

---

# Required Pages

## 1. Landing Page

Include:
- Large animated “Mood Analysis” title
- Short subtitle and introduction
- Animated futuristic background
- Start button with hover animations
- Smooth entrance transitions

---

## 2. Analysis Page

Include:
- Live webcam feed
- Real-time face detection
- Live emotion predictions
- Confidence percentage indicators
- Animated emotion cards
- Detection status messages
- Error handling and loading states

---

## 3. Dashboard Page

Include:
- Current detected emotion
- Emotion history timeline
- Confidence charts using Recharts
- Session analytics
- Summary statistics

---

# Animation and UI Requirements

Use Framer Motion to implement:

- Smooth page transitions
- Fade-in animations
- Scroll-triggered effects
- Hover interactions
- Floating animated UI elements
- Staggered motion effects

Animations should:
- Feel smooth and natural
- Use GPU-friendly properties
- Avoid layout thrashing
- Maintain performance during AI processing

---

# Backend Requirements

Create secure REST APIs using Express.js.

## Required APIs
- Start Session API
- Save Emotion Data API
- Get Emotion History API
- Download Session Report API

## Backend Features
Implement:
- Proper MVC architecture
- Input validation
- Error handling middleware
- Secure API responses
- Environment variable management
- Rate limiting
- Request sanitization

---

# Database Requirements

Store the following information in MongoDB Atlas:

- Username
- Detected emotion
- Confidence percentage
- Timestamp
- Session duration

---

# Security Requirements

Implement:
- Helmet.js security headers
- Express rate limiting
- Environment variable protection
- Input sanitization
- XSS protection
- Secure validation handling

---

# Error Handling Requirements

Gracefully handle:
- Camera permission denied
- No face detected
- Multiple faces detected
- AI model loading failures
- API request failures
- Database connection errors

Display clear and user-friendly error messages throughout the application.

---

# Performance Optimization

Optimize:
- Webcam rendering
- TensorFlow.js inference speed
- API calls
- State management
- Bundle size
- Lazy loading
- Unnecessary re-renders

Ensure the application remains smooth on desktop, tablet, and mobile devices.

---

# Accessibility Requirements

Ensure:
- Mobile responsiveness
- Tablet responsiveness
- Semantic HTML structure
- Keyboard accessibility
- ARIA labels
- Accessible color contrast

---

# Project Structure Requirements

Generate:
- Complete folder structure
- Frontend source code
- Backend source code
- API routes
- MongoDB models
- React components
- Custom hooks
- Utility functions
- Middleware
- Environment variable configuration
- README documentation

---

# Documentation Requirements

Provide:
- Setup instructions
- Installation guide
- Environment variable configuration
- MongoDB Atlas setup
- Development workflow
- Deployment instructions

---

# Output Requirements

The final project should include:

- Real-time facial emotion detection
- Live confidence tracking
- Modern futuristic UI/UX
- Smooth animations and transitions
- Secure backend architecture
- MongoDB session storage
- Emotion analytics dashboard
- Responsive layouts
- Optimized AI performance
- Production-ready scalable architecture

The finished application should feel like a polished modern AI platform with immersive design, real-time AI interaction, and clean user experience.
