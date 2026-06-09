$ErrorActionPreference = 'Stop'

function Get-SafeFileName {
    param([string]$Name)

    $safe = $Name -replace '[<>:"/\\|?*]', '_'
    $safe = $safe -replace '\s+', '_'
    return $safe.Trim('_')
}

function Get-HtmlEncoded {
    param([string]$Text)

    if ($null -eq $Text) {
        return ''
    }

    return [System.Net.WebUtility]::HtmlEncode($Text)
}

function Convert-PythonToHighlightedHtml {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return ''
    }

    $keywords = @{}
    @(
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class',
        'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
        'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass',
        'raise', 'return', 'try', 'while', 'with', 'yield'
    ) | ForEach-Object { $keywords[$_] = $true }

    $builtins = @{}
    @(
        'abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'filter', 'float', 'int', 'len',
        'list', 'map', 'max', 'min', 'open', 'print', 'range', 'reversed', 'set', 'sorted',
        'str', 'sum', 'tuple', 'type', 'zip'
    ) | ForEach-Object { $builtins[$_] = $true }

    $pattern = @'
(#.*$|"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|@[A-Za-z_][A-Za-z0-9_]*|\b\d+(?:\.\d+)?\b|\b[A-Za-z_][A-Za-z0-9_]*\b|[+\-*/%=!<>]=?|[(){}\[\]:.,])
'@.Trim()

    $matches = [regex]::Matches($Text, $pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    $builder = New-Object System.Text.StringBuilder
    $lastIndex = 0
    $functionPending = $false

    foreach ($match in $matches) {
        [void]$builder.Append((Get-HtmlEncoded $Text.Substring($lastIndex, $match.Index - $lastIndex)))

        $value = $match.Value
        $className = ''

        if ($value.StartsWith('#')) {
            $className = 'comment'
        } elseif ($value.StartsWith('"""') -or $value.StartsWith("'''") -or $value.StartsWith('"') -or $value.StartsWith("'")) {
            $className = 'string'
        } elseif ($value.StartsWith('@')) {
            $className = 'decorator'
        } elseif ($value -match '^\d') {
            $className = 'number'
        } elseif ($keywords.ContainsKey($value)) {
            $className = 'keyword'
            $functionPending = ($value -eq 'def')
        } elseif ($builtins.ContainsKey($value)) {
            $className = 'builtin'
        } elseif (($value -match '^[A-Za-z_][A-Za-z0-9_]*$') -and $functionPending) {
            $className = 'function'
            $functionPending = $false
        } elseif ($value -match '^[+\-*/%=!<>]') {
            $className = 'operator'
        } elseif ($value -ne 'def') {
            $functionPending = $false
        }

        if ($className) {
            [void]$builder.Append('<span class="token ')
            [void]$builder.Append($className)
            [void]$builder.Append('">')
            [void]$builder.Append((Get-HtmlEncoded $value))
            [void]$builder.Append('</span>')
        } else {
            [void]$builder.Append((Get-HtmlEncoded $value))
        }

        $lastIndex = $match.Index + $match.Length
    }

    [void]$builder.Append((Get-HtmlEncoded $Text.Substring($lastIndex)))
    return $builder.ToString()
}

function Get-ProblemStem {
    param([string]$ProblemText)

    if ([string]::IsNullOrWhiteSpace($ProblemText)) {
        return ''
    }

    $normalized = $ProblemText -replace "`r`n", "`n"
    $descriptionMatch = [regex]::Match($normalized, '(?m)^##\s*题目描述\s*$')
    if (-not $descriptionMatch.Success) {
        return $ProblemText.Trim()
    }

    $body = $normalized.Substring($descriptionMatch.Index + $descriptionMatch.Length).Trim()
    $splitPattern = "(?m)^(```|示例\s*\d+\s*[：:]|\*\*示例|\*\*提示|\*\*进阶|提示\s*$|进阶\s*$|##\s+提示)"
    $parts = [regex]::Split($body, $splitPattern, 2)
    return $parts[0].Trim()
}

$root = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$sourceDirs = @('Easy', 'Medium', 'Hard') | ForEach-Object { Join-Path $root $_ }
$outputDir = Join-Path $root 'html'

if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Get-ChildItem -LiteralPath $outputDir -Filter '*.html' -File | Remove-Item -Force

$difficultyMap = @{
    '简单' = 'Easy'
    '中等' = 'Medium'
    '困难' = 'Hard'
}

$tagPriority = @(
    '数组',
    '哈希表',
    '字符串',
    '双指针',
    '滑动窗口',
    '栈',
    '队列',
    '链表',
    '二叉树',
    '树',
    '二叉搜索树',
    '深度优先搜索',
    '广度优先搜索',
    '递归',
    '回溯',
    '动态规划',
    '贪心',
    '二分查找',
    '排序',
    '堆（优先队列）',
    '图',
    '拓扑排序',
    '设计',
    '矩阵',
    '位运算',
    '数学',
    '模拟',
    '前缀和',
    '并查集',
    '分治',
    '字典树',
    '单调栈',
    '单调队列',
    '记忆化',
    '快速选择',
    '归并排序',
    '树状数组',
    '线段树',
    '数据流',
    '随机化',
    '迭代器',
    '有序集合',
    '扫描线',
    '桶排序',
    '组合数学',
    '数论',
    '枚举',
    '双向链表',
    '字符串匹配',
    '交互',
    '计数'
)

$tagOrder = @{}
for ($i = 0; $i -lt $tagPriority.Count; $i++) {
    $tagOrder[$tagPriority[$i]] = $i
}

$problems = New-Object System.Collections.Generic.List[object]

foreach ($dir in $sourceDirs) {
    if (-not (Test-Path -LiteralPath $dir)) {
        continue
    }

    foreach ($problemDir in Get-ChildItem -LiteralPath $dir -Directory) {
        $problemPath = Join-Path $problemDir.FullName 'problem.md'
        if (-not (Test-Path -LiteralPath $problemPath)) {
            continue
        }

        $solutionPath = Join-Path $problemDir.FullName 'solution.py'
        $problemText = Get-Content -LiteralPath $problemPath -Encoding UTF8 -Raw
        $problemStem = Get-ProblemStem $problemText
        $solutionText = if (Test-Path -LiteralPath $solutionPath) {
            $raw = Get-Content -LiteralPath $solutionPath -Encoding UTF8 -Raw
            if ([string]::IsNullOrWhiteSpace($raw)) {
                "# TODO: add solution`n"
            } else {
                $raw.TrimEnd()
            }
        } else {
            "# TODO: add solution`n"
        }

        $titleMatch = [regex]::Match($problemText, '(?m)^#\s*(.+)$')
        $difficultyMatch = [regex]::Match($problemText, '\*\*难度:\*\*\s*([^\r\n]+)')
        $tagsMatch = [regex]::Match($problemText, '\*\*标签:\*\*\s*([^\r\n]+)')
        $linkMatch = [regex]::Match($problemText, '\*\*链接:\*\*\s*\[LeetCode\]\(([^)]+)\)')

        $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.Trim() } else { $problemDir.Name }
        $difficultyZh = if ($difficultyMatch.Success) { $difficultyMatch.Groups[1].Value.Trim() } else { '' }
        $difficultyEn = if ($difficultyMap.ContainsKey($difficultyZh)) { $difficultyMap[$difficultyZh] } else { Split-Path $dir -Leaf }
        $tags = if ($tagsMatch.Success) {
            $tagsMatch.Groups[1].Value.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
        } else {
            @('未分类')
        }
        $link = if ($linkMatch.Success) { $linkMatch.Groups[1].Value.Trim() } else { '' }

        foreach ($tag in $tags) {
            $problems.Add([PSCustomObject]@{
                Tag = $tag
                DifficultyZh = $difficultyZh
                DifficultyEn = $difficultyEn
                Title = $title
                Link = $link
                ProblemText = $problemStem
                SolutionText = $solutionText
                RelativePath = $problemDir.FullName.Replace($root + '\', '')
            })
        }
    }
}

$groups = $problems | Group-Object Tag, DifficultyZh | Sort-Object Name
$indexEntries = New-Object System.Collections.Generic.List[object]

foreach ($group in $groups) {
    $first = $group.Group[0]
    $fileBase = '{0}_{1}' -f (Get-SafeFileName $first.Tag), (Get-SafeFileName $first.DifficultyZh)
    $fileName = "$fileBase.html"
    $outputPath = Join-Path $outputDir $fileName
    $pageTitle = "{0} - {1}" -f $first.Tag, $first.DifficultyZh

    $cards = foreach ($item in ($group.Group | Sort-Object Title)) {
@"
    <section class="problem-card">
      <h2>$([System.Net.WebUtility]::HtmlEncode($item.Title))</h2>
      <div class="meta">
        <span>类型：$([System.Net.WebUtility]::HtmlEncode($item.Tag))</span>
        <span>难度：$([System.Net.WebUtility]::HtmlEncode($item.DifficultyZh))</span>
        <span>目录：$([System.Net.WebUtility]::HtmlEncode($item.RelativePath))</span>
      </div>
      <p><a href="$([System.Net.WebUtility]::HtmlEncode($item.Link))" target="_blank" rel="noopener noreferrer">LeetCode 原题链接</a></p>
      <h3>题目内容</h3>
      <pre>$([System.Net.WebUtility]::HtmlEncode($item.ProblemText))</pre>
      <h3>解答方案</h3>
      <pre class="language-python"><code class="language-python">$(Convert-PythonToHighlightedHtml $item.SolutionText)</code></pre>
    </section>
"@
    }

    $html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$([System.Net.WebUtility]::HtmlEncode($pageTitle))</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --line: #d7deea;
      --accent: #2563eb;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 32px 20px 64px;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }
    main {
      max-width: 1100px;
      margin: 0 auto;
    }
    h1 {
      margin: 0 0 8px;
      font-size: 32px;
    }
    .summary {
      color: var(--muted);
      margin-bottom: 24px;
    }
    .back-link {
      display: inline-block;
      margin-bottom: 24px;
      color: var(--accent);
      text-decoration: none;
    }
    .problem-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }
    .problem-card h2,
    .problem-card h3 {
      margin-top: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 16px;
    }
    pre {
      white-space: pre-wrap;
      word-break: break-word;
      background: #0f172a;
      color: #e5e7eb;
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
    }
    code.language-python .token.comment { color: #64748b; }
    code.language-python .token.keyword { color: #c084fc; }
    code.language-python .token.string { color: #86efac; }
    code.language-python .token.number { color: #fca5a5; }
    code.language-python .token.function { color: #7dd3fc; }
    code.language-python .token.builtin { color: #fcd34d; }
    code.language-python .token.decorator { color: #f9a8d4; }
    code.language-python .token.operator { color: #e2e8f0; }
    a { color: var(--accent); }
  </style>
</head>
<body>
  <main>
    <a class="back-link" href="./index.html">返回索引</a>
    <h1>$([System.Net.WebUtility]::HtmlEncode($pageTitle))</h1>
    <p class="summary">共 $($group.Count) 题，按题目原始标签与难度聚合生成。</p>
$(($cards -join "`r`n"))
  </main>
  <script>
    (() => {
      const escapeHtml = (value) =>
        value
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;');

      const keywords = new Set([
        'False','None','True','and','as','assert','async','await','break','class','continue',
        'def','del','elif','else','except','finally','for','from','global','if','import','in',
        'is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield'
      ]);

      const builtins = new Set([
        'abs','all','any','bool','dict','enumerate','filter','float','int','len','list','map',
        'max','min','open','print','range','reversed','set','sorted','str','sum','tuple','type','zip'
      ]);

      const highlightPython = (source) => {
        const pattern = /(#.*$|\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|@[A-Za-z_][A-Za-z0-9_]*|\b\d+(?:\.\d+)?\b|\b[A-Za-z_][A-Za-z0-9_]*\b|[+\-*\/%=!<>]=?|[(){}\[\]:.,])/gm;
        let result = '';
        let lastIndex = 0;
        let functionPending = false;

        source.replace(pattern, (match, _group, offset) => {
          result += escapeHtml(source.slice(lastIndex, offset));
          let className = '';

          if (match.startsWith('#')) {
            className = 'comment';
          } else if (match.startsWith('"""') || match.startsWith(\"'''\") || match.startsWith('\"') || match.startsWith(\"'\")) {
            className = 'string';
          } else if (match.startsWith('@')) {
            className = 'decorator';
          } else if (/^\d/.test(match)) {
            className = 'number';
          } else if (keywords.has(match)) {
            className = 'keyword';
            functionPending = match === 'def';
          } else if (builtins.has(match)) {
            className = 'builtin';
          } else if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(match) && functionPending) {
            className = 'function';
            functionPending = false;
          } else if (/^[+\-*/%=!<>]/.test(match)) {
            className = 'operator';
          } else if (match !== 'def') {
            functionPending = false;
          }

          if (className) {
            result += '<span class="token ' + className + '">' + escapeHtml(match) + '</span>';
          } else {
            result += escapeHtml(match);
          }

          lastIndex = offset + match.length;
          return match;
        });

        result += escapeHtml(source.slice(lastIndex));
        return result;
      };

      document.querySelectorAll('code.language-python').forEach((block) => {
        block.innerHTML = highlightPython(block.textContent || '');
      });
    })();
  </script>
</body>
</html>
"@

    Set-Content -LiteralPath $outputPath -Value $html -Encoding UTF8

    $indexEntries.Add([PSCustomObject]@{
        Tag = $first.Tag
        DifficultyZh = $first.DifficultyZh
        DifficultyEn = $first.DifficultyEn
        FileName = $fileName
        Count = $group.Count
    })
}

$groupedIndex = $indexEntries | Group-Object Tag | Sort-Object @{
    Expression = {
        if ($tagOrder.ContainsKey($_.Name)) { $tagOrder[$_.Name] } else { 9999 }
    }
}, @{
    Expression = { $_.Name }
}
$sections = foreach ($tagGroup in $groupedIndex) {
    $links = foreach ($entry in ($tagGroup.Group | Sort-Object DifficultyEn)) {
@"
      <li><a href="./$($entry.FileName)">$([System.Net.WebUtility]::HtmlEncode($entry.DifficultyZh))</a> <span>($($entry.Count) 题)</span></li>
"@
    }

@"
    <section class="tag-card">
      <h2>$([System.Net.WebUtility]::HtmlEncode($tagGroup.Name))</h2>
      <ul>
$(($links -join "`r`n"))
      </ul>
    </section>
"@
}

$indexHtml = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LeetCode 分类索引</title>
  <style>
    :root {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --line: #d7deea;
      --accent: #2563eb;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 32px 20px 64px;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    main {
      max-width: 1100px;
      margin: 0 auto;
    }
    h1 {
      margin-top: 0;
      margin-bottom: 8px;
      font-size: 32px;
    }
    p {
      color: var(--muted);
      margin-bottom: 24px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
    }
    .tag-card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }
    .tag-card h2 {
      margin-top: 0;
      margin-bottom: 12px;
      font-size: 20px;
    }
    .tag-card ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .tag-card li {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }
    .tag-card span {
      color: var(--muted);
      white-space: nowrap;
    }
    a { color: var(--accent); text-decoration: none; }
  </style>
</head>
<body>
  <main>
    <h1>LeetCode 分类索引</h1>
    <p>按题目自带标签归类，再按难度拆分为独立 HTML 页面。</p>
    <div class="grid">
$(($sections -join "`r`n"))
    </div>
  </main>
</body>
</html>
"@

Set-Content -LiteralPath (Join-Path $outputDir 'index.html') -Value $indexHtml -Encoding UTF8

$repoRoot = Split-Path -Path $PSScriptRoot -Parent
$docsDir = Join-Path $repoRoot 'docs'

if (Test-Path -LiteralPath $docsDir) {
    Remove-Item -LiteralPath $docsDir -Recurse -Force
}

Copy-Item -LiteralPath $outputDir -Destination $docsDir -Recurse -Force
New-Item -ItemType File -Path (Join-Path $docsDir '.nojekyll') -Force | Out-Null

Write-Host ("Generated {0} html files in {1} and mirrored to {2}" -f ($indexEntries.Count + 1), $outputDir, $docsDir)
