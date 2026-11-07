"""食品库存与生命周期的用例入口，尚未实现。"""
from app.commonbase.errors import FeatureNotImplemented


def list_items(filters):
    """食品批次列表。"""
    raise FeatureNotImplemented("食品批次列表")


def create_item(payload):
    """食品建档。"""
    raise FeatureNotImplemented("食品建档")


def get_item(item_id):
    """食品详情。"""
    raise FeatureNotImplemented("食品详情")


def update_item(item_id, payload):
    """编辑食品。"""
    raise FeatureNotImplemented("编辑食品")


def open_item(item_id, payload):
    """食品开封。"""
    raise FeatureNotImplemented("食品开封")


def process_item(item_id, payload):
    """食品处理。"""
    raise FeatureNotImplemented("食品处理")


def list_categories(filters):
    raise FeatureNotImplemented("类别查询")


def list_events(item_id):
    raise FeatureNotImplemented("库存事件查询")
