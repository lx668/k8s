#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/15 6:31 下午
# @Author : Lx
# @Site :
# @File : yamltodict.py
# @Software: PyCharm

import yaml
import os
from collections import OrderedDict


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())


def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)


class Deplyment_yaml(object):
    def __init__(self, service_name, replicas, image, disconf_env, jvm_plugins, ops_monitor, server_opts, http_port,
                 tcp_port, env):
        self.service_name = service_name
        self.replicas = replicas
        self.image = image
        self.version = disconf_env
        self.jvm_plugins = jvm_plugins
        self.ops_monitor = ops_monitor
        self.server_opts = server_opts
        self.http_port = http_port
        self.tcp_port = tcp_port
        self.env = env

    def makeyaml(self):
        setup_yaml()
        deployment = OrderedDict()
        deployment['apiVersion'] = 'apps/v1'
        deployment['kind'] = 'Deployment'
        deployment['metadata'] = {'name': self.service_name, 'namespace': 'default',
                                  'labels': {'app': self.service_name}}

        deployment['spec'] = {'replicas': self.replicas,
                              'selector': {'matchLabels': {'app': self.service_name}},
                              'strategy':
                                  {'rollingUpdate': {'maxSurge': 1, 'maxUnavailable': 0}
                                   },
                              'minReadySeconds': 60,
                              'template': {'metadata': {'labels': {'app': 'zhipin-common'}},
                                           'spec': {
                                               'terminationGracePeriodSeconds': 60,
                                               'containers': [
                                                   {'image': self.image,
                                                    'name': self.service_name,
                                                    'imagePullPolicy': 'IfNotPresent',
                                                    'env': self.env,
                                                    'volumeMounts': [
                                                        {
                                                            'name': 'collect-logs', 'mountPath': '/data/logs'
                                                        },
                                                    ],
                                                    'ports': [
                                                        {
                                                            'name': 'http',
                                                            'containerPort': self.tcp_port
                                                        },
                                                        {
                                                            'name': 'tcp',
                                                            'containerPort': self.http_port
                                                        }
                                                    ],
                                                    'readinessProbe': {
                                                        'httpGet': {
                                                            'path': '/actuator/health',
                                                            'port': self.tcp_port
                                                        },
                                                        'initialDelaySeconds': 40,
                                                        'timeoutSeconds': 10},
                                                    }],
                                               'volumes': [
                                                   {
                                                       'name': 'collect-logs',
                                                       'emptyDir': {}
                                                   }
                                               ]
                                           }
                                           }
                              }
        # print yaml.dump(deployment)

        curpath = os.path.dirname(os.path.realpath(__file__))
        yamlpath = os.path.join(curpath, "deployment.yaml")

        # 写入到yaml文件
        with open(yamlpath, "w") as f:
            yaml.dump(deployment, f, default_flow_style=False, Dumper=yaml.Dumper)


if __name__ == '__main__':
    service_name = 'zhipin-common'
    replicas = 2
    version = "1.0.196"
    disconf_env = 'qa'
    image = "registry-img.weizhipin.com/deploy/" + service_name + "-server:" + version
    jvm_plugins = ''
    ops_monitor = ''
    server_opts = ''
    http_port = 8222
    tcp_port = 18012
    env = [
        {'name': 'APP_NAME', 'value': service_name},
        {'name': 'DISCONF_ENV', 'value': disconf_env},
        {'name': 'JVM_PLUGINS', 'value': jvm_plugins},
        {'name': 'OPS_MONITOR', 'value': ops_monitor},
        {'name': 'SERVER_OPTS', 'value': server_opts},
        {'name': 'aliyun_logs_boss-info', 'value': 'stdout'},
        {'name': 'aliyun_logs_boss-access', 'value': "/data/logs/access/*.log"},
        {'name': 'aliyun_logs_boss-trace', 'value': "/data/logs/trace/*.log"},
        {'name': 'aliyun_logs_boss-info', 'value': "/data/logs/zhipin-common/*.log"},
    ]
    res = Deplyment_yaml(service_name, replicas, image, disconf_env, jvm_plugins, ops_monitor, server_opts, http_port,
                         tcp_port, env)
