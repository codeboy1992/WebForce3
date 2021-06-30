import { BehaviorSubject } from 'rxjs-compat'

export class AuthService {

  isUserAuthenticated$ = new BehaviorSubject<boolean>(false)

  constructor() {}

  login() {
    this.isUserAuthenticated$.next(true)
  }
}