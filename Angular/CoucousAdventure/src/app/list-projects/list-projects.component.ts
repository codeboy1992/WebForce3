import { Component, OnInit } from '@angular/core';
import { ProjectsService } from '../services/projects.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list-projects',
  templateUrl: './list-projects.component.html',
  styleUrls: ['./list-projects.component.scss']
})
export class ListProjectsComponent implements OnInit {

  projects: any[] = this.projectsService.projects;

  constructor(private projectsService: ProjectsService, private router: Router) {}

  ngOnInit(): void {
  }

  onClickProject(id: number): void {
    this.router.navigate(['projects/' + id])
  }

}
