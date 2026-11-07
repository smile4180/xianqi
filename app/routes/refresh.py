"""派生刷新编排的唯一预留入口。待 RiskEval 与 ReminderCenter 实现后接入。

顺序契约：固定 calculation_date → 读取已有未处理提醒 → 更新有效期与风险
→ 刷新提醒。风险与提醒不互相回调。本轮只评分一次。
库存保存与该刷新分开提交；保存成功但刷新失败时，必须保留 save_result，
并返回 refresh_completed=false。不得让客户端重复提交已保存的操作。
"""
from app.commonbase.errors import FeatureNotImplemented


def refresh_derived(item_ids=None, *, calculation_date):
    raise FeatureNotImplemented("派生数据刷新")

