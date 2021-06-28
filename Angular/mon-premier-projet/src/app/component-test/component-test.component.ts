import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-component-test',
  templateUrl: './component-test.component.html',
  styleUrls: ['./component-test.component.scss']
})
export class ComponentTestComponent implements OnInit {

  titre: string = "";
  isAuth: boolean = false;
  text: string = ""

  constructor() {
  }

  ngOnInit(): void {
  }

  onConnect(): void {
    this.isAuth = true
  }

}
