import { render, screen } from '@testing-library/react';
import App from './App';
jest.mock('axios');

test('renders login form elements', () => {
  render(<App />);
  // Check for username and password inputs and login button
  const username = screen.getByPlaceholderText(/username/i);
  const password = screen.getByPlaceholderText(/password/i);
  const button = screen.getByRole('button', { name: /login/i });

  expect(username).toBeInTheDocument();
  expect(password).toBeInTheDocument();
  expect(button).toBeInTheDocument();
});
