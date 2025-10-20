import React, { useState, useEffect } from 'react';
import './App.css';
import * as api from './api';

function App() {
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState('all'); // all, high, medium, low
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [showCreateTask, setShowCreateTask] = useState(false);
  const [healthStatus, setHealthStatus] = useState(null);

  // Form states
  const [newUser, setNewUser] = useState({ email: '', username: '', password: '' });
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'medium' });

  // Load initial data
  useEffect(() => {
    loadData();
    checkHealth();
  }, []);

  // Reload tasks when user or filter changes
  useEffect(() => {
    loadTasks();
    loadStats();
  }, [selectedUser, filter]);

  const checkHealth = async () => {
    try {
      const health = (await api.healthCheck()).data;
      setHealthStatus(health);
    } catch (error) {
      setHealthStatus({ status: 'error', environment: 'unknown' });
    }
  };

  const loadData = async () => {
    try {
      const usersData = (await api.getUsers()).data;
      setUsers(usersData);
      if (usersData.length > 0 && !selectedUser) {
        setSelectedUser(usersData[0]);
      }
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const loadTasks = async () => {
    try {
      let tasksData;
      if (filter !== 'all') {
        tasksData = (await api.getTasksByPriority(filter, selectedUser?.id)).data;
      } else {
        tasksData = (await api.getTasks(selectedUser?.id)).data;
      }
      setTasks(tasksData);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = (await api.getCompletedStats(selectedUser?.id)).data;
      setStats(statsData);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await api.createUser(newUser);
      setNewUser({ email: '', username: '', password: '' });
      setShowCreateUser(false);
      loadData();
    } catch (error) {
      alert('Error creating user: ' + error.response?.data?.detail);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!selectedUser) {
      alert('Please select a user first');
      return;
    }
    try {
      await api.createTask(selectedUser.id, newTask);
      setNewTask({ title: '', description: '', priority: 'medium' });
      setShowCreateTask(false);
      loadTasks();
    } catch (error) {
      alert('Error creating task: ' + error.message);
    }
  };

  const handleToggleComplete = async (task) => {
    try {
      await api.updateTask(task.id, { completed: !task.completed });
      loadTasks();
      loadStats();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Delete this task?')) {
      try {
        await api.deleteTask(taskId);
        loadTasks();
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const handlePriorityChange = async (task, newPriority) => {
    try {
      await api.updateTask(task.id, { priority: newPriority });
      loadTasks();
    } catch (error) {
      console.error('Error updating priority:', error);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const completedTasks = tasks.filter(t => t.completed).length;
  const pendingTasks = tasks.filter(t => !t.completed).length;

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div>
            <h1>📝 Task Management Dashboard</h1>
          </div>
          <div className="health-status">
            {healthStatus && (
              <span className={`health-badge ${healthStatus.status === 'healthy' ? 'healthy' : 'error'}`}>
                {healthStatus.status === 'healthy' ? '✓' : '✗'} {healthStatus.environment}
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-section">
            <div className="sidebar-header">
              <h3>Users</h3>
              <button className="btn-icon" onClick={() => setShowCreateUser(true)}>+</button>
            </div>
            <div className="user-list">
              {users.map(user => (
                <div
                  key={user.id}
                  className={`user-item ${selectedUser?.id === user.id ? 'active' : ''}`}
                  onClick={() => setSelectedUser(user)}
                >
                  <div className="user-avatar">{user.username[0].toUpperCase()}</div>
                  <div className="user-info">
                    <div className="user-name">{user.username}</div>
                    <div className="user-email">{user.email}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          {stats && (
            <div className="sidebar-section stats-section">
              <h3>Statistics</h3>
              <div className="stat-item">
                <span className="stat-label">Total Tasks</span>
                <span className="stat-value">{tasks.length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Completed</span>
                <span className="stat-value success">{completedTasks}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Pending</span>
                <span className="stat-value warning">{pendingTasks}</span>
              </div>
            </div>
          )}
        </aside>

        {/* Tasks Area */}
        <main className="tasks-area">
          {/* Toolbar */}
          <div className="toolbar">
            <div className="toolbar-left">
              <h2>{selectedUser ? `${selectedUser.username}'s Tasks` : 'All Tasks'}</h2>
              <div className="filter-buttons">
                <button 
                  className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                  onClick={() => setFilter('all')}
                >
                  All
                </button>
                <button 
                  className={`filter-btn high ${filter === 'high' ? 'active' : ''}`}
                  onClick={() => setFilter('high')}
                >
                  High
                </button>
                <button 
                  className={`filter-btn medium ${filter === 'medium' ? 'active' : ''}`}
                  onClick={() => setFilter('medium')}
                >
                  Medium
                </button>
                <button 
                  className={`filter-btn low ${filter === 'low' ? 'active' : ''}`}
                  onClick={() => setFilter('low')}
                >
                  Low
                </button>
              </div>
            </div>
            <button className="btn-primary" onClick={() => setShowCreateTask(true)}>
              + New Task
            </button>
          </div>

          {/* Tasks Grid */}
          <div className="tasks-grid">
            {tasks.length === 0 ? (
              <div className="empty-state">
                <p>No tasks yet. Create your first task!</p>
              </div>
            ) : (
              tasks.map(task => (
                <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                  <div className="task-header">
                    <div 
                      className="priority-indicator" 
                      style={{ backgroundColor: getPriorityColor(task.priority) }}
                      title={`Priority: ${task.priority}`}
                    />
                    <select
                      className="priority-select"
                      value={task.priority}
                      onChange={(e) => handlePriorityChange(task, e.target.value)}
                    >
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>
                    <button 
                      className="btn-icon delete"
                      onClick={() => handleDeleteTask(task.id)}
                    >
                      ×
                    </button>
                  </div>
                  <div className="task-body">
                    <h4 className="task-title">{task.title}</h4>
                    {task.description && (
                      <p className="task-description">{task.description}</p>
                    )}
                  </div>
                  <div className="task-footer">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggleComplete(task)}
                      />
                      <span>{task.completed ? 'Completed' : 'Mark complete'}</span>
                    </label>
                    <span className="task-date">
                      {new Date(task.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </main>
      </div>

      {/* Create User Modal */}
      {showCreateUser && (
        <div className="modal-overlay" onClick={() => setShowCreateUser(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Create New User</h3>
            <form onSubmit={handleCreateUser}>
              <input
                type="email"
                placeholder="Email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
              />
              <input
                type="text"
                placeholder="Username"
                value={newUser.username}
                onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={newUser.password}
                onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                required
              />
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowCreateUser(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Create User</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Task Modal */}
      {showCreateTask && (
        <div className="modal-overlay" onClick={() => setShowCreateTask(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Create New Task</h3>
            <form onSubmit={handleCreateTask}>
              <input
                type="text"
                placeholder="Task title"
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                required
              />
              <textarea
                placeholder="Description (optional)"
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                rows="3"
              />
              <select
                value={newTask.priority}
                onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowCreateTask(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">Create Task</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

