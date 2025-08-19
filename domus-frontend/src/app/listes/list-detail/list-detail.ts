import {ActivatedRoute} from '@angular/router';
import {ListService} from '../../core/services/list-service';
import {ItemService} from '../../core/services/item-service';
import {Item, List, Suggestion} from '../../models/interfaces';
import {Component, OnInit} from '@angular/core';
import {ItemCard} from '../item-card/item-card';
import {FormsModule, NgForm} from '@angular/forms';
import {AddItemForm} from '../add-item-form/add-item-form';

@Component({
  selector: 'app-list-detail',
  imports: [
    ItemCard,
    FormsModule,
    AddItemForm
  ],
  templateUrl: './list-detail.html',
  standalone: true,
  styleUrl: './list-detail.css'
})
export class ListDetail implements OnInit {
  listId: number = 0;
  list: List | null = null;
  items: Item[] = [];


  constructor(private route: ActivatedRoute,
              private listService: ListService,
              private itemService: ItemService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.listId = +params['id'];
      this.loadList();
      this.loadItems()
    });
  }

  loadList() {
    this.listService.getList(this.listId).subscribe(data => {
      this.list = data;
    });
  }

  loadItems() {
    this.itemService.getItems(this.listId).subscribe(data => {
      this.items = [...data];
    });
  }

  deleteItem(item_id ?: number) {
    this.items = this.items.filter(item => item.id !== item_id);
  }
}
