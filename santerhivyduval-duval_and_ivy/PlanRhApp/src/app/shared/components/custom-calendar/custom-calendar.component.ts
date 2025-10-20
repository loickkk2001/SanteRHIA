import { Component, Input, Output, EventEmitter, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface CalendarDay {
  day: number;
  date: Date;
  month: number;
  year: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  isPast: boolean;
  isWeekend: boolean;
}

export interface CalendarEvent {
  id: string;
  title: string;
  date: Date;
  timeRange: string;
  color: string;
  status: string;
  type?: 'availability' | 'planning';
}

export interface ViewOption {
  label: string;
  value: 'month' | 'week' | 'day';
  icon: string;
}

export interface FilterOption {
  label: string;
  value: string;
  checked: boolean;
}

export interface CalendarView {
  type: 'month' | 'week' | 'day';
  startDate: Date;
  endDate: Date;
  title: string;
}

@Component({
  selector: 'app-custom-calendar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './custom-calendar.component.html',
  styleUrls: ['./custom-calendar.component.css']
})
export class CustomCalendarComponent implements OnInit, OnChanges {
  @Input() events: CalendarEvent[] = [];
  @Input() selectedDate: Date = new Date();
  @Output() dayClick = new EventEmitter<CalendarDay>();
  @Output() dateChange = new EventEmitter<Date>();
  @Output() viewChange = new EventEmitter<CalendarView>();

  currentDate: Date = new Date();
  calendarDays: CalendarDay[] = [];
  
  // Propriétés pour la navigation
  currentYear: number = new Date().getFullYear();
  currentMonth: number = new Date().getMonth();
  
  // Options d'affichage
  showViewOptions = false;
  showFilterOptions = false;
  currentView: 'month' | 'week' | 'day' = 'month';
  selectedFilters: string[] = [];
  
  // Données pour chaque vue
  currentViewData: CalendarView = {
    type: 'month',
    startDate: new Date(),
    endDate: new Date(),
    title: ''
  };
  
  weekDays: CalendarDay[] = [];
  dayData: CalendarDay | null = null;
  
  weekDaysShort = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
  
  monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ];

  // Options de vue
  viewOptions: ViewOption[] = [
    { label: 'Vue mensuelle', value: 'month', icon: 'pi pi-calendar' },
    { label: 'Vue hebdomadaire', value: 'week', icon: 'pi pi-calendar-times' },
    { label: 'Vue journalière', value: 'day', icon: 'pi pi-calendar-plus' }
  ];

  // Options de filtre
  filterOptions: FilterOption[] = [
    { label: 'Disponibilités', value: 'availability', checked: true },
    { label: 'Plannings', value: 'planning', checked: true },
    { label: 'Congés', value: 'leave', checked: true },
    { label: 'Formations', value: 'training', checked: true },
    { label: 'Réunions', value: 'meeting', checked: true }
  ];

  ngOnInit(): void {
    this.currentDate = new Date(this.selectedDate);
    this.currentYear = this.currentDate.getFullYear();
    this.currentMonth = this.currentDate.getMonth();
    this.updateCurrentView();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedDate']) {
      this.currentDate = new Date(this.selectedDate);
      this.generateCalendarDays();
    }
  }

  generateCalendarDays(): void {
    this.calendarDays = [];
    
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    
    // Premier jour du mois
    const firstDay = new Date(year, month, 1);
    // Dernier jour du mois
    const lastDay = new Date(year, month + 1, 0);
    
    // Premier lundi de la semaine contenant le premier jour du mois
    const startDate = new Date(firstDay);
    const dayOfWeek = firstDay.getDay();
    const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Lundi = 1
    startDate.setDate(firstDay.getDate() + mondayOffset);
    
    // Générer 42 jours (6 semaines)
    for (let i = 0; i < 42; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      
      const day: CalendarDay = {
        day: date.getDate(),
        date: new Date(date),
        month: date.getMonth(),
        year: date.getFullYear(),
        isCurrentMonth: date.getMonth() === month,
        isToday: this.isToday(date),
        isPast: this.isPast(date),
        isWeekend: date.getDay() === 0 || date.getDay() === 6
      };
      
      this.calendarDays.push(day);
    }
  }

  isToday(date: Date): boolean {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  }

  isPast(date: Date): boolean {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    date.setHours(0, 0, 0, 0);
    return date < today;
  }

  generateMonthView(): void {
    this.generateCalendarDays();
  }

  generateWeekView(): void {
    this.weekDays = [];
    const startOfWeek = this.currentViewData.startDate;
    
    for (let i = 0; i < 7; i++) {
      const date = new Date(startOfWeek);
      date.setDate(startOfWeek.getDate() + i);
      
      this.weekDays.push({
        date: date,
        day: date.getDate(),
        month: date.getMonth(),
        year: date.getFullYear(),
        isCurrentMonth: true,
        isToday: this.isToday(date),
        isPast: this.isPast(date),
        isWeekend: date.getDay() === 0 || date.getDay() === 6
      });
    }
  }

  generateDayView(): void {
    this.dayData = {
      date: this.selectedDate,
      day: this.selectedDate.getDate(),
      month: this.selectedDate.getMonth(),
      year: this.selectedDate.getFullYear(),
      isCurrentMonth: true,
      isToday: this.isToday(this.selectedDate),
      isPast: this.isPast(this.selectedDate),
      isWeekend: this.selectedDate.getDay() === 0 || this.selectedDate.getDay() === 6
    };
  }

  getCurrentMonthYear(): string {
    return `${this.monthNames[this.currentDate.getMonth()]} ${this.currentDate.getFullYear()}`;
  }

  navigateMonth(direction: 'prev' | 'next'): void {
    if (direction === 'prev') {
      this.currentDate.setMonth(this.currentDate.getMonth() - 1);
    } else {
      this.currentDate.setMonth(this.currentDate.getMonth() + 1);
    }
    
    this.currentYear = this.currentDate.getFullYear();
    this.currentMonth = this.currentDate.getMonth();
    this.updateCurrentView();
    this.dateChange.emit(new Date(this.currentDate));
  }

  navigateView(direction: 'prev' | 'next'): void {
    switch (this.currentView) {
      case 'month':
        this.navigateMonth(direction);
        break;
      case 'week':
        this.navigateWeek(direction);
        break;
      case 'day':
        this.navigateDay(direction);
        break;
    }
  }

  navigateWeek(direction: 'prev' | 'next'): void {
    const days = direction === 'prev' ? -7 : 7;
    this.selectedDate = new Date(this.selectedDate.getTime() + days * 24 * 60 * 60 * 1000);
    this.dateChange.emit(this.selectedDate);
    this.updateCurrentView();
  }

  navigateDay(direction: 'prev' | 'next'): void {
    const days = direction === 'prev' ? -1 : 1;
    this.selectedDate = new Date(this.selectedDate.getTime() + days * 24 * 60 * 60 * 1000);
    this.dateChange.emit(this.selectedDate);
    this.updateCurrentView();
  }

  goToToday(): void {
    this.currentDate = new Date();
    this.selectedDate = new Date();
    this.updateCurrentView();
    this.dateChange.emit(new Date(this.currentDate));
  }

  onDayClick(day: CalendarDay): void {
    this.dayClick.emit(day);
  }

  getEventsForDay(day: CalendarDay): CalendarEvent[] {
    if (!day.date) return [];
    
    return this.events.filter(event => {
      if (!event.date) return false;
      const eventDate = event.date instanceof Date ? event.date : new Date(event.date);
      return eventDate.toDateString() === day.date.toDateString();
    });
  }

  getFilteredEventsForDay(day: CalendarDay): CalendarEvent[] {
    if (!day.date) return [];
    
    const filteredEvents = this.getFilteredEvents();
    return filteredEvents.filter(event => {
      if (!event.date) return false;
      const eventDate = event.date instanceof Date ? event.date : new Date(event.date);
      const dayDateString = day.date.toDateString();
      const eventDateString = eventDate.toDateString();
      
      console.log('Comparaison de dates:', {
        dayDate: day.date,
        dayDateString: dayDateString,
        eventDate: eventDate,
        eventDateString: eventDateString,
        match: dayDateString === eventDateString
      });
      
      return dayDateString === eventDateString;
    });
  }

  getWeekNumber(date: Date): number {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
  }

  getWeekNumbers(): number[] {
    const weekNumbers: number[] = [];
    for (let i = 0; i < 6; i++) {
      const weekStart = new Date(this.calendarDays[i * 7].date);
      weekNumbers.push(this.getWeekNumber(weekStart));
    }
    return weekNumbers;
  }

  // Méthodes pour les options d'affichage
  toggleViewOptions(): void {
    this.showViewOptions = !this.showViewOptions;
    this.showFilterOptions = false;
  }

  toggleFilterOptions(): void {
    this.showFilterOptions = !this.showFilterOptions;
    this.showViewOptions = false;
  }

  selectView(view: ViewOption): void {
    this.currentView = view.value;
    this.showViewOptions = false;
    this.updateCurrentView();
    this.viewChange.emit(this.currentViewData);
    console.log('Vue sélectionnée:', view.label);
  }

  updateCurrentView(): void {
    const today = new Date();
    
    switch (this.currentView) {
      case 'month':
        this.currentViewData = {
          type: 'month',
          startDate: new Date(this.currentYear, this.currentMonth, 1),
          endDate: new Date(this.currentYear, this.currentMonth + 1, 0),
          title: this.getCurrentMonthYear()
        };
        this.generateMonthView();
        break;
        
      case 'week':
        this.currentViewData = this.getCurrentWeekData();
        this.generateWeekView();
        break;
        
      case 'day':
        this.currentViewData = {
          type: 'day',
          startDate: this.selectedDate,
          endDate: this.selectedDate,
          title: this.selectedDate.toLocaleDateString('fr-FR', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })
        };
        this.generateDayView();
        break;
    }
  }

  getCurrentWeekData(): CalendarView {
    const startOfWeek = this.getStartOfWeek(this.selectedDate);
    const endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);
    
    return {
      type: 'week',
      startDate: startOfWeek,
      endDate: endOfWeek,
      title: `Semaine du ${startOfWeek.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })} au ${endOfWeek.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}`
    };
  }

  getStartOfWeek(date: Date): Date {
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1); // Lundi = 1
    const startOfWeek = new Date(date);
    startOfWeek.setDate(diff);
    return startOfWeek;
  }

  toggleFilter(filter: FilterOption): void {
    filter.checked = !filter.checked;
    this.updateSelectedFilters();
  }

  updateSelectedFilters(): void {
    this.selectedFilters = this.filterOptions
      .filter(option => option.checked)
      .map(option => option.value);
    console.log('Filtres sélectionnés:', this.selectedFilters);
  }

  getFilteredEvents(): CalendarEvent[] {
    if (this.selectedFilters.length === 0) {
      return this.events;
    }
    
    return this.events.filter(event => {
      return this.selectedFilters.includes(event.type || 'availability');
    });
  }

  closeDropdowns(): void {
    this.showViewOptions = false;
    this.showFilterOptions = false;
  }

  getDayClass(day: CalendarDay): { [key: string]: boolean } {
    const classes: { [key: string]: boolean } = {
      'current-month': day.isCurrentMonth,
      'other-month': !day.isCurrentMonth,
      'today': day.isToday,
      'past': day.isPast,
      'weekend': day.isWeekend
    };
    return classes;
  }

  getDayName(date: Date): string {
    return date.toLocaleDateString('fr-FR', { weekday: 'short' });
  }

  getHoursOfDay(): number[] {
    const hours = [];
    for (let i = 0; i < 24; i++) {
      hours.push(i);
    }
    return hours;
  }

  getEventsForHour(hour: number): CalendarEvent[] {
    if (!this.dayData) return [];
    
    const filteredEvents = this.getFilteredEvents();
    return filteredEvents.filter(event => {
      if (!event.date) return false;
      const eventDate = event.date instanceof Date ? event.date : new Date(event.date);
      return eventDate.toDateString() === this.dayData!.date.toDateString();
    });
  }
}
