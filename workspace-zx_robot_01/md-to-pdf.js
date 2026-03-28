const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertMdToPdf(mdPath, pdfPath) {
  // 读取markdown内容
  const mdContent = fs.readFileSync(mdPath, 'utf8');
  
  // 简单的markdown转HTML（这里用基础转换，满足需求）
  let html = mdContent
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
    .replace(/^- (.*)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\|.*\|/g, match => `<table><tr>${match.split('|').filter(cell => cell.trim()).map(cell => `<td>${cell.trim()}</td>`).join('')}</tr></table>`);
  
  // 完整HTML
  const fullHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>三年级下册第七单元大单元教学设计</title>
  <style>
    body {
      font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
      margin: 40px;
      line-height: 1.6;
    }
    h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    h2 { color: #34495e; margin-top: 30px; }
    h3 { color: #4a6fa5; margin-top: 20px; }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 15px 0;
    }
    td {
      border: 1px solid #ddd;
      padding: 8px 12px;
    }
    code {
      background: #f5f5f5;
      padding: 2px 5px;
      border-radius: 3px;
    }
    .mermaid {
      margin: 20px 0;
    }
  </style>
</head>
<body>
  ${html}
</body>
</html>
  `;
  
  // 启动浏览器生成PDF
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(fullHtml);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    margin: {
      top: '20mm',
      right: '20mm',
      bottom: '20mm',
      left: '20mm'
    },
    printBackground: true
  });
  await browser.close();
  
  console.log(`PDF generated successfully: ${pdfPath}`);
}

const mdPath = process.argv[2];
const pdfPath = process.argv[3];

convertMdToPdf(mdPath, pdfPath).catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
