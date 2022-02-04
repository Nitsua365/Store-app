// const GUN = require('gun');
// const gun = GUN();

function hello() {
  global.gun.get('test2').put({name : "Blanchman"});
}

module.exports = { hello };