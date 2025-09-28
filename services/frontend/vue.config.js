const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: ["vuetify"],

  // Development server configuration
  devServer: {
    port: 8080,
    host: "0.0.0.0",
    hot: true,
    liveReload: true,
    watchFiles: {
      paths: ["src/**/*", "public/**/*"],
      options: {
        usePolling: true,
      },
    },
    client: {
      webSocketURL: "ws://localhost:8080/ws",
    },
    allowedHosts: "all",
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers":
        "X-Requested-With, content-type, Authorization",
    },
  },

  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: "all",
        cacheGroups: {
          plotly: {
            name: "plotly",
            test: /[\\/]node_modules[\\/]plotly\.js/,
            chunks: "all",
            priority: 10,
          },
        },
      },
    },
    resolve: {
      alias: {
        "@": require("path").resolve(__dirname, "src"),
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin("define").tap((definitions) => {
      Object.assign(definitions[0], {
        __VUE_OPTIONS_API__: "true",
        __VUE_PROD_DEVTOOLS__: "false",
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
      });
      return definitions;
    });

    // Exclude plotly.js from babel-loader
    config.module
      .rule("js")
      .exclude.add(/node_modules\/plotly\.js/)
      .end();
  },
});
