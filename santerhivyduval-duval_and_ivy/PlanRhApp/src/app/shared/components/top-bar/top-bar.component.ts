import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AvatarModule } from 'primeng/avatar';
import { MenuModule } from 'primeng/menu';
import { DialogModule } from 'primeng/dialog';
import { MenuItem } from 'primeng/api';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth/auth.service';
import { ServiceService } from '../../../services/service/service.service';
import { User } from '../../../models/User';
import { Service } from '../../../models/services';
import { NotificationBellComponent } from '../notification-bell/notification-bell.component';
import { Notification } from '../../../services/notifications/notification.service';

@Component({
  selector: 'app-top-bar',
  standalone: true,
  imports: [AvatarModule, MenuModule, DialogModule, CommonModule, NotificationBellComponent],
  providers: [AuthService, ServiceService], // Explicitly provide AuthService for standalone component
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css'],
})
export class TopBarComponent implements OnInit {
  userRole: string | null = null;
  userName: string | null = null;
  name: string | null = null;
  managerName: string | null = null;
  userId: string = '';
  menuItems: MenuItem[] = [];
  displayProfileModal: boolean = false;
  user: User | null = null;
  today: Date = new Date();

  constructor(private router: Router, private authService: AuthService, private serviceService: ServiceService) {}

  ngOnInit() {
    // Check if user data is already available
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.setUserData(currentUser);
      this.loadServiceHead(currentUser);
    }

    // Subscribe to user changes
    this.authService.getUserInfo().subscribe({
      next: (user: User | null) => {
        console.log('User info received in TopBar:', user);
        if (user) {
          this.setUserData(user);
        } else {
          console.log('No user data available');
          this.user = null;
          this.userRole = null;
          this.userName = null;
          this.name = null;
          this.managerName = null;
          this.menuItems = [];
          this.router.navigate(['/']); // Redirect to login if no user data
        }
      },
      error: (err) => {
        console.error('Error fetching user info in TopBar:', err);
        this.user = null;
        this.userRole = null;
        this.userName = null;
        this.name = null;
        this.managerName = null;
        this.menuItems = [];
        this.router.navigate(['/']);
      }
    });
  }

  private loadServiceHead(user: User) {
    if (user.service_id) {
      this.serviceService.findServiceById(user.service_id).subscribe({
        next: (response) => {
          const service: Service = response.data;
          this.managerName = service.head || 'N/A'; // Set the manager name from the service head
          console.log('Service head loaded:', this.managerName);
        },
        error: (err) => {
          console.error('Error fetching service:', err);
          this.managerName = 'N/A'; // Fallback if service fetch fails
        }
      });
    } else {
      this.managerName = 'N/A'; // No service assigned to the user
    }
  }

  private setUserData(user: User) {
    this.user = user;
    this.userId = user._id || '';
    switch (user.role) {
      case 'admin':
        this.userRole = 'A';
        break;
      case 'cadre':
        this.userRole = 'M';
        break;
      case 'nurse':
        this.userRole = 'C';
        break;
      default:
        this.userRole = 'U';
    }
    this.userName = user.first_name && user.last_name
      ? `${user.first_name.charAt(0).toUpperCase()}${user.last_name.charAt(0).toUpperCase()}`
      : 'N/A';

    this.name = user.first_name && user.last_name
      ? `${user.first_name} ${user.last_name}`
      : 'N/A';

    this.menuItems = [
      { label: 'Profil', icon: 'pi pi-user', command: () => this.showProfile() },
      { label: 'Déconnexion', icon: 'pi pi-sign-out', command: () => this.logout() }
    ];
  }

  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(['']);
      },
      error: (err) => {
        console.error('Erreur lors de la déconnexion', err);
        this.router.navigate(['']);
      }
    });
  }

  showProfile() {
    this.displayProfileModal = true;
  }

  closeProfileModal() {
    this.displayProfileModal = false;
  }

  onNotificationClick(notification: Notification): void {
    // Naviguer vers la page appropriée selon le type de notification
    if (notification.action_url) {
      this.router.navigate([notification.action_url]);
    } else {
      // Navigation par défaut selon la catégorie
      switch (notification.category) {
        case 'alert':
          this.router.navigate(['/sec/alerts']);
          break;
        case 'anomaly':
          this.router.navigate(['/cadre/anomalies']);
          break;
        case 'event':
          this.router.navigate(['/sec/calendar']);
          break;
        default:
          console.log('Notification clicked:', notification);
      }
    }
  }
}

