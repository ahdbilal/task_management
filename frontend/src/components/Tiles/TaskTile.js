import React, { useState } from 'react';
import './TaskTile.css';

const TaskTile = ({ task, onToggleComplete, onDelete, onEdit, variant = 'default' }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const getPriorityColor = (priority) => {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#10b981'
    };
    return colors[priority] || '#6b7280';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'No due date';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return `Overdue by ${Math.abs(diffDays)} days`;
    if (diffDays === 0) return 'Due today';
    if (diffDays === 1) return 'Due tomorrow';
    if (diffDays <= 7) return `Due in ${diffDays} days`;

    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const isOverdue = (dateString) => {
    if (!dateString) return false;
    return new Date(dateString) < new Date();
  };

  if (variant === 'compact') {
    return (
      <div
        className={`task-tile task-tile-compact ${task.completed ? 'completed' : ''} ${isOverdue(task.due_date) && !task.completed ? 'overdue' : ''}`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <div className="task-tile-compact-content">
          <button
            className="task-checkbox"
            onClick={() => onToggleComplete(task.id)}
            title={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.completed && (
              <svg className="checkmark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          <div className="task-tile-info">
            <h3 className="task-tile-title">{task.title}</h3>
            <div className="task-tile-meta">
              <span
                className="task-priority-badge"
                style={{ backgroundColor: getPriorityColor(task.priority) }}
              >
                {task.priority}
              </span>
              <span className="task-due-date">
                {formatDate(task.due_date)}
              </span>
            </div>
          </div>

          <div className={`task-tile-actions ${isHovered ? 'visible' : ''}`}>
            <button
              className="task-action-btn edit"
              onClick={() => onEdit(task)}
              title="Edit task"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              className="task-action-btn delete"
              onClick={() => onDelete(task.id)}
              title="Delete task"
            >
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`task-tile task-tile-card ${task.completed ? 'completed' : ''} ${isOverdue(task.due_date) && !task.completed ? 'overdue' : ''} ${isExpanded ? 'expanded' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="task-tile-header">
        <div className="task-tile-header-left">
          <button
            className="task-checkbox"
            onClick={() => onToggleComplete(task.id)}
            title={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.completed && (
              <svg className="checkmark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          <span
            className="task-priority-indicator"
            style={{ backgroundColor: getPriorityColor(task.priority) }}
            title={`${task.priority} priority`}
          ></span>
        </div>
        <div className={`task-tile-actions ${isHovered ? 'visible' : ''}`}>
          <button
            className="task-action-btn edit"
            onClick={() => onEdit(task)}
            title="Edit task"
          >
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            className="task-action-btn delete"
            onClick={() => onDelete(task.id)}
            title="Delete task"
          >
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <div className="task-tile-body">
        <h3 className="task-tile-title">{task.title}</h3>

        {task.description && (
          <div className="task-tile-description">
            <p className={isExpanded ? 'expanded' : 'truncated'}>
              {task.description}
            </p>
            {task.description.length > 100 && (
              <button
                className="task-expand-btn"
                onClick={() => setIsExpanded(!isExpanded)}
              >
                {isExpanded ? 'Show less' : 'Show more'}
              </button>
            )}
          </div>
        )}

        <div className="task-tile-footer">
          <div className="task-tile-meta">
            <div className="task-meta-item">
              <svg className="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <span
                className="task-priority-badge"
                style={{
                  backgroundColor: getPriorityColor(task.priority),
                  color: 'white'
                }}
              >
                {task.priority}
              </span>
            </div>

            <div className="task-meta-item">
              <svg className="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span className={`task-due-date ${isOverdue(task.due_date) && !task.completed ? 'overdue-text' : ''}`}>
                {formatDate(task.due_date)}
              </span>
            </div>
          </div>

          {task.completed && (
            <div className="task-completed-badge">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Completed</span>
            </div>
          )}
        </div>
      </div>

      {isOverdue(task.due_date) && !task.completed && (
        <div className="task-overdue-indicator">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <span>Overdue</span>
        </div>
      )}
    </div>
  );
};

export default TaskTile;
