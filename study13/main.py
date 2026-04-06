import argparse
from test import 목록, 입력, 수정, 삭제

DESC = "CLI Program"
commands = [
  {"command":"v", "arguments": [], "method": 목록},
  {"command":"a", "arguments": ["t"], "method": 입력},
  {"command":"u", "arguments": ["k", "t"], "method": 수정},
  {"command":"d", "arguments": ["k"], "method": 삭제}
]

def 실행():
  parser = argparse.ArgumentParser(description=DESC)
  subparsers = parser.add_subparsers(dest="command")

  for cmd in commands:
    add_parser = subparsers.add_parser(cmd["command"])
    for arg in cmd["arguments"]:
      add_parser.add_argument(arg)

  args = parser.parse_args()
  for cmd in commands:
    if args.command == cmd["command"]:
      if cmd["method"] == None:
        print("정의 되어 있지 않습니다.")
      else:
        cmd["method"](args)
      break

실행()