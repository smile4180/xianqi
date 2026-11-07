"""提醒中心的用例入口，尚未实现。"""
from app.commonbase.errors import FeatureNotImplemented


def list_reminders(filters):
    """提醒列表。"""
    raise FeatureNotImplemented("提醒列表")


def process_reminder(reminder_id, payload):
    """处理提醒。"""
    raise FeatureNotImplemented("处理提醒")


def get_preferences():
    """提醒偏好查询。"""
    raise FeatureNotImplemented("提醒偏好查询")


def save_preferences(payload):
    """保存提醒偏好。"""
    raise FeatureNotImplemented("保存提醒偏好")
