import {Component, Input, signal} from '@angular/core';
import { NavItem } from '../../../core/utils/interfaces/NavItem';
import {Router} from "@angular/router";
import {NgClass} from "@angular/common";

import { AvatarModule } from 'primeng/avatar';

@Component({
  selector: 'app-side-bar-item',
  standalone: true,
  imports: [NgClass, AvatarModule],
  templateUrl: './side-bar-item.component.html',
  styleUrl: './side-bar-item.component.css',
})
export class SideBarItemComponent {
  @Input() item!: NavItem;
  @Input() isPolicy: boolean = false;
  isSelected = signal(false);
  currentRoute = signal('/');

  constructor(private router: Router) {
  }

  ngOnInit() {
    this.currentRoute.set(this.router.url);
    this.isSelected.set(`${this.currentRoute()}` === this.item.link);
  }
}
