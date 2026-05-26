Prompt
Context and Role

As a Senior Full Stack AI/ML Developer specializing in modern AI-powered web applications, real-time computer vision systems, and scalable full-stack architectures, you are responsible for designing and implementing a complete production-ready AI emotion detection platform called Mood Analysis.

The platform must detect human facial emotions in real-time using the user’s webcam and display live emotion predictions with confidence percentages.

The application should feature a futuristic UI, smooth animations, responsive layouts, secure backend architecture, optimized AI inference, and production-level project structure.

Objective

Develop a complete full-stack AI-powered emotion detection web application that:

Detects facial emotions in real-time using webcam input
Displays live emotion predictions with confidence percentages
Stores emotion analysis sessions securely in MongoDB
Provides analytics dashboards and session summaries
Implements a modern futuristic UI with immersive animations
Maintains high performance, responsiveness, accessibility, and scalability
Technology Stack
Frontend
Next.js
TypeScript
Tailwind CSS
Framer Motion
React Webcam
Axios
Recharts
Backend
Node.js
Express.js
MongoDB Atlas
Mongoose
Helmet.js
express-rate-limit
dotenv
AI / ML
face-api.js
TensorFlow.js
Core Application Flow

The application should work as follows:

User opens the landing page
User enters their name
User clicks “Start Mood Analysis”
Webcam permission is requested
Camera initializes successfully
Face detection activates
Emotion detection runs continuously in real-time
Predicted emotion appears live
Confidence percentage updates dynamically
Emotion logs are securely stored in MongoDB
User can view emotion history and session summaries
Emotion Detection Requirements

The system must detect the following emotions:

Happy
Sad
Angry
Neutral
Fear
Surprise
Disgust

The AI system should:

Detect faces in real-time
Continuously analyze facial expressions
Handle no-face scenarios gracefully
Handle multiple-face detection scenarios
Optimize inference performance for smooth real-time analysis
Frontend Requirements

Build a premium futuristic interface featuring:

Dark theme
Glassmorphism UI cards
Neon gradients
Animated backgrounds
Floating glow effects
Smooth transitions
Framer Motion animations
Responsive layouts

The UI should feel similar to a modern AI SaaS platform.

Required Pages
1. Landing Page

Include:

Large animated “Mood Analysis” title
Subtitle and description
Animated futuristic background
Call-to-action start button
Smooth scroll and entrance animations
2. Analysis Page

Include:

Live webcam feed
Real-time face detection
Live emotion predictions
Confidence percentage indicators
Animated emotion cards
Detection status indicators
User-friendly error messages
3. Dashboard Page

Include:

Current detected emotion
Emotion history timeline
Confidence charts using Recharts
Session analytics and statistics
Recent session summaries
Animation and UI Requirements

Use Framer Motion to implement:

Smooth page transitions
Scroll-triggered animations
Fade-ins and staggered reveals
Hover interactions
Floating animated elements
Dynamic motion transitions

Animations must:

Be performant
Use GPU-friendly properties
Avoid layout thrashing
Maintain smooth rendering during webcam analysis
Backend Requirements

Create secure REST APIs using Express.js.

Required APIs
Start session API
Save emotion data API
Get emotion history API
Download session report API
Backend Features

Implement:

Proper MVC architecture
Secure API responses
Input validation
Error handling middleware
Rate limiting
Environment variable management
API sanitization and security protections
Database Requirements

Store:

Username
Detected emotion
Confidence percentage
Timestamp
Session duration

MongoDB Atlas should be used for persistent storage.

Security Requirements

Implement:

Helmet.js security headers
Express rate limiting
Environment variable protection
Input sanitization
XSS protection
Secure API validation
Error Handling Requirements

Gracefully handle:

Camera permission denied
No face detected
Multiple faces detected
AI model loading failures
API request failures
Database connection errors

Display animated and user-friendly error messages.

Performance Optimization

Optimize:

Webcam rendering performance
TensorFlow.js inference speed
API requests
State management
Bundle size
Lazy loading
Re-render prevention

Ensure the application performs efficiently on desktop and mobile devices.

Accessibility Requirements

Ensure:

Mobile responsiveness
Tablet responsiveness
Semantic HTML
Keyboard accessibility
ARIA labels
Accessible color contrast
Project Structure Requirements

Generate:

Complete folder structure
Frontend implementation
Backend implementation
API routes
MongoDB models
React components
Custom hooks
Utility functions
Middleware
Environment configuration
README documentation
Documentation Requirements

Provide:

Setup instructions
Installation steps
Environment variable configuration
MongoDB Atlas setup
Development workflow
Production deployment steps
Output Requirements

The final project should include:

A fully functional AI emotion detection platform
Real-time webcam-based emotion analysis
Beautiful futuristic UI/UX
Smooth animations and transitions
Secure backend architecture
MongoDB session storage
Emotion analytics dashboard
Production-ready scalable architecture

The final result should resemble a modern AI SaaS product with immersive UI, real-time AI analysis, optimized performance, and enterprise-level code quality.
