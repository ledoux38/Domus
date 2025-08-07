
import {ActivatedRoute} from '@angular/router';
import {ListService} from '../../core/services/list-service';
import {ItemService} from '../../core/services/item-service';
import {Item, List} from '../../models/interfaces';
import {Component, OnInit} from '@angular/core';
import {ItemCard} from '../item-card/item-card';

@Component({
  selector: 'app-list-detail',
  imports: [
    ItemCard
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
      this.items = data;
    });
  }

  toggleItem(item_id: number):void {
    this.itemService.toggleItem(item_id).subscribe(updatedItem => {
      const index = this.items.findIndex(i => i.id === updatedItem.id);
      if (index !== -1) {
        this.items[index] = updatedItem;
      }
    });
  }

  deleteItem(item_id: number):void {
    this.itemService.deleteItem(item_id).subscribe(() => {
      this.loadItems()
    });
  }
}
