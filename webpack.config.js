var path = require("path");
var webpack = require("webpack");

module.exports = {
    entry: {
        "flask-example": path.join(__dirname, 'src', 'main.jsx'),
    },
    output: {
        filename: "dist/[name].js"
    },
    module: {
        loaders: [
            { test: /\.jsx$/, exclude: /node_modules/, loader: "babel-loader"},
            { test: /\.css$/, loader: "style!css" },
            { test: /\.scss$/, loader: "style!css!sass" },
            { test: /\.less$/, loader: "style!css!less" },
            { test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9\.=]+)?$/,
              loader: 'file-loader' }
        ]
    }
};
