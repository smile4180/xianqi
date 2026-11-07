const { health } = require('../../services/system');

Page({
  data: { state: 'idle', message: '', calculationDate: '', serverTime: '' },
  onLoad() { this.alive = true; },
  onUnload() { this.alive = false; },
  async checkConnection() {
    if (this.data.state === 'loading') return;
    this.setData({ state: 'loading', message: '', calculationDate: '', serverTime: '' });
    try {
      const result = await health();
      if (!this.alive) return;
      this.setData({ state: 'success', message: '服务连接正常', calculationDate: result.calculation_date, serverTime: result.server_time });
    } catch (error) {
      if (this.alive) this.setData({ state: 'error', message: error.message });
    }
  },
});
