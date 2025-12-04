import flet


class Router:
    def __init__(self):
        self.data = dict()
        self.routes = {}
        self.body = flet.Container(expand=True)

    def route_change(self, route):
        self.body.content = self.routes[route.route]()
        self.body.content.inicializar()
        self.body.update()
