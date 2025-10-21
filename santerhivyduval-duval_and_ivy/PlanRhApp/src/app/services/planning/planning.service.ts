import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class PlanningService {
  private apiUrl = `${environment.apiUrl}/plannings`;

  constructor(private http: HttpClient) {}

  createPlanning(planning: any): Observable<any> {
    return this.http.post(this.apiUrl, planning);
  }

  getPlanningsByUser(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/user/${userId}`);
  }

  getPlanningsByDate(date: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/date/${date}`);
  }

  getPlanningsByActivity(activityCode: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/activity/${activityCode}`);
  }

  updatePlanning(id: string, planning: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, planning);
  }

  deletePlanning(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getAllPlannings(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  getPlanningStats(): Observable<any> {
    return this.http.get(`${this.apiUrl}/stats/summary`);
  }
}






