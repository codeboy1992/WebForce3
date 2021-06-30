import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-new-project-render',
  templateUrl: './new-project-render.component.html',
  styleUrls: ['./new-project-render.component.scss']
})
export class NewProjectRenderComponent implements OnInit {

  @Input() title: string = ""
  @Input() description: string = ""

  redColor = "red"

  isProjectRendered: boolean = false

  newProject = {
    title: "",
    description: "",
    image: {
      src: "",
      alt: ""
    }
  }

  constructor() {
    
  }

  ngOnInit(): void {
    this.newProject.title = this.title
    this.newProject.description = this.description
  }

  newProjectRender(): void {
    this.isProjectRendered = true
  }

}
