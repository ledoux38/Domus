import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Item} from '../../models/interfaces';

@Injectable({
  providedIn: 'root'
})

export class ItemService {
  private apiUrl = 'http://localhost:5000/api/lists';

  constructor(private http: HttpClient) {
  }

  getItems(listId: number): Observable<Item[]> {
    return this.http.get<Item[]>(`${this.apiUrl}/${listId}/items`);
  }

  toggleItem(item_id: number): Observable<Item> {
    return this.http.patch<Item>(`${this.apiUrl}/items/${item_id}/toggle`, {});
  }

  deleteItem(item_id: number): Observable<Item|null> {
    return this.http.delete<Item|null>(`${this.apiUrl}/items/${item_id}`);
  }
}
