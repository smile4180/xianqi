# 接口约定

所有接口以 `/api` 开头，字段采用 snake_case。当前唯一已经实现的数据接口是 `GET /api/health`。其余 32 个业务接口只用于固定后续协作边界，不保存记录，不执行计算。

## 响应

成功使用 HTTP 200/201：

```json
{"ok": true, "data": {"status": "ok"}}
```

业务占位使用 HTTP 501：

```json
{"ok": false, "error": {"error_code": "NOT_IMPLEMENTED", "message": "食品建档尚未实现", "field": null}}
```

请求体需要 JSON 对象；数组、null、非法 JSON 会返回 400，非 JSON 内容类型返回 415。未定义的路径返回 404，不支持的方法返回 405。未预期异常返回 500 / `SERVER_ERROR`，详细异常只进入日志。

后续业务实现继续使用 `VALIDATION_ERROR`、`DATE_ORDER_ERROR`（400）、`NOT_FOUND`（404）、`QUANTITY_EXCEEDED`、`STATE_CONFLICT`（409）。重复完成计划应返回 200 和原 event_id，而不是重复扣减；该规则尚未实现。

日期为 `YYYY-MM-DD`，时间为 `YYYY-MM-DD HH:mm:ss`，空值为 JSON null。查询条件不传表示不限制；日期和数量等业务字段尚未接入校验。客户端不提供 calculation_date，计算日期以服务端统一时钟为准。

## 接口列表

| 方法 | 路径 | 说明 | 业务包 |
| --- | --- | --- | --- |
| GET | `/api/food/items` | 食品批次列表 | `foodstock` |
| POST | `/api/food/items` | 食品建档 | `foodstock` |
| GET | `/api/food/items/{item_id}` | 食品详情 | `foodstock` |
| PUT | `/api/food/items/{item_id}` | 编辑食品 | `foodstock` |
| POST | `/api/food/items/{item_id}/open` | 食品开封 | `foodstock` |
| POST | `/api/food/items/{item_id}/process` | 食品处理 | `foodstock` |
| GET | `/api/medicine/items` | 药品批次列表 | `medicinestock` |
| POST | `/api/medicine/items` | 药品建档 | `medicinestock` |
| GET | `/api/medicine/items/{item_id}` | 药品详情 | `medicinestock` |
| PUT | `/api/medicine/items/{item_id}` | 编辑药品 | `medicinestock` |
| POST | `/api/medicine/items/{item_id}/open` | 药品开封 | `medicinestock` |
| POST | `/api/medicine/items/{item_id}/action` | 药品处理 | `medicinestock` |
| POST | `/api/risk/refresh` | 风险全量刷新 | `riskeval` |
| POST | `/api/risk/refresh/{item_id}` | 单批次风险刷新 | `riskeval` |
| GET | `/api/risk/snapshots` | 风险列表 | `riskeval` |
| GET | `/api/risk/snapshots/{item_id}` | 风险详情 | `riskeval` |
| GET | `/api/risk/config` | 风险参数查询 | `riskeval` |
| POST | `/api/risk/config` | 保存风险参数 | `riskeval` |
| POST | `/api/risk/config/preview` | 风险参数预览 | `riskeval` |
| GET | `/api/reminders` | 提醒列表 | `remindercenter` |
| POST | `/api/reminders/{reminder_id}/action` | 处理提醒 | `remindercenter` |
| GET | `/api/reminder/preferences` | 提醒偏好查询 | `remindercenter` |
| PUT | `/api/reminder/preferences` | 保存提醒偏好 | `remindercenter` |
| POST | `/api/plans/generate` | 生成计划 | `planstats` |
| GET | `/api/plans/current` | 当前计划 | `planstats` |
| GET | `/api/plans/{plan_id}/entries` | 计划项查询 | `planstats` |
| POST | `/api/plans/entries/{entry_id}/action` | 处理计划项 | `planstats` |
| POST | `/api/plans/{plan_id}/reschedule` | 重新安排计划 | `planstats` |
| GET | `/api/summary` | 首页摘要 | `planstats` |
| GET | `/api/stats` | 处理统计 | `planstats` |
| GET | `/api/categories` | 食品药品类别查询 | `foodstock` |
| GET | `/api/items/{item_id}/events` | 库存事件查询 | `foodstock` |

## 后续参数接入

- 食品建档/修改：name、category_id、quantity、date_kind、production_or_purchase_date、package_expiry；可选 storage_location、storage_condition。开封接口为 opened_date、opened_days；处理接口为 action、quantity、occurred_date 及按操作需要的 reason。
- 药品建档/修改：在基础库存字段上增加固定 display_unit，可选 dosage_form、batch_no、min_stock。开封使用 opened_rule 和按规则需要的 opened_days；领用/停用/处置由 action 决定所需字段。
- 风险配置：item_type、risk_weights、time_window、food_quantity_base、level_thresholds；预览另外传 item_id。
- 提醒查询：filter、item_type、reminder_type；处理为 action、snooze_until；偏好为 food_lead_days、medicine_lead_days、low_stock_enabled、plan_enabled。
- 计划生成：start_date、daily_capacity、scope、replace_current；计划项操作为 action 及需要的 new_date、new_quantity、reason。
- 统计查询：from、to、item_type、category_id、level、reminder_status。

上述仅列协作所需字段，不替代原设计中的范围、条件必填项与业务规则。实现时由各服务校验，不能仅凭数据库字段或本表推定用例已经完成。

`api-routes.json` 是可供测试读取的路由清单。修改接口时同步更新路由、对应小程序服务、清单和测试。小程序占位页不会主动请求这些业务接口，避免把“尚未开发”误显示为“空库存”或“无提醒”。
