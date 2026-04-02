// app.js - 小程序入口文件
App({
  onLaunch() {
    // 小程序启动时执行
    console.log('五子棋小程序启动')
  },

  globalData: {
    userInfo: null,
    gameHistory: []
  }
})
