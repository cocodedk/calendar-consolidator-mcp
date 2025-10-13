# Data Types - Calendar Consolidator MCP

## Purpose
TypeScript interfaces for API data structures

## Core Types

### CalendarInfo
```typescript
interface CalendarInfo {
  id: string;
  name: string;
  type: "graph" | "caldav";
  canWrite: boolean;
}
```

### SourceConfig
```typescript
interface SourceConfig {
  type: "graph" | "caldav";
  calendarId: string;
  name: string;
  credentials: EncryptedCredentials;
  active: boolean;
}
```

### TargetConfig
```typescript
interface TargetConfig {
  type: "graph" | "caldav";
  calendarId: string;
  name: string;
  credentials: EncryptedCredentials;
}
```

### EncryptedCredentials
```typescript
interface EncryptedCredentials {
  encryptedBlob: string;
  // Actual structure stored encrypted
}
```

## Result Types

### SyncResult
```typescript
interface SyncResult {
  success: boolean;
  created: number;
  updated: number;
  deleted: number;
  errors: string[];
  duration: number; // milliseconds
}
```

### DiffSummary
```typescript
interface DiffSummary {
  wouldCreate: number;
  wouldUpdate: number;
  wouldDelete: number;
  sampleEvents: EventPreview[];
}
```

### EventPreview
```typescript
interface EventPreview {
  action: "create" | "update" | "delete";
  title: string;
  start: string; // ISO datetime
  end: string;   // ISO datetime
  sourceId?: number;
}
```

## Status Types

### StatusInfo
```typescript
interface StatusInfo {
  lastSync: string | null; // ISO datetime
  nextSync: string | null;
  activeSources: number;
  recentErrors: number;
  continuousSyncEnabled: boolean;
}
```

### SyncLog
```typescript
interface SyncLog {
  id: number;
  sourceId: number | null;
  timestamp: string; // ISO datetime
  status: "success" | "error" | "partial";
  createdCount: number;
  updatedCount: number;
  deletedCount: number;
  errorMessage: string | null;
  durationMs: number;
}
```
