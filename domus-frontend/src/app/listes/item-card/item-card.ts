import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Item} from '../../models/interfaces';

@Component({
  selector: 'app-item-card',
  imports: [],
  templateUrl: './item-card.html',
  styleUrl: './item-card.css'
})
export class ItemCard {
  @Input() item!: Item;
  @Output() toggle = new EventEmitter<number>();
  @Output() delete = new EventEmitter<number>();

  deleteCard(id: number) {
    if (confirm(`Supprimer l'élément ?`)) {
      this.delete.emit(id);
    }
  }

  toggleCard(id: number) {
    this.toggle.emit(id);
  }
}
