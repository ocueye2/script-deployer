import subprocess
import os
import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

processes = {}

# Base directory of the script
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

def load(file):
    try:
        with open(os.path.join(base_dir, file)) as f:
            return f.read()
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return ""

def run_script(script_name):
    script_path = os.path.join(base_dir, 'scripts', script_name)
    if not os.path.isfile(script_path):
        logging.error(f"Script file {script_path} does not exist.")
        return

    try:
        with open(script_path, 'r') as file:
            script_code = file.read()
        exec(script_code, globals(), locals())
    except Exception as e:
        logging.error(f"Error running script {script_name}: {e}")
    finally:
        if script_name in processes:
            try:
                del processes[script_name]
            except Exception as e:
                logging.error(f"Error removing process: {e}")

def renderhtml(context):
    lookup = TemplateLookup(directories=[os.path.join(base_dir, 'templates')])
    template = lookup.get_template('index.html')
    css_content = load("templates/index.css")
    html_content = template.render(**context)
    out = f"""<html>
<head>
<style>
{css_content}
</style>
</head>
<body>
{html_content}
</body>
</html>"""
    return out

def start_script(script_name):
    if script_name not in processes:
        logging.info(f"Starting script: {script_name}")
        script_path = os.path.join(base_dir, 'scripts', script_name)
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes[script_name] = process
    else:
        logging.info(f"Script {script_name} is already running.")

def stop_script(script_name):
    if script_name in processes:
        process = processes[script_name]
        logging.info(f"Stopping script: {script_name}")
        process.terminate()
        process.wait()  
        del processes[script_name]
    else:
        logging.info(f"Script {script_name} is not running.")

# main website class
class webui(object):
    @cherrypy.expose
    def stop(self):
        cherrypy.engine.exit()
        
    @cherrypy.expose
    def index(self, cmd=""):
        if cmd:
            if cmd in processes:
                stop_script(cmd)
            else:
                logging.info(f"Starting {cmd}")
                start_script(cmd)
        
        scripts_dir = os.path.join(base_dir, 'scripts')
        all_scripts = os.listdir(scripts_dir)
        context = {
            'stopped': [x for x in all_scripts if x not in processes],
            'running': list(processes.keys())
        }
        return renderhtml(context)

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 1232,
        'log.screen': False  
    })
    cherrypy.quickstart(webui())
