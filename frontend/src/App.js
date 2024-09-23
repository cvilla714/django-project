// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import UploadPage from './pages/UploadPage';
import ApolloProvider from './ApolloProvider';

function App() {
  return (
    <ApolloProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </Router>
    </ApolloProvider>
  );
}

export default App;
