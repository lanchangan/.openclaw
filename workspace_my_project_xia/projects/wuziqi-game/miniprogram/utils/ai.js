/**
 * ai.js - 五子棋AI算法
 * 基于评分策略的AI
 */

/**
 * 获取AI最佳落子位置
 * @param {Array} board - 棋盘数组
 * @param {number} size - 棋盘大小
 * @returns {Object|null} {row, col} 或 null
 */
function getAIMove(board, size) {
  const emptyPositions = getEmptyPositions(board)
  
  if (emptyPositions.length === 0) return null
  
  // 计算每个空位的分数
  let bestScore = -Infinity
  let bestMoves = []
  
  for (const pos of emptyPositions) {
    const score = evaluatePosition(board, pos.row, pos.col, size)
    
    if (score > bestScore) {
      bestScore = score
      bestMoves = [pos]
    } else if (score === bestScore) {
      bestMoves.push(pos)
    }
  }
  
  // 从最佳位置中随机选择一个
  const randomIndex = Math.floor(Math.random() * bestMoves.length)
  return bestMoves[randomIndex]
}

/**
 * 评估某个位置的分数
 * @param {Array} board - 棋盘数组
 * @param {number} row - 行
 * @param {number} col - 列
 * @param {number} size - 棋盘大小
 * @returns {number} 分数
 */
function evaluatePosition(board, row, col, size) {
  // AI（白棋）得分 - 进攻
  const aiScore = calculateScore(board, row, col, 2, size)
  // 玩家（黑棋）得分 - 防守
  const playerScore = calculateScore(board, row, col, 1, size)
  
  // 防守优先级略高于进攻
  return Math.max(aiScore * 1.0, playerScore * 1.1)
}

/**
 * 计算某位置对于某玩家的分数
 * @param {Array} board - 棋盘数组
 * @param {number} row - 行
 * @param {number} col - 列
 * @param {number} player - 玩家
 * @param {number} size - 棋盘大小
 * @returns {number} 分数
 */
function calculateScore(board, row, col, player, size) {
  const directions = [
    [0, 1],   // 水平
    [1, 0],   // 垂直
    [1, 1],   // 主对角线
    [1, -1]   // 副对角线
  ]
  
  let totalScore = 0
  
  for (const [dx, dy] of directions) {
    const lineInfo = analyzeLine(board, row, col, dx, dy, player, size)
    totalScore += getLineScore(lineInfo)
  }
  
  return totalScore
}

/**
 * 分析某方向上的连子情况
 * @param {Array} board - 棋盘数组
 * @param {number} row - 行
 * @param {number} col - 列
 * @param {number} dx - 行方向
 * @param {number} dy - 列方向
 * @param {number} player - 玩家
 * @param {number} size - 棋盘大小
 * @returns {Object} {count, openEnds}
 */
function analyzeLine(board, row, col, dx, dy, player, size) {
  let count = 0
  let openEnds = 0
  
  // 正向计数
  let r = row + dx
  let c = col + dy
  while (isValidPosition(r, c, size) && board[r][c] === player) {
    count++
    r += dx
    c += dy
  }
  // 检查正向末端是否开放
  if (isValidPosition(r, c, size) && board[r][c] === 0) {
    openEnds++
  }
  
  // 反向计数
  r = row - dx
  c = col - dy
  while (isValidPosition(r, c, size) && board[r][c] === player) {
    count++
    r -= dx
    c -= dy
  }
  // 检查反向末端是否开放
  if (isValidPosition(r, c, size) && board[r][c] === 0) {
    openEnds++
  }
  
  return { count, openEnds }
}

/**
 * 根据连子情况返回分数
 * @param {Object} lineInfo - {count, openEnds}
 * @returns {number} 分数
 */
function getLineScore(lineInfo) {
  const { count, openEnds } = lineInfo
  
  // 连5 - 必胜
  if (count >= 4) return 100000
  
  // 连4
  if (count === 3) {
    if (openEnds === 2) return 10000  // 活四
    if (openEnds === 1) return 1000   // 冲四
  }
  
  // 连3
  if (count === 2) {
    if (openEnds === 2) return 1000   // 活三
    if (openEnds === 1) return 100    // 眠三
  }
  
  // 连2
  if (count === 1) {
    if (openEnds === 2) return 100    // 活二
    if (openEnds === 1) return 10     // 眠二
  }
  
  // 单子
  if (openEnds === 2) return 10
  if (openEnds === 1) return 1
  
  return 0
}

/**
 * 检查位置是否有效
 * @param {number} row - 行
 * @param {number} col - 列
 * @param {number} size - 棋盘大小
 * @returns {boolean} 是否有效
 */
function isValidPosition(row, col, size) {
  return row >= 0 && row < size && col >= 0 && col < size
}

/**
 * 获取所有空位
 * @param {Array} board - 棋盘数组
 * @returns {Array} 空位数组
 */
function getEmptyPositions(board) {
  const positions = []
  const size = board.length
  
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      if (board[i][j] === 0) {
        // 只考虑周围有棋子的位置
        if (hasNeighbor(board, i, j, size)) {
          positions.push({ row: i, col: j })
        }
      }
    }
  }
  
  // 如果棋盘为空，返回中心点
  if (positions.length === 0) {
    const center = Math.floor(size / 2)
    positions.push({ row: center, col: center })
  }
  
  return positions
}

/**
 * 检查某位置周围是否有棋子
 * @param {Array} board - 棋盘数组
 * @param {number} row - 行
 * @param {number} col - 列
 * @param {number} size - 棋盘大小
 * @param {number} range - 检查范围（默认2）
 * @returns {boolean} 是否有邻居
 */
function hasNeighbor(board, row, col, size, range = 2) {
  for (let i = -range; i <= range; i++) {
    for (let j = -range; j <= range; j++) {
      if (i === 0 && j === 0) continue
      const r = row + i
      const c = col + j
      if (isValidPosition(r, c, size) && board[r][c] !== 0) {
        return true
      }
    }
  }
  return false
}

module.exports = {
  getAIMove,
  evaluatePosition,
  calculateScore,
  analyzeLine,
  getLineScore
}
