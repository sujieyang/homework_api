from api接口.models import db, app, Thing
from flask_restful import  Api, reqparse, abort,MethodView
from flask import render_template, jsonify
import json

"""
    api返回格式为{"status":XXX,
                  "message":XXX,
                  "data":{...}}
"""

# 实例化对象
api = Api(app)
# 参数解析,方便验证表单
parse = reqparse.RequestParser()
parse.add_argument('thing', type=str)
parse.add_argument('status', type=int)
parse.add_argument('addtime', type=str)
parse.add_argument('deadline', type=str)

# 添加待办事项
class AddThing(MethodView):
    def post(self):
        # 获取post传来的数据
        args = parse.parse_args()
        thing = args["thing"]
        status = args["status"]
        addtime = args["addtime"]
        deadline = args["deadline"]
        try:
            new_thing = Thing(thing=thing, status=status, addtime=addtime, deadline=deadline)
            db.session.add(new_thing)
            db.session.commit()
            return {"status": 200,
                    "message": "Add success",
                    "data": None}
        except:
            return {"status": 404,
                    "message": "Add failed",
                    "data": None}

    def get(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have post method.",
            "data": None,
        })

    def put(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have post method.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have post method.",
            "data": None,
        })


# 将待办事项设置为已完成
class Be_finished(MethodView):
    def put(self, id):
        i = Thing.query.filter_by(id=id).first()
        if i == None:
            abort(404, message="Thing is not found!")
        if id == 0:  # id=0时，则将所有得事项全部置为完成。
            item_list = Thing.query.filter_by(status=0).all()
            for item in item_list:
                item.status = 1
            db.session.commit()
            return {"status": 200,
                    "message": "All things have finished !",
                    "data": None
                    }
        else:  # id不为0时将相应id的事项设置为已完成
            item = Thing.query.filter_by(id=id).first()
            item.status = 1
            db.session.commit()
            return {"status": 200,
                    "message": "Thing (id = %d) have finished !" % id,
                    "data": None
                    }

    def get(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })

class Be_todoed(MethodView):
    def put(self, id):
        i = Thing.query.filter_by(id=id).first()
        if i == None:
            abort(404, message="Thing is not found!")
        if id == 0:  # id=0时，则将所有得事项全部置为待办。
            item_list = Thing.query.filter_by(status=1).all()
            for item in item_list:
                item.status = 0
            db.session.commit()
            return {"status": 200,
                    "message": "All things have todoed !",
                    "data": None
                    }
        else:  # id不为0时将相应id的事项设置为已完成
            item = Thing.query.filter_by(id=id).first()
            item.status = 0
            db.session.commit()
            return {"status": 200,
                    "message": "Thing (id = %d) have todoed !" % id,
                    "data": None
                    }

    def get(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have put method.",
            "data": None,
        })


class Get_thing(MethodView):  # all则输出所有事项，finished则输出状态为已经完成得，todo则输出未完成得。
    def get(self, order):
        data = {}
        if order == "all":
            thing_list = Thing.query.all()
            for thing in (thing_list):
                data["thing_id=%d" % thing.id] = {"thing_thing": thing.thing,
                                                  "thing_status": "待办" if thing.status == 0 else "已完成",
                                                  "thing_addtime": thing.addtime,
                                                  "thing_deadline": thing.deadline}
        elif order == "finished":
            thing_list = Thing.query.filter_by(status=1).all()
            for thing in thing_list:
                data["thing_id=%d" % thing.id] = {"thing_thing": thing.thing,
                                                  "thing_status": "已完成",
                                                  "thing_addtime": thing.addtime,
                                                  "item_deadline": thing.deadline}
        elif order == "todo":
            thing_list = Thing.query.filter_by(status=0).all()
            for thing in thing_list:
                data["thing_id=%d" % thing.id] = {"thing_thing": thing.thing,
                                                  "thing_status": "待办",
                                                  "thing_addtime": thing.addtime,
                                                  "thing_deadline": thing.deadline}
        else:
            abort(404, message="Invalid instruction,your order must have"
                               " 'all' , 'todo'  or 'finished'.")
        return jsonify({'status': 200,
                        'message': 'get ' + order + ' data',
                        'data': [data]})

    def post(self, instruction):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })

    def delete(self, instruction):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })

    def put(self, instruction):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })


# 获取事项数量
class Get_count(MethodView):
    def get(self, order):
        if order == "all":
            count = len(Thing.query.all())
        elif order == "finished":
            count = len(Thing.query.filter_by(status=1).all())
        elif order == "todo":
            count = len(Thing.query.filter_by(status=0).all())
        else:
            abort(404, message="Invalid instruction,your order must have"
                               " 'all' , 'todo'  or 'finished'.")
        return json.dumps({
            "status": 200,
            "message": "get '" + order + "' item count.",
            "data": count,
        }, ensure_ascii=False)

    def post(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })

    def delete(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })

    def put(self):
        return json.dumps({
            "status": 555,
            "message": "Invalid method.Only have get method.",
            "data": None,
        })


# 删除某id事项
class Delete_thing(MethodView):
    def delete(self, id):
        thing = Thing.query.filter_by(id=id).first()
        if thing == None:
            abort(404, message="Thing is not found!")
        db.session.delete(thing)
        db.session.commit()
        return json.dumps({
            "static": 200,
            "message": "Thing (id = %d) has been deleted !" % id,
            "data": None
        })

    def put(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })

    def get(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })


# 删除多项事项
class Delete_things(MethodView):
    def delete(self, order):
        if order == "all":
            things = Thing.query.all()
        elif order == "finished":
            things = Thing.query.filter_by(status=1).all()
        elif order == "todo":
            things = Thing.query.filter_by(status=0).all()
        else:
            abort(404, message="invalid instruction,your order must have"
                               " 'all' , 'todo'  or 'finished'.")
        count = 0
        for thing in things:
            count += 1
            db.session.delete(thing)
            db.session.commit()
        return json.dumps({
            "status": 200,
            "message": "delete '" + order + "' item success!",
            "data": {"delete_count": count},
        }, ensure_ascii=False)  # json让其输出中文

    def put(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })

    def post(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })

    def get(self):
        return json.dumps({
            "status": 555,
            "message": "invalid method.Only have delete method.",
            "data": None,
        })


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(AddThing, '/Add_thing')
api.add_resource(Be_finished, '/Be_finished/<int:id>')
api.add_resource(Be_todoed, '/Be_todoed/<int:id>')
api.add_resource(Get_thing, '/Get_thing/<string:order>')
api.add_resource(Get_count, '/Get_count/<string:order>')
api.add_resource(Delete_thing, '/Del_thing/<int:id>')
api.add_resource(Delete_things, '/Del_things/<string:order>')

if __name__ == '__main__':
    app.run()
