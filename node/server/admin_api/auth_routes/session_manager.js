/**
 * Session manager for OAuth flows.
 * Stores temporary authentication state in memory.
 */

import crypto from 'crypto';

const sessions = new Map();
const SESSION_TIMEOUT_MS = 10 * 60 * 1000;

/**
 * Create a new OAuth session.
 */
export function createSession(type, flowData) {
  const sessionId = crypto.randomBytes(16).toString('hex');
  const session = {
    id: sessionId,
    type,
    flowData,
    status: 'pending',
    credentials: null,
    calendars: null,
    error: null,
    createdAt: Date.now(),
    expiresAt: Date.now() + SESSION_TIMEOUT_MS
  };
  sessions.set(sessionId, session);
  setTimeout(() => sessions.delete(sessionId), SESSION_TIMEOUT_MS);
  return sessionId;
}

/**
 * Get session by ID.
 */
export function getSession(sessionId) {
  const session = sessions.get(sessionId);
  if (!session) return null;
  if (Date.now() > session.expiresAt) {
    sessions.delete(sessionId);
    return null;
  }
  return session;
}

/**
 * Update session with credentials.
 */
export function updateSessionCredentials(sessionId, credentials) {
  const session = getSession(sessionId);
  if (!session) {
    throw new Error('Session not found or expired');
  }
  session.credentials = credentials;
  session.status = 'complete';
  sessions.set(sessionId, session);
}

/**
 * Update session with calendars.
 */
export function updateSessionCalendars(sessionId, calendars) {
  const session = getSession(sessionId);
  if (!session) {
    throw new Error('Session not found or expired');
  }
  session.calendars = calendars;
  sessions.set(sessionId, session);
}

/**
 * Update session with error.
 */
export function updateSessionError(sessionId, error) {
  const session = getSession(sessionId);
  if (session) {
    session.status = 'error';
    session.error = error;
    sessions.set(sessionId, session);
  }
}

/**
 * Delete session.
 */
export function deleteSession(sessionId) {
  sessions.delete(sessionId);
}
