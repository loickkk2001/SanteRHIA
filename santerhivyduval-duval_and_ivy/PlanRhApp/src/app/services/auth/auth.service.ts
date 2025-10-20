import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, switchMap } from 'rxjs/operators';
import { environment } from '../../environment/environment';
import { Response } from '../../dtos/response/Response';
import { User } from '../../models/User';
import { TokenService } from '../../services/token/token.service';
import { CreateUserRequest } from '../../dtos/request/CreateUserRequest';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  apiUrl = environment.apiUrl;
  private userSubject = new BehaviorSubject<User | null>(null);
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient, private tokenService: TokenService) {
    this.restoreUserFromToken();
  }

  login(matricule: string, password: string): Observable<Response<User>> {
    const loginData = {
      matricule: matricule,
      password: password
    };
    // Ajoutez le header Content-Type
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    return this.http
      .post<Response<User>>(`${this.apiUrl}/login`, loginData, { headers })
      .pipe(
        tap((response: Response<User>) => {
          if (response.token && response.data) {
            console.log('Login successful, saving token:', response.token);
            this.tokenService.saveToken(response.token);
            const userId = response.data._id || this.tokenService.getUserId();
            if (!userId) {
              throw new Error('No valid user ID provided in response or token');
            }
            const userData: User = {
              _id: userId,
              first_name: response.data.first_name,
              last_name: response.data.last_name,
              email: response.data.email,
              phoneNumber: response.data.phoneNumber,
              role: response.data.role,
              service: response.data.service,
              service_id: response.data.service_id,
              speciality_id: response.data.speciality_id,
              matricule: response.data.matricule,
            };
            console.log('User data saved after login:', userData);
            this.tokenService.saveUserData(userData);
            this.userSubject.next(userData);
          }
        })
      );
  }

  logout(): Observable<any> {
    const token = this.tokenService.getToken();
    const headers = token ? new HttpHeaders({ Authorization: `Bearer ${token}` }) : new HttpHeaders();
    console.log('Logging out, clearing all authentication data');
    return this.http.post(`${this.apiUrl}/logout`, {}, { headers }).pipe(
      tap(() => {
        this.tokenService.clearStorage();
        this.userSubject.next(null);
      })
    );
  }

  getUserInfo(): Observable<User | null> {
    const currentUser = this.userSubject.getValue();
    if (currentUser) {
      console.log('Returning current user from BehaviorSubject:', currentUser);
      return of(currentUser);
    }

    const token = this.tokenService.getToken();
    if (!token || this.tokenService.isExpired()) {
      console.log('No valid token found or token expired:', {
        token,
        isExpired: this.tokenService.isExpired(),
      });
      this.tokenService.clearStorage();
      this.userSubject.next(null);
      return of(null);
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    console.log('Fetching user info from API with token:', token);
    return this.http
      .get<Response<User>>(`${this.apiUrl}/user-info`, { headers })
      .pipe(
        switchMap((response: Response<User>) => {
          if (!response.data) {
            console.log('No user data returned from API');
            this.tokenService.clearStorage();
            this.userSubject.next(null);
            return of(null);
          }
          const userId = this.tokenService.getUserId();
          if (!userId) {
            console.log('No user ID found in token');
            this.tokenService.clearStorage();
            this.userSubject.next(null);
            return of(null);
          }
          const userData: User = {
            _id: userId,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            email: response.data.email,
            phoneNumber: response.data.phoneNumber,
            role: response.data.role,
            service: response.data.service,
            service_id: response.data.service_id,
            speciality_id: response.data.speciality_id,
            matricule: response.data.matricule,
          };
          console.log('User data fetched from API:', userData);
          this.tokenService.saveUserData(userData);
          this.userSubject.next(userData);
          return of(userData);
        }),
        tap({
          error: (err) => {
            console.error('Error fetching user info:', err);
            this.tokenService.clearStorage();
            this.userSubject.next(null);
          },
        })
      );
  }

  getCurrentUser(): User | null {
    const currentUser = this.userSubject.getValue();
    console.log('Getting current user:', currentUser);
    return currentUser;
  }

  isAuthenticated(): boolean {
    const token = this.tokenService.getToken();
    const isExpired = this.tokenService.isExpired();
    const isAuthenticated = !!token && !isExpired;
    console.log('Checking authentication status:', {
      token,
      isExpired,
      isAuthenticated,
    });
    return isAuthenticated;
  }

  createUser(createUserRequest: CreateUserRequest): Observable<Response<User>> {
    return this.http.post<Response<User>>(
      `${this.apiUrl}/users/register`,
      createUserRequest
    );
  }

  private restoreUserFromToken(): void {
    const token = this.tokenService.getToken();
    if (token && !this.tokenService.isExpired()) {
      const userData = this.tokenService.getUserData();
      if (userData && userData.role) {
        console.log('Restored user from token:', userData);
        this.userSubject.next(userData);
      } else {
        console.log('No valid user data or role in storage, clearing storage');
        this.tokenService.clearStorage();
        this.userSubject.next(null);
      }
    } else {
      console.log('No valid token found or token expired, clearing storage');
      this.tokenService.clearStorage();
      this.userSubject.next(null);
    }
  }
}