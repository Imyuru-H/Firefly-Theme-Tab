from datetime import datetime
import requests
import pandas as pd
from flask import *
import logging
from werkzeug.serving import WSGIRequestHandler
import random
import os
os.environ["PYTHONIOENCODING"] = "utf-8"


app = Flask(__name__)
app.static_folder = 'static'


class StatusCodeFilter(logging.Filter):
    def __init__(self, exclude_codes):
        self.exclude_codes = set(map(str, exclude_codes))  # 转字符串防意外

    def filter(self, record):
        # 关键技巧：从日志参数中提取状态码
        if len(record.args) >=3 and str(record.args[1]) in self.exclude_codes:
            return False  # 匹配到排除状态码则拦截
        return True

# 配置Werkzeug日志过滤器
werkzeug_log = logging.getLogger('werkzeug')
handler = logging.StreamHandler()
handler.addFilter(StatusCodeFilter(exclude_codes=[200, 304]))  # 过滤200和304
werkzeug_log.addHandler(handler)


@app.route('/')
def index():
    tip = ["主人要搜些什么呢喵~?",]
    kwargs = {
        "tip" : random.choice(tip)
    }
    return render_template('Firefly.html', **kwargs, timestamp=int(datetime.now().timestamp()))

@app.route('/api/submit', methods=['POST'])
def handle_submit():
    data = request.get_json()
    received_text = data.get('text', '')
    print(received_text)
    
    return redirect(f"https://cn.bing.com/search?q={received_text}")

from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


if __name__ == '__main__':
    # 关闭Werkzeug默认的日志处理器
    WSGIRequestHandler.log = lambda self, type, message, *args: None
    
    # 配置生产环境日志格式
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    
    app.run(debug=True, use_reloader=False, port=8080)
