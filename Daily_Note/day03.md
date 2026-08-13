# Day 3 Linux 进程与远程任务笔记

日期：2026-08-13  
学习环境：CentOS 7 client / CentOS 9 server  
学习主题：SSH 免密登录、nohup 后台训练、远程提交任务

## 一、今天的目标

今天重点练习的是用两台 CentOS 虚拟机模拟远程提交训练任务，核心内容包括：

1. CentOS 7 作为 client，负责提交任务
2. CentOS 9 作为 server，负责运行任务
3. 配置 SSH 密钥免密登录
4. 编写 `nohup` 后台运行训练脚本
5. 从 client 远程查看日志和停止任务

## 二、整体思路

这次实验可以理解成：

```text
CentOS 7 client
        |
        | ssh / scp
        v
CentOS 9 server
```

client 负责发命令，server 负责真正运行训练程序。

一句话总结：

**先让 client 能免密登录 server，再让 server 后台运行训练脚本。**

## 三、实验重点

### 1. 确认两台机器能连通

先在 server 上查看 IP：

```bash
ip addr
```

然后在 client 上测试：

```bash
ping server的IP
```

如果能收到回复，说明两台虚拟机网络是通的。

### 2. server 开启 SSH 服务

在 CentOS 9 server 上执行：

```bash
sudo systemctl status sshd
sudo systemctl start sshd
sudo systemctl enable sshd
```

如果开了防火墙，还需要允许 SSH：

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### 3. 配置 SSH 免密登录

在 CentOS 7 client 上生成密钥：

```bash
ssh-keygen -t rsa -b 4096
```

把公钥复制到 server：

```bash
ssh-copy-id trainer@server的IP
```

测试免密登录：

```bash
ssh trainer@server的IP
```

如果不用输入密码就能进入 server，说明免密登录成功。

## 四、nohup 后台训练脚本

在 server 上创建训练目录：

```bash
mkdir -p ~/train_demo/logs
cd ~/train_demo
```

创建 `train.py`：

```python
import time

for epoch in range(1, 101):
    print('epoch {}: training...'.format(epoch), flush=True)
    time.sleep(2)

print('training finished', flush=True)
```

这个脚本只是模拟训练过程，每隔 2 秒输出一次训练信息。

创建 `run_train.sh`：

```bash
#!/bin/bash

cd ~/train_demo || exit 1

mkdir -p logs

nohup python3 train.py > logs/train.log 2>&1 &

echo $! > logs/train.pid
echo "Training started"
echo "PID: $(cat logs/train.pid)"
echo "Log: ~/train_demo/logs/train.log"
```

添加执行权限：

```bash
chmod +x run_train.sh
```

其中：

- `nohup`：让程序不受终端关闭影响
- `>`：把正常输出写入日志
- `2>&1`：把错误信息也写入同一个日志
- `&`：让程序进入后台运行
- `$!`：获取刚刚启动的后台进程 PID

## 五、远程提交任务

在 CentOS 7 client 上执行：

```bash
ssh trainer@server的IP "cd ~/train_demo && ./run_train.sh"
```

这条命令的意思是：

1. 从 client 登录 server
2. 进入 server 的训练目录
3. 执行后台训练脚本

任务启动后，client 可以退出，不影响 server 上的训练程序继续运行。

## 六、查看和停止任务

查看日志：

```bash
ssh trainer@server的IP "tail -f ~/train_demo/logs/train.log"
```

查看进程：

```bash
ssh trainer@server的IP "ps -ef | grep train.py"
```

查看 PID：

```bash
ssh trainer@server的IP "cat ~/train_demo/logs/train.pid"
```

停止任务：

```bash
ssh trainer@server的IP "kill \$(cat ~/train_demo/logs/train.pid)"
```

注意：`tail -f` 只是查看日志，按 `Ctrl + C` 只是停止查看，不会停止训练任务。

## 七、今天学到的命令

| 命令 | 用途 |
|---|---|
| `ip addr` | 查看机器 IP 地址 |
| `ping` | 测试两台机器是否连通 |
| `systemctl status sshd` | 查看 SSH 服务状态 |
| `ssh` | 远程登录或远程执行命令 |
| `ssh-keygen` | 生成 SSH 密钥 |
| `ssh-copy-id` | 把公钥复制到 server |
| `scp` | 在两台机器之间传文件 |
| `nohup` | 后台运行程序 |
| `ps -ef` | 查看进程 |
| `kill` | 停止进程 |
| `tail -f` | 实时查看日志 |

## 八、易错点

1. Linux 路径区分大小写，`/home` 和 `/HOME` 不是一个目录。
2. `ssh-copy-id` 要在 client 上执行，不是在 server 上执行。
3. 私钥 `id_rsa` 不能给别人，公钥 `id_rsa.pub` 可以放到 server。
4. `nohup` 后面一般要加 `&`，否则还是会占着终端。
5. `kill` 后面要写 PID，不是写脚本文件名。
6. `tail -f` 只是看日志，不代表停止任务。
7. Python 报错时可以用 `cat -n train.py` 查看具体行号。
8. `scp` 的远程路径中间有冒号，例如 `trainer@192.168.119.128:~/train_demo/`。

## 九、今日总结

今天的重点是理解远程任务的基本流程：

**client 连接 server -> 配置免密登录 -> server 后台运行任务 -> client 远程查看日志。**

这个流程以后在服务器训练模型、远程跑脚本、提交后台任务时都会经常用到。
