from flask import Blueprint,render_template

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@error_pages.app_errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
