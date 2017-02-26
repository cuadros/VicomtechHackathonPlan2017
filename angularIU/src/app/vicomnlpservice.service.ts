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

/*  findDate(text: string): Observable<string> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    console.log('Calling analyzeText with text: ' + text);
    return this.http
      .post(this.path_analyze, JSON.stringify({ 'title': text }), options)
      .map((r: Response) => r.json() as string);
  }
*/
  analyzeText2(text: string): Observable<string> {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    console.log('Calling analyzeText with text: ' + text);
    return this.http
      .post(this.path_analyze, JSON.stringify({ 'title': text }), options)
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


  buscarEventos5(entradaEvento:Nerc): Observable<Event[]> {
//     return this.http.get(`${this.path_analyze_get}/?type=${entradaEvento.eventvicom}&municipality=${entradaEvento.loc}`).map((r: Response) => r.json() as Event[]);
     return this.http.get(`${this.path_analyze_get}/?type=${entradaEvento.eventvicom}&municipality=null`).map((r: Response) => r.json() as Event[]);

   }
   buscarEventosB(entradaEvento: Nerc): Observable<Event[]> {
     let texto="municipality=tolosa"
      return this.http.get(this.path_analyze_get + '?' + texto).map((r: Response) => r.json() as Event[]);
    }

  buscarEventosK(entradaEvento: Nerc): Observable<Event[]> {
    let texto="25/3/2017&municipality=tolosa"
     return this.http.get(this.path_analyze_get + '?date=' + texto).map((r: Response) => r.json() as Event[]);
   }

   buscarEventos2(municipality: string, eventType:string, date:string): Observable<Event[]> {
      return this.http.get(`${this.path_analyze_get}/?type=${eventType}&municipality=${municipality}`).map((r: Response) => r.json() as Event[]);
    }
    buscarEventos(entradaEvento:Nerc): Observable<Event[]> {
      let fecha="25/3/2017"
      let sitio:string;
      let evento:string;
      evento=null; sitio=null;
      let busqueda="date="+fecha;

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
      console.log(busqueda);
      return this.http.get(`${this.path_analyze_get}/?${busqueda}`).map((r: Response) => r.json() as Event[]);
     }

  getProba(user:string):string{
    console.log("holaaa, "+user);
    //return user;
    //return this.montseService.getUsers("uauauuaa");
    //return "<font color='red'>"+user+"</font>";
   //return "<alert type='info'>hello world!</alert>";
   //return  " <span class='alert alert-default'>New</span>"
  return "Uiii <span class='alert alert-success'>Aiiii</span>"
  }

}
