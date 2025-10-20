import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { BadgeModule } from 'primeng/badge';
import { CardModule } from 'primeng/card';
import { ChartModule } from 'primeng/chart';
import { CalendarModule } from 'primeng/calendar';
import { AbsenceService } from '../../../services/absence/absence.service';
import { UserService } from '../../../services/user/user.service';
import { ServiceService } from '../../../services/service/service.service';
import { AuthService } from '../../../services/auth/auth.service';
import { AlertsService } from '../../../services/alerts/alerts.service';
import { AnomaliesService } from '../../../services/anomalies/anomalies.service';
import { EventsService } from '../../../services/events/events.service';
import { Alert } from '../../../models/alert';
import { Anomaly } from '../../../models/anomaly';
import { PendingEvent } from '../../../models/pendingEvent';
import { Absence } from '../../../models/absence';
import { User } from '../../../models/User';
import { Service } from '../../../models/services';
import { forkJoin } from 'rxjs';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { Router } from '@angular/router';
import { TagModule } from 'primeng/tag';

@Component({
  selector: 'app-cadre-home',
  imports: [
    CommonModule, 
    TableModule, 
    CardModule,
    ChartModule,
    BadgeModule,
    ToastModule,
    TagModule,
    CalendarModule
  ],
  standalone: true,
  templateUrl: './cadre-home.component.html',
  styleUrls: ['./cadre-home.component.css'],
  providers: [MessageService, AuthService]
})
export class CadreHomeComponent implements OnInit {
  // Tableau des absences
  cols: any[] = [
    { field: 'staffName', header: 'Nom employé' },
    { field: 'startDate', header: 'Date début' },
    { field: 'endDate', header: 'Date Fin' },
    { field: 'replacementName', header: 'Remplaçant' },
    { field: 'status', header: 'Statut' }
  ];

  // Données pour les cartes
  stats = {
    todayAbsences: 0,
    tomorrowAbsences: 0,
    monthAbsences: 0,
    serviceStaff: 0,
    availableReplacements: 0
  };

  // Données pour les graphiques
  chartData: any;
  chartOptions: any;

  absences: any[] = [];
  todayAbsences: any[] = [];
  tomorrowAbsences: any[] = [];
  allAbsences: Absence[] = [];
  allUsers: User[] = [];
  allServices: Service[] = [];
  loggedInUser: User | null = null;

  // Specific anomaly counters
  errorsCount: number = 0;
  unjustifiedAbsencesCount: number = 0;
  overtimeCount: number = 0;
  
  // Specific event counters  
  teamRequestsCount: number = 0;
  
  // Current alert message
  currentAlertMessage: string = '';
  
  // Nearest HR event
  nearestHREvent: any = null;

  // New properties for SAPHIR portal
  alerts: Alert[] = [];
  anomalies: Anomaly[] = [];
  pendingEvents: PendingEvent[] = [];
  upcomingEvents: PendingEvent[] = [];
  anomaliesCount: number = 0;
  pendingEventsCount: number = 0;
  currentDate: string = '';

  constructor(
    private absenceService: AbsenceService,
    private userService: UserService,
    private serviceService: ServiceService,
    private authService: AuthService,
    private alertsService: AlertsService,
    private anomaliesService: AnomaliesService,
    private eventsService: EventsService,
    private messageService: MessageService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadUserAndData();
    this.initChart();
    this.setCurrentDate();
  }

  setCurrentDate(): void {
    const today = new Date();
    const options: Intl.DateTimeFormatOptions = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    this.currentDate = today.toLocaleDateString('fr-FR', options);
  }

  loadUserAndData(): void {
    this.authService.getUserInfo().subscribe({
      next: (user: User | null) => {
        if (user?._id) {
          this.loggedInUser = user;
          this.loadAllData();
        } else {
          this.showError('Impossible de charger les informations utilisateur');
        }
      },
      error: (err) => {
        this.showError('Échec de la connexion au serveur');
      }
    });
  }

  loadAllData(): void {
    forkJoin([
      this.absenceService.findAllAbsences(),
      this.userService.findAllUsers(),
      this.serviceService.findAllServices(),
      this.alertsService.getAlertsByService(this.loggedInUser?.service_id || ''),
      this.anomaliesService.getAnomaliesByService(this.loggedInUser?.service_id || ''),
      this.eventsService.getEventsByService(this.loggedInUser?.service_id || ''),
      this.eventsService.getUpcomingEvents()
    ]).subscribe({
      next: ([absencesResponse, usersResponse, servicesResponse, alertsResponse, anomaliesResponse, eventsResponse, upcomingEventsResponse]) => {
        this.allAbsences = absencesResponse?.data || [];
        this.allUsers = usersResponse?.data || [];
        this.allServices = servicesResponse?.data || [];

        // Load new SAPHIR portal data
        this.alerts = alertsResponse?.data || [];
        this.anomalies = anomaliesResponse?.data || [];
        this.pendingEvents = eventsResponse?.data || [];
        this.upcomingEvents = upcomingEventsResponse?.data || [];
        
        // Calculate counts
        this.anomaliesCount = this.anomalies.filter(a => a.status === 'detected' || a.status === 'in_progress').length;
        this.pendingEventsCount = this.pendingEvents.filter(e => e.status === 'pending').length;

        this.calculateStats();
        this.loadFilteredAbsences();
        this.loadTomorrowAbsences();
        this.updateChart();
      },
      error: (err) => {
        console.error('Error loading data:', err);
        this.showError('Échec du chargement des données');
      }
    });
  }

  calculateStats(): void {
    if (!this.loggedInUser?.service_id) return;
  
    const today = new Date().toISOString().split('T')[0];
    const currentMonth = new Date().getMonth() + 1;
    const currentYear = new Date().getFullYear();
  
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];
  
    // Compter les absences d'aujourd'hui (validées par le cadre)
    const todayAbsencesList = this.allAbsences.filter(absence => 
      absence.start_date <= today && 
      absence.end_date >= today &&
      absence.service_id === this.loggedInUser?.service_id &&
      ['Validé par le cadre'].includes(absence.status)
    );
    this.stats.todayAbsences = todayAbsencesList.length;
  
    // Compter les absences de demain (validées par le cadre)
    const tomorrowAbsencesList = this.allAbsences.filter(absence => 
      absence.start_date <= tomorrowStr && 
      absence.end_date >= tomorrowStr &&
      absence.service_id === this.loggedInUser?.service_id &&
      ['Validé par le cadre'].includes(absence.status)
    );
    this.stats.tomorrowAbsences = tomorrowAbsencesList.length;
  
    // Compter les absences du mois (validées par le cadre)
    this.stats.monthAbsences = this.allAbsences.filter(absence => {
      const absenceDate = new Date(absence.start_date);
      return absenceDate.getMonth() + 1 === currentMonth && 
             absenceDate.getFullYear() === currentYear &&
             absence.service_id === this.loggedInUser?.service_id &&
             ['Validé par le cadre'].includes(absence.status);
    }).length;

    // Compter le personnel du service (excluant l'utilisateur connecté)
    const serviceStaffList = this.allUsers.filter(user => 
      user.service_id === this.loggedInUser?.service_id &&
      user.id !== this.loggedInUser?.id
    );
    this.stats.serviceStaff = serviceStaffList.length;
  
    // Compter les personnes disponibles (qui travaillent aujourd'hui, excluant l'utilisateur connecté)
    const absentStaffIds = todayAbsencesList.map(absence => absence.staff_id);
    this.stats.availableReplacements = serviceStaffList.filter(
      staff => !absentStaffIds.includes(staff._id)
    ).length;
  }

  loadFilteredAbsences(): void {
    if (!this.loggedInUser?.service_id) return;

    this.absences = this.allAbsences
      .filter(absence => absence.service_id === this.loggedInUser?.service_id)
      .map(this.mapAbsenceData.bind(this));
  }

  /*loadTodayAbsences(): void {
    if (!this.loggedInUser?.service_id) return;

    const today = new Date().toISOString().split('T')[0];
    
    this.todayAbsences = this.allAbsences
      .filter(absence => 
        absence.start_date <= today && 
        absence.end_date >= today &&
        absence.service_id === this.loggedInUser?.service_id &&
        ['Validé par le cadre'].includes(absence.status)
      )
      .map(this.mapAbsenceData.bind(this))
      .sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at) : new Date(0);
        const dateB = b.created_at ? new Date(b.created_at) : new Date(0);
        return dateB.getTime() - dateA.getTime();
      });
  }*/

  loadTomorrowAbsences(): void {
    if (!this.loggedInUser?.service_id) return;
  
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];
    
    this.tomorrowAbsences = this.allAbsences
      .filter(absence => 
        absence.start_date <= tomorrowStr && 
        absence.end_date >= tomorrowStr &&
        absence.service_id === this.loggedInUser?.service_id
      )
      .map(this.mapAbsenceData.bind(this))
      .sort((a, b) => {
        const dateA = a.created_at ? new Date(a.created_at) : new Date(0);
        const dateB = b.created_at ? new Date(b.created_at) : new Date(0);
        return dateB.getTime() - dateA.getTime();
      });
  }

  mapAbsenceData(absence: Absence): any {
    const staffUser = this.allUsers.find(user => user.id === absence.staff_id);
    const replacementUser = absence.replacement_id
      ? this.allUsers.find(user => user.id === absence.replacement_id)
      : null;

    return {
      id: absence._id,
      staffName: staffUser ? `${staffUser.first_name} ${staffUser.last_name}` : 'Inconnu',
      startDate: this.formatDate(absence.start_date),
      endDate: this.formatDate(absence.end_date),
      replacementName: replacementUser
        ? `${replacementUser.first_name} ${replacementUser.last_name}`
        : 'Non spécifié',
      status: absence.status
    };
  }

  initChart(): void {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');
  
    this.chartOptions = {
      maintainAspectRatio: false,
      aspectRatio: 0.8,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: textColor,
            usePointStyle: true,
            padding: 20
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          stacked: false,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false
          }
        },
        y: {
          stacked: false,
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder,
            drawBorder: false
          }
        }
      }
    };
  
    // Initialisation avec des données vides
    this.chartData = {
      labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
      datasets: [
        {
          label: 'Absences validées',
          data: Array(12).fill(0),
          backgroundColor: documentStyle.getPropertyValue('--green-500'),
          borderColor: documentStyle.getPropertyValue('--green-500'),
          tension: 0.4
        },
        {
          label: 'Absences refusées',
          data: Array(12).fill(0),
          backgroundColor: documentStyle.getPropertyValue('--red-500'),
          borderColor: documentStyle.getPropertyValue('--red-500'),
          tension: 0.4
        }
      ]
    };
  }

  updateChart(): void {
    if (!this.allAbsences.length) return;
  
    const monthlyCountsValidated = Array(12).fill(0);
    const monthlyCountsRejected = Array(12).fill(0);
    const currentYear = new Date().getFullYear();
  
    this.allAbsences.forEach(absence => {
      const date = new Date(absence.start_date);
      if (date.getFullYear() === currentYear && 
          absence.service_id === this.loggedInUser?.service_id) {
        const month = date.getMonth();
        
        if (absence.status === 'Validé par le cadre') {
          monthlyCountsValidated[month]++;
        } else if (absence.status === 'Refusé par le cadre') {
          monthlyCountsRejected[month]++;
        }
      }
    });
  
    const documentStyle = getComputedStyle(document.documentElement);
  
    this.chartData = {
      labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
      datasets: [
        {
          label: 'Absences validées',
          data: monthlyCountsValidated,
          backgroundColor: documentStyle.getPropertyValue('--green-500'),
          borderColor: documentStyle.getPropertyValue('--green-500'),
          tension: 0.4
        },
        {
          label: 'Absences refusées',
          data: monthlyCountsRejected,
          backgroundColor: documentStyle.getPropertyValue('--red-500'),
          borderColor: documentStyle.getPropertyValue('--red-500'),
          tension: 0.4
        }
      ]
    };
  }

  getBadgeSeverity(status: string):  'success' | 'info' | 'danger' | 'secondary' | 'warn'   {
    switch (status.toLowerCase()) {
      case 'accepté par le remplaçant': return 'warn';
      case 'validé par le cadre': return 'success';
      case 'en cours': return 'info';
      case 'refusé par le remplaçant':
      case 'refusé par le cadre': return 'danger';
      default: return 'secondary';
    }
  }

  viewDetails(absenceId: string): void {
    this.router.navigate(['/cadre/treat-absence', absenceId]);
  }

  private formatDate(dateString: string): string {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return isNaN(date.getTime()) 
      ? dateString 
      : date.toLocaleDateString('fr-FR');
  }

  private showError(message: string): void {
    this.messageService.add({
      severity: 'error',
      summary: 'Erreur',
      detail: message
    });
  }

  formatEventDate(dateString: string): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
  }

  // Méthodes SAPHIR manquantes
  calculateSpecificCounts(): void {
    // Calculate specific anomaly counts
    this.errorsCount = this.anomalies.filter(a => 
      a.type === 'rule_violation' && (a.status === 'detected' || a.status === 'in_progress')
    ).length;
    
    this.unjustifiedAbsencesCount = this.anomalies.filter(a => 
      a.type === 'unjustified_absence' && 
      (a.status === 'detected' || a.status === 'in_progress')
    ).length;
    
    this.overtimeCount = this.anomalies.filter(a => 
      a.type === 'overtime' && 
      (a.status === 'detected' || a.status === 'in_progress')
    ).length;
    
    // Calculate total anomalies
    this.anomaliesCount = this.errorsCount + this.unjustifiedAbsencesCount + this.overtimeCount;
    
    // Calculate team requests count
    this.teamRequestsCount = this.pendingEvents.filter(e => 
      e.type === 'approval' && e.status === 'pending' && 
      e.related_entity_type === 'absence'
    ).length;
    
    // Calculate total pending events
    this.pendingEventsCount = this.teamRequestsCount + this.pendingEvents.filter(e => 
      e.type !== 'approval' && e.status === 'pending'
    ).length;
  }

  setCurrentAlertMessage(): void {
    if (this.alerts.length === 0) {
      this.currentAlertMessage = 'Aucune alerte en cours.';
    } else {
      // Get the most recent unresolved alert
      const unresolvedAlerts = this.alerts.filter(a => a.status !== 'resolved');
      if (unresolvedAlerts.length > 0) {
        const latestAlert = unresolvedAlerts.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )[0];
        this.currentAlertMessage = latestAlert.description;
      } else {
        this.currentAlertMessage = 'Aucune alerte en cours.';
      }
    }
  }

  findNearestHREvent(): void {
    if (this.upcomingEvents.length === 0) {
      this.nearestHREvent = null;
      return;
    }
    
    const today = new Date();
    const futureEvents = this.upcomingEvents.filter(e => 
      e.due_date && new Date(e.due_date) >= today
    );
    
    if (futureEvents.length > 0) {
      this.nearestHREvent = futureEvents.sort((a, b) => 
        new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime()
      )[0];
    } else {
      this.nearestHREvent = null;
    }
  }
}