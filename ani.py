#!/usr/bin/env python3
import colorama

colorama.init()


def main():
    from options import options
    
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Programa interrompido')
        
    # except Exception as error:
    #     print(error)
        