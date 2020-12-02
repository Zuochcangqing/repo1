"""Mongodb条件查询:
<<比较符号>>
符号:              含义:                   示例:
1. $gt             大于                    {'age': {'$gt': 20}}
2. $lt             小于                    {'age': {'$lt': 20}}
3. $gte            大于等于                {'age': {'$gte': 20}}
4. $lte            小于等于                {'age': {'$lte': 20}}
5. $ne:            不等于                  {'age': {'$ne': 20}}
6. $in             在范围内                {'age': {'$in': [20, 30]}}
7. $nin            不在范围内              {'age': {'$nin': [20, 30]}}
<<功能符号>>
符号:               含义:                  示例:
1. $regex          匹配正则表达式          {'name': {'$regex': '^M.*'}}  # 查询以M开头的name值
2. $exists         属性是否存在            {'name': {'$exists': True}}  # 查询name属性是否存在
3. $type           类型判断                {'age': {'$type': 'int'}}  # 查询age的类型为int
3. $mod            数字模操作              {'age': {'$mod': [5, 0]]}}  # 查询年龄为模5余0的结果
3. $text           文本查询                {'$text': {'$search': 'Mike'}}  # 查询text类型的属性中包含'Mike'字符串的结果
3. $where          高级条件查询            {'name': {'$where': 'obj.fans_count == obj.follows_count'}}  # 自身粉丝数等于关注数

Mongodb数据更新指令: (指令必须使用双引号)
1: $inc增加字段值
    db.test.update({'id':6},{"$inc":{'id':2}})  # result：id=8
    db.test.update({'id':6},{$inc:{id:2}})  # 在mongodb交互环境中的写法

2: $set更新字段值
    db.test.update({'id':6},{"$set":{'id':2}})  result：id=2
    db.test.update({'id':6},{$set:{id:2}})  # 在mongodb交互环境中的写法

3: $unset删除字段
    db.test.update({'id':6},{"$unset":{'id':6}})
    db.test.update({'id':6},{$unset:{id:6}})  # 在mongodb交互环境中的写法

4: $rename重命名字段
    db.test.update({'id':1},{"$rename":{'id':'name'}})
    db.test.update({id:10},{$rename:{id:'name'}})  # 在mongodb交互环境中的写法
"""
# -*- coding:utf-8 -*-
import pymongo
from bson.objectid import ObjectId

__author__ = 'Evan'


def mongodb_handle(host='localhost', port=27017):
    """
    连接mongodb客户端
    :param host: mongodb host
    :param port: mongodb access port
    :return:
    """
    # 连接mongodb客户端
    client = pymongo.MongoClient(host=host, port=port)

    # 创建数据库example
    database = client['example']  # 或者写成 client.example
    db_name = eval(str(database).split()[-1][:-1])
    print('创建数据库: {}'.format(db_name))

    # 创建集合table
    table = database['table']  # 或者写成 database.table
    table_name = eval(str(table).split()[-1][:-1])
    print('创建集合: {}'.format(table_name))

    # 定义字段
    name = dict(name='Evan')
    age = dict(age=24)
    stature = dict(stature=177)

    # 插入数据到table集合
    table.insert_one(name)  # 插入单行数据
    table.insert_many([age, stature])  # 插入多行数据

    # 更新table集合中数据
    update_format = {"$set": {'stature': 26}}  # 更新age值为26
    result = table.update_one(age, update_format)  # 更新匹配到的第一个数据
    print('更新个数: {}'.format(result.matched_count))  # 查看更新个数
    table.update_one(age, {"$set": age}, upsert=True)  # 数据去重，如果集合里面有age字段就更新该字段，没有则创建一个age字段
    table.update_many(age, update_format)  # 更新匹配到的所有数据

    # 查询table集合中数据
    print(table.find_one({'_id': ObjectId('5dd642b94957a6800e0187c1')}))  # 根据ID查询，返回匹配到的第一个结果
    print(table.find_one(name))  # 根据name字段查询，返回匹配到的第一个结果
    print(table.find_one({'age': {'$gt': 10}}))  # 使用比较符号查询，返回结果大于10的age字段
    print(table.find_one({'name': {'$regex': 'Ev.+'}}))  # 使用正则表达式查询，返回匹配到的第一个结果
    print([i for i in table.find(name)])  # 返回匹配到的所有name字段
    print([i for i in table.find()])  # 返回集合中所有数据
    # 计数
    print('查询name字段个数: {}'.format(table.count_documents(name)))  # 查询指定字段个数
    # 字段排序
    print([table.find().sort('name', pymongo.DESCENDING)])  # 返回所有数据，并且name字段是以降序排序的
    print([table.find().sort('name', pymongo.ASCENDING)])  # 返回所有数据，并且name字段是以升序排序的
    # 字段偏移
    print([table.find().sort('name', pymongo.ASCENDING).skip(2)])  # 忽略前2个name字段，返回从第三个及以后的name字段
    print([table.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)])  # 只保留第三个及以后name字段的2个匹配结果

    # 删除table集合中数据
    result = table.delete_one(stature)  # 删除匹配到的第一个数据
    print('删除个数: {}'.format(result.deleted_count))  # 查看删除个数
    table.delete_many(stature)  # 删除匹配到的所有数据

    # 关闭客户端连接
    client.close()


if __name__ == '__main__':
    mongodb_handle(host='localhost')