#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
import alsaaudio
#import lights, sounds, 
import newspaper

## DOMAIN CONFIGURATION ##
domain = {"meinberg": "meinberg.local",
        "morgenpost": "morgenpost.meinberg.local",
        "antenne": "antenne.meinberg.local",
        "cloudberry": "cloudberry.local",
        "luchsen": "luchsen.local",
        "vitholm": "vitholm.local",
        "zandhoek": "zandhoek.local"}

## AUDIO CONFIGURATION ##
global mixer
mixer = alsaaudio.Mixer('Headphone')


## FLASK ##
app = Flask(__name__, host_matching=True, static_host=domain["cloudberry"])
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)


##############
# CLOUDBERRY #
##############

@app.route('/', host=domain["cloudberry"])
def cloudberry():
    return render_template('cloudberry.html')

######################
# MEINBERG-ZUGSPITZE #
######################

@app.route('/', host=domain["meinberg"])
def meinberg():
    return render_template('meinberg_index.html')

#@app.route('/lights/<device>/<action>')
#def light(device, action):
#    lights.control(int(device), action)
#    return ("Turning "+action+" light ID"+device)

#@app.route('/sound/<device>/<ping_num>')
#def ping(device, ping_num):
#    sounds.ping(int(device), int(ping_num))
#    return ("Ring the bell No."+device)


#@app.route('/church/<id>/<action>')
#def church(id, action):
#    candles = lights.Chapel()
#    if action == "on":
#      candles.start()
#      return render_template('index.html')
#    if action == "off":
#      candles.stop()
#      return render_template('index.html')

# Environment
@app.route('/environment', host=domain["meinberg"])
def meinberg_environment():
    vol_level = mixer.getvolume()
    return render_template('meinberg_environment.html', vol_level = vol_level[0])

@app.route('/environment/volume/<value>', host=domain["meinberg"])
def setvol(value):
    mixer.setvolume(int(value))
    return ("Volume adjusted to "+value+"%")

# Trains/Cable car
@app.route('/railways/railjet', host=domain["meinberg"])
def railjet():
    return render_template('meinberg_railways_railjet.html')

@app.route('/railways/cityjeteco', host=domain["meinberg"])
def cityjeteco():
    return render_template('meinberg_railways_cityjeteco.html')

@app.route('/railways/cablecar', host=domain["meinberg"])
def cablecar():
    return render_template('meinberg_railways_cablecar.html')

# Town
@app.route('/town', host=domain["meinberg"])
def town():
    return render_template('meinberg_town.html')


### Morgenpost ###
@app.route('/', host=domain["morgenpost"])
def news():
    rows = newspaper.News().headlines()
    return render_template('news_headlines.html', rows=rows)

@app.route('/new', host=domain['morgenpost'])
def new():
    return render_template('news_new.html', host=domain["morgenpost"])

@app.route('/edit', host=domain["meinberg"])
def editlist():
    return render_template('news_new.html', host=domain["morgenpost"])

@app.route('/edit/<id>', host=domain["morgenpost"])
def edit(id):
        post = newspaper.News()
        article = post.editarticle(id)
        return render_template('news_edit.html', id=id, article=article)

@app.route('/new/post', methods=['POST'], host=domain["morgenpost"])
def post():
    title = request.form['title']
    photo = request.files['file']
    filename = photo.filename
    article = request.form['article']
    newpost = newspaper.News()
    newpost.postarticle(title, article, photo, filename)
    return redirect(url_for('news'))

@app.route('/edit/update', methods=['POST'], host=domain["morgenpost"])
def update():
    id = request.form['id']
    title = request.form['title']
    article = request.form['article']
    update = newspaper.News()
    update.updatearticle(id, title, article)
    return redirect(url_for('news'))


### Radio ###
@app.route('/', host=domain["antenne"])
def radio():
    return redirect('http://antenne.meinberg.local:8000')

@app.route('/stream', host=domain["antenne"])
def stream():
    return redirect('http://antenne.meinberg.local:8000/stream')

####################
# ZANDHOEK ANN ZEE #
####################

@app.route('/', host=domain["zandhoek"])
def zandhoek():
    return render_template('zandhoek_index.html')

# Strand
@app.route('/strand', host=domain["zandhoek"])
def zandhoek_strand():
    return render_template('zandhoek_strand.html')

# Environment
@app.route('/environment', host=domain["zandhoek"])
def zandhoek_environment():
    return render_template('zandhoek_environment.html')


####################################
# LUCHSEN IM BAYERISCHEN WAELDCHEN #
####################################

@app.route('/', host=domain["luchsen"])
def luchsen():
    return render_template('luchsen_index.html')

# Environment
@app.route('/environment', host=domain["luchsen"])
def luchsen_environment():
    return render_template('luchsen_environment.html')

# Park
@app.route('/park', host=domain["luchsen"])
def luchsen_park():
    return render_template('luchsen_park.html')

# Traffic
@app.route('/traffic', host=domain["luchsen"])
def luchsen_traffic():
    return render_template('luchsen_traffic.html')

###########
# VITHOLM #
###########
@app.route('/', host=domain["vitholm"])
def vitholm():
    return render_template('vitholm_index.html')

@app.route('/village', host=domain["vitholm"])
def vitholm_village():
    return render_template('vitholm_village.html')

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80, debug=True)


if __name__ == "__main__":
    reactor_args = {}

    def run_twisted_wsgi():
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = Site(resource)
        reactor.listenTCP(80, site)
        reactor.run(**reactor_args)

    if app.debug:
        # Disable twisted signal handlers in development only.
        reactor_args['installSignalHandlers'] = 0
        # Turn on auto reload.
        import werkzeug.serving
        run_twisted_wsgi = werkzeug.serving.run_with_reloader(run_twisted_wsgi)

    run_twisted_wsgi()
