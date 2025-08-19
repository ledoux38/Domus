import {Component, EventEmitter, Input, Output} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {ActivatedRoute} from '@angular/router';
import {Suggestion} from '../../models/interfaces';
import {ListService} from '../../core/services/list-service';
import {ItemService} from '../../core/services/item-service';

@Component({
  selector: 'app-add-item-form',
  imports: [
    FormsModule
  ],
  templateUrl: './add-item-form.html',
  styleUrl: './add-item-form.css'
})
export class AddItemForm {
  item: string = '';
  newItemText: string = '';
  suggestions: Suggestion[] = [];
  @Output() add = new EventEmitter<{ item: string }>();
  @Input() listId: number = 0;

  constructor(private itemService: ItemService) {
  }

  addItem(form: NgForm) {
    const text = this.newItemText.trim();
    if (!text) {
      return;
    }
    this.itemService.addItem(this.listId, text).subscribe(item => {
      // this.items.push(item);
      form.resetForm();
      this.newItemText = '';
      this.suggestions = [];
    });
  }

  searchSuggestions() {
    const q = this.newItemText.trim();
    if (!q) {
      this.suggestions = [];
      return;
    }
    this.itemService.searchSuggestions(this.listId, q).subscribe(data => {
      this.suggestions = data;
    });
  }
}
