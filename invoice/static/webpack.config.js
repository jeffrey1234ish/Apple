var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var debug = false;

module.exports = {
  context: __dirname,
  entry: './assets/src/js',
  watch: true,
  output: {
      path: path.resolve('./assets/dist/'),
      filename: "[name].js"
  },

  plugins: debug ? [] : [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
        jQuery: 'jquery'
    }),
    new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false})
  ]
}
