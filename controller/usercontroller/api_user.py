import datetime
import json

from dao import success
from flask import Blueprint, request
from mapper import userMapper
from flask import render_template
from dao.User import User
from utils.page import create_page

api_url_user = Blueprint('/', __name__)


# 用户个人主页
@api_url_user.route('/myinfo')
def get_myinfo():
    return render_template("myinfo.html")


# 用户列表
@api_url_user.route('/list', methods=['POST', 'GET'])
def get_list():
    if request.method == "GET":
        username = request.args['username']
        if username != "null":
            password = request.args['password']
            sex = request.args['sex']
            root = request.args['root']
        else:
            return render_template("userlist.html")
            # 查询是否存在该用户账号
        res = userMapper.select_user_have(username)
        create_time = str(datetime.datetime.now())
        user = User()
        user.setuser_password(password)
        user.setuser_name(username)
        user.setuser_sex(sex)
        user.setuser_root(root)
        user.setuser_createtime(create_time)
        if res['id'] != 0:
            user.setuser_id(res['id'])
            userMapper.update_info(user)
        else:
            userMapper.add_user(user)
    return render_template("userlist.html")


# 用户登陆接口
@api_url_user.route("/login", methods=['POST', 'GET'])
def login():
    username = request.args['username']
    password = request.args['password']
    res = userMapper.select_userisok(username, password)
    print(res)
    if res['code'] != 0:
        return success.res(res['user'], 1, "登陆成功")
    else:
        return success.res("", -1, "登陆失败，请检查用户名密码")


# 用户注册逻辑
@api_url_user.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        root = request.form['root']
        # 查询是否存在该用户账号
        res = userMapper.select_userisok(username, password)
        if res['code'] != 0:
            return success.res(res, 2, "当前存在该账户，请勿重复注册")
    else:
        username = request.args['username']
        password = request.args['password']
        sex = request.args['sex']
        root = request.args['root']
    create_time = str(datetime.datetime.now())
    user = User()
    user.setuser_password(password)
    user.setuser_name(username)
    user.setuser_sex(sex)
    user.setuser_root(root)
    user.setuser_createtime(create_time)
    res = userMapper.add_user(user)
    if res != 0:
        return success.res("", 1, "注册成功")
    else:
        return success.res("", -1, "注册失败，请稍后重试")


# 用户修改密码
@api_url_user.route("/update/information", methods=['POST', 'GET'])
def updateInformation():
    # 验证密码是否正确
    # TODO 查库
    # 如果密码正常，支持修改
    # TODO 改库
    # 确认修改成功
    if True:
        return success.res("", 1, "账号修改成功")
    else:
        return success.res("", -1, "账号修改失败，请重新尝试")


# 管理员权限设置
"""
  id:id序号
  root：角色1代表普通用户，角色2代表管理员
"""


# 权限修改
@api_url_user.route("/update/root", methods=['POST', 'GET'])
def updata_root():
    # 将对应的id人员的root字段改为设置的角色字段
    if True:
        return success.res("", 1, "权限修改成功")
    else:
        return success.res("", -1, "账号权限修改失败，请重新尝试")


# 列表维护
@api_url_user.route("/user_list", methods=['POST', 'GET'])
def get_userlist():
    page = request.args['page']
    limit = request.args['limit']
    list = userMapper.select_User("-1", "")
    res = create_page(int(page), int(limit), list)
    res_data = {
        "code": 0,
        "msg": "",
        "count": len(list),
        "data": res
    }
    return json.dumps(res_data).encode('utf-8')


# 模糊搜索
@api_url_user.route("/sreach_list", methods=['POST', 'GET'])
def get_userlist_sreach():
    page = request.args['page']
    limit = request.args['limit']
    username = request.args['username']
    ids = request.args['id']
    print("ids", ids)
    if ids != '':
        list_res = userMapper.select_User(str(ids), username)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    else:
        list_res = userMapper.select_User("-1", username)
        res = create_page(int(page), int(limit), list_res)
        res_data = {
            "code": 0,
            "msg": "",
            "count": len(list_res),
            "data": res
        }
    return json.dumps(res_data).encode('utf-8')


@api_url_user.route("/del_user", methods=['POST', 'GET'])
def del_user():
    id = request.args['id']
    userMapper.del_user(str(id))
    res = {
        'code': 1,
        'msg': "删除成功"
    }
    return json.dumps(res).encode("utf-8")


@api_url_user.route("/update_info", methods=['POST', 'GET'])
def info_user():
    id = request.form['id']
    username = request.form['username']
    sign = request.form['sign']
    sex = request.form['sex']
    res_data = userMapper.user_info(id, username, sign, sex)
    if res_data == 1:
        res = {
            'code': 1,
            'msg': "修改成功，请退出登陆，查看信息"
        }
    else:
        res = {
            'code': 0,
            'msg': "修改失败，请重新尝试"
        }
    return json.dumps(res).encode("utf-8")


@api_url_user.route("/update_info_pass", methods=['POST', 'GET'])
def info_user_pass():
    id = request.form['id']
    username = request.form['username']
    oldpassword = request.form['oldpas']
    newpassword = request.form['newpas']
    res_isok = userMapper.select_userisok(username, oldpassword)
    if res_isok['code'] != 0:
        res_pass = userMapper.user_info_pass(id, username, newpassword)
        if res_pass == 1:
            res = {
                'code': 1,
                'msg': "修改成功，请退出登陆"
            }
        else:
            res = {
                'code': 0,
                'msg': "修改失败，请重新尝试"
            }
    else:
        res = {
            'code': 0,
            'msg': "旧密码核验不成功！请重新输入"
        }
    return json.dumps(res).encode("utf-8")


# 我的借阅
@api_url_user.route("/mybook", methods=['POST', 'GET'])
def get_mybook():
    return render_template("mybook.html")


# 我的分享
@api_url_user.route("/myshare", methods=['POST', 'GET'])
def get_myshare():
    return render_template("myshare.html")
