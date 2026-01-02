module.exports = {
  // Renovate self-hosted configuration
  platform: 'gitea',
  endpoint: process.env.RENOVATE_ENDPOINT || 'http://gitea:3000',
  token: process.env.RENOVATE_TOKEN,

  // Repository discovery
  autodiscover: true,
  autodiscoverFilter: ['*/*'],

  // Logging
  logLevel: 'debug',
  logFile: '/tmp/renovate.log',
  logFileLevel: 'debug',

  // Git configuration
  gitAuthor: 'Renovate Bot <renovate@localhost>',

  // PR configuration
  onboarding: true,
  onboardingConfig: {
    extends: ['config:recommended'],
  },

  // Rate limiting
  prHourlyLimit: 10,
  prConcurrentLimit: 5,

  // Merge configuration
  automerge: false,
  automergeType: 'pr',

  // Dependency Dashboard
  dependencyDashboard: true,
  dependencyDashboardTitle: 'Dependency Dashboard',
};
