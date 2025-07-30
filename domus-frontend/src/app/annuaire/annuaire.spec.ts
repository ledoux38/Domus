import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Annuaire } from './annuaire';

describe('Annuaire', () => {
  let component: Annuaire;
  let fixture: ComponentFixture<Annuaire>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Annuaire]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Annuaire);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
