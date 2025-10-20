import { Component } from '@angular/core';
import {NavItem} from '../../../core/utils/interfaces/NavItem';
import {PrimeIcons} from 'primeng/api';
import {SideBarItemComponent} from '../side-bar-item/side-bar-item.component';
import { MenuItem } from 'primeng/api';
import { MenuModule } from 'primeng/menu';
import { SideBarDropComponent } from '../side-bar-drop/side-bar-drop.component';

@Component({
  selector: 'app-cadre-side-bar',
  imports: [SideBarItemComponent, MenuModule, SideBarDropComponent],
  standalone : true,
  templateUrl: './cadre-side-bar.component.html',
  styleUrl: './cadre-side-bar.component.css'
})
export class CadreSideBarComponent {
  items: NavItem[] = [
    {title: 'Accueil', link: '/cadre', icon: PrimeIcons.HOME},
    {title: 'Personnel Paramédical', link: '/cadre/medical-staff', icon: PrimeIcons.CLIPBOARD},
    {title: 'Calendrier', link: '/cadre/calendar', icon: PrimeIcons.CALENDAR},
    {title: 'Planification', link: '/cadre/planification', icon: PrimeIcons.CALENDAR_PLUS},
    {title: 'Absences', link: '/cadre/absence', icon: PrimeIcons.INFO_CIRCLE},
    {title: 'Mes anomalies', link: '/cadre/anomalies', icon: PrimeIcons.EXCLAMATION_TRIANGLE},
  ];

  others: NavItem[] = [
    { title: 'Accéder à l\'aide', link: '/cadre/aide', icon: PrimeIcons.QUESTION_CIRCLE },
    { title: 'Déconnexion', link: '/logout', icon: PrimeIcons.SIGN_OUT },
    { title: 'Politique de confidentialité', link: '/cadre/politique', icon: PrimeIcons.SHIELD }
  ];


}
