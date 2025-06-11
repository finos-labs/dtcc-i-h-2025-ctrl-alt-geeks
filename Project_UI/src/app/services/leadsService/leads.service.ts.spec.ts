import { TestBed } from '@angular/core/testing';

import { LeadsServiceTs } from './leads.service.ts';

describe('LeadsServiceTs', () => {
  let service: LeadsServiceTs;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LeadsServiceTs);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
