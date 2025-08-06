import { Routes } from '@angular/router';

import { Agenda } from './agenda/agenda';
import { Listes } from './listes/listes';
import { Annuaire } from './annuaire/annuaire';
import { Temperature } from './temperature/temperature';
import {ListDetail} from './listes/list-detail/list-detail';

export const routes: Routes = [
  { path: 'agenda', component: Agenda },
  { path: 'annuaire', component: Annuaire },
  { path: 'listes', component: Listes },
  { path: 'listes/:id', component: ListDetail },
  { path: 'temperature', component: Temperature },
  { path: '', redirectTo: '/listes', pathMatch: 'full' },
  { path: '**', redirectTo: '/listes' }
];
