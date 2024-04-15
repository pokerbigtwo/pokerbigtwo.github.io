import json

hook_frame = '''
import sys

def hook(evt, arg):
    if evt in ["sys._getframe", "object.__getattr__", "object.__setattr__"]:
        return
    frame = sys._getframe(0)
    f = frame.f_code.co_filename
    
    while frame:
        if frame.f_back is None:
            break
        else:
            frame = frame.f_back
        
        try:
            class_name = frame.f_locals['self'].__class__.__name__
        except KeyError:
            class_name = None
        
        func_name = frame.f_code.co_name
        if frame.f_code.co_filename == f:
{hook_condition}
'''

hook_script = '''
            if func_name == \"{func_name}\":
                if evt not in {evt}:
                    raise RuntimeError('Event not allowed')
'''

class_hook_script = '''
            if class_name == {class_name}:
                if func_name == \"{func_name}\":
                    if evt not in {evt}:
                        raise RuntimeError('Event not allowed')
'''

def get_all_callees(caller, call_graph, visited=None):
    if visited is None:
        visited = set()
    visited.add(caller)
    callees = call_graph[caller]
    for callee in callees:
        if callee not in visited:
            visited |= get_all_callees(callee, call_graph, visited)
    return visited

def get_call_graph(call_graph):
    result = {}
    for caller in call_graph:
        result[caller] = get_all_callees(caller, call_graph)
    return result

# get dependency relation in the script
def clean_cg(cg_dep, entry_name):
    clean_dep = {}
    # get all function calling dependency
    call_deps = get_call_graph(cg_dep)
    
    # find real name in cg_dep
    if entry_name not in cg_dep:
        entry_name = "..." + entry_name
    
    # get all function from the script
    for caller, callee in call_deps.items():
        # if caller.find(entry_name) != -1:
        clean_dep[caller] = call_deps[caller]
    
    # print(clean_dep)
    return clean_dep

# map function to audit event
def function_event(clean_dep):
    caller_audit = {}
    with open("dep_data/standard_audit.json") as open_file:
        standard_audit = json.load(open_file)
    with open("dep_data/audit_package.json") as open_file2:
        audit_package = json.load(open_file2)
    
    file1=open("pycg.log","w")
    file2=open("rule.log","w")
    for caller, callees in clean_dep.items():
        caller_audit[caller] = set()
        file1.write(f"{caller}: {list(callees)}\n")
        for callee in callees:
            if callee in standard_audit:
                caller_audit[caller].update(set(standard_audit[callee]))

        # TODO: need to handle package
        for callee in callees:
            if callee in audit_package:
                caller_audit[caller].update(set(audit_package[callee]))
        # print(caller, caller_audit[caller])
        caller_audit[caller] = list(caller_audit[caller])
        file2.write(f"{caller}: {caller_audit[caller]}\n")
    return caller_audit

def function_event_tornado(clean_dep):
    # print("tornado")
    caller_audit = {}
    with open("dep_data/standard_audit.json") as open_file:
        standard_audit = json.load(open_file)
    with open("dep_data/audit_package.json") as open_file2:
        audit_package = json.load(open_file2)
    
    file1=open("pycg.log","w")
    file2=open("rule.log","w")
    for caller, callees in clean_dep.items():
        caller_audit[caller] = set()
        file1.write(f"{caller}: {list(callees)}\n")
        for callee in callees:
            if callee in standard_audit:
                caller_audit[caller].update(set(standard_audit[callee]))

        # TODO: need to handle package
        for callee in callees:
            if callee in audit_package:
                caller_audit[caller].update(set(audit_package[callee]))
        
        # print(callees)
        if caller[-3:]=="get":
            caller_audit[caller].update(set(["open","exec","compile"]))
        # print(caller, caller_audit[caller])
        caller_audit[caller] = list(caller_audit[caller])
        file2.write(f"{caller}: {caller_audit[caller]}\n")
    return caller_audit



class HookGenerator():
    def __init__(self, entry, filename, package):
        # usaully python file name, take xxx.py -> xxx
        # ex. ../exploit/main.py -> ...exploit.main
        self.entry_name = entry[0][1:-3].replace('/', '.')
        self.filename = filename
        self.package = package

    # call relation of input script
    def set_cg_dep(self, cg_dep):
        self.cg_dep = cg_dep
        self.clean_dep = dict()
        self.script_call_event = dict()
        
    def set_class_dep(self, class_dep):
        self.class_dep = []
        for class_name, class_func in class_dep.items():
            self.class_dep.append(class_name.split(".")[-1])
        # print(self.class_dep)
        

    def generate_hook(self):
        
        if len(self.script_call_event) > 0:
            hook_condition = ""
        else:
            return
        
        hook_code = ""
        if len(self.entry_name.split("."))>3:
            self.entry_name = self.entry_name.split(".")[-3]+"."+self.entry_name.split(".")[-2]+"."+self.entry_name.split(".")[-1]
        # print(self.entry_name)
        for func, evt in self.script_call_event.items():
            # print(func,evt)
            if self.entry_name in func and len(evt) > 0:
                if len(func.split("."))>=3 and func.split(".")[-2] in self.class_dep:
                    class_name = func.split(".")[-2]
                    class_name="\""+class_name+"\""
                    func_name = func.split(".")[-1]
                    hook_condition = hook_condition + class_hook_script.format(class_name=class_name,func_name=func_name, evt=evt)
                else:
                    func_name = func.split(".")[-1]
                    hook_condition = hook_condition + class_hook_script.format(class_name=None,func_name=func_name, evt=evt)
                hook_code = hook_frame.format(hook_condition=hook_condition)
        
        with open(self.filename, 'w') as f:
            f.write(hook_code)


    def analyze(self):
        
        self.clean_dep = clean_cg(self.cg_dep, self.entry_name)
        # print(self.cg_dep)
        if self.package=="tornado":
            self.script_call_event = function_event_tornado(self.clean_dep)
        else: 
            self.script_call_event = function_event(self.clean_dep)
        self.generate_hook()