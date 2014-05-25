def setUpJinjaEnv(app):
    """ Set up the jinja environment for the given app """
    app.jinja_env.block_start_string = '[['
    app.jinja_env.block_end_string = ']]'
    app.jinja_env.variable_start_string = '[-'
    app.jinja_env.variable_end_string = '-]'
    app.jinja_env.comment_start_string = '[#'
    app.jinja_env.comment_end_string = '#]'
