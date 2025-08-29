import {Component, EventEmitter, Input, Output} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {Suggestion} from '../../models/interfaces';
import {ItemService} from '../../core/services/item-service';

@Component({
  selector: 'app-add-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './add-form.html',
  styleUrl: './add-form.css'
})
export class AddForm {
  @Input() context: 'item' | 'list' = 'item';
  @Input() listId: number = 0;
  @Output() add = new EventEmitter<{ name: string; tag: string }>();

  newItemText: string = '';
  suggestions: Suggestion[] = [];
  newName: string = '';
  newTag: string = '';

  constructor(private itemService: ItemService) {}

  submit(form: NgForm) {
    if (this.context === 'item') {
      const text = this.newItemText.trim();
      if (!text) {
        return;
      }
      this.itemService.addItem(this.listId, text).subscribe(() => {
        form.resetForm();
        this.newItemText = '';
        this.suggestions = [];
      });
    } else {
      if (this.newName.trim()) {
        this.add.emit({name: this.newName, tag: this.newTag || 'indefinie'});
        form.resetForm();
      }
    }
  }

  searchSuggestions() {
    if (this.context !== 'item') {
      return;
    }
    const q = this.newItemText.trim();
    if (!q) {
      this.suggestions = [];
      return;
    }
    this.itemService.searchSuggestions(this.listId, q).subscribe(data => {
      this.suggestions = data;
    });
  }

  maybeAddSuggestion() {
    if (this.context !== 'item') {
      return;
    }
    const text = this.newItemText.trim();
    const match = this.suggestions.find(s => s.text.toLowerCase() === text.toLowerCase());
    if (match) {
      this.itemService.addItem(this.listId, match.text).subscribe(() => {
        this.newItemText = '';
        this.suggestions = [];
      });
    }
  }
}
