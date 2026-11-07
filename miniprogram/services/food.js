const { request } = require('../utils/request');

module.exports = {
  list_items(filters) {
    return request({ path: `/food/items`, method: 'GET', data: filters });
  },
  create_item(payload) {
    return request({ path: `/food/items`, method: 'POST', data: payload });
  },
  get_item(item_id) {
    return request({ path: `/food/items/${encodeURIComponent(item_id)}`, method: 'GET' });
  },
  update_item(item_id, payload) {
    return request({ path: `/food/items/${encodeURIComponent(item_id)}`, method: 'PUT', data: payload });
  },
  open_item(item_id, payload) {
    return request({ path: `/food/items/${encodeURIComponent(item_id)}/open`, method: 'POST', data: payload });
  },
  process_item(item_id, payload) {
    return request({ path: `/food/items/${encodeURIComponent(item_id)}/process`, method: 'POST', data: payload });
  },
};
