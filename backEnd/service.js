const GUN = require('gun');
const gun = GUN();

function hello() {
  gun.get('test2').put({name : "Blanchman"});
}

function insert(path, item) {
  gun.get(path).put(item);
}

function getAll() {
  return gun.get('newPerson').map().get("Austin Blanchard").map(data => { return data.get; });
}

module.exports = { hello, insert, getAll };