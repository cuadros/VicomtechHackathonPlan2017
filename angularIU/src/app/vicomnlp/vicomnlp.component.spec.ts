/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { VicomnlpComponent } from './vicomnlp.component';

describe('VicomnlpComponent', () => {
  let component: VicomnlpComponent;
  let fixture: ComponentFixture<VicomnlpComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VicomnlpComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VicomnlpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
