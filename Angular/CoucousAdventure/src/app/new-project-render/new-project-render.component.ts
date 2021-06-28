import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-new-project-render',
  templateUrl: './new-project-render.component.html',
  styleUrls: ['./new-project-render.component.scss']
})
export class NewProjectRenderComponent implements OnInit {

  newProject = {
    title: "",
    description: "",
    image: {
      src: "",
      alt: ""
    }
  }

  constructor() { }

  ngOnInit(): void {
  }

}
