#!/usr/bin/env python3
from flask import Flask, render_template

## FLASK ##
app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    title = "Base"
    return render_template("base.html", title = title)

#TEST ENVIRONMENT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1706, debug=True)


#PRODUCTIVE ENVIRONMENT
#if __name__ == "__main__":
#    reactor_args = {}
#
#    def run_twisted_wsgi():
#        from twisted.internet import reactor
#        from twisted.web.server import Site
#        from twisted.web.wsgi import WSGIResource
#
#        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
#        site = Site(resource)
#        reactor.listenTCP(80, site)
#        reactor.run(**reactor_args)
#
#    if app.debug:
#        # Disable twisted signal handlers in development only.
#        reactor_args['installSignalHandlers'] = 0
#        # Turn on auto reload.
#        import werkzeug.serving
#        run_twisted_wsgi = werkzeug.serving.run_with_reloader(run_twisted_wsgi)
#
#    run_twisted_wsgi()
