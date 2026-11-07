from app.routes import food, medicine, plan, reminder, risk, shared, system


def register_routes(app):
    for module in (system, food, medicine, risk, reminder, plan, shared):
        app.register_blueprint(module.bp)

