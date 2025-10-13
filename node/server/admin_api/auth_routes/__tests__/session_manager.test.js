/**
 * Tests for session manager.
 */

import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import {
  createSession,
  getSession,
  updateSessionCredentials,
  updateSessionCalendars,
  updateSessionError,
  deleteSession
} from '../session_manager.js';

describe('Session Manager', () => {
  let sessionId;

  beforeEach(() => {
    sessionId = createSession('google', { flowData: 'test' });
  });

  it('creates session with unique ID', () => {
    expect(sessionId).toBeTruthy();
    expect(typeof sessionId).toBe('string');
  });

  it('retrieves session by ID', () => {
    const session = getSession(sessionId);
    expect(session).toBeTruthy();
    expect(session.type).toBe('google');
    expect(session.status).toBe('pending');
  });

  it('returns null for invalid session', () => {
    expect(getSession('invalid-id')).toBeNull();
  });

  it('updates session credentials', () => {
    const creds = { access_token: 'token123' };
    updateSessionCredentials(sessionId, creds);
    const session = getSession(sessionId);
    expect(session.credentials).toEqual(creds);
    expect(session.status).toBe('complete');
  });

  it('updates session calendars', () => {
    const calendars = [{ id: 'cal1', name: 'Calendar 1' }];
    updateSessionCalendars(sessionId, calendars);
    const session = getSession(sessionId);
    expect(session.calendars).toEqual(calendars);
  });

  it('updates session error', () => {
    updateSessionError(sessionId, 'Test error');
    const session = getSession(sessionId);
    expect(session.status).toBe('error');
    expect(session.error).toBe('Test error');
  });

  it('deletes session', () => {
    deleteSession(sessionId);
    expect(getSession(sessionId)).toBeNull();
  });

  it('expires old sessions', async () => {
    jest.useFakeTimers();
    const oldSessionId = createSession('graph', { flowData: 'old' });
    jest.advanceTimersByTime(11 * 60 * 1000); // 11 minutes
    expect(getSession(oldSessionId)).toBeNull();
    jest.useRealTimers();
  });
});
