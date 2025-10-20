import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';

// PrimeNG Modules
import { DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { TextareaModule } from 'primeng/textarea';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { CardModule } from 'primeng/card';
import { TagModule } from 'primeng/tag';
import { BadgeModule } from 'primeng/badge';

// Custom Calendar Component
import { CustomCalendarComponent, CalendarDay, CalendarEvent, CalendarView } from '../../../shared/components/custom-calendar/custom-calendar.component';

// Services
import { AvailabilityService } from '../../../services/availability/availability.service';
import { PlanningService } from '../../../services/planning/planning.service';
import { AuthService } from '../../../services/auth/auth.service';

// Models
import { Availability } from '../../../models/availability';
import { Planning } from '../../../models/planning';

// Les interfaces CalendarEvent et CalendarDay sont maintenant importées du composant custom-calendar

@Component({
  selector: 'app-mon-agenda',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    CustomCalendarComponent,
    DialogModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    TextareaModule,
    ToastModule,
    CardModule,
    TagModule,
    BadgeModule
  ],
  providers: [MessageService],
  templateUrl: './mon-agenda.component.html',
  styleUrls: ['./mon-agenda.component.css']
})
export class MonAgendaComponent implements OnInit, OnDestroy, AfterViewInit {
  private destroy$ = new Subject<void>();

  // Calendar properties
  selectedDate: Date = new Date();
  events: CalendarEvent[] = [];
  loading = false;

  // Modal properties
  showAvailabilityModal = false;
  showPlanningModal = false;
  selectedDay: any = null;

  // Form data
  availabilityForm = {
    start_time: '',
    end_time: '',
    commentaire: ''
  };

  planningForm = {
    activity_code: '',
    plage_horaire: '',
    commentaire: ''
  };

  // Options
  activityCodes = [
    { label: 'Soins', value: 'SOIN' },
    { label: 'Congé', value: 'CONGÉ' },
    { label: 'Repos', value: 'REPOS' },
    { label: 'Formation', value: 'FORMATION' },
    { label: 'Administratif', value: 'ADMINISTRATIF' }
  ];

  timeSlots = [
    { label: 'Matin (08:00-12:00)', value: '08:00-12:00' },
    { label: 'Après-midi (13:00-17:00)', value: '13:00-17:00' },
    { label: 'Soir (18:00-22:00)', value: '18:00-22:00' },
    { label: 'Journée complète (08:00-17:00)', value: '08:00-17:00' },
    { label: 'Nuit (20:00-08:00)', value: '20:00-08:00' }
  ];

  // User info
  currentUser: any = null;

  // ViewChild pour accéder au calendrier
  // @ViewChild('calendar') calendarRef!: ElementRef; // Plus nécessaire avec le calendrier personnalisé

  // Les styles du calendrier sont maintenant gérés par le composant custom-calendar

  // La locale française est maintenant gérée par le composant custom-calendar

  constructor(
    private availabilityService: AvailabilityService,
    private planningService: PlanningService,
    private authService: AuthService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.loadUserAndData();
  }

  ngAfterViewInit(): void {
    // Plus besoin de forcer la taille du calendrier avec le composant personnalisé
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadUserAndData(): void {
    this.authService.getUserInfo()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (user: any) => {
          this.currentUser = user;
          this.loadCalendarData();
        },
        error: (error: any) => {
          console.error('Erreur lors du chargement de l\'utilisateur:', error);
        }
      });
  }

  loadCalendarData(): void {
    if (!this.currentUser?._id) return;

    this.loading = true;
    
    // Réinitialiser les événements pour éviter les doublons
    this.events = [];
    
    // Charger les disponibilités et plannings du mois courant
    const startDate = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth(), 1);
    const endDate = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth() + 1, 0);

    // Charger les disponibilités
    this.availabilityService.getAvailabilitiesByUser(this.currentUser._id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          const availabilities = response.data || [];
          this.processAvailabilities(availabilities);
        },
        error: (error) => {
          console.error('Erreur lors du chargement des disponibilités:', error);
        }
      });

    // Charger les plannings
    this.planningService.getPlanningsByUser(this.currentUser._id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: any) => {
          const plannings = response.data || [];
          this.processPlannings(plannings);
          this.loading = false;
        },
        error: (error: any) => {
          console.error('Erreur lors du chargement des plannings:', error);
          this.loading = false;
        }
      });
  }

  processAvailabilities(availabilities: any[]): void {
    availabilities.forEach(availability => {
      // Vérifier que la date existe et est valide
      if (!availability.date) {
        console.warn('Disponibilité sans date:', availability);
        return;
      }
      
      // Créer la date en évitant les problèmes de fuseau horaire
      const dateStr = availability.date;
      const [year, month, day] = dateStr.split('-').map(Number);
      const eventDate = new Date(year, month - 1, day); // month - 1 car les mois commencent à 0
      
      console.log('Disponibilité:', {
        originalDate: availability.date,
        parsedDate: eventDate,
        dateString: eventDate.toDateString(),
        day: eventDate.getDate(),
        month: eventDate.getMonth() + 1,
        year: eventDate.getFullYear()
      });
      
      const event: CalendarEvent = {
        id: availability._id,
        title: `Disponibilité (${availability.status})`,
        date: eventDate,
        type: 'availability',
        status: availability.status,
        timeRange: `${availability.start_time}-${availability.end_time}`,
        color: this.getStatusColor(availability.status)
      };
      this.events.push(event);
    });
  }

  processPlannings(plannings: any[]): void {
    plannings.forEach(planning => {
      // Vérifier que la date existe et est valide
      if (!planning.date) {
        console.warn('Planning sans date:', planning);
        return;
      }
      
      // Créer la date en évitant les problèmes de fuseau horaire
      const dateStr = planning.date;
      const [year, month, day] = dateStr.split('-').map(Number);
      const eventDate = new Date(year, month - 1, day); // month - 1 car les mois commencent à 0
      
      const event: CalendarEvent = {
        id: planning._id,
        title: planning.activity_code,
        date: eventDate,
        type: 'planning',
        status: 'validé',
        timeRange: planning.plage_horaire,
        color: this.getActivityColor(planning.activity_code)
      };
      this.events.push(event);
    });
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'validé': return '#10b981'; // Vert
      case 'proposé': return '#f59e0b'; // Orange
      case 'refusé': return '#ef4444'; // Rouge
      default: return '#6b7280'; // Gris
    }
  }

  getActivityColor(activityCode: string): string {
    switch (activityCode) {
      case 'SOIN': return '#3b82f6'; // Bleu
      case 'CONGÉ': return '#8b5cf6'; // Violet
      case 'REPOS': return '#06b6d4'; // Cyan
      case 'FORMATION': return '#f59e0b'; // Orange
      case 'ADMINISTRATIF': return '#6b7280'; // Gris
      default: return '#6b7280';
    }
  }

  onDateSelect(event: any): void {
    this.selectedDate = event;
    this.loadCalendarData();
  }

  onDayClick(day: CalendarDay): void {
    console.log('Jour cliqué:', day);
    this.selectedDay = day.date;
    this.showAvailabilityModal = true;
    this.resetForms();
    console.log('Modal ouverte:', this.showAvailabilityModal);
  }

  resetForms(): void {
    this.availabilityForm = {
      start_time: '',
      end_time: '',
      commentaire: ''
    };
    this.planningForm = {
      activity_code: '',
      plage_horaire: '',
      commentaire: ''
    };
  }

  setQuickTime(type: 'start' | 'end', time: string): void {
    if (type === 'start') {
      this.availabilityForm.start_time = time;
    } else {
      this.availabilityForm.end_time = time;
    }
  }

  openPlanningModal(): void {
    this.showAvailabilityModal = false;
    this.showPlanningModal = true;
  }

  closeModals(): void {
    this.showAvailabilityModal = false;
    this.showPlanningModal = false;
    this.selectedDay = null;
  }

  submitAvailability(): void {
    console.log('Tentative de soumission de disponibilité...');
    console.log('Utilisateur:', this.currentUser);
    console.log('Jour sélectionné:', this.selectedDay);
    console.log('Formulaire:', this.availabilityForm);
    
    if (!this.currentUser?._id || !this.selectedDay) {
      console.error('Données manquantes pour la soumission');
      this.messageService.add({
        severity: 'error',
        summary: 'Erreur',
        detail: 'Données manquantes pour la soumission'
      });
      return;
    }

    // Validation des champs d'heure
    if (!this.availabilityForm.start_time || !this.availabilityForm.end_time) {
      console.error('Heures de début et fin requises');
      this.messageService.add({
        severity: 'error',
        summary: 'Erreur',
        detail: 'Veuillez renseigner l\'heure de début et l\'heure de fin'
      });
      return;
    }

    // Validation de la cohérence des heures
    if (this.availabilityForm.start_time >= this.availabilityForm.end_time) {
      console.error('L\'heure de fin doit être postérieure à l\'heure de début');
      this.messageService.add({
        severity: 'error',
        summary: 'Erreur',
        detail: 'L\'heure de fin doit être postérieure à l\'heure de début'
      });
      return;
    }

    // Convertir selectedDay en format YYYY-MM-DD
    let dateString = '';
    if (this.selectedDay instanceof Date) {
      dateString = this.selectedDay.toISOString().split('T')[0];
    } else if (this.selectedDay.year && this.selectedDay.month !== undefined && this.selectedDay.day) {
      const dateObj = new Date(this.selectedDay.year, this.selectedDay.month, this.selectedDay.day);
      dateString = dateObj.toISOString().split('T')[0];
    }

    const availabilityData = {
      user_id: this.currentUser._id,
      date: dateString,
      start_time: this.availabilityForm.start_time,
      end_time: this.availabilityForm.end_time,
      commentaire: this.availabilityForm.commentaire
    };

    console.log('Données à envoyer:', availabilityData);

    this.availabilityService.createAvailability(availabilityData)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          console.log('Réponse du serveur:', response);
          this.messageService.add({
            severity: 'success',
            summary: 'Succès',
            detail: 'Disponibilité proposée avec succès'
          });
          this.closeModals();
          this.loadCalendarData();
        },
        error: (error) => {
          console.error('Erreur lors de la création:', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Erreur lors de la création de la disponibilité'
          });
        }
      });
  }

  submitPlanning(): void {
    if (!this.currentUser?._id || !this.selectedDay) return;

    const planningData = {
      user_id: this.currentUser._id,
      date: this.selectedDay.toISOString().split('T')[0],
      activity_code: this.planningForm.activity_code,
      plage_horaire: this.planningForm.plage_horaire,
      commentaire: this.planningForm.commentaire
    };

    this.planningService.createPlanning(planningData)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response: any) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Succès',
            detail: 'Planning créé avec succès'
          });
          this.closeModals();
          this.loadCalendarData();
        },
        error: (error: any) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Erreur lors de la création du planning'
          });
        }
      });
  }

  // Ces méthodes sont maintenant gérées par le composant custom-calendar

  formatDate(date: any): string {
    if (!date) return '';
    
    // Si c'est déjà un objet Date
    if (date instanceof Date) {
    return date.toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
    
    // Si c'est un objet avec year, month, day (format PrimeNG)
    if (date.year && date.month !== undefined && date.day) {
      const dateObj = new Date(date.year, date.month, date.day);
      return dateObj.toLocaleDateString('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
    
    return '';
  }

  onViewChange(view: CalendarView): void {
    console.log('Vue changée:', view);
    // Optionnel : sauvegarder la préférence utilisateur
    localStorage.setItem('calendar-view', view.type);
  }

  // Les méthodes de navigation sont maintenant gérées par le composant custom-calendar

  // La méthode forceCalendarSize n'est plus nécessaire avec le calendrier personnalisé
}
