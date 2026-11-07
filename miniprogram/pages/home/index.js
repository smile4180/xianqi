const { navigate } = require('../../utils/navigation');

Page({
  data: {
    entries: [
      { key: 'inventory', title: '库存', subtitle: '食品与药品，按批次管理' },
      { key: 'risk', title: '风险评估', subtitle: '查看管理优先级与原因' },
      { key: 'stats', title: '处理统计', subtitle: '回顾使用、丢弃与计划执行' },
      { key: 'settings', title: '我的设置', subtitle: '提醒偏好与服务连接' },
    ],
  },
  openPage(event) { navigate(event.currentTarget.dataset.route); },
});
