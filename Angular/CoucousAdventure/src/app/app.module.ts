import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { ListProjectsComponent } from './list-projects/list-projects.component';
import { NewProjectRenderComponent } from './new-project-render/new-project-render.component';

import { ProjectsService } from './services/projects.service';
import { AuthService } from './services/auth.service';
import { HomeComponent } from './home/home.component';
import { NavigationComponent } from './navigation/navigation.component';
import { ProjectVueComponent } from './project-vue/project-vue.component';
import { FourOhFourComponent } from './four-oh-four/four-oh-four.component';
import { AuthGuard } from './services/authGuard.service';

const appRoutes: Routes = [
  { path: 'projects', canActivate: [AuthGuard], component: ListProjectsComponent },
  { path: 'projects/:id', canActivate: [AuthGuard], component: ProjectVueComponent},
  { path: '', component: HomeComponent },
  { path: 'not-found', component: FourOhFourComponent },
  { path: '**', redirectTo: 'not-found' }
]

@NgModule({
  declarations: [
    AppComponent,
    ListProjectsComponent,
    NewProjectRenderComponent,
    HomeComponent,
    NavigationComponent,
    ProjectVueComponent,
    FourOhFourComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [
    ProjectsService,
    AuthService,
    AuthGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
