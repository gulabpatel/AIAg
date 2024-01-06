import { MONTHS, DAYS } from './DateConstants';

const date = new Date();

// getWeekDays: Returns an array of week days starting from today. 
// For example, if today is Wednesday, it returns ["Wednesday", "Thursday", ..., "Tuesday"].
export function getWeekDays() {
  const dayInAWeek = new Date().getDay();
  const days = DAYS.slice(dayInAWeek, DAYS.length).concat(
    DAYS.slice(0, dayInAWeek)
  );
  return days;
}

// getDayMonthFromDate: Returns a string representing today's date in the format 'Day Month', 
// e.g., '24 Nov'. The month name is abbreviated to its first three letters.
export function getDayMonthFromDate() {
  const month = MONTHS[date.getMonth()].slice(0, 3);
  const day = date.getUTCDate();

  return day + ' ' + month;
}

// transformDateFormat: Converts the current date and time into a formatted string 
// in the format 'YYYY-MM-DD HH:MM:SS', using the local time.
export function transformDateFormat() {
  const month = date.toLocaleString('en-US', { month: '2-digit' });
  const day = date.toLocaleString('en-US', { day: '2-digit' });
  const year = date.getFullYear();
  const time = date.toLocaleString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hourCycle: 'h23',
  });

  const newFormatDate = year.toString().concat('-', month, '-', day, ' ', time);
  return newFormatDate;
}

// getUTCDatetime: Returns the current date and time in UTC format as a string.
// The date is in the format 'YYYY-MM-DD', and the time is in the format 'HH:MM', both in UTC.
export function getUTCDatetime() {
  const utcTime = date.toLocaleString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
    timeZone: 'UTC',
  });

  const isoDateString = new Date().toISOString();
  const utcDate = isoDateString.split('T')[0].concat(' ', utcTime);
  return utcDate;
}

// getUTCTime: Returns the current time in UTC format as a string, in the format 'HH:MM:SS'.
export function getUTCTime() {
  const utcTime = date.toLocaleString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hourCycle: 'h23',
    timeZone: 'UTC',
  });

  return utcTime;
}
