import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthService } from '../services/auth.service'
import { Router } from '@angular/router';
import { Subscription } from 'rxjs-compat';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit, OnDestroy {

  isAuth: boolean = false
  isAuthSub: Subscription = new Subscription();

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.isAuthSub = this.authService.isUserAuthenticated$.subscribe(
      data => { this.isAuth = data },
      error => { console.log('Une erreur est survenue ' + error) },
      () => { console.log('Observation terminée') }
    );
  }

  ngOnDestroy(): void {
    this.isAuthSub.unsubscribe()
  }

  onLogin() {
    this.authService.login()
    this.router.navigate([''])
  }

}
