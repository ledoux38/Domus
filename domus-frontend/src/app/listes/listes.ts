import {Component, OnInit} from '@angular/core';
import {List, ListService} from '../core/services/listService';
import {FormsModule, NgForm} from '@angular/forms';
import {ChangeDetectorRef} from '@angular/core';
import {ListCard} from './list-card/list-card';
import {AddListForm} from './add-list-form/add-list-form';

@Component({
  selector: 'app-listes',
  imports: [
    FormsModule,
    ListCard,
    AddListForm
  ],
  templateUrl: './listes.html',
  standalone: true,
  styleUrl: './listes.css'
})
export class Listes implements OnInit {
  lists: ListCard[] = [];

  constructor(private listService: ListService, private cdr: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.loadLists();
  }

  addList({name, tag}: { name: string, tag: string }) {
    this.listService.addList(name, tag).subscribe(() => {
      this.loadLists();
    });
  }

  loadLists(): void {
    this.listService.getLists().subscribe(lists => {
      this.lists = [...lists]
      this.cdr.detectChanges();
    });

  }

  deleteList({id}: { id: number }) {
    if (confirm(`supprimer la liste ?`)) {
      this.listService.deleteList(id).subscribe(() => {
        this.loadLists();
      });
    }
  }
}
