/* ============================================================
 * state.js — Reference State Manager
 * ============================================================
 * Single global STATE object, plus loadAllData() and helpers.
 * The dashboard is small enough that we don't need Redux/MobX.
 * ============================================================ */

const STATE = {
  index: null,           // data/index.json — lightweight per-day summaries
  daysData: {},          // { date: { platform: { total_messages, channels, ... } } }
  currentDate: null,     // selected date (YYYY-MM-DD)
  currentPlatform: 'all', // 'all' | 'discord' | 'facebook' | ...
  currentRoute: 'home',  // current page
  loaded: false,
};

async function loadAllData() {
  // 1. Load the index
  const idxRes = await fetch('./data/index.json');
  if (!idxRes.ok) throw new Error(`Failed to load index.json: ${idxRes.status}`);
  STATE.index = await idxRes.json();

  if (!STATE.index.days || STATE.index.days.length === 0) {
    throw new Error('index.json has no days');
  }

  // 2. Set the default date to the most recent
  STATE.currentDate = STATE.index.days[STATE.index.days.length - 1].date;

  // 3. Load all daily files in parallel
  const promises = [];
  for (const day of STATE.index.days) {
    for (const platform of Object.keys(day.platforms || {})) {
      promises.push(
        fetch(`./data/daily/${platform}_${day.date}.json`)
          .then(r => r.ok ? r.json() : null)
          .then(d => {
            if (d) {
              if (!STATE.daysData[day.date]) STATE.daysData[day.date] = {};
              STATE.daysData[day.date][platform] = d;
            }
          })
      );
    }
  }
  await Promise.all(promises);

  STATE.loaded = true;
}

function getDaysDataForDate(date) {
  return STATE.daysData[date] || {};
}

function getDaySummaryForPlatform(dayItem, platform) {
  if (!dayItem || !dayItem.platforms) return null;
  if (platform === 'all') {
    return {
      total_messages: dayItem.total_messages,
      positive: dayItem.positive,
      negative: dayItem.negative,
      feedback: dayItem.feedback,
      neutral: dayItem.neutral,
    };
  }
  return dayItem.platforms[platform] || null;
}
