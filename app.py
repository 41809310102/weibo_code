import json

from flask import Flask, render_template, request

from controller.datacontroller.feelcheck_api import api_url_check
from controller.usercontroller.api_user import api_url_user
from service.feelcheck import read_files, getcloud_chart, getap10_chart
from utils import mybaits

app = Flask(__name__)

movice = []

app = Flask(import_name=__name__,
            static_url_path='',  # 配置静态文件的访问url前缀
            static_folder='static',  # 配置静态文件的文件夹
            template_folder='templates')  # 配置模板文件的文件夹


# 加载爬取的网站数据
def read_file(data):
    with open("service/moviesky.txt", "r", encoding="utf-8") as f:  # 打开文件
        line = f.readline()  # 调用文件的 readline()方法，一次读取一行
        while line:
            res = eval(str(line))
            movice.append(res)
            line = f.readline()
        f.close()


@app.route('/lay.html')
def moban():
    return render_template("lay.html")


# 统计电影类别数
@app.route('/chart/mydata')
def get_mov_type():
    # read_file()
    sql = "select type from wblog where id>0"
    data_wb = mybaits.select(sql, ['type'])
    type_list = ['政治', '科技', '社会', '明星', '电影', '音乐', '数码', '体育', '汽车']
    data_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for obj in data_wb:
        for t in type_list:
            if str(obj['type']).find(t) != -1:
                if t == '政治':
                    data_count[0] = data_count[0] + 1
                if t == '科技':
                    data_count[1] = data_count[1] + 1
                if t == '社会':
                    data_count[2] = data_count[2] + 1
                if t == '明星':
                    data_count[3] = data_count[3] + 1
                if t == '电影':
                    data_count[4] = data_count[4] + 1
                if t == '同城':
                    data_count[5] = data_count[5] + 1
                if t == '数码':
                    data_count[6] = data_count[6] + 1
                if t == '体育':
                    data_count[7] = data_count[7] + 1
                if t == '汽车':
                    data_count[8] = data_count[8] + 1
    res = {'政治': data_count[0],
           '科技': data_count[1],
           '社会': data_count[2],
           '明星': data_count[3],
           '电影': data_count[4],
           '同城': data_count[5],
           '数码': data_count[6],
           '体育': data_count[7],
           '汽车': data_count[8]}
    # Address = Count_Flag_And_Flow("d://access_log")
    return render_template("mydata.html", data=json.dumps(res))


# 统计豆瓣评分分数个数
@app.route('/chart/read_file')
def get_grade():
    name = request.args['name']
    csv_file = "G:/代做毕业设计/film-recommend/static/{}.csv".format(name)
    try:
        data = read_files(csv_file)
        num1 = 0  # 大于8分
        num2 = 0  # 大于7分小于8分
        num3 = 0  # 大于6分小于7分
        num4 = 0  # 大于5分小于6分
        num5 = 0  # 大于3分小于5分
        num6 = 0  # 小于3分
        for k in data['emotion']:
            data = str(k)
            grade = float(data) * 10
            if grade >= 8.0:
                num1 += 1
            elif 7.0 <= grade < 8.0:
                num2 += 1
            elif 6.0 <= grade < 7.0:
                num3 += 1
            elif 5.0 <= grade < 6.0:
                num4 += 1
            elif 3.0 <= grade < 5.0:
                num5 += 1
            else:
                num6 += 1

        name_type = ['大于8分', '大于7分小于8分', '大于6分小于7分', '大于5分小于6分', '大于3分小于5分', '小于3分']
        data_value = [num1, num2, num3, num4, num5, num6]
        res = {
            'code': 0,
            'data': name_type,
            'value': data_value
        }
    except:
        res = {
            'code': -2,
            'msg': "当前事件数据不存在，请前往热点分析爬取评论数据"
        }

    return json.dumps(res).encode('utf-8')


# 频率分布直方图
@app.route('/chart/year')
def get_year_num():
    name = request.args['name']
    csv_file = "G:/代做毕业设计/film-recommend/static/{}.csv".format(name)
    try:
        data = read_files(csv_file)
        year_name = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        data_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in data['emotion']:
            data = str(k)
            grade = int(float(data) * 10)
            if grade == 1:
                data_value[0] += 1
            elif grade == 2:
                data_value[1] += 1
            elif grade == 3:
                data_value[2] += 1
            elif grade == 4:
                data_value[3] += 1
            elif grade == 5:
                data_value[4] += 1
            elif grade == 6:
                data_value[5] += 1
            elif grade == 7:
                data_value[6] += 1
            elif grade == 8:
                data_value[7] += 1
            elif grade == 9:
                data_value[8] += 1
            else:
                data_value[9] += 1
        res = {
            'code': -1,
            'data': year_name,
            'value': data_value
        }
    except:
        res = {
            'code': -2,
        }
    return json.dumps(res).encode('utf-8')


# 分析评论地址
@app.route('/chart/country')
def get_year_country():
    name = request.args['name']
    csv_file = "G:/代做毕业设计/film-recommend/static/{}.csv".format(name)
    try:
        data = read_files(csv_file)
        country_name = ['北京', '上海', '广东', '深圳', '南京', '杭州', '西安', '重庆', '成都']
        data_value = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for country in data['source']:
            start = 0
            for k in country_name:
                if str(country).find(k) != -1:
                    data_value[start] = data_value[start] + 1
                    start = 0
                else:
                    start += 1
        res = {
            'code': -1,
            'data': country_name,
            'value': data_value
        }
    except:
        res = {
            'code': -2
        }
    return json.dumps(res).encode('utf-8')


# 统计情绪分
@app.route('/chart/time')
def get_time():
    name = request.args['name']
    csv_file = "G:/代做毕业设计/film-recommend/static/{}.csv".format(name)
    try:
        data = read_files(csv_file)
        count_data = [0, 0, 0]
        for time_long in data['emotion']:
            if time_long < 0.5:
                count_data[0] += 1
            elif 0.5 <= time_long < 0.7:
                count_data[1] += 1
            else:
                count_data[2] += 1
        time_name = ['情绪积极用户', '情绪平稳用户', '情绪消极用户']
        pie_node = {
            'name': time_name[2],
            'value': count_data[0]
        }
        pie_node1 = {
            'name': time_name[1],
            'value': count_data[1]
        }
        pie_node2 = {
            'name': time_name[0],
            'value': count_data[2]
        }
        res = {
            'code': 1,
            'data': [pie_node, pie_node1, pie_node2]
        }
        getcloud_chart(getap10_chart(data))
    except:
        res = {
            'code': -2
        }
        # 生成词云
    return json.dumps(res).encode('utf-8')


# 首页
@app.route('/')
def login():
    return render_template("login.html")


# 注册页面
@app.route('/register')
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.register_blueprint(api_url_user, url_prefix='/admin')
    app.register_blueprint(api_url_check, url_prefix='/weibo')
    app.run('0.0.0.0', port=5001, debug=False)
