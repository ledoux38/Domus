import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, map} from 'rxjs';

@Injectable({providedIn: 'root'})
export class TagService {
  private apiUrl = 'http://localhost:5000/api/tags';

  constructor(private http: HttpClient) {}

  searchSuggestions(q: string): Observable<string[]> {
    const params = {q};
    return this.http.get<{suggestions: string[]}>(`${this.apiUrl}/suggestions`, {params})
      .pipe(map(res => res.suggestions));
  }
}
