// require our dependencies
var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    // the base directory(absolute path) for resolving the entry option
    context: __dirname,
    // your current directory. Yuo don't have to specify the extension now,
    // because you will specify extensions later in the `resolve` section
    entry: './assets/js/index',
    output: {
        // where you want your compiled bundle to be stored
        path: path.resolve('./assets/bundles'),
        // naming convetion webpac should use for your files
        filename: '[name]-[hash].js'
    },
    plugins: [
        // tells webpack where to store data about your bundle
        new BundleTracker({filename: './webpack-stats.json'}),
        // makes jQuery available in every module
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        })
    ],

    module: {
        rules: [
            // a regexp that tells webpack to use the following loaders on all
            // .js and .jsx files
            {
                test: /\.jsx?$/,
                // we definitely don't want babel to transpile all the files in
                // node_modules. That would take a long time.
                exclude: /node_modules/,
                // use the babel loader
                loader: 'babel-loader',
                query: {
                    // specify that we will be dealing with React code
                    presets: ['react']
                }
            },
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ]
            },
            {
                test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
                loader: 'url-loader',
                options: {
                    limit: 10000
                }
            }
        ]
    },

    resolve: {
        // tells webpack where to look for modules
        modules: ['node_modules'],
        // extensions that should be used to resolve modules
        extensions: ['.js', '.jsx', '.css']
    }
}
