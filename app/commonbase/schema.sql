-- 概要设计 V1.3 的九张表。仅建立结构，不预置业务记录或演示计算结果。
-- SQLite CHECK 负责基础存储约束，跨表业务规则由后续 services 实现。
CREATE TABLE category_rule (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL CHECK(length(trim(category_name)) > 0),
    item_type TEXT NOT NULL CHECK(item_type IN ('FOOD', 'MEDICINE')),
    default_opened_days INTEGER CHECK(default_opened_days BETWEEN 1 AND 3650),
    storage_hint TEXT NOT NULL DEFAULT '' CHECK(length(storage_hint) <= 120),
    UNIQUE(item_type, category_name),
    CHECK(item_type = 'FOOD' OR default_opened_days IS NULL)
);

CREATE TABLE item_batch (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT NOT NULL CHECK(item_type IN ('FOOD', 'MEDICINE')),
    name TEXT NOT NULL CHECK(length(trim(name)) BETWEEN 1 AND 60),
    batch_no TEXT NOT NULL DEFAULT '' CHECK(length(batch_no) <= 40),
    category_id INTEGER NOT NULL REFERENCES category_rule(category_id),
    quantity INTEGER NOT NULL CHECK(typeof(quantity) = 'integer' AND quantity BETWEEN 0 AND 9999),
    display_unit TEXT NOT NULL CHECK(length(trim(display_unit)) BETWEEN 1 AND 10),
    date_kind TEXT NOT NULL CHECK(date_kind IN ('PRODUCTION', 'PURCHASE')),
    production_or_purchase_date TEXT NOT NULL,
    package_expiry TEXT NOT NULL CHECK(package_expiry >= production_or_purchase_date),
    opened_date TEXT,
    opened_days INTEGER CHECK(opened_days IS NULL OR (typeof(opened_days) = 'integer' AND opened_days BETWEEN 1 AND 3650)),
    opened_rule TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK(opened_rule IN ('LIMITED', 'NONE', 'UNKNOWN')),
    effective_expiry TEXT,
    storage_location TEXT NOT NULL DEFAULT '' CHECK(length(storage_location) <= 30),
    storage_condition TEXT NOT NULL DEFAULT '' CHECK(length(storage_condition) <= 120),
    dosage_form TEXT NOT NULL DEFAULT '' CHECK(length(dosage_form) <= 30),
    min_stock INTEGER NOT NULL DEFAULT 0 CHECK(typeof(min_stock) = 'integer' AND min_stock BETWEEN 0 AND 9999),
    stock_status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(stock_status IN ('ACTIVE', 'STOPPED', 'ARCHIVED')),
    CHECK(item_type = 'MEDICINE' OR stock_status != 'STOPPED')
);
CREATE INDEX idx_batch_type_status ON item_batch(item_type, stock_status);

CREATE TABLE inventory_event (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL REFERENCES item_batch(item_id),
    event_type TEXT NOT NULL CHECK(event_type IN ('IN', 'EDIT', 'OPEN', 'CONSUME', 'TAKE', 'STOP', 'DISCARD')),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK(typeof(quantity) = 'integer' AND quantity BETWEEN 0 AND 9999),
    reason TEXT NOT NULL DEFAULT '' CHECK(length(reason) <= 120),
    occurred_date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    change_detail TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(change_detail))
);
CREATE INDEX idx_event_item_date ON inventory_event(item_id, occurred_date);

CREATE TABLE risk_snapshot (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL UNIQUE REFERENCES item_batch(item_id),
    model_version TEXT NOT NULL,
    calculation_date TEXT NOT NULL,
    calculated_at TEXT NOT NULL,
    days_left INTEGER,
    input_snapshot TEXT NOT NULL CHECK(json_valid(input_snapshot)),
    factors TEXT CHECK(factors IS NULL OR json_valid(factors)),
    contributions TEXT CHECK(contributions IS NULL OR json_valid(contributions)),
    score INTEGER CHECK(score IS NULL OR (typeof(score) = 'integer' AND score BETWEEN 0 AND 100)),
    level TEXT CHECK(level IN ('正常', '关注', '预警', '紧急')),
    data_state TEXT NOT NULL CHECK(data_state IN ('READY', 'INFO_REQUIRED', 'EXPIRED')),
    confidence NUMERIC NOT NULL CHECK(confidence BETWEEN 0 AND 100)
);

CREATE TABLE risk_config (
    config_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT NOT NULL CHECK(item_type IN ('FOOD', 'MEDICINE')),
    risk_weights TEXT NOT NULL CHECK(json_valid(risk_weights)),
    time_window INTEGER NOT NULL CHECK(typeof(time_window) = 'integer' AND time_window BETWEEN 1 AND 3650),
    food_quantity_base INTEGER CHECK(food_quantity_base IS NULL OR (typeof(food_quantity_base) = 'integer' AND food_quantity_base BETWEEN 1 AND 9999)),
    level_thresholds TEXT NOT NULL CHECK(json_valid(level_thresholds)),
    model_version TEXT NOT NULL CHECK(length(model_version) BETWEEN 1 AND 40),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK(is_current IN (0, 1)),
    UNIQUE(item_type, model_version)
);
CREATE UNIQUE INDEX uq_current_risk_config ON risk_config(item_type) WHERE is_current = 1;

CREATE TABLE reminder (
    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_kind TEXT NOT NULL CHECK(source_kind IN ('ITEM', 'ENTRY')),
    source_id INTEGER NOT NULL,
    reminder_type TEXT NOT NULL CHECK(reminder_type IN ('EXPIRED', 'INFO', 'NEAR', 'LOW_STOCK', 'STOPPED', 'PLAN')),
    status TEXT NOT NULL DEFAULT 'UNREAD' CHECK(status IN ('UNREAD', 'READ', 'SNOOZED', 'RESOLVED')),
    triggered_at TEXT NOT NULL,
    due_date TEXT,
    snooze_until TEXT,
    read_at TEXT,
    resolved_at TEXT,
    message TEXT NOT NULL CHECK(length(message) BETWEEN 1 AND 200),
    triggered_date TEXT NOT NULL,
    UNIQUE(source_kind, source_id, reminder_type)
);

CREATE TABLE reminder_preference (
    preference_id INTEGER PRIMARY KEY CHECK(preference_id = 1),
    food_lead_days INTEGER NOT NULL DEFAULT 3 CHECK(typeof(food_lead_days) = 'integer' AND food_lead_days BETWEEN 0 AND 365),
    medicine_lead_days INTEGER NOT NULL DEFAULT 30 CHECK(typeof(medicine_lead_days) = 'integer' AND medicine_lead_days BETWEEN 0 AND 365),
    low_stock_enabled INTEGER NOT NULL DEFAULT 1 CHECK(low_stock_enabled IN (0, 1)),
    plan_enabled INTEGER NOT NULL DEFAULT 1 CHECK(plan_enabled IN (0, 1))
);

CREATE TABLE daily_plan (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL CHECK(end_date = date(start_date, '+6 days')),
    daily_capacity INTEGER NOT NULL CHECK(typeof(daily_capacity) = 'integer' AND daily_capacity BETWEEN 1 AND 9999),
    potential_waste INTEGER NOT NULL DEFAULT 0 CHECK(typeof(potential_waste) = 'integer' AND potential_waste >= 0),
    is_current INTEGER NOT NULL DEFAULT 1 CHECK(is_current IN (0, 1)),
    selection_scope TEXT NOT NULL CHECK(json_valid(selection_scope)),
    unassigned_details TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(unassigned_details)),
    generated_date TEXT NOT NULL
);
CREATE UNIQUE INDEX uq_current_plan ON daily_plan(is_current) WHERE is_current = 1;

CREATE TABLE plan_entry (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL REFERENCES daily_plan(plan_id),
    item_id INTEGER NOT NULL REFERENCES item_batch(item_id),
    plan_date TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(typeof(quantity) = 'integer' AND quantity > 0),
    entry_status TEXT NOT NULL DEFAULT 'PENDING' CHECK(entry_status IN ('PENDING', 'COMPLETED', 'SKIPPED')),
    event_id INTEGER UNIQUE REFERENCES inventory_event(event_id),
    reason TEXT NOT NULL DEFAULT '' CHECK(length(reason) <= 120),
    UNIQUE(plan_id, item_id, plan_date)
);
