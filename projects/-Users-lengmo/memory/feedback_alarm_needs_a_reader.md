---
name: feedback-alarm-needs-a-reader
description: 加任何告警/兜底前先确认这个信号最终被谁读；没有读者的通道等于哑铃，做了比不做更危险
metadata:
  type: feedback
---

接到「给它加个告警/兜底」的活，**动手前先回答：这条信号最终会被谁读、怎么读**。
现成的日志文件、`OnFailure` 钩子、监控合同 JSON，都可能只是看起来像通道。

**Why**：2026-08-22 soliloquy 备份兜底。owner 给了两个选项（OnFailure 挂通知 / 让现成的定期检查顺手核一眼），
照字面做出来两个都掉坑——现成那个定期检查往 `watch.log` 追行，**没有任何程序或人在读**；
而那台机器上当时根本没有对外通道（只有 curl 和 jq，无 MTA 无 webhook）。仓里 `外部服务台账.md` §6
当时把「uptime 供应商未选、owner 通知通道未定」登记成硬缺口，`minute-alerts.json` 里连
「备份恢复失败」这条 P0 信号都写好了，只是没有任何东西把它送出去。
装个没人读的告警，比明说「现在没有通道」更糟——它制造已经被监控的错觉。

**缺口已补（2026-08-26/28 复核，本条是已兑现的判例、不是待办）**：`docs/ops/外部服务台账.md` §6 现在写的是
「uptime 供应商 = 已上线，Healthchecks 8 个独立检查（7 个 monitor check 10 分钟 period + 5 分钟 grace，
backup heartbeat 6 小时 + 1 小时 grace）」「owner 告警通道 = 已绑定 owner 邮件集成，可控 Down→Up 两次 ping 均 200」
「备份心跳接口 = production 脚本侧已接（成功 GET `BACKUP_HEARTBEAT_URL`、失败 GET `.../fail`）」——
落地形态正是下面第 3 条推荐的 dead man's switch。再读这条别照着一个已经不存在的缺口行动。

**How to apply**：
1. 先 grep 有没有真的 sink（webhook / MTA / 已在跑且会通知的 CI workflow / 外部探针供应商）。
2. 没有 sink 就**明说**，别硬做；把信号做成本机可见的确定状态（unit 进 `failed`），
   再留一个配置化的空钩子（URL 填了才发），让 owner 自己接通道。
3. 选「成功时 ping」的 dead man's switch 而不是「失败时告警」——只有前者盖得住机器关机，
   那时本机没有任何东西还能把告警发出去。
4. owner 给的选项本身不够用时要顶回并给更强的组合，这跟 CLAUDE.md 开工三问 #3
   「有更简单的形态要说」是同一条规则的反向。参见 [[feedback-gates-must-fail-on-purpose]]。
