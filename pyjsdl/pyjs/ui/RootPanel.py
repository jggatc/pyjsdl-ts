class RootPanel:

    def add(self, panel):
        document.body.append(panel._widget._canvas)

