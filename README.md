# Mini Trello

A real-time Kanban board application built with Flask and Socket.IO, featuring drag-and-drop functionality, collaborative editing, and comprehensive project management tools.

## Tech Stack & Rationale

This application is built using Flask as the web framework due to its simplicity and flexibility for rapid development. Flask-SocketIO enables real-time collaboration features, allowing multiple users to see changes instantly without page refreshes. The frontend uses vanilla JavaScript with SortableJS for drag-and-drop functionality, Bootstrap for responsive UI components, and Socket.IO client for real-time communication. This tech stack was chosen to minimize complexity while providing a rich, interactive user experience.

The database layer uses SQLAlchemy ORM with SQLite for development (easily configurable for PostgreSQL/MySQL in production), providing a robust data persistence layer with relationship management. Flask-JWT-Extended handles authentication with session-based fallback, while Flask-CORS enables cross-origin requests for API endpoints. The modular blueprint architecture ensures clean separation of concerns and easy maintainability.

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Backend Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mini-trello
```

2. **Create virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration:**
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration (see Environment Variables section below).

### Database Migration & Seed

1. **Initialize database:**
```bash
python app.py
```
The application automatically creates database tables and seeds demo data on first run.

2. **For production, use Flask-Migrate:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Frontend Setup

The frontend uses CDN-hosted libraries, so no additional setup is required. All static assets (CSS, JavaScript) are included in the `static/` directory:

- **CSS:** `static/css/style.css`
- **JavaScript:** `static/js/app.js`, `static/js/member-management.js`
- **Templates:** Located in `templates/` directory

### Running the Application

**Development Server:**
```bash
python app.py
```

**Production Server:**
```bash
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

The application will be available at:
- Local: `http://localhost:5000`
- Network: `http://0.0.0.0:5000`

**Demo Credentials:**
- Username: `demo`
- Password: `demo123`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Application Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///mini_trello.db
# For PostgreSQL: postgresql://username:password@localhost:5432/mini_trello
# For MySQL: mysql://username:password@localhost:3306/mini_trello

# Optional Production Settings
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Database Schema Overview

The application uses a relational database with the following key entities:

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│    User     │    │  Workspace   │    │    Board    │
├─────────────┤    ├──────────────┤    ├─────────────┤
│ id          │◄──►│ id           │◄──►│ id          │
│ username    │    │ name         │    │ title       │
│ email       │    │ description  │    │ description │
│ password_hash│   │ owner_id     │    │ owner_id    │
│ name        │    │ created_at   │    │ workspace_id│
│ avatar      │    └──────────────┘    │ visibility  │
│ created_at  │                        │ bg_color    │
└─────────────┘                        │ created_at  │
                                       └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│    List     │    │    Card      │    │   Comment   │
├─────────────┤    ├──────────────┤    ├─────────────┤
│ id          │◄──►│ id           │◄──►│ id          │
│ title       │    │ title        │    │ text        │
│ position    │    │ description  │    │ card_id     │
│ board_id    │    │ labels       │    │ author_id   │
│ created_at  │    │ due_date     │    │ created_at  │
└─────────────┘    │ position     │    │ updated_at  │
                   │ list_id      │    └─────────────┘
                   │ created_at   │
                   │ updated_at   │
                   └──────────────┘

Association Tables:
• board_members (user_id, board_id)
• card_assignees (user_id, card_id)
• workspace_members (user_id, workspace_id)

Additional Tables:
• ActivityLog (id, action, entity_type, entity_id, user_id, board_id, details, created_at)
```

### Key Tables/Collections

**Users Table:**
- Stores user authentication and profile information
- Relationships: owns workspaces/boards, member of boards/workspaces, assigned to cards

**Boards Table:**
- Main project containers with members, lists, and activities
- Supports visibility settings (private, workspace, public)
- Tracks ownership and membership through association tables

**Lists Table:**
- Columns within boards, ordered by position for drag-and-drop
- Contains multiple cards in ordered sequence

**Cards Table:**
- Individual tasks with title, description, labels, due dates
- Support for multiple assignees and position-based ordering
- JSON-stored labels for flexible categorization

**Comments Table:**
- Card-specific discussions with author tracking
- Supports real-time collaborative communication

**ActivityLog Table:**
- Comprehensive audit trail of all board activities
- Tracks actions across all entity types for activity feeds

## Real-time Server

The application includes integrated real-time functionality using Flask-SocketIO. No separate server is required.

**Real-time Features:**
- Instant card creation, updates, and deletion
- Live list reordering and management
- Real-time member collaboration indicators
- Activity feed updates
- Comment synchronization

**Socket.IO Events:**
- `join_board`: User joins board room for updates
- `card_created/updated/deleted`: Card lifecycle events
- `list_created/updated/deleted`: List management events
- `member_added/removed`: Board membership changes
- `comment_created`: New comment notifications
- `card_drag_start/end`: Collaborative drag indicators

**Connection Configuration:**
The Socket.IO server is automatically started with the Flask application. For production deployments, ensure proper WebSocket support in your web server configuration.

## Features

**Core Functionality:**
- User authentication and authorization
- Workspace and board management
- Drag-and-drop list and card reordering
- Card labels, due dates, and assignees
- Real-time collaborative editing
- Comment system with threading
- Activity tracking and audit logs
- Advanced search and filtering
- Member management and permissions
- Responsive design for mobile/desktop

**Technical Features:**
- RESTful API architecture
- WebSocket real-time communication
- Session-based and JWT authentication
- Database migrations with Flask-Migrate
- Comprehensive error handling and logging
- CORS support for API access
- Modular blueprint architecture

## Project Structure

```
mini-trello/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── socket_events.py     # Socket.IO event handlers
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── api.py           # API endpoints
│       └── main.py          # Main web routes
├── static/
│   ├── css/
│   │   └── style.css        # Application styles
│   └── js/
│       ├── app.js           # Main JavaScript
│       └── member-management.js
├── templates/
│   ├── base.html            # Base template
│   ├── auth/                # Authentication templates
│   └── boards/              # Board-related templates
├── app.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## API Documentation

The application provides RESTful API endpoints for all major operations:

**Authentication:**
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

**Boards:**
- `GET /api/boards` - List user boards
- `POST /api/boards` - Create new board
- `GET /api/boards/{id}` - Get board details
- `PUT /api/boards/{id}` - Update board
- `DELETE /api/boards/{id}` - Delete board

**Lists:**
- `POST /api/lists` - Create new list
- `PUT /api/lists/{id}` - Update list
- `DELETE /api/lists/{id}` - Delete list

**Cards:**
- `POST /api/cards` - Create new card
- `GET /api/cards/{id}` - Get card details
- `PUT /api/cards/{id}` - Update card
- `DELETE /api/cards/{id}` - Delete card

**Additional endpoints for comments, member management, search, and activities are available. See `app/routes/api.py` for complete API documentation.**

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

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
