# 百度迁徙平台数据获取

[百度迁徙平台](http://qianxi.baidu.com/#/)（百度慧眼）几乎是日前最具有参考价值的中国人口迁徙数据，许多论文以此为数据基础。但在其官网上既没有展示**所有的**数据，也没有提他们有公开的接口，只有一句“获取详情数据请点击[联系我们](https://huiyan.baidu.com/contact?article=qianxi)”。实际上除了没有给出公开的文档以外，百度迁徙平台不仅留了免费的接口，还能获取**几乎所有的**数据。~~感觉百度的意思就是：你有能力爬，我们愿意把数据给你；你没能力爬，那就花钱找我们要。~~ 2024 年初 GitHub 上没有仍然在更新的、满足相同需求的代码，我们尝试抛砖引玉补齐这些，并整理好信息为后来人提供帮助。

2024.12.6 对代码进行了测试，似乎仍有效。

**注：似乎部分日期的部分数据缺失。如果不幸通过本仓库的方法获取到的数据中，您需要的日期刚好没有数据，也许可以尝试直接联系百度迁徙获得……**

## 接口

以下面的接口为例。

http://huiyan.baidu.com/migration/cityrank.jsonp?dt=province&id=330000&type=move_in&callback=jsonp_1581412681419_9173670

其中 `cityrank`（`/migration/` 后、`.jsonp` 前） 处的可选项一共有四个：`cityrank`、`provincerank`、`lastdate`、`historycurve`。其中 `historycurve` 比较特殊，直接返回历史上所有日期的数据。

## 参数

请参考 `main.py` 中的注释。以下给出简要说明：

`dt`：级别。可选的值有：`country`、`province`、`city`。

`id`：六位数，代表区域（可以是省，也可以是市），如：360100。如果是 dt 是 country，不需要给这个参数。

`type`: `move_in`, `move_out` 分别代表迁入迁出数据。

`date`: 长度为8、格式为年月日的日期，如：`20240130`。如果接口是 `historycurve`，不需要给这个参数。

`callback`: 时间戳，他调取的时候格式为：`jsonp_X_Y`，其中 X 经实验为 13 位的毫秒级时间戳，Y是7位数字，估计是更精确的时间。爬取的时候甚至不需要填写这个。它只是代表“我给你返回的数据确实是你这次获取的数据”。

## 代码

运行`main.py`，查找“请修改这里”，并修改这些地方为你所需要的数据即可。所有爬到的 json 数据会保存在`./data/`下面。如果需要改为其他的格式（如 `csv`），可以在代码中操作 `json_data`。

## 已知问题

1. 经反馈，由于当前版本的保存的目标路径是写死的（`./data/`），如果使用 Pytorch 等特殊环境可能会很难找到最后生成的文件到底在哪里。之后有时间可能会将这些改成一个变量方便修改。

## 遇到了问题……

可以提 [Issue](https://github.com/baisebaoma/baiduqianxi/issues) 或 [发送邮件](mailto:baisebaoma@foxmail.com) 联系我。我更建议您提 Issue，这样其他人也可以看到并参与讨论您的问题！

## Star History

如果您觉得有用，请点一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=baisebaoma/baiduqianxi&type=Date)](https://star-history.com/#baisebaoma/baiduqianxi&Date)
