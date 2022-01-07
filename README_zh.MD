
- [English](README.MD)
- 中文

# Delay ExE

- 一个延迟 _(直到服务器没有玩家)_ 才执行指定命令的插件
- 可以当做*API*用
- ~~原理非常简单, 就不多介绍了~~

### API示例

```python

import delayexe

def a_method():
	delayexe.add_delay_task('say There are no player online') # 执行minecraft命令
	delayexe.add_delay_task('kill @a') # 不会有任何东西被杀死, 在任何时候
	delayexe.add_delay_task(lambda: print('There are no player online')) # 可以执行python无参函数
	delayexe.clear_delay_task() # 清除所有任务

# ...

a_method()

# ...

```
