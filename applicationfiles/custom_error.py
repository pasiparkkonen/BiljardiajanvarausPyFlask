from flask import render_template, url_for

def handle_error(error_message):
    error_message = error_message
    return render_template('error.html', error_message=error_message, redirect_url=url_for('home'))