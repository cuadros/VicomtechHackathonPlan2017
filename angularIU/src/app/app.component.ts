import { Component } from '@angular/core';
import { VicomnlpComponent } from './vicomnlp/vicomnlp.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [VicomnlpComponent]
})
export class AppComponent {
  title = '¿Me das alguna idea sobre ... ?';
  lat: number =  43.292239;
  lng: number =  -1.985692;



}
