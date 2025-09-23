import {Component, EventEmitter, Input, Output, computed, signal} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {Suggestion} from '../../models/interfaces';
import {ItemService} from '../../core/services/item-service';
import {TagService} from '../../core/services/tag-service';

type SuggestionsResult =
  | { kind: 'item'; values: Suggestion[] }
  | { kind: 'tag'; values: string[] };

@Component({
  selector: 'app-add-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './add-form.html',
  styleUrl: './add-form.css'
})
export class AddForm {
  private readonly contextSignal = signal<'item' | 'list'>('item');
  private readonly itemSuggestionsSignal = signal<Suggestion[]>([]);
  private readonly tagSuggestionsSignal = signal<string[]>([]);

  protected readonly suggestions = computed<SuggestionsResult>(() =>
    this.contextSignal() === 'item'
      ? {kind: 'item', values: this.itemSuggestionsSignal()}
      : {kind: 'tag', values: this.tagSuggestionsSignal()}
  );

  @Input()
  set context(value: 'item' | 'list' | undefined) {
    this.contextSignal.set(value ?? 'item');
  }

  get context(): 'item' | 'list' {
    return this.contextSignal();
  }
  @Input() listId: number = 0;
  @Output() add = new EventEmitter<{ name: string; tag: string }>();

  newItemText: string = '';
  newName: string = '';
  tagInput: string = '';

  constructor(private itemService: ItemService, private tagService: TagService) {}

  submit(form: NgForm) {
    if (this.context === 'item') {
      const text = this.newItemText.trim();
      if (!text) {
        return;
      }
      this.itemService.addItem(this.listId, text).subscribe(() => {
        form.resetForm();
        this.newItemText = '';
        this.itemSuggestionsSignal.set([]);
      });
    } else {
      const name = this.newName.trim();
      if (!name) {
        return;
      }
      this.add.emit({name, tag: this.tagInput || 'indefinie'});
      form.resetForm();
      this.tagSuggestionsSignal.set([]);
    }
  }

  searchSuggestions() {
    if (this.context === 'item') {
      const q = this.newItemText.trim();
      if (!q) {
        this.itemSuggestionsSignal.set([]);
        return;
      }
      this.itemService.searchSuggestions(this.listId, q).subscribe(data => {
        this.itemSuggestionsSignal.set(data);
      });
    } else {
      const q = this.tagInput.trim();
      if (!q) {
        this.tagSuggestionsSignal.set([]);
        return;
      }
      this.tagService.searchSuggestions(q).subscribe(data => {
        this.tagSuggestionsSignal.set(data);
      });
    }
  }

  maybeAddSuggestion() {
    if (this.context !== 'item') {
      return;
    }
    const text = this.newItemText.trim();
    const match = this.itemSuggestionsSignal().find(s => s.text.toLowerCase() === text.toLowerCase());
    if (match) {
      this.itemService.addItem(this.listId, match.text).subscribe(() => {
        this.newItemText = '';
        this.itemSuggestionsSignal.set([]);
      });
    }
  }
}
