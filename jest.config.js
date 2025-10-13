/**
 * Jest configuration for ES modules.
 */

export default {
  testEnvironment: 'node',
  transform: {},
  testMatch: ['**/__tests__/**/*.test.js'],
  collectCoverageFrom: [
    'node/server/**/*.js',
    '!node/server/**/__tests__/**'
  ]
};
