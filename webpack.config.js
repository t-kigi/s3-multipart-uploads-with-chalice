const path = require("path");

module.exports = {
  // モードの設定。指定可能な値は、none, development ,production（デフォルト）
  // https://webpack.js.org/concepts/mode/#mode-development
  mode: "development",
  // mode: 'production',

  // アプリケーションが実行を開始されるポイント(エントリーポイント)
  // 配列で指定すると、すべての項目が実行される
  // https://webpack.js.org/configuration/entry-context/#entry
  entry: "./js/upload.js",
  output: {
    filename: "upload.min.js",
    // ビルド後のファイルが出力される"絶対パス"ディレクトリ
    // https://webpack.js.org/configuration/output/#outputpath
    path: path.join(__dirname, "apis/chalicelib/static/js"),
    environment: {
      arrowFunction: false,
    },
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: [
          {
            loader: "babel-loader",
            options: {
              presets: [["@babel/preset-env", { modules: false }]],
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: [".js"],
  },
  externals: {
  },
};
