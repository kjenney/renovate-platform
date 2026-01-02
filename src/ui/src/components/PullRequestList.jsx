import React from 'react';
import { gql, useQuery } from '@apollo/client';
import './PullRequestList.css';

const OPEN_PULL_REQUESTS_QUERY = gql`
  query OpenPullRequests {
    openPullRequests {
      id
      number
      title
      state
      htmlUrl
      createdAt
      updatedAt
      userLogin
      userAvatarUrl
      repoOwner
      repoName
      headBranch
      baseBranch
    }
  }
`;

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function PullRequestCard({ pr }) {
  return (
    <div className="pr-card">
      <div className="pr-header">
        <img
          src={pr.userAvatarUrl}
          alt={pr.userLogin}
          className="pr-avatar"
        />
        <div className="pr-title-section">
          <a
            href={pr.htmlUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="pr-title"
          >
            {pr.title}
          </a>
          <div className="pr-meta">
            <span className="pr-repo">{pr.repoOwner}/{pr.repoName}</span>
            <span className="pr-number">#{pr.number}</span>
          </div>
        </div>
      </div>
      <div className="pr-details">
        <div className="pr-branches">
          <span className="pr-branch">{pr.headBranch}</span>
          <span className="pr-arrow">→</span>
          <span className="pr-branch">{pr.baseBranch}</span>
        </div>
        <div className="pr-info">
          <span className="pr-author">by {pr.userLogin}</span>
          <span className="pr-date">opened {formatDate(pr.createdAt)}</span>
        </div>
      </div>
    </div>
  );
}

function PullRequestList() {
  const { loading, error, data, refetch } = useQuery(OPEN_PULL_REQUESTS_QUERY, {
    pollInterval: 30000, // Refresh every 30 seconds
  });

  if (loading) {
    return (
      <div className="pr-list-container">
        <h2>Open Pull Requests</h2>
        <div className="pr-loading">Loading pull requests...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="pr-list-container">
        <h2>Open Pull Requests</h2>
        <div className="pr-error">
          Error loading pull requests: {error.message}
        </div>
      </div>
    );
  }

  const pullRequests = data?.openPullRequests || [];

  return (
    <div className="pr-list-container">
      <div className="pr-list-header">
        <h2>Open Pull Requests</h2>
        <button onClick={() => refetch()} className="pr-refresh-btn">
          Refresh
        </button>
      </div>
      {pullRequests.length === 0 ? (
        <div className="pr-empty">No open pull requests found.</div>
      ) : (
        <div className="pr-list">
          <div className="pr-count">{pullRequests.length} open pull request{pullRequests.length !== 1 ? 's' : ''}</div>
          {pullRequests.map((pr) => (
            <PullRequestCard key={pr.id} pr={pr} />
          ))}
        </div>
      )}
    </div>
  );
}

export default PullRequestList;
