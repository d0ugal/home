
def syncdb():
    from home import app, db

    with app.app_context():
        db.create_all()


def get_or_create(model, **kwargs):

    from home import db

    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        return instance
