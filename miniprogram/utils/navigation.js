const routes = {
  home: '/pages/home/index',
  inventory: '/pages/inventory/index',
  reminders: '/pages/reminders/index',
  plan: '/pages/plan/index',
  risk: '/pages/risk/index',
  riskDetail: '/pages/risk-detail/index',
  riskConfig: '/pages/risk-config/index',
  stats: '/pages/stats/index',
  settings: '/pages/settings/index',
  itemDetail: '/pages/item-detail/index',
  itemForm: '/pages/item-form/index',
  events: '/pages/events/index',
};
const tabs = ['home', 'inventory', 'reminders', 'plan'];

function navigate(key, params = {}) {
  if (!routes[key]) throw new Error(`Unknown page: ${key}`);
  if (tabs.includes(key)) {
    wx.switchTab({ url: routes[key] });
    return;
  }
  const query = Object.keys(params)
    .filter((name) => params[name] !== undefined && params[name] !== null)
    .map((name) => `${encodeURIComponent(name)}=${encodeURIComponent(params[name])}`)
    .join('&');
  wx.navigateTo({ url: routes[key] + (query ? `?${query}` : '') });
}

module.exports = { navigate, routes };
