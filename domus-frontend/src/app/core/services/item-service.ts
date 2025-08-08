import {Observable, map} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Item, Suggestion} from '../../models/interfaces';

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

  addItem(listId: number, text: string): Observable<Item> {
    return this.http.post<Item>(`${this.apiUrl}/${listId}/items`, {text});
  }

  searchSuggestions(listId: number, q: string): Observable<Suggestion[]> {
    return this.http.get<{suggestions: Suggestion[]}>(`${this.apiUrl}/${listId}/suggestions`, {params: {q}})
      .pipe(map(res => res.suggestions));
  }

  toggleItem(item_id: number): Observable<Item> {
    return this.http.patch<Item>(`${this.apiUrl}/items/${item_id}/toggle`, {});
  }

  deleteItem(item_id: number): Observable<Item|null> {
    return this.http.delete<Item|null>(`${this.apiUrl}/items/${item_id}`);
  }
}
