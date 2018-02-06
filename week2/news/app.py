import json
import os
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#def br(cont):
#    new_cont = cont.replace('\\n','<br/>')
#    return new_cont

#app.add_template_filter(br)


@app.route('/')
def index():
    contents = []
    for root, dirs, files in os.walk('/home/shiyanlou/files'):
        for name in files:
            new_name = os.path.join(root,name)
            with open(new_name, 'r') as fil:
                content = json.loads(fil.read())
                contents.append(content)
    return render_template('index.html',contents=contents)	


@app.route('/files/<filename>')
def file(filename):
    filepath = '/home/shiyanlou/files/{}.json'.format(filename)
    result = os.path.exists(filepath)
    if result == True:
        with open(filepath, 'r') as f:
            load = json.loads(f.read())
            return render_template('file.html', load=load)
    else:
        abort(404)
	
@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run()