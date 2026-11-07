"""综合风险评估的用例入口，尚未实现。"""
from app.commonbase.errors import FeatureNotImplemented


def refresh_all():
    """风险全量刷新。"""
    raise FeatureNotImplemented("风险全量刷新")


def refresh_item(item_id):
    """单批次风险刷新。"""
    raise FeatureNotImplemented("单批次风险刷新")


def list_snapshots(filters):
    """风险列表。"""
    raise FeatureNotImplemented("风险列表")


def get_snapshot(item_id):
    """风险详情。"""
    raise FeatureNotImplemented("风险详情")


def get_config(filters):
    """风险参数查询。"""
    raise FeatureNotImplemented("风险参数查询")


def save_config(payload):
    """保存风险参数。"""
    raise FeatureNotImplemented("保存风险参数")


def preview_config(payload):
    """风险参数预览。"""
    raise FeatureNotImplemented("风险参数预览")
