# Mergington High School Activities

A comprehensive web application that allows teachers to manage student enrollment in extracurricular activities at Mergington High School.

## Features

### For Students and Visitors
- **Browse Activities**: View all available extracurricular activities with detailed information
- **Advanced Filtering**: Filter activities by:
  - Category (Sports, Arts, Academic, Community, Technology)
  - Day of the week (Monday through Sunday, including weekends)
  - Time of day (Morning, Afternoon, Weekend)
- **Search Functionality**: Search activities by name, description, or schedule
- **Activity Details**: View comprehensive information including:
  - Activity description and schedule
  - Current participant count and maximum capacity
  - Meeting days and times

### For Teachers (Authenticated Users)
- **Secure Login**: Teacher authentication system with username/password
- **Student Management**: 
  - Register students for activities
  - Remove students from activities
  - View current enrollment for each activity
- **Session Management**: Automatic session validation and logout functionality

### Technical Features
- **Real-time Updates**: Dynamic loading and filtering without page refreshes
- **Responsive Design**: Mobile-friendly interface with modern styling
- **MongoDB Backend**: Persistent data storage with sample activities and teacher accounts
- **RESTful API**: Clean API endpoints for all functionality

## Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python with FastAPI framework
- **Database**: MongoDB with PyMongo driver
- **Authentication**: SHA-256 password hashing with Argon2 support
- **Server**: Uvicorn ASGI server

## Sample Activities

The system comes pre-loaded with diverse activities including:
- **Academic**: Chess Club, Math Club, Programming Class, Debate Team
- **Sports**: Soccer Team, Basketball Team, Morning Fitness
- **Arts**: Art Club, Drama Club
- **STEM**: Weekend Robotics Workshop, Science Olympiad
- **Weekend Programs**: Sunday Chess Tournament, Science Olympiad

## API Endpoints

### Activities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activities` | Get all activities with optional filtering by day and time |
| GET | `/activities/days` | Get list of all days that have activities scheduled |
| POST | `/activities/{activity_name}/signup?email={email}&teacher_username={username}` | Register a student for an activity (requires teacher authentication) |
| POST | `/activities/{activity_name}/unregister?email={email}&teacher_username={username}` | Remove a student from an activity (requires teacher authentication) |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login?username={username}&password={password}` | Teacher login authentication |
| GET | `/auth/check-session?username={username}` | Validate existing session |

### Sample Teacher Accounts
- **Username**: `mrodriguez`, **Password**: `art123` (Ms. Rodriguez - Teacher)
- **Username**: `mchen`, **Password**: `chess456` (Mr. Chen - Teacher)  
- **Username**: `principal`, **Password**: `admin789` (Principal Martinez - Admin)

> [!IMPORTANT]
> All activity registration and management requires teacher authentication. Students cannot self-register.

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
