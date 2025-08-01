import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app'; // ou './app/app.component' selon le nom
import {appConfig} from './app/app.config';

bootstrapApplication(App, appConfig)
  .catch(err => console.error(err));
