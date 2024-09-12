import os
import sys
if __name__ == '__main__':
    # env_vars = os.environ
    # # print(env_vars)
    # for kwy, value in env_vars.items():
    #     print(f'{kwy}={value}')
        
    def get_command_line_args():
        for _, args in  enumerate(sys.argv[1:]):
            print(args)
            
