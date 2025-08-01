import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {ListCard} from '../../listes/list-card/list-card';

export interface List {
  id:number;
  name:string;
  tags:string;
  creation_date:string;
  }


@Injectable({providedIn: 'root'})
export class ListService {
  private apiUrl = 'http://localhost:5000/api/lists';

  constructor(private http: HttpClient) {
  }

  getLists(): Observable<ListCard[]> {
    return this.http.get<ListCard[]>(this.apiUrl);
  }

  addList(name: string, tag: string): Observable<List> {
    return this.http.post<List>(this.apiUrl, {name, tag});
  }

  deleteList(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

}
