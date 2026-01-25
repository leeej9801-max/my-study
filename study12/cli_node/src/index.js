// console.log("자바스크립트");

import { Command } from 'commander';
// import { add, list } from './cmd.js';
import { list, insert, update, remove } from './words.js';

const program = new Command();

/*
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
*/



program.command('list').action(list);
program.command('insert').argument('<word>').action(insert);
program.command('update').argument('<id>').argument('<word>').action(update);
program.command('delete').argument('<id>').action(remove);

program.parse(process.argv);