import datetime
import json

from flask import render_template, Blueprint, request

from service.getdata import get_readUrl, get_data
from utils import create_sql, mybaits

api_url_check = Blueprint('/feelCheck', __name__)


# 用户个人主页
@api_url_check.route('/weibo_page')
def get_check_info():
    return render_template("getdata.html")


# 用户登陆接口
@api_url_check.route("/weibo_data", methods=['POST', 'GET'])
def get_datas():
    url = request.form['url_name']
    url_get = "https://m.weibo.cn/comments/hotflow"
    cookie = request.form['cookie']
    comment = request.form['comment']
    type = request.form['type']
    name = request.form['name']
    try:
        res_comment_url = get_readUrl(comment)
        res_commit = get_data(url_get, res_comment_url, cookie, name)
        res = []
        for k in res_commit:
            res_data = "编号:" + str(k['id']) + "  评论:" + k['console'] + "  地点:" + k['source'] + "\n"
            res.append(res_data)
        str_data = ""
        for k in res:
            str_data = str_data + k
        if request.form['save'] == "是":
            time_data = str(datetime.datetime.now())
            data = ["'{}'".format(time_data), "'{}'".format(url), "'{}'".format(cookie), "'{}'".format(comment),
                    "'{}'".format(type), "'{}'".format(name)]
            sql = create_sql.create_insert(['createTime', 'url', 'cookie', 'commit_url', 'type', 'name'], data, "wblog")
            mybaits.add(sql)
        if len(res) > 0:
            res_data = {
                "code": 1,
                "msg": name + "事件用户评论获取成功",
                "data": str_data
            }
        else:
            res_data = {
                "code": -2,
                "msg": "登录态失效，请重新刷新尝试",
                "data": str_data
            }
        return json.dumps(res_data).encode('utf-8')
    except:
        res_data = {
            "code": -1,
            "msg": "系统网络不稳定",
            "data": str_data
        }
        return json.dumps(res_data).encode('utf-8')


# 用户个人主页
@api_url_check.route('/weibo_log')
def get_check_infos():
    return render_template("wblog.html")


# 获取爬取记录
@api_url_check.route('/get_wblog')
def get_check_data():
    sql = "select * from wblog where id>0 order by id desc"
    res_data = ['id', 'createTime', 'url', 'cookie', 'commit_url', 'type', 'name']
    res = mybaits.select(sql, res_data)
    res_succ = {
        'code': 1,
        'msg': "success",
        'data': res
    }
    return json.dumps(res_succ).encode("utf-8")
