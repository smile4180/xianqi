const config = require('../config/index');

class ApiError extends Error {
  constructor(message, { code = 'REQUEST_FAILED', status = 0, field = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.field = field;
  }
}

function cleanQuery(data) {
  const result = {};
  Object.keys(data || {}).forEach((key) => {
    const value = data[key];
    if (value !== undefined && value !== null && value !== '') result[key] = value;
  });
  return result;
}

// 不自动重试写操作；页面负责 loading、错误展示和用户手动重载。
function request({ path, method = 'GET', data = {} }) {
  return new Promise((resolve, reject) => {
    if (!/^https?:\/\//.test(config.baseUrl) || !path.startsWith('/') || path.startsWith('//')) {
      reject(new ApiError('服务地址配置不正确', { code: 'CONFIG_ERROR' }));
      return;
    }
    wx.request({
      url: config.baseUrl.replace(/\/$/, '') + path,
      method,
      data: method === 'GET' ? cleanQuery(data) : data,
      timeout: config.timeout,
      header: { 'content-type': 'application/json' },
      success(response) {
        const { statusCode, data: body } = response;
        if (statusCode >= 200 && statusCode < 300 && body && body.ok === true) {
          resolve(body.data);
          return;
        }
        const error = body && body.error;
        reject(new ApiError((error && error.message) || '服务返回了无法识别的响应', {
          code: (error && error.error_code) || 'INVALID_RESPONSE',
          status: statusCode,
          field: (error && error.field) || null,
        }));
      },
      fail(error) {
        const timeout = /timeout/i.test(error.errMsg || '');
        reject(new ApiError(timeout ? '连接超时，请稍后重新加载' : '无法连接服务，请检查网络和服务地址', {
          code: timeout ? 'TIMEOUT' : 'NETWORK_ERROR',
        }));
      },
    });
  });
}

module.exports = { request, ApiError };
