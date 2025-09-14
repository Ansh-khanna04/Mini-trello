
# Mini Trello - Kanban Board Application

A simplified Trello-like Kanban board application built with Flask, featuring real-time collaboration, drag-and-drop functionality, and comprehensive task management.

![Mini Trello Demo](https://img.shields.io/badge/Status-Complete-success)

## 🚀 Features

### Core Functionality
- **User Authentication**: JWT-based authentication with signup/login
- **Kanban Boards**: Create and manage multiple boards with custom backgrounds
- **Lists & Cards**: Organize tasks in customizable lists with drag-and-drop support
- **Real-time Collaboration**: Live updates using WebSockets for multiple users
- **Comments System**: Add comments to cards with timestamps
- **Activity Tracking**: Comprehensive activity log for all board operations
- **Search & Filtering**: Find cards by title, labels, assignees, or due dates
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

### Technical Features
- **RESTful API**: Complete REST API for all operations
- **WebSocket Support**: Real-time updates using Flask-SocketIO
- **Database**: SQLite for development (easily switchable to MySQL/PostgreSQL)
- **Modern Frontend**: Bootstrap 5, SortableJS for drag-and-drop
- **Security**: Password hashing, CORS support, input validation

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SocketIO** - WebSocket support
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-Migrate** - Database migrations
- **SQLite/MySQL** - Database

### Frontend
- **Jinja2** - Template engine
- **Bootstrap 5** - UI framework
- **SortableJS** - Drag and drop functionality
- **Socket.IO** - Real-time communication
- **Vanilla JavaScript** - Frontend logic

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone/Download the project**
   ```bash
   # Navigate to the project directory
   cd mini-trello
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`
   - Use the demo credentials or create a new account

## 🎮 Demo Credentials

**Username:** `demo`  
**Password:** `demo123`

The application includes pre-loaded demo data with a sample board and cards.

## 🏗️ Project Structure

```
mini-trello/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── socket_events.py     # WebSocket event handlers
│   └── routes/
│       ├── auth.py          # Authentication routes
│       ├── api.py           # REST API routes
│       └── main.py          # Main web routes
├── templates/
│   ├── base.html            # Base template
│   ├── auth/                # Authentication templates
│   └── boards/              # Board templates
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── app.js           # Frontend JavaScript
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Default settings are provided in `.env`:

```env
SECRET_KEY=mini-trello-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
DATABASE_URL=sqlite:///mini_trello.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### Database Configuration

**SQLite (Default):**
```env
DATABASE_URL=sqlite:///mini_trello.db
```

**MySQL:**
```env
DATABASE_URL=mysql://username:password@localhost/mini_trello
```

**PostgreSQL:**
```env
DATABASE_URL=postgresql://username:password@localhost/mini_trello
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user info

### Board Management
- `GET /api/boards` - Get user's boards
- `POST /api/boards` - Create new board
- `GET /api/boards/<id>` - Get board with lists and cards
- `PUT /api/boards/<id>` - Update board
- `DELETE /api/boards/<id>` - Delete board

### List Management
- `POST /api/lists` - Create new list
- `PUT /api/lists/<id>` - Update list
- `DELETE /api/lists/<id>` - Delete list

### Card Management
- `POST /api/cards` - Create new card
- `GET /api/cards/<id>` - Get card details
- `PUT /api/cards/<id>` - Update card
- `DELETE /api/cards/<id>` - Delete card

### Comments
- `GET /api/cards/<id>/comments` - Get card comments
- `POST /api/cards/<id>/comments` - Add comment

### Search & Activity
- `GET /api/boards/<id>/search` - Search cards
- `GET /api/boards/<id>/activities` - Get board activities

## 🎯 Usage Guide

### Getting Started
1. **Sign Up/Login**: Create an account or use demo credentials
2. **Create Board**: Click "Create New Board" on the dashboard
3. **Add Lists**: Use "Add List" to create columns (e.g., To Do, In Progress, Done)
4. **Add Cards**: Click "Add a card" in any list to create tasks
5. **Drag & Drop**: Move cards between lists by dragging
6. **Card Details**: Click on cards to view/edit details and add comments

### Board Management
- **Create Board**: Choose title, description, visibility, and background color
- **Board Members**: Invite users to collaborate (owner permissions)
- **Activity Sidebar**: View real-time activity log
- **Search**: Find cards quickly using the search function

### Real-time Features
- Live card movements
- Instant comment updates
- Activity notifications
- Multi-user collaboration

## 🔒 Security Features

- **Password Hashing**: Secure password storage using bcrypt
- **JWT Authentication**: Stateless authentication tokens
- **Input Validation**: Server-side validation for all inputs
- **XSS Protection**: HTML escaping and content security
- **CORS Configuration**: Controlled cross-origin requests

## 🚀 Deployment

### Production Setup

1. **Update Environment Variables**
   ```env
   SECRET_KEY=your-super-secret-production-key
   JWT_SECRET_KEY=your-jwt-production-key
   DATABASE_URL=postgresql://user:pass@localhost/mini_trello
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

2. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn -k eventlet -w 1 --bind 0.0.0.0:8000 app:app
   ```

3. **Database Migration**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## 🤝 Contributing

This is a demonstration project showcasing full-stack development skills. Feel free to fork and enhance with additional features:

- Email notifications
- File attachments
- Labels and due dates
- Team workspaces
- Advanced permissions
- Mobile app
- Third-party integrations

## 📝 License

This project is created for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Flask Team** - Excellent web framework
- **Bootstrap Team** - Beautiful UI components
- **SortableJS** - Smooth drag-and-drop functionality
- **Socket.IO** - Real-time communication

---


*Demonstrating full-stack development skills with modern web technologies*

