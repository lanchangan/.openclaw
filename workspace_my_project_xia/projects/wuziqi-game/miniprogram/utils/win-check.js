/**
 * win-check.js - 五子棋胜负判定
 */

/**
 * 检查是否获胜
 * @param {Array} board - 棋盘数组
 * @param {number} row - 最后落子行
 * @param {number} col - 最后落子列
 * @param {number} player - 当前玩家 (1:黑棋, 2:白棋)
 * @param {number} winCount - 连子数 (默认5)
 * @returns {boolean} 是否获胜
 */
function checkWin(board, row, col, player, winCount = 5) {
  const directions = [
    [0, 1],   // 水平
    [1, 0],   // 垂直
    [1, 1],   // 主对角线
    [1, -1]   // 副对角线
  ]
  
  for (const [dx, dy] of directions) {
    let count = 1
    
    // 正向检查
    count += countInDirection(board, row, col, player, dx, dy, winCount)
    // 反向检查
    count += countInDirection(board, row, col, player, -dx, -dy, winCount)
    
    if (count >= winCount) {
      return true
    }
  }
  
  return false
}

/**
 * 计算某方向上连续棋子数
 * @param {Array} board - 棋盘数组
 * @param {number} row - 起始行
 * @param {number} col - 起始列
 * @param {number} player - 玩家
 * @param {number} dx - 行方向
 * @param {number} dy - 列方向
 * @param {number} maxCount - 最大检查数
 * @returns {number} 连续棋子数
 */
function countInDirection(board, row, col, player, dx, dy, maxCount) {
  let count = 0
  let r = row + dx
  let c = col + dy
  
  while (isValidPosition(board, r, c) && board[r][c] === player && count < maxCount - 1) {
    count++
    r += dx
    c += dy
  }
  
  return count
}

/**
 * 检查位置是否有效
 * @param {Array} board - 棋盘数组
 * @param {number} row - 行
 * @param {number} col - 列
 * @returns {boolean} 是否有效
 */
function isValidPosition(board, row, col) {
  return row >= 0 && row < board.length && col >= 0 && col < board[0].length
}

/**
 * 获取所有空位
 * @param {Array} board - 棋盘数组
 * @returns {Array} 空位数组 [{row, col}, ...]
 */
function getEmptyPositions(board) {
  const positions = []
  const size = board.length
  
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      if (board[i][j] === 0) {
        positions.push({ row: i, col: j })
      }
    }
  }
  
  return positions
}

module.exports = {
  checkWin,
  countInDirection,
  isValidPosition,
  getEmptyPositions
}
