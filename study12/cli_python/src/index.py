print("파이썬")

import argparse
# from cmd import add, list
from words import list, insert, update, remove

parser = argparse.ArgumentParser(description="CLI 프로그램")
subparsers = parser.add_subparsers(dest="command")

# add_parser = subparsers.add_parser("add", help="메모 추가")
# add_parser.add_argument("a", help="첫번째 값")
# add_parser.add_argument("b", help="두번째 값")
# add_parser = subparsers.add_parser("list", help="목록보기")

add_parser = subparsers.add_parser("list")
add_parser = subparsers.add_parser("insert")
add_parser.add_argument("word")
add_parser = subparsers.add_parser("update")
add_parser.add_argument("id")
add_parser.add_argument("word")
add_parser = subparsers.add_parser("delete")
add_parser.add_argument("id")

args = parser.parse_args()

# if args.command == "add":
#   add(args.a, args.b)
# elif args.command == "list":
#   list()

if args.command == "list": list()
if args.command == "insert": insert(args.word)
if args.command == "update": update(args.id, args.word)
if args.command == "delete": remove(args.id)
