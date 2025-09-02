import {ComponentFixture, TestBed} from '@angular/core/testing';
import {AddForm} from './add-form';
import {HttpClientTestingModule} from '@angular/common/http/testing';

describe('AddForm', () => {
  let component: AddForm;
  let fixture: ComponentFixture<AddForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddForm, HttpClientTestingModule]
    }).compileComponents();

    fixture = TestBed.createComponent(AddForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
