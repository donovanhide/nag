#!/usr/bin/env python

import os
import argparse
import StringIO

class NagItem():
    
    def __init__(self,priority,task):
        self.priority = int(priority)
        self.task = task
        
    def __cmp__(self,other):
        return cmp(self.priority,other.priority) or cmp(self.task,other.task)

    def __str__(self):
        return '%s\t%s' % (self.priority,self.task)
    
    def __repr__(self):
        return self.__str__()

class Nag():
    
    def __init__(self):
        self.parse()

    def __iter__(self):
        try:
            with open(self.args.filename,"r") as f:
                return (NagItem(*line.strip().split('\t',1)) for line in f.readlines())
        except IOError:
            return iter([])
            
    def __str__(self):
        string = StringIO.StringIO()
        string.write("Line:\tPriority:\tTask:\n")
        for line_number,item in enumerate(self):
            if not hasattr(self.args,'term') or self.args.term.lower() in item.task.lower():
                string.write("%s\t%s\t\t%s\n" %(line_number+1,item.priority,item.task))
        return string.getvalue()
    
    def __save__(self,new_content):
        with open(self.args.filename, "w") as f:
            for item in sorted(new_content):
                f.write('%s\n'%item)
    
    @property
    def items(self):
        return [item for item in self]

    def list(self):
        print self

    def add(self):
        self.__save__(self.items+[NagItem(self.args.priority,self.args.item)])

    def clear(self):
        answer = raw_input("Are you sure you want to clear your nag list? (y or n)")
        if answer == "y":
            self.__save__([])
            print "List cleared!"

    def delete(self):
        current = self.items
        try:
            del current[self.args.line-1]
            self.__save__(current)
        except IndexError:
            print "Item: %s doesn't exist! You only have %s items " % (self.args.line,len(current))

    def parse(self):
        parser = argparse.ArgumentParser(description='Yet another TODO list!')
        subparsers = parser.add_subparsers(help='commands')

        list_parser = subparsers.add_parser('list', help='List items')
        list_parser.set_defaults(func=self.list)

        add_parser = subparsers.add_parser('add', help="Add an item")
        add_parser.add_argument('--item','-i',help="Item to add", required=True)
        add_parser.add_argument('--priority','-p',help="Priority of item [default=%(default)s]",type=int,default=1)
        add_parser.set_defaults(func=self.add)

        clear_parser = subparsers.add_parser('clear', help='Clear all items')
        clear_parser.set_defaults(func=self.clear)

        search_parser = subparsers.add_parser('search',help='Search for an item')
        search_parser.add_argument('--term','-t',help='Term to search for',required=True)
        search_parser.set_defaults(func=self.list)

        delete_parser = subparsers.add_parser('delete',help='Delete an item')
        delete_parser.add_argument('--line','-l',help='Line number of item to delete',required=True,type=int)
        delete_parser.set_defaults(func=self.delete)

        parser.add_argument('-f','--file',help='TODO list to process [default=%default]',
                                          dest='filename',
                                          default=os.path.join(os.getenv('HOME'),'.nag'))
        parser.add_argument('--version', action='version', version='%(prog)s 0.1')

        self.args = parser.parse_args()
        self.args.func()

if __name__ == "__main__":
    Nag()
