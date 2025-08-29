import {Component, OnInit} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {ChangeDetectorRef} from '@angular/core';
import {AddForm} from './add-form/add-form';
import {ListService} from '../core/services/list-service';
import {List} from '../models/interfaces';
import {ListCard} from './list-card/list-card';

@Component({
  selector: 'app-listes',
  imports: [
    FormsModule,
    AddForm,
    ListCard
  ],
  templateUrl: './listes.html',
  standalone: true,
  styleUrl: './listes.css'
})
export class Listes implements OnInit {
  lists: List[] = [];

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
