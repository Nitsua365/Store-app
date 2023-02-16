const path = require('path');
module.exports = {
  entry: {
    popup: './src/popup.js',
    background: './src/background.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
  },
  devtool: 'cheap-module-source-map'
};