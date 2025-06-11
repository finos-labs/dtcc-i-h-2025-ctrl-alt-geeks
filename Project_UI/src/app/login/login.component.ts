import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  standalone: false,
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  mockCredentials = {
    username: 'user',
    password: 'password',
  };

  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(private router: Router) {}

  login() {
    this.isLoading = true;

    // Simulate API call delay
    setTimeout(() => {
      // if (
      //   this.username === this.mockCredentials.username &&
      //   this.password === this.mockCredentials.password
      // ) {
      this.router.navigate(['/leads']);
      // } else {
      //   this.errorMessage = 'Invalid credentials. Please try again.';
      // }
      this.isLoading = false;
    }, 1000);
  }

  onSubmit() {
    this.clearError();
    this.login();
  }

  clearError() {
    this.errorMessage = '';
  }
}
