const path = require('path');

module.exports = {
  entry: {
    "content-bundle": './src/content-bundle.js',
    background: './src/background.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js'
  },
  devtool: 'cheap-module-source-map',
  module: {
    rules: [
      {
        test: '/\.png/',
        type: 'asset'
      }
    ]
  }
};