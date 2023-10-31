import { render, screen } from '@testing-library/react';
import App from './App.js';

// Test Case for Text

test('renders Location Data as a Text ', async() => {
  render(<App />);
  
  const locDataElement = await screen.getByText('LOCATION DATA');
  expect(locDataElement).toBeInTheDocument();
});
