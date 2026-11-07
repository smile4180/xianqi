// 无 npm 依赖的静态检查；不能替代微信开发者工具编译与真机验收。
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const mini = path.join(root, 'miniprogram');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const app = readJson(path.join(mini, 'app.json'));
const project = readJson(path.join(root, 'project.config.json'));
assert.equal(project.miniprogramRoot, 'miniprogram/');
assert.equal(new Set(app.pages).size, app.pages.length, 'Duplicate page registration');

function checkBundle(relative) {
  for (const ext of ['js', 'json', 'wxml', 'wxss']) {
    assert.ok(fs.existsSync(path.join(mini, `${relative}.${ext}`)), `Missing ${relative}.${ext}`);
  }
}
app.pages.forEach(checkBundle);
app.tabBar.list.forEach((tab) => assert.ok(app.pages.includes(tab.pagePath), `Unknown tab ${tab.pagePath}`));
Object.values(app.usingComponents).forEach((component) => {
  checkBundle(component.replace(/^\//, ''));
  assert.equal(readJson(path.join(mini, `${component}.json`)).component, true);
});
assert.ok(fs.existsSync(path.join(mini, app.sitemapLocation)));

let jsCount = 0;
function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) { walk(file); continue; }
    if (file.endsWith('.json')) readJson(file);
    if (!file.endsWith('.js')) continue;
    const code = fs.readFileSync(file, 'utf8');
    new vm.Script(code, { filename: file });
    for (const [, dependency] of code.matchAll(/require\(['"]([^'"]+)['"]\)/g)) {
      assert.ok(dependency.startsWith('.'), `Unexpected external dependency ${dependency}`);
      const target = path.resolve(path.dirname(file), dependency);
      assert.ok(fs.existsSync(target) || fs.existsSync(`${target}.js`), `Missing ${dependency} in ${file}`);
    }
    jsCount += 1;
  }
}
walk(mini);
const { routes } = require('../miniprogram/utils/navigation');
Object.values(routes).forEach((route) => assert.ok(app.pages.includes(route.slice(1)), `Unregistered route ${route}`));
console.log(`Mini program static checks passed: ${app.pages.length} pages, ${jsCount} JavaScript files.`);
