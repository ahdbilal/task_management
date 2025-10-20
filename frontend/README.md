# Task Management UI - React Dashboard

Professional React dashboard for the Task Management API demo.

## Features

- **User Management**: Create users, switch between users
- **Task Board**: Visual task cards with drag-and-drop feel
- **Priority Management**: High/Medium/Low with color coding
- **Task Operations**: Create, update, complete, delete tasks
- **Filtering**: Filter by priority level
- **Statistics**: Real-time task completion stats
- **Health Monitoring**: API health status indicator
- **Responsive Design**: Works on desktop, tablet, mobile

## Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Start Development Server

```bash
npm start
```

The UI will open at `http://localhost:3000`

**Important**: Make sure the backend API is running on `http://localhost:8000` first!

### Start Backend API

```bash
# In the main workspace directory
python3 main.py
```

## Demo Usage

### 1. Create Users
- Click the "+" button in the sidebar
- Enter email, username, password
- User appears in the sidebar

### 2. Create Tasks
- Select a user from sidebar
- Click "New Task" button
- Fill in title, description, priority
- Task appears in the grid

### 3. Manage Tasks
- Click checkbox to mark complete
- Change priority with dropdown
- Click "×" to delete

### 4. Filter Tasks
- Use High/Medium/Low buttons to filter
- Click "All" to see everything

### 5. View Stats
- See total, completed, pending counts
- Updates in real-time

## Tech Stack

- **React 18**: UI framework
- **Axios**: HTTP client for API calls
- **CSS3**: Custom styling (no frameworks)
- **React Scripts**: Build tooling

## Architecture

```
src/
├── index.js       # Entry point
├── App.js         # Main component
├── App.css        # Styles
├── api.js         # API service layer
└── index.css      # Global styles
```

## API Integration

All API calls are abstracted in `api.js`:

```javascript
// User operations
getUsers()
createUser(userData)
getUser(userId)

// Task operations
getTasks(userId)
createTask(userId, taskData)
updateTask(taskId, taskData)
deleteTask(taskId)
getTasksByPriority(priority, userId)

// Stats
getCompletedStats(userId)
healthCheck()
```

## Color Scheme

- **Primary**: Purple gradient (#667eea → #764ba2)
- **High Priority**: Red (#ef4444)
- **Medium Priority**: Orange (#f59e0b)
- **Low Priority**: Green (#10b981)
- **Success**: Green (#10b981)
- **Background**: Light gray (#f5f5f7)

## Responsive Breakpoints

- **Desktop**: > 1024px
- **Tablet**: 640px - 1024px
- **Mobile**: < 640px

## Production Build

```bash
npm run build
```

Creates optimized build in `build/` directory.

## Demo Scenarios with UI

### Show Task Creation
"Let's create a new task through the UI..."

### Show Priority Management
"Watch as I change the priority and the color updates..."

### Show Real-time Stats
"Notice the stats update automatically when I complete a task..."

### AI Agent Integration
"Now let's ask the AI agent to modify the UI..."

```bash
python3 remote_claude.py ask "add a search box to filter tasks by title"
```

The AI can:
- Add new UI components
- Modify styling
- Add features
- Fix bugs
- Update the design

## UI Screenshots (Conceptual)

**Main Dashboard**:
- Left sidebar: User list + stats
- Main area: Task grid with cards
- Top toolbar: Filters and new task button

**Task Card**:
- Color-coded priority indicator
- Title and description
- Checkbox for completion
- Delete button
- Priority dropdown

**Modals**:
- Create user form
- Create task form
- Clean, centered overlays

---

**Built for**: Admin-Governed Staging Environment Demo
**Purpose**: Visual demonstration of AI-assisted development

