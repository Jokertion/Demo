// 抽象语法树和UglifyJS的基本概念和语法
let UglifyJS = require('uglify-js');
let ast = UglifyJS.parse("function sum(x,y) { return x + y}");
console.log(ast);

console.log('------------------');

console.log(ast.body[0].name.name);  // sum
console.log(ast.body[0].argnames[0].name);  // x
console.log(ast.body[0].argnames[1].name);  // y


