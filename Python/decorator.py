# 装饰器让你在一个函数的前后去执行代码。
# 所以被装饰的函数要作为参数传递给装饰器。
def a_new_decorator(a_func):
	def wrapTheFunction():
		print("I am doing some boring work before executing a_func()")
		a_func()
		print("I am doing some boring work after executing a_func()")
	return wrapTheFunction

def a_function_requiring_decoration():
	print("I am the function which needs")

a_function_requiring_decoration()

a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

a_function_requiring_decoration()

# 使用@符号
@a_new_decorator
def a_function_requiring_decoration():
    """
    Hey you! Decorate me!
    """
    print("I am the function which needs some decoration to remove my foul smell")

a_function_requiring_decoration()

# 如果运行如下代码会存在一个问题：
print(a_function_requiring_decoration.__name__)

# 函数的名字和注释文档被重写了
# 所以要使用functools.wraps来解决这个问题。

from functools import wraps

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    """
    Hey you! Decorate me!
    """
    print("I am the function which needs some decoration to remove my foul smell")

print(a_function_requiring_decoration.__name__)

# 装饰器蓝本规范

from functools import wraps

def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated

@decorator_name
def func():
    return("Function is running")

can_run = True
print(func())

can_run = False
print(func())


# 授权

from functools import wraps

def requires_auth(f):
    @wraps
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated

# 日志

from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
    """
    Do some math.
    """
    return x + x

result = addition_func(4)

# 带参数的装饰器

from functools import wraps

def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            # 打开logfile，并写入内容
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1()

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()

# 装饰器类
from functools import wraps

class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)
        return wrapped_function

    def notify():
        # logit只打日志，不做别的
        pass

class email_logit(logit):
    '''
    一个logit的实现版本，可以在函数调用时发送email给管理员
    '''
    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(logit, self).__init__(*args, **kwargs)

    def notify(self):
        # 发送一封email到self.email
        # 这里就不做实现了
        pass