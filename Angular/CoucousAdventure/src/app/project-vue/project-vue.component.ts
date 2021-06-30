import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProjectsService } from '../services/projects.service';

@Component({
  selector: 'app-project-vue',
  templateUrl: './project-vue.component.html',
  styleUrls: ['./project-vue.component.scss']
})
export class ProjectVueComponent implements OnInit {

  id: number = 0

  constructor(private activatedRoute: ActivatedRoute, private projectsService: ProjectsService, private router: Router) {}

  ngOnInit(): void {
    const idTmp = this.activatedRoute.snapshot.params['id']
    if (idTmp >= this.projectsService.projects.length) {
      this.router.navigate(['not-found'])
    }
    else {
      this.id = idTmp
    }
  }

}
