import {Component, EventEmitter, Input, Output, computed, effect, signal} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {Suggestion} from '../../models/interfaces';
import {ItemService} from '../../core/services/item-service';
import {TagService} from '../../core/services/tag-service';

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

  newItemText = signal('');
  newName = signal('');
  tagInput = signal('');
  private itemSuggestions = signal<Suggestion[]>([]);
  private tagSuggestions = signal<string[]>([]);
  suggestions = computed(() => this.context === 'item' ? this.itemSuggestions() : this.tagSuggestions());
  constructor(private itemService: ItemService, private tagService: TagService) {
    effect(() => {
      if (this.context === 'item') {
        const q = this.newItemText().trim();
        if (!q) {
          this.itemSuggestions.set([]);
          return;
        }
        this.itemService.searchSuggestions(this.listId, q).subscribe(data => this.itemSuggestions.set(data));
      } else {
        const q = this.tagInput().trim();
        if (!q) {
          this.tagSuggestions.set([]);
          return;
        }
        this.tagService.searchSuggestions(q).subscribe(data => this.tagSuggestions.set(data));
      }
    });
  }

  submit(form: NgForm) {
    if (this.context === 'item') {
      const text = this.newItemText().trim();
      if (!text) {
        return;
      }
      this.itemService.addItem(this.listId, text).subscribe(() => {
        form.resetForm();
        this.newItemText.set('');
        this.itemSuggestions.set([]);
      });
    } else {
      const name = this.newName().trim();
      if (!name) {
        return;
      }
      this.add.emit({name, tag: this.tagInput() || 'indefinie'});
      form.resetForm();
      this.tagSuggestions.set([]);
    }
  }

  maybeAddSuggestion() {
    if (this.context !== 'item') {
      return;
    }
    const text = this.newItemText().trim();
    const match = this.itemSuggestions().find(s => s.text.toLowerCase() === text.toLowerCase());
    if (match) {
      this.itemService.addItem(this.listId, match.text).subscribe(() => {
        this.newItemText.set('');
        this.itemSuggestions.set([]);
      });
    }
  }
}
