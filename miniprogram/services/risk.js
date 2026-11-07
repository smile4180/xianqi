const { request } = require('../utils/request');

module.exports = {
  refresh_all() {
    return request({ path: `/risk/refresh`, method: 'POST' });
  },
  refresh_item(item_id) {
    return request({ path: `/risk/refresh/${encodeURIComponent(item_id)}`, method: 'POST' });
  },
  list_snapshots(filters) {
    return request({ path: `/risk/snapshots`, method: 'GET', data: filters });
  },
  get_snapshot(item_id) {
    return request({ path: `/risk/snapshots/${encodeURIComponent(item_id)}`, method: 'GET' });
  },
  get_config(filters) {
    return request({ path: `/risk/config`, method: 'GET', data: filters });
  },
  save_config(payload) {
    return request({ path: `/risk/config`, method: 'POST', data: payload });
  },
  preview_config(payload) {
    return request({ path: `/risk/config/preview`, method: 'POST', data: payload });
  },
};
