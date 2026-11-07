const { request } = require('../utils/request');

module.exports = {
  generate_plan(payload) {
    return request({ path: `/plans/generate`, method: 'POST', data: payload });
  },
  get_current_plan() {
    return request({ path: `/plans/current`, method: 'GET' });
  },
  list_entries(plan_id) {
    return request({ path: `/plans/${encodeURIComponent(plan_id)}/entries`, method: 'GET' });
  },
  process_entry(entry_id, payload) {
    return request({ path: `/plans/entries/${encodeURIComponent(entry_id)}/action`, method: 'POST', data: payload });
  },
  reschedule_plan(plan_id) {
    return request({ path: `/plans/${encodeURIComponent(plan_id)}/reschedule`, method: 'POST' });
  },
  get_summary() {
    return request({ path: `/summary`, method: 'GET' });
  },
  get_stats(filters) {
    return request({ path: `/stats`, method: 'GET', data: filters });
  },
};
