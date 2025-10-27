import React, { useState, useEffect } from 'react';
import TaskTile from '../Tiles/TaskTile';
import './Dashboard.css';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [filterPriority, setFilterPriority] = useState('all');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });
  const [isLoading, setIsLoading] = useState(true);

  // API base URL
  const API_BASE = 'http://localhost:8000/api';

  // Fetch users on mount
  useEffect(() => {
    fetchUsers();
  }, []);

  // Fetch tasks when user is selected
  useEffect(() => {
    if (selectedUser) {
      fetchTasks();
    }
  }, [selectedUser, filterPriority]);

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE}/users/`);
      const data = await response.json();
      setUsers(data);
      if (data.length > 0) {
        setSelectedUser(data[0].id);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchTasks = async () => {
    setIsLoading(true);
    try {
      let url = `${API_BASE}/tasks/`;

      if (filterPriority !== 'all') {
        url = `${API_BASE}/tasks/priority/${filterPriority}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      // Filter tasks by selected user
      const userTasks = data.filter(task => task.owner_id === selectedUser);
      setTasks(userTasks);

      // Calculate stats
      const completed = userTasks.filter(task => task.completed).length;
      setStats({
        total: userTasks.length,
        completed: completed,
        pending: userTasks.length - completed
      });
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleComplete = async (taskId) => {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    try {
      await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed })
      });

      // Update local state
      setTasks(tasks.map(t =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      ));
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;

    try {
      await fetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'DELETE'
      });

      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleEditTask = (task) => {
    // Placeholder for edit functionality
    console.log('Edit task:', task);
    alert('Edit functionality coming soon!');
  };

  const getFilteredTasks = () => {
    return tasks;
  };

  return (
    <div className="dashboard-v2">
      {/* Header */}
      <header className="dashboard-header">
        <div className="dashboard-title-section">
          <h1 className="dashboard-title">Task Management Dashboard v2</h1>
          <span className="dashboard-subtitle">
            Organize, track, and complete your tasks efficiently
          </span>
        </div>

        <div className="dashboard-header-actions">
          <div className="view-toggle">
            <button
              className={`view-toggle-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
              title="Grid view"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
            <button
              className={`view-toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
              title="List view"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="dashboard-stats-bar">
        <div className="stat-card stat-total">
          <div className="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Total Tasks</span>
          </div>
        </div>

        <div className="stat-card stat-completed">
          <div className="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.completed}</span>
            <span className="stat-label">Completed</span>
          </div>
        </div>

        <div className="stat-card stat-pending">
          <div className="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="stat-content">
            <span className="stat-value">{stats.pending}</span>
            <span className="stat-label">Pending</span>
          </div>
        </div>

        <div className="stat-card stat-progress">
          <div className="stat-content">
            <span className="stat-value">
              {stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0}%
            </span>
            <span className="stat-label">Progress</span>
          </div>
          <div className="progress-bar-container">
            <div
              className="progress-bar-fill"
              style={{
                width: `${stats.total > 0 ? (stats.completed / stats.total) * 100 : 0}%`
              }}
            ></div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="dashboard-main">
        {/* Sidebar */}
        <aside className="dashboard-sidebar">
          <div className="sidebar-section">
            <h3 className="sidebar-title">Users</h3>
            <div className="user-list">
              {users.map(user => (
                <button
                  key={user.id}
                  className={`user-item ${selectedUser === user.id ? 'active' : ''}`}
                  onClick={() => setSelectedUser(user.id)}
                >
                  <div className="user-avatar">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <div className="user-info">
                    <span className="user-name">{user.username}</span>
                    <span className="user-email">{user.email}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="sidebar-section">
            <h3 className="sidebar-title">Filter by Priority</h3>
            <div className="filter-buttons">
              <button
                className={`filter-btn ${filterPriority === 'all' ? 'active' : ''}`}
                onClick={() => setFilterPriority('all')}
              >
                All
              </button>
              <button
                className={`filter-btn filter-high ${filterPriority === 'high' ? 'active' : ''}`}
                onClick={() => setFilterPriority('high')}
              >
                High
              </button>
              <button
                className={`filter-btn filter-medium ${filterPriority === 'medium' ? 'active' : ''}`}
                onClick={() => setFilterPriority('medium')}
              >
                Medium
              </button>
              <button
                className={`filter-btn filter-low ${filterPriority === 'low' ? 'active' : ''}`}
                onClick={() => setFilterPriority('low')}
              >
                Low
              </button>
            </div>
          </div>
        </aside>

        {/* Tasks Area */}
        <main className="dashboard-content">
          {isLoading ? (
            <div className="loading-state">
              <div className="loader"></div>
              <p>Loading tasks...</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="empty-state">
              <svg className="empty-state-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              <h3>No tasks found</h3>
              <p>Create your first task to get started!</p>
            </div>
          ) : (
            <div className={`tasks-container tasks-${viewMode}`}>
              {getFilteredTasks().map(task => (
                <TaskTile
                  key={task.id}
                  task={task}
                  onToggleComplete={handleToggleComplete}
                  onDelete={handleDeleteTask}
                  onEdit={handleEditTask}
                  variant={viewMode === 'list' ? 'compact' : 'default'}
                />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
