import {ChangeDetectorRef, Component, EventEmitter, Input, Output} from '@angular/core';
import {Item} from '../../models/interfaces';
import {ItemService} from '../../core/services/item-service';

@Component({
  selector: 'app-item-card',
  imports: [],
  templateUrl: './item-card.html',
  standalone: true,
  styleUrl: './item-card.css'
})
export class ItemCard {
  @Input() item!: Item;
  @Output() delete = new EventEmitter<number>();

  constructor(private itemService: ItemService, private cdr: ChangeDetectorRef) {
  }

  deleteItem() {
    this.itemService.deleteItem(this.item.id).subscribe((item) => {
      if(item){
        this.item = item;
        this.cdr.detectChanges();
      } else {
        this.delete.emit(this.item.id);
      }
    });
  }

  toggle() {
    this.itemService.toggleItem(this.item.id).subscribe((updatedItem) => {
        this.item.done = updatedItem.done;
        this.cdr.detectChanges();
      }
    );
  }
}
