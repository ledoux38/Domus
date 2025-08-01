import {Component, EventEmitter, Output} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';

@Component({
  selector: 'app-add-list-form',
  imports: [
    FormsModule
  ],
  templateUrl: './add-list-form.html',
  standalone: true,
  styleUrl: './add-list-form.css'
})
export class AddListForm {
  newName: string = '';
  newTag: string = '';

  @Output() add = new EventEmitter<{ name: string, tag: string }>();

  addList(form: NgForm) {
    if (this.newName.trim()) {

      this.add.emit({name: this.newName, tag: this.newTag || 'indefinie'});
      form.resetForm();
    }
  }
}
