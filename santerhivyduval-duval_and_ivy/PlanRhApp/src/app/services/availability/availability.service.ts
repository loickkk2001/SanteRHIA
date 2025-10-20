import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environment/environment';

@Injectable({
  providedIn: 'root'
})
export class AvailabilityService {
  private apiUrl = `${environment.apiUrl}/availabilities`;

  constructor(private http: HttpClient) {}

  createAvailability(availability: any): Observable<any> {
    return this.http.post(this.apiUrl, availability);
  }

  getAvailabilitiesByUser(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/user/${userId}`);
  }

  getAvailabilitiesByDate(date: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/date/${date}`);
  }

  getAvailabilitiesByStatus(status: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/status/${status}`);
  }

  updateAvailability(id: string, availability: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, availability);
  }

  deleteAvailability(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getAllAvailabilities(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}





