// index.js - 首页逻辑
Page({
  data: {
    showModal: false
  },

  // 人机对战
  startPvE() {
    wx.navigateTo({
      url: '/pages/game/game?mode=pve'
    })
  },

  // 双人对战
  startPvP() {
    wx.navigateTo({
      url: '/pages/game/game?mode=pvp'
    })
  },

  // 显示规则
  showRules() {
    this.setData({ showModal: true })
  },

  // 隐藏规则
  hideRules() {
    this.setData({ showModal: false })
  },

  // 阻止冒泡
  preventClose() {}
})
