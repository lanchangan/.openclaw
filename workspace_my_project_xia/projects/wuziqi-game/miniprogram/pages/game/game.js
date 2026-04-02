// game.js - 游戏核心逻辑

// 导入工具函数
const { checkWin } = require('../../utils/win-check')
const { getAIMove } = require('../../utils/ai')

// 棋盘配置
const BOARD_SIZE = 15  // 15x15棋盘
const WIN_COUNT = 5    // 五子连珠

Page({
  data: {
    // 游戏模式：pve-人机对战，pvp-双人对战
    mode: 'pvp',
    
    // 当前玩家：1-黑棋，2-白棋
    currentPlayer: 1,
    
    // 玩家名称
    player1Name: '黑棋',
    player2Name: '白棋',
    
    // 游戏状态
    statusText: '黑棋先行',
    gameOver: false,
    winner: 0,
    resultText: '',
    
    // 悔棋
    canUndo: false,
    moveHistory: [],
    
    // Canvas相关
    canvas: null,
    ctx: null,
    boardPixelSize: 0,
    cellSize: 0,
    padding: 0,
    canvasLeft: 0,
    canvasTop: 0,
    
    // 棋盘状态：0-空，1-黑棋，2-白棋
    board: []
  },

  onLoad(options) {
    const mode = options.mode || 'pvp'
    this.setData({ 
      mode,
      player2Name: mode === 'pve' ? '电脑' : '白棋'
    })
    this.initGame()
  },

  onReady() {
    this.initCanvas()
  },

  // 初始化游戏
  initGame() {
    // 初始化棋盘数组
    const board = []
    for (let i = 0; i < BOARD_SIZE; i++) {
      board[i] = []
      for (let j = 0; j < BOARD_SIZE; j++) {
        board[i][j] = 0
      }
    }
    
    this.setData({
      board,
      currentPlayer: 1,
      gameOver: false,
      winner: 0,
      statusText: '黑棋先行',
      canUndo: false,
      moveHistory: []
    })
  },

  // 初始化Canvas
  initCanvas() {
    const query = wx.createSelectorQuery()
    query.select('#chessBoard')
      .fields({ node: true, size: true, rect: true })
      .exec((res) => {
        if (!res[0]) return
        
        const canvas = res[0].node
        const ctx = canvas.getContext('2d')
        const rect = res[0] // 获取 Canvas 位置信息
        
        // 获取设备像素比
        const dpr = wx.getWindowInfo().pixelRatio
        
        // 计算棋盘尺寸（留出边距）
        const windowWidth = wx.getWindowInfo().windowWidth
        const boardPixelSize = Math.min(windowWidth - 80, 650)
        
        canvas.width = boardPixelSize * dpr
        canvas.height = boardPixelSize * dpr
        
        ctx.scale(dpr, dpr)
        
        // 计算格子大小
        const padding = boardPixelSize / (BOARD_SIZE + 1)
        const cellSize = (boardPixelSize - padding * 2) / (BOARD_SIZE - 1)
        
        this.setData({
          canvas,
          ctx,
          boardPixelSize,
          cellSize,
          padding,
          canvasLeft: rect.left || 0,  // Canvas 左边距
          canvasTop: rect.top || 0     // Canvas 上边距
        })
        
        this.drawBoard()
      })
  },

  // 绘制棋盘
  drawBoard() {
    const { ctx, boardPixelSize, cellSize, padding, board } = this.data
    if (!ctx) return
    
    // 清空画布
    ctx.clearRect(0, 0, boardPixelSize, boardPixelSize)
    
    // 绘制棋盘背景
    ctx.fillStyle = '#d4a574'
    ctx.fillRect(0, 0, boardPixelSize, boardPixelSize)
    
    // 绘制网格线
    ctx.strokeStyle = '#8b6914'
    ctx.lineWidth = 1
    
    for (let i = 0; i < BOARD_SIZE; i++) {
      // 横线
      ctx.beginPath()
      ctx.moveTo(padding, padding + i * cellSize)
      ctx.lineTo(boardPixelSize - padding, padding + i * cellSize)
      ctx.stroke()
      
      // 竖线
      ctx.beginPath()
      ctx.moveTo(padding + i * cellSize, padding)
      ctx.lineTo(padding + i * cellSize, boardPixelSize - padding)
      ctx.stroke()
    }
    
    // 绘制星位（天元和四个角星）
    const starPoints = [
      [3, 3], [3, 11], [11, 3], [11, 11], [7, 7],
      [3, 7], [7, 3], [7, 11], [11, 7]
    ]
    
    ctx.fillStyle = '#8b6914'
    starPoints.forEach(([x, y]) => {
      ctx.beginPath()
      ctx.arc(padding + x * cellSize, padding + y * cellSize, 4, 0, Math.PI * 2)
      ctx.fill()
    })
    
    // 绘制已下的棋子
    for (let i = 0; i < BOARD_SIZE; i++) {
      for (let j = 0; j < BOARD_SIZE; j++) {
        if (board[i][j] !== 0) {
          this.drawChess(i, j, board[i][j])
        }
      }
    }
  },

  // 绘制棋子
  drawChess(row, col, player) {
    const { ctx, cellSize, padding } = this.data
    const x = padding + col * cellSize
    const y = padding + row * cellSize
    const radius = cellSize * 0.4
    
    // 创建径向渐变
    const gradient = ctx.createRadialGradient(
      x - radius * 0.3, y - radius * 0.3, radius * 0.1,
      x, y, radius
    )
    
    if (player === 1) {
      // 黑棋
      gradient.addColorStop(0, '#666666')
      gradient.addColorStop(1, '#1a1a1a')
    } else {
      // 白棋
      gradient.addColorStop(0, '#ffffff')
      gradient.addColorStop(1, '#cccccc')
    }
    
    // 绘制棋子阴影
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)'
    ctx.beginPath()
    ctx.arc(x + 2, y + 2, radius, 0, Math.PI * 2)
    ctx.fill()
    
    // 绘制棋子
    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fill()
    
    // 绘制棋子边框
    ctx.strokeStyle = player === 1 ? '#000' : '#999'
    ctx.lineWidth = 1
    ctx.stroke()
  },

  // 触摸结束 - 直接处理落子
  onTouchEnd(e) {
    if (this.data.gameOver) return
    if (this.data.mode === 'pve' && this.data.currentPlayer === 2) return
    
    const { padding, cellSize, board, canvasLeft, canvasTop } = this.data
    
    // 使用 changedTouches（touchend 时 touches 为空）
    const touch = e.changedTouches[0]
    if (!touch) return
    
    // 计算相对于 Canvas 的坐标
    const relativeX = touch.x - canvasLeft
    const relativeY = touch.y - canvasTop
    
    // 计算点击的格子位置
    const col = Math.round((relativeX - padding) / cellSize)
    const row = Math.round((relativeY - padding) / cellSize)
    
    console.log('触摸坐标:', touch.x, touch.y)
    console.log('Canvas偏移:', canvasLeft, canvasTop)
    console.log('相对坐标:', relativeX, relativeY)
    console.log('计算格子:', row, col)
    
    // 检查是否在有效范围内
    if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) return
    
    // 检查该位置是否已有棋子
    if (board[row][col] !== 0) return
    
    // 落子
    this.placeChess(row, col)
  },

  // 落子
  placeChess(row, col) {
    const { board, currentPlayer, moveHistory } = this.data
    
    // 更新棋盘
    board[row][col] = currentPlayer
    
    // 记录历史
    const newHistory = [...moveHistory, { row, col, player: currentPlayer }]
    
    this.setData({
      board,
      moveHistory: newHistory,
      canUndo: newHistory.length > 0
    })
    
    // 重绘棋盘
    this.drawBoard()
    
    // 检查胜负
    if (checkWin(board, row, col, currentPlayer, WIN_COUNT)) {
      this.gameWin(currentPlayer)
      return
    }
    
    // 检查平局
    if (this.isBoardFull()) {
      this.gameDraw()
      return
    }
    
    // 切换玩家
    const nextPlayer = currentPlayer === 1 ? 2 : 1
    const statusText = nextPlayer === 1 ? '黑棋思考中...' : 
                       (this.data.mode === 'pve' ? '电脑思考中...' : '白棋思考中...')
    
    this.setData({
      currentPlayer: nextPlayer,
      statusText
    })
    
    // 如果是人机模式且轮到AI
    if (this.data.mode === 'pve' && nextPlayer === 2) {
      setTimeout(() => this.aiMove(), 500)
    }
  },

  // AI落子
  aiMove() {
    if (this.data.gameOver) return
    
    const { board } = this.data
    const move = getAIMove(board, BOARD_SIZE)
    
    if (move) {
      this.placeChess(move.row, move.col)
    }
  },

  // 检查棋盘是否已满
  isBoardFull() {
    const { board } = this.data
    for (let i = 0; i < BOARD_SIZE; i++) {
      for (let j = 0; j < BOARD_SIZE; j++) {
        if (board[i][j] === 0) return false
      }
    }
    return true
  },

  // 游戏胜利
  gameWin(winner) {
    const winnerName = winner === 1 ? '黑棋' : 
                       (this.data.mode === 'pve' ? '电脑' : '白棋')
    
    this.setData({
      gameOver: true,
      winner,
      resultText: `${winnerName}获胜！`,
      statusText: '游戏结束'
    })
  },

  // 游戏平局
  gameDraw() {
    this.setData({
      gameOver: true,
      winner: 0,
      resultText: '平局！',
      statusText: '游戏结束'
    })
  },

  // 悔棋
  undoMove() {
    const { moveHistory, board, mode } = this.data
    
    if (moveHistory.length === 0) return
    
    // 人机模式需要撤销两步（玩家和AI各一步）
    const undoCount = mode === 'pve' && moveHistory.length >= 2 ? 2 : 1
    
    for (let i = 0; i < undoCount && moveHistory.length > 0; i++) {
      const lastMove = moveHistory.pop()
      board[lastMove.row][lastMove.col] = 0
    }
    
    const currentPlayer = moveHistory.length % 2 === 0 ? 1 : 2
    
    this.setData({
      board,
      moveHistory,
      currentPlayer,
      canUndo: moveHistory.length > 0,
      statusText: currentPlayer === 1 ? '黑棋思考中...' : '白棋思考中...'
    })
    
    this.drawBoard()
  },

  // 重新开始
  restartGame() {
    this.initGame()
    this.drawBoard()
  },

  // 返回首页
  backHome() {
    wx.navigateBack()
  }
})
