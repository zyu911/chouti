#!/usr/bin/env python
# -*- coding:utf-8 -*-


class DIMapper:

    __mapper_dict = {}

    @staticmethod
    def inject(cls, arg):
        if cls not in DIMapper.__mapper_dict:
            DIMapper.__mapper_dict[cls] = arg

        print(DIMapper.__mapper_dict)

    @staticmethod
    def get_mappers():
        return DIMapper.__mapper_dict


class DIMetaClass(type):

    def __call__(cls, *args, **kwargs):
        # 获取配置的对应的对象，携带进入
        obj = cls.__new__(cls, *args, **kwargs)

        mapper_dict = DIMapper.get_mappers()
        if cls in mapper_dict:
            cls.__init__(obj, mapper_dict[cls])
        else:
            cls.__init__(obj, *args, **kwargs)
        return obj


"""
# How To Use:

class Foo(metaclass=DIMetaClass):

    def __init__(self, name):
        self.name = name

DIMapper.inject(Foo,'123')
f = Foo()
print(f.name)

"""