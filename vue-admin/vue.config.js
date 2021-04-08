module.exports = {
  devServer: {
    disableHostCheck: true,
    proxy: {
      '/group': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/user': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/permission': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/k8s': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/toolkit': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/job': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/deploy': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/audit': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
      '/rbac-k8s': {
        target: 'http://localhost:8000/',
        ws: true,
        changeOrigin: true,
      },
    }
  }
}