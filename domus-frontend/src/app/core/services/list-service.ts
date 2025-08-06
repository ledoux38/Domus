import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {List} from '../../models/interfaces';

@Injectable({providedIn: 'root'})
export class ListService {
  private apiUrl = 'http://localhost:5000/api/lists';

  constructor(private http: HttpClient) {
  }

  getLists(): Observable<List[]> {
    return this.http.get<List[]>(this.apiUrl);
  }

  addList(name: string, tag: string): Observable<List> {
    return this.http.post<List>(this.apiUrl, {name, tag});
  }

  deleteList(listId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${listId}`);
  }

  getList(listId: number): Observable<List> {
    return this.http.get<any>(`${this.apiUrl}/${listId}`);
  }

}
