import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil } from 'rxjs';

// PrimeNG Modules
import { DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { DropdownModule } from 'primeng/dropdown';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { CardModule } from 'primeng/card';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

// Services
import { PlanificationService, PlanningAgent, PlanningCell, PlanningWeek, PlanningFilters } from '../../../services/planification/planification.service';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-planification',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    DialogModule,
    ButtonModule,
    DropdownModule,
    ToastModule,
    CardModule,
    ProgressSpinnerModule
  ],
  templateUrl: './planification.component.html',
  styleUrls: ['./planification.component.css']
})
export class PlanificationComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Données
  agents: PlanningAgent[] = [];
  planningCells: PlanningCell[] = [];
  planningWeeks: PlanningWeek[] = [];
  
  // Filtres
  filters: PlanningFilters = {
    annee: new Date().getFullYear(),
    mois: new Date().getMonth() + 1,
    semaine: this.getCurrentWeek()
  };
  
  // Options des filtres
  annees: number[] = [];
  mois: {label: string, value: number}[] = [];
  semaines: {label: string, value: number}[] = [];
  
  // États
  editMode = false;
  hasChanges = false;
  showSimulationModal = false;
  showEditModal = false;
  showSimulationOptions = false;
  showPublishOptions = false;
  loading = false;
  currentWeekOffset = 0; // Offset pour la navigation par blocs de semaines
  
  // Édition manuelle
  selectedAgentId: string = '';
  selectedDate: string = '';
  selectedActivityCode: string = '';
  
  // Codes d'activité
  activityCodes = [
    {label: 'RH', value: 'RH'},
    {label: 'CA', value: 'CA'},
    {label: 'J\'', value: 'J\''},
    {label: 'EX', value: 'EX'},
    {label: 'CSF', value: 'CSF'},
    {label: 'F', value: 'F'},
    {label: 'DISP', value: 'DISP'}
  ];

  constructor(
    private planificationService: PlanificationService,
    private authService: AuthService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.initializeFilters();
    this.loadData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  // Tâche 1.3.1 : Initialisation des filtres
  initializeFilters(): void {
    // Générer les années (année actuelle ± 2)
    const currentYear = new Date().getFullYear();
    for (let i = currentYear - 2; i <= currentYear + 2; i++) {
      this.annees.push(i);
    }
    
    // Générer les mois
    this.mois = [
      {label: 'Janvier', value: 1},
      {label: 'Février', value: 2},
      {label: 'Mars', value: 3},
      {label: 'Avril', value: 4},
      {label: 'Mai', value: 5},
      {label: 'Juin', value: 6},
      {label: 'Juillet', value: 7},
      {label: 'Août', value: 8},
      {label: 'Septembre', value: 9},
      {label: 'Octobre', value: 10},
      {label: 'Novembre', value: 11},
      {label: 'Décembre', value: 12}
    ];
    
    // Générer les semaines du mois
    this.updateSemaines();
  }

  // Tâche 1.3.1 : Chargement des données
  loadData(): void {
    this.loading = true;
    this.loadAgents();
    this.loadPlanningData();
    this.loadAvailabilities(); // Tâche 1.3.2
  }

  loadAgents(): void {
    // Utiliser les utilisateurs existants comme agents
    this.planificationService.getUsers()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (users) => {
          let currentUser = JSON.parse(localStorage.getItem('user') || '{}');
          
          // Fallback : si localStorage est vide, chercher John Steve dans la liste des utilisateurs
          if (!currentUser.service_id || !currentUser.first_name) {
            console.log('⚠️ localStorage vide ou incomplet, recherche de l\'utilisateur connecté...');
            const johnSteve = users.find(user => 
              user.first_name === 'John' && user.last_name === 'Steve' && user.role === 'cadre'
            );
            if (johnSteve) {
              currentUser = johnSteve;
              console.log('✅ Utilisateur trouvé via API:', currentUser);
            }
          }
          
          // DEBUG : Afficher les informations
          console.log('🔍 DEBUG - Current User (John Steve):', currentUser);
          console.log('🔍 DEBUG - All Users from API:', users);
          console.log('🔍 DEBUG - John Steve service_id:', currentUser.service_id);
          
          const serviceUsers = users.filter(user => {
            const matches = user.service_id === currentUser.service_id && user.role !== 'cadre';
            console.log(`🔍 DEBUG - User ${user.first_name} ${user.last_name}:`, {
              service_id: user.service_id,
              role: user.role,
              matches: matches,
              currentUserService: currentUser.service_id
            });
            return matches;
          });
          
          console.log('🔍 DEBUG - Filtered Users:', serviceUsers);
          
          this.agents = serviceUsers.map(user => ({
            id: user._id,
            nom: user.last_name || user.nom || '',
            prenom: user.first_name || user.prenom || '',
            contrat_hebdo: user.contrat_horaire || 35, // Utiliser le contrat réel
            service_id: user.service_id || ''
          }));
          
          console.log('🔍 DEBUG - Final agents:', this.agents);
          
          this.generatePlanningWeeks();
          this.loading = false;
        },
        error: (error) => {
          this.handleError(error, 'chargement des agents');
          this.loading = false;
        }
      });
  }

  loadPlanningData(): void {
    this.planificationService.getPlanningData(this.filters)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (data) => {
          this.planningCells = data;
        },
        error: (error) => {
          this.handleError(error, 'chargement du planning');
          // Initialiser avec des cellules vides si pas de données
          this.planningCells = [];
        }
      });
  }

  // Tâche 1.3.2 : Charger les propositions de disponibilité
  loadAvailabilities(): void {
    this.planificationService.getAvailabilities(this.filters)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (availabilities) => {
          this.processAvailabilities(availabilities);
          this.loading = false;
        },
        error: (error) => {
          this.handleError(error, 'chargement des disponibilités');
          this.loading = false;
        }
      });
  }

  processAvailabilities(availabilities: any[]): void {
    availabilities.forEach(availability => {
      if (availability.status === 'proposé') {
        const cell: PlanningCell = {
          agent_id: availability.user_id,
          date: availability.date,
          code_activite: 'DISP', // Code spécial pour disponibilité proposée
          statut: 'proposé',
          availability_id: availability._id
        };
        
        // Vérifier si la cellule existe déjà
        const existingCellIndex = this.planningCells.findIndex(c => 
          c.agent_id === cell.agent_id && c.date === cell.date
        );
        
        if (existingCellIndex >= 0) {
          // Mettre à jour la cellule existante
          this.planningCells[existingCellIndex] = cell;
        } else {
          // Ajouter une nouvelle cellule
          this.planningCells.push(cell);
        }
      }
    });
  }

  // Génération des semaines de planification (limité à 2-3 semaines)
  generatePlanningWeeks(): void {
    this.planningWeeks = [];
    const year = this.filters.annee;
    const month = this.filters.mois;
    
    // Calculer les semaines du mois
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    
    let currentWeek = this.getWeekNumber(firstDay);
    const weeksInMonth = this.getWeekNumber(lastDay) - currentWeek + 1;
    
    // Limiter à 2 semaines maximum pour un meilleur affichage
    const maxWeeks = Math.min(weeksInMonth, 2);
    
    // Appliquer l'offset pour la navigation
    const startWeek = currentWeek + this.currentWeekOffset;
    
    for (let i = 0; i < maxWeeks; i++) {
      const weekStart = this.getStartOfWeek(firstDay, startWeek + i);
      const dates = [];
      
      for (let j = 0; j < 7; j++) {
        const date = new Date(weekStart);
        date.setDate(weekStart.getDate() + j);
        dates.push(date.toISOString().split('T')[0]);
      }
      
      this.planningWeeks.push({
        semaine: startWeek + i,
        annee: year,
        dates: dates
      });
    }
  }

  // Navigation par blocs de semaines
  previousWeeks(): void {
    this.currentWeekOffset = Math.max(0, this.currentWeekOffset - 2);
    this.generatePlanningWeeks();
  }

  nextWeeks(): void {
    const year = this.filters.annee;
    const month = this.filters.mois;
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    const currentWeek = this.getWeekNumber(firstDay);
    const weeksInMonth = this.getWeekNumber(lastDay) - currentWeek + 1;
    
    if (this.currentWeekOffset + 2 < weeksInMonth) {
      this.currentWeekOffset += 2;
      this.generatePlanningWeeks();
    }
  }

  canGoPrevious(): boolean {
    return this.currentWeekOffset > 0;
  }

  canGoNext(): boolean {
    const year = this.filters.annee;
    const month = this.filters.mois;
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    const currentWeek = this.getWeekNumber(firstDay);
    const weeksInMonth = this.getWeekNumber(lastDay) - currentWeek + 1;
    
    return this.currentWeekOffset + 2 < weeksInMonth;
  }

  // Tâche 1.3.3 : Valider une proposition
  validerProposition(agentId: string, date: string, event: Event): void {
    event.stopPropagation();
    
    const cell = this.planningCells.find(c => 
      c.agent_id === agentId && c.date === date && c.statut === 'proposé'
    );
    
    if (cell && cell.availability_id) {
      this.planificationService.updateAvailabilityStatus(
        cell.availability_id, 
        'validé'
      )
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          cell.statut = 'validé';
          cell.code_activite = 'RH'; // Code par défaut après validation
          this.messageService.add({
            severity: 'success',
            summary: 'Succès',
            detail: 'Proposition validée'
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Impossible de valider la proposition'
          });
        }
      });
    }
  }

  // Tâche 1.3.3 : Refuser une proposition
  refuserProposition(agentId: string, date: string, event: Event): void {
    event.stopPropagation();
    
    const cell = this.planningCells.find(c => 
      c.agent_id === agentId && c.date === date && c.statut === 'proposé'
    );
    
    if (cell && cell.availability_id) {
      this.planificationService.updateAvailabilityStatus(
        cell.availability_id, 
        'refusé'
      )
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          cell.statut = 'refusé';
          this.messageService.add({
            severity: 'success',
            summary: 'Succès',
            detail: 'Proposition refusée'
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Impossible de refuser la proposition'
          });
        }
      });
    }
  }

  // Tâche 1.3.4 : Mode édition manuelle
  toggleEditMode(): void {
    this.editMode = !this.editMode;
    this.messageService.add({
      severity: 'info',
      summary: 'Mode édition',
      detail: this.editMode ? 'Mode édition activé' : 'Mode édition désactivé'
    });
  }

  onCellClick(agentId: string, date: string): void {
    if (this.editMode) {
      this.selectedAgentId = agentId;
      this.selectedDate = date;
      this.selectedActivityCode = this.getCellCode(agentId, date);
      this.showEditModal = true;
    }
  }

  saveManualEdit(): void {
    const cell = this.planningCells.find(c => 
      c.agent_id === this.selectedAgentId && c.date === this.selectedDate
    );
    
    if (cell) {
      cell.code_activite = this.selectedActivityCode;
      cell.statut = 'validé';
    } else {
      this.planningCells.push({
        agent_id: this.selectedAgentId,
        date: this.selectedDate,
        code_activite: this.selectedActivityCode,
        statut: 'validé'
      });
    }
    
    this.hasChanges = true;
    this.showEditModal = false;
    
    this.messageService.add({
      severity: 'success',
      summary: 'Succès',
      detail: 'Modification enregistrée'
    });
  }

  cancelManualEdit(): void {
    this.showEditModal = false;
    this.selectedAgentId = '';
    this.selectedDate = '';
    this.selectedActivityCode = '';
  }

  // Méthodes utilitaires
  getCellCode(agentId: string, date: string): string {
    const cell = this.planningCells.find(c => 
      c.agent_id === agentId && c.date === date
    );
    return cell ? cell.code_activite : '';
  }

  getCellStatus(agentId: string, date: string): string {
    const cell = this.planningCells.find(c => 
      c.agent_id === agentId && c.date === date
    );
    return cell ? cell.statut : 'vide';
  }

  getAllDays(): string[] {
    const days: string[] = [];
    this.planningWeeks.forEach(week => {
      days.push(...week.dates);
    });
    return days;
  }

  getWeekLabel(week: PlanningWeek): string {
    const monthName = this.mois.find(m => m.value === this.filters.mois)?.label || '';
    return `${monthName} ${week.annee} sem ${week.semaine}`;
  }

  getDayName(date: string): string {
    const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
    return dayNames[new Date(date).getDay()];
  }

  getDayNumber(date: string): string {
    return new Date(date).getDate().toString();
  }

  formatContractHours(hours: number): string {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    return `${h}:${m.toString().padStart(2, '0')}`;
  }

  onFilterChange(): void {
    this.loadData();
  }

  updateSemaines(): void {
    this.semaines = [];
    const year = this.filters.annee;
    const month = this.filters.mois;
    
    const firstDay = new Date(year, month - 1, 1);
    const lastDay = new Date(year, month, 0);
    
    let currentWeek = this.getWeekNumber(firstDay);
    const weeksInMonth = this.getWeekNumber(lastDay) - currentWeek + 1;
    
    for (let i = 0; i < weeksInMonth; i++) {
      this.semaines.push({
        label: `Semaine ${currentWeek + i}`,
        value: currentWeek + i
      });
    }
  }

  getCurrentWeek(): number {
    const now = new Date();
    return this.getWeekNumber(now);
  }

  getSelectedAgentName(): string {
    const agent = this.agents.find(a => a.id === this.selectedAgentId);
    return agent ? `${agent.nom} ${agent.prenom}` : '';
  }

  getWeekNumber(date: Date): number {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
  }

  getStartOfWeek(date: Date, weekNumber: number): Date {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const startOfWeek = new Date(firstDayOfYear);
    startOfWeek.setDate(firstDayOfYear.getDate() + (weekNumber - 1) * 7);
    
    // Ajuster pour commencer le lundi
    const dayOfWeek = startOfWeek.getDay();
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
    startOfWeek.setDate(startOfWeek.getDate() + mondayOffset);
    
    return startOfWeek;
  }

  // Simulation
  simulerAvecContratActuel(): void {
    this.planificationService.simulatePlanning(this.filters, 'contrat_actuel')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (result) => {
          this.planningCells = result;
          this.hasChanges = true;
          this.messageService.add({
            severity: 'success',
            summary: 'Simulation',
            detail: 'Planning simulé avec succès'
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Impossible de simuler le planning'
          });
        }
      });
  }

  simulerAvecContratPersonnalise(): void {
    this.showSimulationModal = true;
  }

  validerPlanning(): void {
    this.planificationService.savePlanning(this.planningCells)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.hasChanges = false;
          this.messageService.add({
            severity: 'success',
            summary: 'Succès',
            detail: 'Planning validé et sauvegardé'
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Erreur',
            detail: 'Impossible de sauvegarder le planning'
          });
        }
      });
  }

  // Méthodes utilitaires
  getCellTooltip(agentId: string, date: string): string {
    const cell = this.planningCells.find(c => 
      c.agent_id === agentId && c.date === date
    );
    
    if (!cell) {
      return this.editMode ? 'Cliquer pour ajouter une activité' : '';
    }
    
    const agent = this.agents.find(a => a.id === agentId);
    const agentName = agent ? `${agent.prenom} ${agent.nom}` : 'Agent';
    
    switch (cell.statut) {
      case 'proposé':
        return `${agentName} - Proposition de disponibilité (${cell.date})`;
      case 'validé':
        return `${agentName} - Activité validée: ${cell.code_activite}`;
      case 'refusé':
        return `${agentName} - Proposition refusée`;
      default:
        return `${agentName} - ${cell.code_activite}`;
    }
  }

  // Amélioration de la gestion des erreurs
  private handleError(error: any, context: string): void {
    console.error(`Erreur ${context}:`, error);
    
    let message = 'Une erreur est survenue';
    if (error.error?.detail) {
      message = error.error.detail;
    } else if (error.message) {
      message = error.message;
    }
    
    this.messageService.add({
      severity: 'error',
      summary: 'Erreur',
      detail: message
    });
  }
}
