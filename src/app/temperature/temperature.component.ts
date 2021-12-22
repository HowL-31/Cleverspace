import { Component } from '@angular/core';
import { FormControl, FormGroup } from "@angular/forms";
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.css']
})


export class TemperatureComponent {

  constructor(
    private http: HttpClient
  ){}
  // private http: HttpClient;
  image = new FormControl('');
  CityForm = new FormGroup({
    cityName : new FormControl(''),
  })
  url: any = '';
  public show = false;
  public div = false;

  onSubmit(){
    var formData: any = new FormData();
    
    // console.log(this.CityForm.get('cityName')?.value);
    formData.append("city", this.CityForm.get('cityName')?.value);
    console.log(formData);
    this.url = '';
    this.div = false;
    this.show = true;
    // var div: unknown = document.getElementById('img')
    console.log(this.url)
    this.http.post('http://127.0.0.1:8000/api/historical', formData).subscribe(
    (response) => {console.log(response);
        this.show = false;
        this.div = true;
        var src: any = response;
        this.url = response;
      },
      (error) => console.log(error)
    )
  }
}
