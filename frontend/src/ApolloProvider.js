// src/ApolloProvider.js
import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider as Provider, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

// Setup HTTP link to your GraphQL server
const httpLink = createHttpLink({
  uri: 'http://127.0.0.1:8000/graphql/', // your Django server URL
});

// Setup Auth link for passing token
const authLink = setContext(() => {
  const token = localStorage.getItem('token');
  return {
    headers: {
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

// Create Apollo client
const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});

function ApolloProvider({ children }) {
  return <Provider client={client}>{children}</Provider>;
}

export default ApolloProvider;
