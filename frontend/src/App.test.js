import { render, screen } from '@testing-library/react';
import App from './App';

test('renders navigation', () => {
  render(<App />);
  const brandElement = screen.getByText(/Vibe Fitness/i);
  expect(brandElement).toBeInTheDocument();
});

test('renders home page by default', () => {
  render(<App />);
  const headingElement = screen.getByText(/Welcome to Vibe Fitness/i);
  expect(headingElement).toBeInTheDocument();
});
