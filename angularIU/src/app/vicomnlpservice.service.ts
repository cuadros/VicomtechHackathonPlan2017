import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import {Observable} from 'rxjs/Rx';
import 'rxjs/add/operator/map';

import {Event} from './model/event'
import {Nerc} from './model/nerc'

@Injectable()
export class VicomnlpService {

  constructor(private http: Http) {}
  private path_analyze= 'http://localhost:5065/analyze';
  private path_findDates= 'http://localhost:5067/findDates';
  private path_analyze_get= 'http://localhost:8080/events';

  findDate(text: string): Observable<string> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    console.log('Calling analyzeText with text: ' + text);
    return this.http
      .post(this.path_findDates, JSON.stringify({ 'title': text }), options)
      .map((r: Response) => r.json() as string);
  }



  analyzeText(text: string): Observable<Nerc[]> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    console.log('Calling analyzeText with text: ' + text);
    return this.http
      .post(this.path_analyze, JSON.stringify({ 'title': text }), options)
      .map((r: Response) => r.json() as Nerc[]);
  }



    buscarEventos(entradaEvento:Nerc): Observable<Event[]> {
      let fecha="25/3/2017"
      let sitio:string;
      let evento:string;
      evento=null; sitio=null;
      let busqueda:string;

      if (entradaEvento.eventvicom){
        evento=entradaEvento.eventvicom;
        if (busqueda) {busqueda=busqueda+"&type="+evento;}
        else{busqueda="type="+evento}
      }
      if (entradaEvento.loc){
        sitio=entradaEvento.loc;
        if (busqueda) {busqueda=busqueda+"&municipality="+sitio;}
        else{busqueda="municipality="+sitio}
      }
      if (entradaEvento.vicomdate){
        if (busqueda) {busqueda=busqueda+"&date="+fecha;}
        else{busqueda="date="+fecha}
      }
      console.log(busqueda);
      return this.http.get(`${this.path_analyze_get}/?${busqueda}`).map((r: Response) => r.json() as Event[]);
     }



}
