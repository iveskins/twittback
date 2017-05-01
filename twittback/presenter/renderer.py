import jinja2


class Renderer:
    def __init__(self, app=None):
        self.app = app
        loader = jinja2.PackageLoader("twittback", "templates")
        self.env = jinja2.Environment(loader=loader)

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        context["app"] = self.app
        return template.render(context)
