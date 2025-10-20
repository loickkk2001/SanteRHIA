import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environment/environment';

export interface PlanningAgent {
  id: string;
  nom: string;
  prenom: string;
  contrat_hebdo: number; // en heures
  service_id: string;
}

export interface PlanningCell {
  agent_id: string;
  date: string; // YYYY-MM-DD
  code_activite: string; // RH, CA, J', EX, CSF, F, etc.
  statut: 'proposé' | 'validé' | 'refusé' | 'vide';
  availability_id?: string; // si c'est une proposition
}

export interface PlanningWeek {
  semaine: number;
  annee: number;
  dates: string[]; // [YYYY-MM-DD, ...]
}

export interface PlanningFilters {
  annee: number;
  mois: number;
  semaine: number;
}

@Injectable({
  providedIn: 'root'
})
export class PlanificationService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Tâche 1.3.1 : Récupérer les agents
  getAgents(): Observable<PlanningAgent[]> {
    return this.http.get<PlanningAgent[]>(`${this.apiUrl}/agents`);
  }

  // Tâche 1.3.1 : Récupérer les données de planning
  getPlanningData(filters: PlanningFilters): Observable<PlanningCell[]> {
    const params = new HttpParams()
      .set('date', this.getDateRange(filters))
      .set('service_id', this.getCurrentUserServiceId());
    
    return this.http.get<any>(`${this.apiUrl}/plannings`, { params })
      .pipe(
        map(response => {
          // Si la réponse a une propriété 'data', transformer data, sinon transformer la réponse complète
          const data = response && response.data ? response.data : response;
          return this.transformPlanningData(data);
        }),
        catchError(this.handleError)
      );
  }

  // Tâche 1.3.2 : Récupérer les propositions de disponibilité
  getAvailabilities(filters: PlanningFilters): Observable<any[]> {
    const params = new HttpParams()
      .set('status', 'proposé')
      .set('service_id', this.getCurrentUserServiceId());
    
    return this.http.get<any>(`${this.apiUrl}/availabilities`, { params })
      .pipe(
        map(response => {
          // Si la réponse a une propriété 'data', retourner data, sinon retourner la réponse complète
          if (response && response.data && Array.isArray(response.data)) {
            return response.data;
          }
          // Si la réponse est directement un tableau
          if (Array.isArray(response)) {
            return response;
          }
          // Sinon retourner un tableau vide
          return [];
        }),
        catchError(this.handleError)
      );
  }

  // Tâche 1.3.3 : Mettre à jour le statut d'une disponibilité
  updateAvailabilityStatus(availabilityId: string, status: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/availabilities/${availabilityId}`, {
      status: status
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Tâche 1.3.4 : Sauvegarder le planning
  savePlanning(cells: PlanningCell[]): Observable<any> {
    const planningData = cells.map(cell => ({
      user_id: cell.agent_id,
      date: cell.date,
      activity_code: cell.code_activite,
      plage_horaire: '08:00-17:00', // Valeur par défaut
      commentaire: `Planning créé le ${new Date().toISOString()}`
    }));

    return this.http.post(`${this.apiUrl}/plannings`, planningData)
      .pipe(
        catchError(this.handleError)
      );
  }

  // Simulation
  simulatePlanning(filters: PlanningFilters, type: string): Observable<PlanningCell[]> {
    return this.http.post<PlanningCell[]>(`${this.apiUrl}/planning/simulate`, {
      filters: filters,
      type: type
    });
  }

  // Récupérer les utilisateurs (agents) pour le planning
  getUsers(): Observable<any[]> {
    return this.http.get<any>(`${this.apiUrl}/users`)
      .pipe(
        map(response => {
          // Si la réponse a une propriété 'data', retourner data, sinon retourner la réponse complète
          if (response && response.data && Array.isArray(response.data)) {
            return response.data;
          }
          // Si la réponse est directement un tableau
          if (Array.isArray(response)) {
            return response;
          }
          // Sinon retourner un tableau vide
          return [];
        }),
        catchError(this.handleError)
      );
  }

  // Méthodes utilitaires
  private getDateRange(filters: PlanningFilters): string {
    const year = filters.annee;
    const month = filters.mois;
    const startDate = new Date(year, month - 1, 1);
    const endDate = new Date(year, month, 0);
    return `${startDate.toISOString().split('T')[0]},${endDate.toISOString().split('T')[0]}`;
  }

  private getCurrentUserServiceId(): string {
    // Récupérer l'ID du service de l'utilisateur connecté
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return user.service_id || '';
  }

  private transformPlanningData(response: any[]): PlanningCell[] {
    return response.map(item => ({
      agent_id: item.user_id,
      date: item.date,
      code_activite: item.activity_code,
      statut: 'validé' as const,
      availability_id: undefined
    }));
  }

  private handleError(error: any): Observable<never> {
    console.error('Erreur dans PlanificationService:', error);
    return throwError(() => error);
  }
}
