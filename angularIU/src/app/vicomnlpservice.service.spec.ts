/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { VicomnlpserviceService } from './vicomnlpservice.service';

describe('VicomnlpserviceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VicomnlpserviceService]
    });
  });

  it('should ...', inject([VicomnlpserviceService], (service: VicomnlpserviceService) => {
    expect(service).toBeTruthy();
  }));
});
