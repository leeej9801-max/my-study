console.log("자바스크립트");

import { Command } from 'commander';
import { add, list } from './cmd.js';

const program = new Command();

program
  .command('add')
  .argument('<a>')
  .argument('<b>')
  .description('메모 추가')
  .action(add);

program
  .command('list')
  .description('목록보기')
  .action(list);

program.parse(process.argv);