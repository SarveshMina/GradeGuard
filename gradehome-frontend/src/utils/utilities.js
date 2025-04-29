// utilities.js -------------------------------------------------------------
/**
 * Take { date: '2025-04-28', time: '09:00' } that you know is UTC
 * and return the hour / minute in *local* time.
 */
export function utcToLocalHM(dateStr, timeStr) {
    // Ensure we have “seconds” so the Date ctor is happy
    const iso = `${dateStr}T${timeStr.padEnd(8, ':00')}Z`; // Z = UTC
    const d   = new Date(iso);              // browser converts to local TZ
    return { h: d.getHours(), m: d.getMinutes() };
  }
  