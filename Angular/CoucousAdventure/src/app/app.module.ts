import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { ListProjectsComponent } from './list-projects/list-projects.component';
import { NewProjectRenderComponent } from './new-project-render/new-project-render.component';

@NgModule({
  declarations: [
    AppComponent,
    ListProjectsComponent,
    NewProjectRenderComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
