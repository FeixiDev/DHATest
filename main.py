import argparse

class argparse_operator:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='argparse')
        self.setup_parse()

    def setup_parse(self):
        sub_parser = self.parser.add_subparsers()

        self.parser.add_argument('-v',
                                 '--version',
                                 dest='version',
                                 help='Show current version',
                                 action='store_true')

        parser_diskful = sub_parser.add_parser("diskful", aliases=['f'], help='diskful test')
        parser_diskless = sub_parser.add_parser("diskless", aliases=['l'], help='diskless test')

        self.parser.set_defaults(func=self.main_usage)

        parser_diskful.set_defaults(func=self.diskful_operation)
        parser_diskless.set_defaults(func=self.diskless_operation)

        sub_parser_diskful = parser_diskful.add_subparsers()
        parser_diskful_shutdown = sub_parser_diskful.add_parser("shutdown", aliases=['d'], help='diskful shutdown')
        parser_diskful_poweroff = sub_parser_diskful.add_parser("poweroff", aliases=['o'], help='diskful poweroff')
        parser_diskful_ifconfig = sub_parser_diskful.add_parser("ifconfig", aliases=['i'], help='diskful ifconfig')
        parser_diskful_line = sub_parser_diskful.add_parser("line", aliases=['l'], help='diskful network line')
        parser_diskful_port = sub_parser_diskful.add_parser("port", aliases=['p'], help='diskful port')
        parser_diskful_switch = sub_parser_diskful.add_parser("switch", aliases=['s'], help='diskful switch')

        sub_parser_diskless = parser_diskless.add_subparsers()
        parser_diskless_shutdown = sub_parser_diskless.add_parser("shutdown", aliases=['d'], help='diskless shutdown')
        parser_diskless_poweroff = sub_parser_diskless.add_parser("poweroff", aliases=['o'], help='diskless poweroff')
        parser_diskless_ifconfig = sub_parser_diskless.add_parser("ifconfig", aliases=['i'], help='diskless ifconfig')
        parser_diskless_line = sub_parser_diskless.add_parser("line", aliases=['l'], help='diskless network line')
        parser_diskless_port = sub_parser_diskless.add_parser("port", aliases=['p'], help='diskless port')
        parser_diskless_switch = sub_parser_diskless.add_parser("switch", aliases=['s'], help='diskless switch')

        parser_diskful_shutdown.set_defaults(func=self.diskful_shutdown)
        parser_diskful_poweroff.set_defaults(func=self.diskful_poweroff)
        parser_diskful_ifconfig.set_defaults(func=self.diskful_ifconfig)
        parser_diskful_line.set_defaults(func=self.diskful_line)
        parser_diskful_port.set_defaults(func=self.diskful_port)
        parser_diskful_switch.set_defaults(func=self.diskful_switch)
        
        parser_diskless_shutdown.set_defaults(func=self.diskless_shutdown)
        parser_diskless_poweroff.set_defaults(func=self.diskless_poweroff)
        parser_diskless_ifconfig.set_defaults(func=self.diskless_ifconfig)
        parser_diskless_line.set_defaults(func=self.diskless_line)
        parser_diskless_port.set_defaults(func=self.diskless_port)
        parser_diskless_switch.set_defaults(func=self.diskless_switch)

    def main_usage(self,args):
        if args.version:
            print(f'Version: ？')
        else:
            self.parser.print_help()

    def diskful_operation(self,args):
        print("python3 main.py diskful")

    def diskless_operation(self,args):
        print("python3 main.py diskless")

    def diskful_shutdown(self,arg):
        print("python3 main.py diskful shutdown")

    def diskful_poweroff(self,arg):
        print("python3 main.py diskful poweroff")

    def diskful_ifconfig(self,arg):
        print("python3 main.py diskful ifconfig")

    def diskful_line(self,arg):
        print("python3 main.py diskful line")

    def diskful_port(self,arg):
        print("python3 main.py diskful port")
        
    def diskful_switch(self,arg):
        print("python3 main.py diskful switch")

    def diskless_shutdown(self, arg):
        print("python3 main.py diskless shutdown")

    def diskless_poweroff(self, arg):
        print("python3 main.py diskless poweroff")

    def diskless_ifconfig(self, arg):
        print("python3 main.py diskless ifconfig")

    def diskless_line(self, arg):
        print("python3 main.py diskless line")

    def diskless_port(self, arg):
        print("python3 main.py diskless port")

    def diskless_switch(self, arg):
        print("python3 main.py diskless switch")

    def parser_init(self):
        args = self.parser.parse_args()
        args.func(args)

if __name__ == "__main__":
    cmd = argparse_operator()
    cmd.parser_init()