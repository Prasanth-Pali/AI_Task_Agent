
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';


// Task response model
export interface Task {
  taskId: number;
  title: string;
  description: string | null;
  dueDateUtc: string | null;
  status: string;
  createdAtUtc: string | null;
  updatedAtUtc: string | null;
}

// Create task request
export interface TaskCreate {
  title: string;
  description?: string;
  due_date_utc?: string;
  status: string;
}

// Update task request
export interface TaskUpdate {
  title?: string;
  description?: string | null;
  due_date_utc?: string | null;
  status?: string;
}

// Chat request and response
export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  summary: string;
}

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // GET: Retrieve all tasks
  getAllTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/tasks`);
  }

  // POST: Create task
  createTask(payload: TaskCreate): Observable<Task> {
    return this.http.post<Task>(
      `${this.apiUrl}/tasks`,
      payload
    );
  }

  // PATCH: Update task
  updateTask(
    taskId: number,
    payload: TaskUpdate
  ): Observable<Task> {
    return this.http.patch<Task>(
      `${this.apiUrl}/tasks/${taskId}`,
      payload
    );
  }

  // DELETE: Delete task
  deleteTask(taskId: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/tasks/${taskId}`
    );
  }

  // POST: Ask AI about tasks
  askAI(question: string, sessionId: string) {
  return this.http.post<ChatResponse>(
    `${this.apiUrl}/chat`,
    {
      question: question,
      session_id: sessionId
    }
  );
}
}
