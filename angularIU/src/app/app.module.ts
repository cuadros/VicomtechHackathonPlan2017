import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ApplicationRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { VicomnlpComponent } from './vicomnlp/vicomnlp.component';
import { AgmCoreModule } from 'angular2-google-maps/core';


import {VicomnlpService} from './vicomnlpservice.service';

@NgModule({
  declarations: [
    AppComponent,
    VicomnlpComponent

  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCakT_nyrSoS52r7Qw8sUWRiozH9s6Ej08'
    })
  ],
  providers: [VicomnlpService],
  bootstrap: [AppComponent]
})
export class AppModule { }
