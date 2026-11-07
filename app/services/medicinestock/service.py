"""药品库存与生命周期的用例入口，尚未实现。"""
from app.commonbase.errors import FeatureNotImplemented


def list_items(filters):
    """药品批次列表。"""
    raise FeatureNotImplemented("药品批次列表")


def create_item(payload):
    """药品建档。"""
    raise FeatureNotImplemented("药品建档")


def get_item(item_id):
    """药品详情。"""
    raise FeatureNotImplemented("药品详情")


def update_item(item_id, payload):
    """编辑药品。"""
    raise FeatureNotImplemented("编辑药品")


def open_item(item_id, payload):
    """药品开封。"""
    raise FeatureNotImplemented("药品开封")


def process_item(item_id, payload):
    """药品处理。"""
    raise FeatureNotImplemented("药品处理")
