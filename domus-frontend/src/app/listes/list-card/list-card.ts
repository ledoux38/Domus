import {Component, EventEmitter, Input, Output} from '@angular/core';
import {RouterLink} from '@angular/router';
import {List} from '../../models/interfaces';


@Component({
  selector: 'app-list-card',
  imports: [
    RouterLink
  ],
  templateUrl: './list-card.html',
  standalone: true,
  styleUrl: './list-card.css'
})
export class ListCard {
  @Input() list!: List;
  @Output() delete = new EventEmitter<{ id: number }>();

  deleteCard(id: number) {
    this.delete.emit({id});
  }
}
