import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, Observable } from 'rxjs-compat'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  secondes: number = 0
  counterSubscription: Subscription = new Subscription();

  constructor() {}

  ngOnInit(): void {
    const counter = Observable.interval(1000)
    this.counterSubscription = counter.subscribe(
      value => { this.secondes = value },
      error => { console.log('Une erreur est survenue : ' + error) },
      () => { console.log('Observation terminée') }
    )
  }

  ngOnDestroy() {
    this.counterSubscription.unsubscribe()
  }

}
