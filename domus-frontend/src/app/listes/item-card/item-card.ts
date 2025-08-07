import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Item} from '../../models/interfaces';

@Component({
  selector: 'app-item-card',
  imports: [],
  templateUrl: './item-card.html',
  standalone: true,
  styleUrl: './item-card.css'
})
export class ItemCard {
  @Input() item!: Item;
  @Output() toggle = new EventEmitter<number>();
  @Output() delete = new EventEmitter<number>();

  deleteCard() {
      this.delete.emit(this.item.id);
  }

  toggleCard() {
    this.toggle.emit(this.item.id);
  }
}
