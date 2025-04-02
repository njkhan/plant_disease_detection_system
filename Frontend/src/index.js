import React from 'react';
import ReactDOM from 'react-dom';  // Use 'react-dom' instead of 'react-dom/client' for React 17
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();
