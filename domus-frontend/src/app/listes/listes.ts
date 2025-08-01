import {Component, OnInit} from '@angular/core';
import {List, ListService} from '../core/services/listService';
import {FormsModule, NgForm} from '@angular/forms';
import {RouterLink} from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
@Component({
  selector: 'app-listes',
  imports: [
    FormsModule,
    RouterLink
  ],
  templateUrl: './listes.html',
  standalone: true,
  styleUrl: './listes.css'
})
export class Listes implements OnInit {
  lists: List[] = [];
  newName: string = '';
  newTag: string = '';

  constructor(private listService: ListService, private cdr: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.loadLists();
  }

  loadLists(): void {
    this.listService.getLists().subscribe(lists => {
      this.lists = [...lists]
      this.cdr.detectChanges();
    });

  }

  addList(form: NgForm) {
    if (this.newName.trim()) {
      this.listService.addList(this.newName, this.newTag || 'indefinie').subscribe(() => {
        this.newName = '';
        this.newTag = '';
        form.resetForm();
        this.loadLists();
      });
    }
  }

  trackById(index: number, item: any): number {
    return item.id;
  }

  deleteList(list: List) {
    if (confirm(`supprimer la liste "${list.name}" ?`)) {
      this.listService.deleteList(list.id).subscribe(() => {
        this.loadLists();
      });
    }
  }
}
