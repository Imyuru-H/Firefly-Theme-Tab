# !/usr/bin/python
# **coding:utf-8**

import os, time
os.environ["PYTHONIOENCODING"] = "utf-8"

start_time = time.time()

from datetime import datetime
import random
from urllib.parse import quote

import init
import requests
import pandas as pd
from flask import *
import logging
from werkzeug.serving import WSGIRequestHandler
from werkzeug.exceptions import NotFound
import yaml


from log import *
import tips
import crawler


# 创建日志类
Logs = Info()

# 初始化Flask app
app = Flask(__name__)
app.static_folder = 'static'
Logs.info("Flask app init over.")

session = {
    'error' : None
}


# 防止日志刷屏
class StatusCodeFilter(logging.Filter):
    def __init__(self, exclude_codes):
        self.exclude_codes = set(map(str, exclude_codes))  # 转字符串防意外

    def filter(self, record):
        # 关键技巧：从日志参数中提取状态码
        if len(record.args) >= 3 and str(record.args[1]) in self.exclude_codes:
            return False  # 匹配到排除状态码则拦截
        return True

# 配置Werkzeug日志过滤器
werkzeug_log = logging.getLogger('werkzeug')
handler = logging.StreamHandler()
handler.addFilter(StatusCodeFilter(exclude_codes=[200, 304]))  # 过滤200和304
werkzeug_log.addHandler(handler)
Logs.info("Werkzeug log filter config over.")


# 先判断背景地址类型是否为url, 如果是, 则直接返回url, 如果不是, 判断地址对应的文件是否存在, 若存在, 则返回完整相对地址, 若不存在, 则返回默认背景的完整相对地址 
DEFAUT_BG_PATH = "background.png"
bg = lambda path_type,path : path if path_type == 'url' else path if os.path.exists(f"/static/background/{path}") else f"/static/background/{DEFAUT_BG_PATH}"

# 读取配置信息
with open("settings.yml") as settings:
    settings = yaml.load(settings, Loader=yaml.FullLoader)
BG_PATH = bg(settings['background_type'], settings['background'])


# 配置Flask app
@app.route('/')
def index():
    global session
    
    # 配置tips
    is_empty = lambda x,y: y if x==None else tips.errors[session['error']]
    kwargs = {
        "tip" : is_empty(session['error'], random.choice(tips.tips)),
        "background" : f"/static/background/{BG_PATH}"
    }
    session['error'] = None
    
    # 返回Firefly.html
    return render_template('Firefly.html', **kwargs), Logs.info("Return Firefly.html over.") 

@app.route('/search<string:question>')
def search(question):
    url = f"https://cn.bing.com/search?q={quote(question)}"
    Logs.info(f"Url: {url}")
    # 发送请求
    return jsonify({'url':url})

@app.route('/api/submit', methods=['POST'])
def handle_submit():
    data = request.get_json()
    is_empty = lambda x: "None" if x=="" else x
    received_text = is_empty(data.get('text', ''))
    
    if received_text == "None":
        return jsonify({'error': 'No input provided'}), 400, Logs.error("No input provided, return 400 error.")
    return redirect(url_for('search', question=received_text, _external=True), code=302), Logs.info("Redirect to search over.")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )

@app.errorhandler(400)
def error400(e):
    global session
    session['error'] = 400
    return redirect(url_for('index')), Logs.error("Error 400: Bad Request, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/400test')
def error400test():
    return abort(400)

@app.errorhandler(401)
def error401(e):
    global session
    session['error'] = 401
    return redirect(url_for('index')), Logs.error("Error 401: Unauthorized, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/401test')
def error401test():
    return abort(401)

@app.errorhandler(403)
def error403(e):
    global session
    session['error'] = 403
    return redirect(url_for('index')), Logs.error("Error 403: Forbidden, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/403test')
def error403test():
    return abort(403)

@app.errorhandler(404)
def error404(e):
    global session
    session['error'] = 404
    return redirect(url_for('index')), Logs.error("Error 404: Not Found, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/404test')
def error404test():
    return abort(404)

@app.errorhandler(405)
def error405(e):
    global session
    session['error'] = 405
    return redirect(url_for('index')), Logs.error("Error 405: Method Not Allowed, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/405test')
def error405test():
    return abort(405)

@app.errorhandler(500)
def error500(e):
    global session
    session['error'] = 500
    return redirect(url_for('index')), Logs.error("Error 500: Internal Server Error, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/500test')
def error500test():
    return abort(500)

@app.errorhandler(501)
def error501(e):
    global session
    session['error'] = 501
    return redirect(url_for('index')), Logs.error("Error 501: Not Implemented, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/501test')
def error501test():
    return abort(501)

@app.errorhandler(502)
def error502(e):
    global session
    session['error'] = 502
    return redirect(url_for('index')), Logs.error("Error 502: Bad Gateway, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/502test')
def error502test():
    return abort(502)

@app.errorhandler(503)
def error503(e):
    global session
    session['error'] = 503
    return redirect(url_for('index')), Logs.error("Error 503: Service Unavailable, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/503test')
def error503test():
    return abort(503)

@app.errorhandler(504)
def error504(e):
    global session
    session['error'] = 504
    return redirect(url_for('index')), Logs.error("Error 504: Gateway Time-out, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/504test')
def error504est():
    return abort(504)

@app.errorhandler(505)
def error505(e):
    global session
    session['error'] = 505
    return redirect(url_for('index')), Logs.error("Error 505: HTTP Version not supported, redirected to Firefly.html..."), Logs.error(e.description)

@app.route('/505test')
def error505test():
    return abort(505)


if __name__ == '__main__':
    # 关闭Werkzeug默认的日志处理器
    WSGIRequestHandler.log = lambda self, type, message, *args: None
    
    # 配置生产环境日志格式
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    
    # 输出启动时长
    end_time = time.time()
    Logs.info(f"App start duration: {end_time-start_time:.2f}s")
    
    # 启动web app
    app.run(debug=True, use_reloader=False, port=8080)
