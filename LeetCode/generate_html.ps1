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

$root = Join-Path $PSScriptRoot '.'
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
                ProblemText = $problemText.Trim()
                SolutionText = $solutionText
                RelativePath = $problemDir.FullName.Substring($root.Length).TrimStart('\')
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
      <pre><code>$([System.Net.WebUtility]::HtmlEncode($item.SolutionText))</code></pre>
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

$groupedIndex = $indexEntries | Group-Object Tag | Sort-Object Name
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

Write-Host ("Generated {0} html files in {1}" -f ($indexEntries.Count + 1), $outputDir)
