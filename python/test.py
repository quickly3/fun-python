#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 演示获得数据库配置参数，使用必备参数
def demo_get_conf1(*params):
    print(params)


def demo_get_conf2(**params):
    print(params)


demo_get_conf2(conf={'root', '1234', '127.0.0.1', '3306', 'tests', 'utf8'})
