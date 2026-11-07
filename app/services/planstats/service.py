"""七日计划与统计的用例入口，尚未实现。"""
from app.commonbase.errors import FeatureNotImplemented


def generate_plan(payload):
    """生成计划。"""
    raise FeatureNotImplemented("生成计划")


def get_current_plan():
    """当前计划。"""
    raise FeatureNotImplemented("当前计划")


def list_entries(plan_id):
    """计划项查询。"""
    raise FeatureNotImplemented("计划项查询")


def process_entry(entry_id, payload):
    """处理计划项。"""
    raise FeatureNotImplemented("处理计划项")


def reschedule_plan(plan_id):
    """重新安排计划。"""
    raise FeatureNotImplemented("重新安排计划")


def get_summary():
    """首页摘要。"""
    raise FeatureNotImplemented("首页摘要")


def get_stats(filters):
    """处理统计。"""
    raise FeatureNotImplemented("处理统计")
