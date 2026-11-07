from enum import StrEnum


class ItemType(StrEnum):
    FOOD = "FOOD"
    MEDICINE = "MEDICINE"


class DateKind(StrEnum):
    PRODUCTION = "PRODUCTION"
    PURCHASE = "PURCHASE"


class StockStatus(StrEnum):
    ACTIVE = "ACTIVE"
    STOPPED = "STOPPED"
    ARCHIVED = "ARCHIVED"


class EventType(StrEnum):
    IN = "IN"
    EDIT = "EDIT"
    OPEN = "OPEN"
    CONSUME = "CONSUME"
    TAKE = "TAKE"
    STOP = "STOP"
    DISCARD = "DISCARD"


class OpenedRule(StrEnum):
    LIMITED = "LIMITED"
    NONE = "NONE"
    UNKNOWN = "UNKNOWN"


class DataState(StrEnum):
    READY = "READY"
    INFO_REQUIRED = "INFO_REQUIRED"
    EXPIRED = "EXPIRED"


class RiskLevel(StrEnum):
    NORMAL = "正常"
    ATTENTION = "关注"
    WARNING = "预警"
    URGENT = "紧急"


class ReminderSource(StrEnum):
    ITEM = "ITEM"
    ENTRY = "ENTRY"


class ReminderType(StrEnum):
    EXPIRED = "EXPIRED"
    INFO = "INFO"
    NEAR = "NEAR"
    LOW_STOCK = "LOW_STOCK"
    STOPPED = "STOPPED"
    PLAN = "PLAN"


class ReminderStatus(StrEnum):
    UNREAD = "UNREAD"
    READ = "READ"
    SNOOZED = "SNOOZED"
    RESOLVED = "RESOLVED"


class EntryStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"

