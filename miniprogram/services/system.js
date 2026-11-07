const { request } = require('../utils/request');

module.exports = {
  health: () => request({ path: '/health' }),
  categories: (filters) => request({ path: '/categories', data: filters }),
  events: (itemId) => request({ path: `/items/${encodeURIComponent(itemId)}/events` }),
};
