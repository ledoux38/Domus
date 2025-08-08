import {Component, EventEmitter, Output} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';

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

  @Output() add = new EventEmitter<{ item: string }>();

  addItem(form: NgForm) {
  }
}
