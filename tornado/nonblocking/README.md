# tornado_nonblocking

前段时间公司项目中的api，变得非常卡，导致前台某些页面的响应时间达到5、6秒，这已经超出了可接受范围。tornado据称是异步非堵塞的web框架，所以当时才选用它的，但具体怎么非堵塞的，非堵塞的原理，以及是否不用设置就是非堵塞的，这些一直不太明白，趁着遇到这个问题，把tornado文档从头到尾看了一遍，大致搞懂了一些，下面做个总结。

## 测试步骤

* 把项目clone到本机

``` sh
cd ~/dev/
git clone ....
```

* 启动Server和Client

打开两个terminal窗口，分别切换到项目目录，并启动服务

``` sh
# 窗口一：模拟耗时的服务
cd ~/dev/tornado_nonblocking
python blockingServer.py

# 窗口二：模拟tornado的堵塞和非堵塞调用
cd ~/dev/tornado_nonblocking
python blockingServer.py
```

* 用siege模拟并发访问堵塞和非堵塞的url

``` sh
siege http://127.0.0.1/non_blocking1 -c10 -t60s
siege http://127.0.0.1/non_blocking2 -c10 -t60s # 两张非堵塞方式都可以，参考两张写法的不同
siege http://127.0.0.1/blocking -c10 -t60s # 堵塞方式
```

* 并发访问的同时访问其它页面
打开浏览器，访问 http://127.0.0.1/common ，查看不同模拟情况下，访问是否正常

## 参考

* https://my.oschina.net/zhengtong0898/blog/715615
* http://demo.pythoner.com/itt2zh/ch5.html
