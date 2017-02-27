import { Component, OnInit } from '@angular/core';
import {VicomnlpService} from '../vicomnlpservice.service'
import {Event} from '../model/event'
import {Nerc} from '../model/nerc'

import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';

import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/of';


@Component({
  selector: 'app-vicomnlp',
  templateUrl: './vicomnlp.component.html',
  styleUrls: ['./vicomnlp.component.css'],
  providers: [VicomnlpService]

})
export class VicomnlpComponent implements OnInit {

  private currentSearchSubject = new Subject<string>();
  // Esta es la variable que recogerá el resultado Observable del servicio (lista de eventos en este caso de ejemplo)
  private resultObservable: Observable<Nerc[]>;
// Esta es la variable que recogerá los resultados de los Observables
  private searchResult: Nerc[] = [];

  private currentSearchSubject2 = new Subject<Nerc>();
  // Esta es la variable que recogerá el resultado Observable del servicio (lista de eventos en este caso de ejemplo)
  private resultObservable2: Observable<Event[]>;
  // Esta es la variable que recogerá los resultados de los Observables
  private searchResult2: Event[] = [];

  output_get:Event[];
  output_post:Nerc[];
  busqueda:Nerc[];
  evento:string;
  sitio:string;
  output_time:string;
  fecha:string;
  constructor(private vicomnlpservice: VicomnlpService) {


  }
//  constructor() {}

  funcionAuxiliar (resultatBusqueda:string){
    this.currentSearchSubject.next(resultatBusqueda);
  //  this.convertirFecha("hoy");
    let entradaBuscador:Nerc;
    for (let entry of this.searchResult) {
      entradaBuscador=entry;
      this.currentSearchSubject2.next(entradaBuscador)

      }
  }


  convertirFecha(fecha:string){
    let output_time:string;
    this.vicomnlpservice.findDate(fecha).subscribe(x=>this.output_time=x);

  }



  ngOnInit() {
    this.resultObservable = this.currentSearchSubject
      .debounceTime(300)        // wait for 300ms pause in events
      .distinctUntilChanged()   // ignore if next search term is same as previous
      .switchMap(text => text   // switch to new observable each time
        // return the http search observable
        ? this.vicomnlpservice.analyzeText(text)
        // or the observable of empty heroes if no search term
        : Observable.of<Nerc[]>([]))
      .catch(error => {
        // TODO: real error handling
        console.log(error);
        return Observable.of<Nerc[]>([]);
      });
    this.resultObservable.subscribe(x => this.searchResult = x);

    this.resultObservable2 = this.currentSearchSubject2
      .debounceTime(300)        // wait for 300ms pause in events
      .distinctUntilChanged()   // ignore if next search term is same as previous
      // le puedo pasar 3 parametros aqui??? cAAAH
      .switchMap(text => text   // switch to new observable each time
        // return the http search observable
        ? this.vicomnlpservice.buscarEventos(text)
        // or the observable of empty heroes if no search term
        : Observable.of<Event[]>([]))
      .catch(error => {
        // TODO: real error handling
        console.log(error);
        return Observable.of<Event[]>([]);
      });
    this.resultObservable2.subscribe(x => this.searchResult2 = x);



  }



}
