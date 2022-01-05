
- English
- [中文](README_zh.MD)

# Delay ExE

- A plugin for delay execute command until there are no player online
- You can use it API

### Example for API

```python

import delayexe

def a_method():
	delayexe.add_delay_task('say There are no player online') # run minecraft command
	delayexe.add_delay_task('kill @a') # Must nothing to kill
	delayexe.add_delay_task(lambda: print('There are no player online')) # run python method
	delayexe.clear_delay_task() # clear all delay task

# ...

a_method()

# ...

```

