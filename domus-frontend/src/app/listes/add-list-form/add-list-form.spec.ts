import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddListForm } from './add-list-form';

describe('AddListForm', () => {
  let component: AddListForm;
  let fixture: ComponentFixture<AddListForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddListForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddListForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
