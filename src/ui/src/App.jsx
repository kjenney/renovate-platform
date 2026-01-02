import React, { useState, useEffect } from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';
import PullRequestList from './components/PullRequestList';
import './App.css';

const client = new ApolloClient({
  uri: '/graphql',
  cache: new InMemoryCache(),
});

const HEALTH_QUERY = gql`
  query Health {
    health
    version
  }
`;

function HealthStatus() {
  const { loading, error, data } = useQuery(HEALTH_QUERY);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error connecting to API</p>;

  return (
    <div className="health-status">
      <p>API Status: {data.health}</p>
      <p>Version: {data.version}</p>
    </div>
  );
}

function App() {
  const [apiStatus, setApiStatus] = useState('checking...');

  useEffect(() => {
    fetch('/health')
      .then(response => {
        if (!response.ok) {
          throw new Error('API returned error status');
        }
        return response.json();
      })
      .then(data => setApiStatus(data?.status || 'unknown'))
      .catch(() => setApiStatus('disconnected'));
  }, []);

  return (
    <ApolloProvider client={client}>
      <div className="App">
        <header className="App-header">
          <h1>Renovate Platform</h1>
          <p>Manage your self-hosted Renovate installation</p>
          <div className="status-container">
            <p>REST API: {apiStatus}</p>
            <HealthStatus />
          </div>
        </header>
        <main className="App-main">
          <PullRequestList />
        </main>
      </div>
    </ApolloProvider>
  );
}

export default App;
