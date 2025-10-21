import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CalendarEvent {
  id: string;
  title: string;
  date: Date;
  type: 'availability' | 'planning';
  status: string;
  color: string;
  timeRange: string;
}

@Component({
  selector: 'app-custom-calendar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './custom-calendar.component.html',
  styleUrls: ['./custom-calendar.component.css']
})
export class CustomCalendarComponent implements OnInit {
  @Input() selectedDate: Date | null = null;
  @Input() showWeekNumbers: boolean = true;
  @Input() showButtonBar: boolean = false;
  @Input() events: CalendarEvent[] = [];
  @Output() dateSelect = new EventEmitter<Date>();
  @Output() proposalClick = new EventEmitter<Date>();

  currentDate = new Date();
  calendarDays: Date[] = [];
  weekDays = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM'];
  
  // Options d'affichage
  displayMode: 'monthly' | 'weekly' | 'daily' = 'monthly';
  showDisplayOptions = false;
  showMissionFilters = false;
  
  // Filtres de missions
  missionFilters = {
    disponibiliteValidee: true,
    disponibiliteProposee: true,
    disponibiliteRefusee: true,
    soins: true,
    conge: true,
    repos: true
  };
  monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ];

  ngOnInit() {
    this.generateCalendarDays();
  }

  get currentMonth(): string {
    return `${this.monthNames[this.currentDate.getMonth()]} ${this.currentDate.getFullYear()}`;
  }

  generateCalendarDays() {
    this.calendarDays = [];
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    
    // Premier jour du mois
    const firstDay = new Date(year, month, 1);
    // Dernier jour du mois
    const lastDay = new Date(year, month + 1, 0);
    
    // Commencer au dimanche de la semaine du premier jour
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    // Générer 42 jours (6 semaines)
    for (let i = 0; i < 42; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      this.calendarDays.push(date);
    }
  }

  getWeeks(): Date[][] {
    const weeks: Date[][] = [];
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    
    // Premier jour du mois
    const firstDay = new Date(year, month, 1);
    
    // Commencer au lundi de la semaine du premier jour
    const startDate = new Date(firstDay);
    const dayOfWeek = firstDay.getDay(); // 0 = dimanche, 1 = lundi, etc.
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Ajuster pour commencer le lundi
    startDate.setDate(startDate.getDate() + mondayOffset);
    
    // Générer 6 semaines
    for (let week = 0; week < 6; week++) {
      const weekDates: Date[] = [];
      for (let day = 0; day < 7; day++) {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + (week * 7) + day);
        weekDates.push(date);
      }
      weeks.push(weekDates);
    }
    
    return weeks;
  }

  previousMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    this.generateCalendarDays();
  }

  nextMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    this.generateCalendarDays();
  }

  selectDate(date: Date | null) {
    this.selectedDate = date;
    if (date) {
      this.dateSelect.emit(date);
    }
  }

  clearSelection() {
    this.selectedDate = null;
  }

  selectToday() {
    this.selectDate(new Date());
  }

  isSelected(date: Date): boolean {
    if (!this.selectedDate) return false;
    return date.toDateString() === this.selectedDate.toDateString();
  }

  isToday(date: Date): boolean {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  }

  isCurrentMonth(date: Date): boolean {
    return date.getMonth() === this.currentDate.getMonth();
  }

  getWeekNumber(date: Date): number {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
  }

  // Méthodes pour gérer les événements
  getEventsForDate(date: Date): CalendarEvent[] {
    return this.getFilteredEvents().filter(event => 
      event.date.toDateString() === date.toDateString()
    );
  }

  hasEvents(date: Date): boolean {
    return this.getEventsForDate(date).length > 0;
  }

  getEventColor(date: Date): string {
    const events = this.getEventsForDate(date);
    if (events.length === 0) return '';
    
    // Retourner la couleur du premier événement
    return events[0].color;
  }

  getEventTooltip(date: Date): string {
    const events = this.getEventsForDate(date);
    if (events.length === 0) return '';
    
    return events.map(event => `${event.title} - ${event.timeRange}`).join('\n');
  }

  // Méthodes pour les propositions de disponibilité
  canProposeAvailability(date: Date): boolean {
    // Ne pas proposer pour les jours passés ou les jours avec événements déjà validés
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (date < today) return false;
    if (!this.isCurrentMonth(date)) return false;
    
    const events = this.getEventsForDate(date);
    const hasValidatedEvent = events.some(event => event.status === 'validé');
    
    return !hasValidatedEvent;
  }

  hasProposal(date: Date): boolean {
    const events = this.getEventsForDate(date);
    return events.some(event => event.status === 'proposé');
  }

  proposeAvailability(date: Date, event: Event): void {
    event.stopPropagation();
    this.proposalClick.emit(date);
  }

  toggleDisplayOptions(): void {
    this.showDisplayOptions = !this.showDisplayOptions;
    this.showMissionFilters = false; // Fermer l'autre menu
  }

  toggleMissions(): void {
    this.showMissionFilters = !this.showMissionFilters;
    this.showDisplayOptions = false; // Fermer l'autre menu
  }

  setDisplayMode(mode: 'monthly' | 'weekly' | 'daily'): void {
    this.displayMode = mode;
    this.showDisplayOptions = false;
    // Regénérer le calendrier selon le mode
    this.generateCalendarDays();
  }

  toggleMissionFilter(filterKey: string): void {
    this.missionFilters[filterKey as keyof typeof this.missionFilters] = 
      !this.missionFilters[filterKey as keyof typeof this.missionFilters];
  }

  getFilteredEvents(): CalendarEvent[] {
    return this.events.filter(event => {
      switch (event.status) {
        case 'validé':
          return this.missionFilters.disponibiliteValidee;
        case 'proposé':
          return this.missionFilters.disponibiliteProposee;
        case 'refusé':
          return this.missionFilters.disponibiliteRefusee;
        case 'soins':
          return this.missionFilters.soins;
        case 'congé':
          return this.missionFilters.conge;
        case 'repos':
          return this.missionFilters.repos;
        default:
          return true;
      }
    });
  }
}