import sys
import dis
import traceback
import functools

def allowed_events(allowed):
    def decorator(func):
        func.__allowed_events__ = allowed
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
    return decorator


def audithook(event, args):
    if event in ['sys._getframe',]:        
        return

    try:
        frame = sys._getframe(1)
    except ValueError:
        return

    if event == 'object.__getattr__' and repr(frame).split()[-1] == 'audithook>' and args[1] == 'f_code':
        return
        

    func_name = frame.f_code.co_name
    func = frame.f_locals.get(func_name)
    while func is None:
        frame = frame.f_back
        func = frame.f_locals.get(func_name)
    allowed = getattr(func, '__allowed_events__', {})

    if event not in allowed:
        raise RuntimeError('Event not allowed')
    
    for a, b in zip(allowed[event], args):
        if a != b:
            raise RuntimeError('Event not allowed')



sys.addaudithook(audithook)


@allowed_events({'open': ('good1.txt',)})
def f():
    @allowed_events({'open': ('good2.txt',)})
    def f_1():
        print(open('good2.txt').read())
    
    f_1()
    print(open('good1.txt').read())
    print(open('bad.txt').read())

f()

