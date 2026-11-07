const { test, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const { request } = require('../miniprogram/utils/request');
const { navigate } = require('../miniprogram/utils/navigation');

afterEach(() => { delete global.wx; });

test('request unwraps data and keeps false and zero query values', async () => {
  global.wx = { request(options) {
    assert.deepEqual(options.data, { opened: false, count: 0 });
    assert.match(options.url, /\/api\/items$/);
    options.success({ statusCode: 200, data: { ok: true, data: null } });
  } };
  assert.equal(await request({ path: '/items', data: { opened: false, count: 0, name: '', missing: undefined } }), null);
});

test('request preserves server error code, field and HTTP status', async () => {
  global.wx = { request(options) {
    options.success({ statusCode: 400, data: { ok: false, error: { error_code: 'VALIDATION_ERROR', message: '数量无效', field: 'quantity' } } });
  } };
  await assert.rejects(request({ path: '/food/items', method: 'POST', data: { quantity: -1 } }),
    (error) => error.code === 'VALIDATION_ERROR' && error.field === 'quantity' && error.status === 400);
});

test('write failure is not retried and 501 is not treated as empty success', async () => {
  let calls = 0;
  global.wx = { request(options) {
    calls += 1;
    options.success({ statusCode: 501, data: { ok: false, error: { error_code: 'NOT_IMPLEMENTED', message: '尚未实现' } } });
  } };
  await assert.rejects(request({ path: '/food/items', method: 'POST' }), { code: 'NOT_IMPLEMENTED' });
  assert.equal(calls, 1);
});

test('malformed service responses are errors', async () => {
  global.wx = { request(options) { options.success({ statusCode: 200, data: '<html>error</html>' }); } };
  await assert.rejects(request({ path: '/health' }), { code: 'INVALID_RESPONSE' });
});

test('network timeout is readable and not automatically retried', async () => {
  let calls = 0;
  global.wx = { request(options) { calls += 1; options.fail({ errMsg: 'request:fail timeout' }); } };
  await assert.rejects(request({ path: '/health' }), { code: 'TIMEOUT' });
  assert.equal(calls, 1);
});

test('navigation uses tab API for tabs and encodes detail query', () => {
  const calls = [];
  global.wx = { switchTab: (o) => calls.push(['tab', o.url]), navigateTo: (o) => calls.push(['detail', o.url]) };
  navigate('inventory');
  navigate('itemDetail', { item_id: 1, item_type: 'FOOD', label: 'a&b' });
  assert.deepEqual(calls, [
    ['tab', '/pages/inventory/index'],
    ['detail', '/pages/item-detail/index?item_id=1&item_type=FOOD&label=a%26b'],
  ]);
  assert.throws(() => navigate('missing'));
});
