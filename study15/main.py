import argparse
from method import empty, select, insert, update, delete

DESC = "CLI Program"
commands = [
  {"command":"list", "arguments": [], "method": select},
  {"command":"add", "arguments": ["word"], "method": insert},
  {"command":"edit", "arguments": ["id", "word"], "method": update},
  {"command":"remove", "arguments": ["id"], "method": delete}
]

def checkCLI(args):
  for cmd in commands:
    if args.command == cmd["command"]:
      if cmd["method"] == None:
        empty()
      else:
        cmd["method"](args)
      break
  print("종료")

def run():
  parser = argparse.ArgumentParser(description=DESC)
  subparsers = parser.add_subparsers(dest="command")

  for cmd in commands:
    name = cmd["command"]
    arguments = cmd["arguments"]
    add_parser = subparsers.add_parser(name)
    for arg in arguments:
      add_parser.add_argument(arg)

  checkCLI(parser.parse_args())

if __name__ == "__main__":
  run()
