const { request } = require('../utils/request');

module.exports = {
  list_reminders(filters) {
    return request({ path: `/reminders`, method: 'GET', data: filters });
  },
  process_reminder(reminder_id, payload) {
    return request({ path: `/reminders/${encodeURIComponent(reminder_id)}/action`, method: 'POST', data: payload });
  },
  get_preferences() {
    return request({ path: `/reminder/preferences`, method: 'GET' });
  },
  save_preferences(payload) {
    return request({ path: `/reminder/preferences`, method: 'PUT', data: payload });
  },
};
