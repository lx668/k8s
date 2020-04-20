## 常规部署
`kubectl apply -f zhipin-common.yaml`

升级pod期间如果是deployment控制器资源的修改,可使用"apply"和"patch"命令来执行; 如果仅仅是修改容器镜像,可使用"set image"
```
[root@master log-pilot]# kubectl patch deployments zhipin-common -p '{"spec": {"minReadySeconds": 50}}'
deployment.extensions/zhipin-common patched

[root@master log-pilot]# kubectl patch deployments zhipin-common -p '{"spec": {"containers": [{"name":"zhipin-common"},{"images":"registry-img.weizhipin.com/deploy/zhipin-common-server:1.0.196"}]}}'
deployment.extensions/zhipin-common patched (no change)

[root@master log-pilot]# kubectl set image deployments zhipin-common zhipin-common=registry-img.weizhipin.com/deploy/zhipin-common-server:1.0.196
```

## 金丝雀部署方式
```
[root@master log-pilot]# kubectl set image deployments zhipin-common zhipin-common=registry-img.weizhipin.com/deploy/zhipin-common-server:1.0.197 && kubectl rollout pause deployments zhipin-common
[root@master log-pilot]# kubectl rollout resume deployments zhipin-common

查看监控的状态
kubectl rollout status deployments zhipin-common
```

