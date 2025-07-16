import { render, screen } from '@testing-library/react';
import App from './App';
jest.mock('axios');

test('renders login heading and button', () => {
  render(<App />);
  // Check for the Login heading
  const heading = screen.getByRole('heading', { name: /login/i });
  expect(heading).toBeInTheDocument();
  // Check for the Login button
  const button = screen.getByRole('button', { name: /login/i });
  expect(button).toBeInTheDocument();
});
