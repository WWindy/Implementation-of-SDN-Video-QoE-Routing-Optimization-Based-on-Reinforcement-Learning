module.exports = {
  devServer:{
    open:true,
  },
  publicPath: process.env.NODE_ENV === 'production'
    ? '/D3-EasyFlowRender/'
    : '/',
  outputDir: 'dist',
  lintOnSave: true,
};

