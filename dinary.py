from settings import *
import os

log_count = iter(range(100))

def log_init(fileName=None):
    if fileName is None:
        fileName = DNINARY_DEFAULT_NAME
    with open(os.path.join(DNINARY_PATH, fileName), "w") as log_file:
        pass

def log_write(message, layer=None, fileName=None):
    """撰写简单的日志"""
    if fileName is None:
        fileName = DNINARY_DEFAULT_NAME
    if layer is None:
        layer = next(log_count)
    def decoter(func):
        def ff(*arg, **kwargs):
            try:
                f = open(os.path.join(DNINARY_PATH, fileName), mode="a")
                f.write(layer * "\t" + f"Calling {message}...\n")
                f.close()
                
                ret = func(*arg, **kwargs)

                f = open(os.path.join(DNINARY_PATH, fileName), mode="a")
                f.write(layer * "\t" + f"{message} return\n")
            except Exception as e:
                print(e)
            finally:
                f.close()
            return ret
        return ff
    return decoter
