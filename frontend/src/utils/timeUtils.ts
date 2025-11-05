/**
 * Time utility functions for timezone handling
 * Frontend displays user's local timezone
 * Server keeps server timezone
 */

/**
 * Get user's timezone name
 */
export function getUserTimezone(): string {
  return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

/**
 * Get timezone abbreviation (e.g., PST, EST, GMT+7)
 */
export function getTimezoneAbbr(): string {
  const date = new Date();
  const tzString = date.toLocaleTimeString('en-US', { timeZoneName: 'short' });
  const match = tzString.match(/\b[A-Z]{2,5}\b|\bGMT[+-]\d+\b/);
  return match ? match[0] : '';
}

/**
 * Format date for display in user's timezone
 */
export function formatLocalDateTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true,
    timeZoneName: 'short'
  });
}

/**
 * Format time only
 */
export function formatLocalTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  });
}

/**
 * Format date only
 */
export function formatLocalDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

/**
 * Get UTC offset in hours
 */
export function getUTCOffset(): string {
  const offset = -new Date().getTimezoneOffset();
  const hours = Math.floor(Math.abs(offset) / 60);
  const minutes = Math.abs(offset) % 60;
  const sign = offset >= 0 ? '+' : '-';
  return `UTC${sign}${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}
