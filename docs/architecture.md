# 框架与开发约定

客户端仅负责交互与展示，HTTP 路由解析参数、调用服务并组装响应；业务规则归属各 `services` 包，SQL 放在对应 `repository.py`。公共能力集中于 `app/commonbase/`。框架采用 Flask 应用工厂及 Blueprint，参见 [Flask 官方应用工厂说明](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)。

## 模块边界

| 模块 | 后端目录 | 小程序入口 | 后续责任 |
| --- | --- | --- | --- |
| CSCI-1 | `services/foodstock` | 库存食品页、批次表单和详情、记录 | 成员 A；食品生命周期与共享类别/事件查询 |
| CSCI-2 | `services/medicinestock` | 库存药品页、批次表单和详情、记录 | 成员 A；药品生命周期 |
| CSCI-3 | `services/riskeval` | 风险列表、详情、参数 | 成员 B；评分、分级和版本 |
| CSCI-4 | `services/remindercenter` | 提醒、我的设置 | 成员 B；提醒、去重与偏好 |
| CSCI-5 | `services/planstats` | 首页、计划、统计 | 成员 C；食品计划与统计 |
| CSCI-6 | `commonbase` | 公共请求、组件与导航 | 全组；框架基础能力 |

每个业务包已包含 `service.py` 与 `repository.py`。`service.py` 的函数签名对应路由；所有用例暂时抛出 `FeatureNotImplemented`。`repository.py` 只标记 SQL 所属位置，不生成通用 CRUD，也不在此阶段加入业务数据模型、算法或假数据。

公共校验通过抛出带字段信息的 `ApiError` 终止当前请求，外层统一转为文档要求的错误 JSON。这是对文档中“返回是否通过、错误字段和原因”的 Python 实现方式，避免调用方忘记检查校验结果。

## 数据和事务

九张表结构位于 `app/commonbase/schema.sql`。JSON 以 TEXT 保存，日期使用 `YYYY-MM-DD`，时间使用 `YYYY-MM-DD HH:mm:ss`。每个连接启用外键，`PRAGMA user_version=1` 标识当前结构。

数据库初始化是显式 CLI 操作。重复执行保留已有记录；遇到未知结构拒绝覆盖。普通启动以 `mode=rw` 打开现有文件，路径错误不会悄悄创建新数据库。后续表结构变更应增加版本及明确迁移脚本，不能修改原建表 SQL 后要求用户重建已有数据。

```python
from app.commonbase.db import execute, transaction

# 仅展示事务调用方式，不代表已实现的业务用例。
with transaction() as connection:
    execute("UPDATE item_batch SET quantity=? WHERE item_id=?",
            (new_quantity, item_id), connection=connection)
    # 调用其他模块写入事件或计划状态时传入同一个 connection。
```

事务由最外层发起方提交；内部函数不得自行 commit、另开事务或通过 HTTP 调用另一个业务模块。数据库异常会回滚整个短事务。SQL 值必须参数化。表名和列名只能来自代码白名单，不能拼接用户输入。

表级 CHECK 和外键只负责基础数据完整性。日期合法性、类别类型一致、计划只包含食品、开封规则、库存状态转移、扣减上限和计划容量等业务校验仍由业务模块负责，当前未实现。风险模型每类一个当前版本、当前计划唯一、提醒来源去重、计划事件关联唯一等约束已建立。

## 时钟与刷新

所有业务日期通过 `clock.today()` 获取；同一请求第一次读取后固定，避免跨午夜导致本轮计算不一致。`clock.now()` 始终返回指定时区的真实时间。演示日期仅来自部署配置，不允许客户端覆盖。

`routes/refresh.py` 是唯一的派生刷新编排预留点，目前不执行任何业务计算。后续实现按以下顺序连接各模块：固定计算日期 → 读取本轮已有未处理提醒 → 更新有效期与风险快照 → 更新提醒。本轮不因新提醒再评分，风险与提醒不得相互调用。

库存和事件先一起提交；计划完成时，库存、食用事件和计划完成状态要在同一事务提交。派生刷新在提交后单独进行。若保存已成功而刷新失败，响应必须保留实际 `save_result` 并设置 `refresh_completed=false`，提示用户手动重载，不能诱导重复保存。当前占位接口全部返回 501，尚未实现这条业务链路。

## 小程序边界

页面通过 `services/*.js` 调用接口，不直接拼接服务地址或重复封装 `wx.request`。请求层保留错误码、字段名和 HTTP 状态，不自动重试写入。公共状态组件由页面决定何时展示，不在请求层强制弹窗。

四个底部页使用 `wx.switchTab`，详情页使用 `wx.navigateTo`；统一由 `utils/navigation.js` 管理。库存食品/药品切换只是页面状态，不读写业务库存。详情、表单和记录页已注册，待业务模块完成后再从真实批次入口传入编号，不用假编号制造可用效果。

## 后续接入顺序

1. 各成员从设计说明书确认本模块字段，替换自己包中的用例占位，加入相应 SQL 和输入校验。
2. 先由库存域提供真实批次与事件，再接入风险和提醒，最后联调计划与统计。
3. 实现具体用例时新增业务测试，并将对应的 501 占位测试调整为真实成功和失败用例。
4. 业务模块明确分类、风险默认参数和演示样例后再提供独立初始化命令；框架 `init-db` 保持只建结构。
5. 完成后用真实 AppID 和手机验收导航、网络、重复操作与布局。当前测试不能作为业务验收或性能承诺。

