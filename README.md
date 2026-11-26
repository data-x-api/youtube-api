# YouTube 数据接口（YouTube API）：视频搜索、详情、评论、字幕、频道

**YouTube API · YouTube transcripts · YouTube comments · YouTube channel videos**

这个仓库是 [DataXAPI](https://dataxapi.com/zh/?ref=gh-youtube-api) 的YouTube接口说明和能直接跑的脚本：10 个接口，一把 Key，按次付费，$0.002 起，**出错不收费**。不用登录平台账号，不用 Cookie，不开浏览器。

[免费拿 Key：试用最多 333 次，不用绑卡](https://dataxapi.com/zh/signin/?button=gh-youtube-api) · [全部接口文档](https://dataxapi.com/zh/apis/?ref=gh-youtube-api) · [接进 AI（MCP）](#接进-aimcp) · [English](#english)

最低充 $10，余额不过期；支持支付宝、微信支付和银行卡。

## 全部 10 个接口

### 频道

| 接口 | 拿到什么 | 价格 | 编号 |
|---|---|---|---|
| [YouTube 频道资料](https://dataxapi.com/zh/apis/youtube/channels/get/?ref=gh-youtube-api) | 按频道编号或账号名取 YouTube 频道资料：名称、简介、订阅数、视频数、总播放数、是否认证、创建日期，“关于”里列的链接（官网、其他社交账号）和频道关键词。 | $0.002 一次 | `youtube.channels.get` |
| [YouTube 频道搜索](https://dataxapi.com/zh/apis/youtube/channels/search/?ref=gh-youtube-api) | 按搜索词找 YouTube 频道：名称、账号名、简介、订阅数、是否认证。 | $0.002 一次 | `youtube.channels.search` |
| [YouTube 频道视频](https://dataxapi.com/zh/apis/youtube/channels/videos/list/?ref=gh-youtube-api) | 按频道编号或账号名取一页该 YouTube 频道的视频或 Shorts，可按最新或最热排：标题、简介、发布时间、播放数、点赞数、时长。 | $0.002 一次 | `youtube.channels.videos.list` |
| [YouTube 频道帖子](https://dataxapi.com/zh/apis/youtube/channels/posts/list/?ref=gh-youtube-api) | 按频道编号或账号名取一页该 YouTube 频道“帖子”栏（原“社区”）里的帖子，从最新的开始：正文、图片、点赞数、附带的视频。 | $0.002 一次 | `youtube.channels.posts.list` |

### 评论

| 接口 | 拿到什么 | 价格 | 编号 |
|---|---|---|---|
| [YouTube 评论回复](https://dataxapi.com/zh/apis/youtube/comments/replies/list/?ref=gh-youtube-api) | 用评论列表给的回复标识，取一页这条 YouTube 评论下的回复：正文、回复者、点赞数。 | $0.002 一次 | `youtube.comments.replies.list` |

### 视频

| 接口 | 拿到什么 | 价格 | 编号 |
|---|---|---|---|
| [YouTube 视频评论](https://dataxapi.com/zh/apis/youtube/videos/comments/list/?ref=gh-youtube-api) | 按视频编号或链接取一页 YouTube 评论，可按热门或最新排：正文、评论者、点赞数、回复数，以及取回复用的标识。 | $0.002 一次 | `youtube.videos.comments.list` |
| [YouTube 视频详情](https://dataxapi.com/zh/apis/youtube/videos/get/?ref=gh-youtube-api) | 按视频编号或链接取一个 YouTube 视频：标题、简介、频道、发布时间、播放数、点赞数、评论数、时长，作者设的标签、分类、章节。 | $0.002 一次 | `youtube.videos.get` |
| [YouTube 视频搜索](https://dataxapi.com/zh/apis/youtube/videos/search/?ref=gh-youtube-api) | 按搜索词找 YouTube 视频，可按相关或播放数排、按发布时间筛：标题、频道、播放数、时长。 | $0.002 一次 | `youtube.videos.search` |
| [YouTube 视频字幕](https://dataxapi.com/zh/apis/youtube/videos/transcript/get/?ref=gh-youtube-api) | 按视频编号或链接取 YouTube 视频的字幕全文和带时间的分段，可用 lang 指定字幕语言。 | $0.002 一次 | `youtube.videos.transcript.get` |

### 内容

| 接口 | 拿到什么 | 价格 | 编号 |
|---|---|---|---|
| [YouTube 帖子详情](https://dataxapi.com/zh/apis/youtube/posts/get/?ref=gh-youtube-api) | 按帖子编号或链接取一条 YouTube 频道帖子（原“社区”帖）：正文、频道、图片、点赞数、附带的视频。 | $0.002 一次 | `youtube.posts.get` |

## 真实返回长什么样

**YouTube 视频搜索**（`youtube.videos.search`，参数 `{"query":"meteor shower"}`），录下的真实返回，个人信息换成了 …：

```json
{
  "data": {
    "items": [
      {
        "id": "…",
        "url": "https://example.com/…",
        "type": "video",
        "title": "…",
        "author": {
          "id": "…",
          "username": "…",
          "name": "…",
          "avatar_url": "https://example.com/…"
        },
        "metrics": {
          "views": 1840
        },
        "images": [
          "https://example.com/…"
        ]
      }
    ]
  },
  "page": {
    "next_cursor": "example-cursor-1",
    "cursor_expires_at": "2026-10-12T19:50:45.000Z",
    "has_more": true,
    "returned": 20
  }
}
```

每个接口都是同一种结构：列表在 `data.items`，单个在 `data.item`，下一页用 `page.next_cursor`，这次扣了多少在 `meta.billing.amount`，平台不给的字段为 `null` 并在 `meta.unavailable` 里写明。

## 快速开始

1. [拿一把 Key](https://dataxapi.com/zh/signin/?button=gh-youtube-api)（`dx_` 开头），放进环境变量：`export DATAXAPI_API_KEY=dx_...`
2. 调一次接口：

```bash
curl -G "https://api.dataxapi.com/v1/youtube/videos/search" \
  -H "Authorization: Bearer $DATAXAPI_API_KEY" \
  --data-urlencode 'query=meteor shower'
```

3. 或者跑 `examples/` 里的脚本。只用 Python 标准库（3.9 以上）；不加 `--yes` 只报价、不调用，加了才真跑，跑完告诉你实际花了多少：

| 脚本 | 做什么 | 先看要花多少 |
|---|---|---|
| [quickstart.py](examples/quickstart.py) | 取几页结果，存成 CSV | `cd examples && python3 quickstart.py 'meteor shower'` |

## 接进 AI（MCP）

Claude Code：

```bash
claude mcp add --transport http --scope user dataxapi https://api.dataxapi.com/mcp --header "Authorization: Bearer $DATAXAPI_API_KEY"
```

Cursor、Cherry Studio、WorkBuddy 等支持远程 MCP 的客户端：

```json
{
  "mcpServers": {
    "dataxapi": {
      "url": "https://api.dataxapi.com/mcp",
      "headers": {
        "Authorization": "Bearer dx_..."
      }
    }
  }
}
```

接上以后直接用中文问，比如“帮我看看这个关键词最近一个月在抖音上的热度”。AI 花钱前可以先免费查接口和价格。也可以装成技能：`npx skills add data-x-api/skills`。

## 常见问题

**要不要平台账号、Cookie 或扫码？**

不要。只要一把 DataXAPI Key，不碰你的账号，也就不存在账号被风控的问题。

**调用出错扣钱吗？**

不扣。每次返回里的 `meta.billing.amount` 写明这次扣了多少（美元）。

**数据有多新？**

默认在你调用时从平台实时读取，返回里的 `meta.fetched_at` 写明读取时间。

**怎么翻页？**

列表接口一次返回一页，把返回里的 `page.next_cursor` 作为 `cursor` 传回去取下一页，每一页单独计费。

## English

YouTube API: video search, video details, comments, transcripts and channels, through one key, paid per call, no quota.

No platform account, cookie or QR login. Paid per call from $0.002; errors are not charged. Free trial: up to 333 calls, no card. [Get a key](https://dataxapi.com/signin/?button=gh-youtube-api) · [All endpoints](https://dataxapi.com/apis/?ref=gh-youtube-api) · MCP: `https://api.dataxapi.com/mcp`.

## License

MIT

<sub>接口和价格取自 DataXAPI 的目录 0051cce45e9530b9、价格版本 22；以 [dataxapi.com/zh/apis](https://dataxapi.com/zh/apis/?ref=gh-youtube-api) 为准。</sub>
