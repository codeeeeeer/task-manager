# Project Context

## Purpose
任务分发工具 (Task Manager) - A lightweight task distribution and tracking system designed for team collaboration with real-time notifications and comprehensive task management capabilities.

Core features:
- Task creation, transfer, and status tracking
- Real-time notifications and comments
- Task categorization (版本任务, 紧急任务, 普通任务, 定时周期任务, 其他任务)
- Progress tracking (task progress and time-based progress)
- File attachments and rich text descriptions
- User management with role-based access
- Chrome browser extension for quick access and notifications

## Tech Stack

### Backend
- **Framework**: Flask 2.3.3 with Python 3
- **Database**: SQLite3 (development), PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0.20 with Flask-SQLAlchemy 3.0.5
- **Real-time**: Flask-SocketIO 5.3.4 with Eventlet 0.33.3
- **Authentication**: Flask-JWT-Extended 4.5.2 (24-hour token expiry)
- **Scheduled Tasks**: APScheduler 3.10.4
- **Migrations**: Flask-Migrate 4.0.5 (Alembic)
- **Security**: Bcrypt 4.0.1, Bleach 6.0.0
- **Data Processing**: Pandas 2.1.0, NumPy 1.24.3, OpenPyXL 3.1.2

### Frontend
- **Framework**: Vue 3.3.4 with Composition API
- **Build Tool**: Vite 4.4.9
- **UI Library**: Element Plus 2.3.14
- **State Management**: Pinia 2.1.6
- **Real-time Client**: Socket.IO Client 4.7.2
- **Routing**: Vue Router 4.2.4
- **HTTP Client**: Axios 1.5.0
- **Rich Text**: WangEditor 5.1.23, Vue Quill 1.2.0
- **Date Utility**: Day.js 1.11.9
- **Styling**: Sass 1.66.1

### Client
- Chrome Extension (JavaScript-based)

## Project Conventions

### Code Style
- **Backend**: Chinese docstrings and comments (e.g., `"""任务模型"""`), snake_case for variables/functions
- **Frontend**: Chinese UI text and comments, camelCase for JavaScript variables, kebab-case for component files
- **Naming**: Descriptive Chinese comments for business logic, English for technical code
- **Indentation**: 4 spaces for Python, 2 spaces for JavaScript/Vue
- **String Quotes**: Single quotes preferred in Python and JavaScript

### Architecture Patterns
- **Backend**: Layered architecture with separation of concerns
  - `api/` - Blueprint routes and request handling
  - `models/` - SQLAlchemy ORM models with BaseModel inheritance
  - `services/` - Business logic layer
  - `utils/` - Shared utility functions
- **Frontend**: Component-based architecture
  - `views/` - Page-level components
  - `components/` - Reusable UI components
  - `api/` - API client functions
  - `store/` - Pinia state management
- **Real-time Communication**: WebSocket via SocketIO for live updates
- **API Design**: RESTful endpoints with standardized JSON responses
- **Database**: Foreign key relationships with cascade delete, check constraints for data validation

### Testing Strategy
- Currently no automated test suite
- Manual testing for features
- Future: Consider adding pytest for backend, Vitest for frontend

### Git Workflow
- **Main Branch**: `main`
- **Commit Messages**: Chinese descriptive messages focusing on the change
  - Examples: "添加高科技风格", "修复后端接口响应超时的问题", "优化客户端插件的响应功能"
- **Commit Style**: Descriptive, action-oriented (添加/修复/优化 + specific change)

## Domain Context
- **Task Statuses**: 新建 → 待响应 → 处理中 → 挂起/已完成/关闭
- **Task Categories**: 版本任务, 紧急任务, 普通任务, 定时周期任务, 其他任务
- **Progress Tracking**:
  - Task progress (0-100%): Manual progress updates
  - Time progress (0-100%): Calculated based on expected_start_time and expected_end_time
- **User Roles**: Users can be task creators or handlers
- **Task Transfer**: Tasks can be transferred between users with history tracking
- **Timezone**: Asia/Shanghai (UTC+8)

## Important Constraints
- **File Upload Limit**: 16MB maximum
- **Allowed File Types**: PNG, JPG, JPEG, GIF, PDF, DOC, DOCX, XLS, XLSX
- **JWT Token Expiry**: 24 hours
- **CORS**: Enabled for all origins (configure for production)
- **Database Constraints**:
  - Progress values must be 0-100
  - Task categories must match predefined list
- **Real-time**: WebSocket connections require proper proxy configuration in production

## External Dependencies
- **Production Deployment**:
  - Nginx for static file serving and API proxy
  - Gunicorn + Eventlet for WSGI server
  - PostgreSQL for production database
  - Optional: Redis for SocketIO message queue in multi-process setup
- **Browser Extension**: Chrome Web Store for distribution
- **No External APIs**: Self-contained system with no third-party API dependencies
