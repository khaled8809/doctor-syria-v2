export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high';
  assignedTo?: string;
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  category?: 'medical' | 'administrative' | 'emergency' | 'follow_up';
  estimatedDuration?: number;
  actualDuration?: number;
  location?: string;
  department?: string;
  patientId?: string;
  tags?: string[];
  attachments?: string[];
  notes?: string[];
  subtasks?: SubTask[];
  dependencies?: string[];
  watchers?: string[];
  recurrence?: TaskRecurrence;
}

export interface SubTask {
  id: string;
  title: string;
  completed: boolean;
  assignedTo?: string;
  dueDate?: string;
}

export interface TaskRecurrence {
  type: 'daily' | 'weekly' | 'monthly' | 'custom';
  interval: number;
  endDate?: string;
  daysOfWeek?: number[];
  daysOfMonth?: number[];
}

export interface TaskManagementProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updates: Partial<Task>) => void;
  onTaskDelete?: (taskId: string) => void;
  onTaskCreate?: (task: Omit<Task, 'id'>) => void;
  onSubtaskUpdate?: (taskId: string, subtaskId: string, completed: boolean) => void;
  onTagsUpdate?: (taskId: string, tags: string[]) => void;
  onWatchersUpdate?: (taskId: string, watchers: string[]) => void;
}

export interface TaskFilter {
  status?: ('pending' | 'in_progress' | 'completed' | 'cancelled')[];
  priority?: ('low' | 'medium' | 'high')[];
  assignedTo?: string[];
  category?: string[];
  department?: string[];
  dueDate?: {
    start?: string;
    end?: string;
  };
  tags?: string[];
  search?: string;
}

export interface TaskStats {
  total: number;
  completed: number;
  inProgress: number;
  pending: number;
  overdue: number;
  completionRate: number;
  averageDuration: number;
  byPriority: {
    high: number;
    medium: number;
    low: number;
  };
  byCategory: {
    [key: string]: number;
  };
  byDepartment: {
    [key: string]: number;
  };
}

export interface TaskNotification {
  id: string;
  taskId: string;
  type: 'reminder' | 'update' | 'assignment' | 'mention' | 'due_soon' | 'overdue';
  message: string;
  timestamp: string;
  read: boolean;
  priority: 'high' | 'medium' | 'low';
  actionRequired?: boolean;
  actionType?: 'review' | 'approve' | 'update' | 'complete';
  sender?: string;
  recipients: string[];
}

export interface TaskAnalytics {
  timeDistribution: {
    morning: number;
    afternoon: number;
    evening: number;
  };
  userPerformance: {
    userId: string;
    completed: number;
    overdue: number;
    averageCompletionTime: number;
  }[];
  taskTrends: {
    date: string;
    created: number;
    completed: number;
  }[];
  bottlenecks: {
    category: string;
    averageTime: number;
    failureRate: number;
  }[];
}
