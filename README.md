# 百度迁徙平台数据获取

[English brief description](#english)

[百度迁徙平台](http://qianxi.baidu.com/#/)（百度慧眼）几乎是日前最具有参考价值的中国人口迁徙数据，许多论文以此为数据基础。但在其官网上既没有展示**所有的**数据，也没有提他们有公开的接口，只有一句“获取详情数据请点击[联系我们](https://huiyan.baidu.com/contact?article=qianxi)”。实际上除了没有给出公开的文档以外，百度迁徙平台不仅留了免费的接口，还能获取**几乎所有的**数据。~~感觉百度的意思就是：你有能力爬，我们愿意把数据给你；你没能力爬，那就花钱找我们要。~~ 2024 年初（本仓库创立之时） GitHub 上没有仍然在更新的、满足相同需求的代码，我们尝试抛砖引玉补齐这些，并整理好信息为后来人提供帮助。

查看本 API 提供的参考数据请见[更新日志](#更新日志)！

**注：似乎部分日期的部分数据缺失。如果不幸通过本仓库的方法获取到的数据中，您需要的日期刚好没有数据，也许可以尝试直接联系百度迁徙获得……**

## 接口

以下面的接口为例（似乎添加了除以下列出的以外的新的接口。请自行尝试！）。

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

配置好环境，运行`main.py`，查找“请修改这里”，并修改这些地方为你所需要的数据即可。所有下载到的 json 数据会保存在`./data/`下面。如果需要改为其他的格式（如 `csv`），可以在代码中操作 `json_data`。

因为这份代码是两年之前手工写的了，可能现在看起来有点简陋，所以您可能可以让一个大语言模型阅读过之后再撰写代码来获取数据。可以考虑把本文档（也就是 `README.md`）也喂给它，方便它理解。毕竟现在已经是 AI Coding 的时代了！

### 已知问题

1. 经反馈，由于当前版本的保存的目标路径是写死的（`./data/`），如果使用 Pytorch、Jupyter Notebook 等特殊环境可能会很难找到最后生成的文件到底在哪里。之后有时间可能会将这些改成一个变量方便修改。

2. 这份代码使用的是单线程遍历的做法，如果您需要获取大量数据，可能是非常耗时间的。所以我建议您在指挥大模型的时候，要求它写一个多线程。我给出的一个典型的提示词例子是（是的，我近年几乎都没有自己亲自写代码，都是让大语言模型帮我完成的）：

> 扮演 Python 专家。请阅读这份代码和 README.md。请基于这些代码创建一个新的现代的完整的代码，获取[从某个时间段]到[某个时间段]的某个城市的迁入迁出数据……我需要的接口有……请使用多线程的方式完成。请加入错误处理。……你可能需要首先理解这个 API 的工作方式，并且实验是否当前它工作正常。先不要生成代码，与我讨论你的计划，我同意之后，你再开始写代码。准备好就开始。

## 遇到了问题……

可以提 [Issue](https://github.com/baisebaoma/baiduqianxi/issues) 或 [发送邮件](mailto:baisebaoma@foxmail.com) 联系我。

我更建议您提 Issue，这样其他人也可以看到并参与讨论您的问题（并且这样做也会同时给我发邮件）！

我每天都看邮件！能帮助您很高兴，一起学习进步！

## 更新日志

### 2026.2.11

增加了下面这些说明，给出参考数据，方便大伙可以直接看到数据内容长什么样，适不适合您的研究。

以防您不知道：在这些数据中，类似“\u91cd\u5e86\u5e02”（意为“重庆市”）的看起来像乱码一样的内容是汉字 Unicode 编码。您可能需要把它们转化为正确的汉字后，查看会比较方便。

#### 获取最新数据日期 (Last Date)
- 说明：查看目前数据库里最新的数据更新到了哪一天（我刚刚已获取过，数据是“20260210”。也就是说它其实一直在实时更新！）。
- 参考数据：[http://huiyan.baidu.com/migration/lastdate.jsonp](http://huiyan.baidu.com/migration/lastdate.jsonp)

#### 迁徙规模指数趋势图 (History Curve)
- 说明：获取某城市（如南昌）历史上每一天的迁徙规模指数。
- 参考数据：[http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=360100&type=move_in](http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=360100&type=move_in)

#### 城市级别来源/目的地排名 (City Rank)
- 说明：查看在指定日期（如 20240130），迁入南昌的人主要来自哪些城市，以及具体的百分比（如果我没记错的话）。
- 参考数据：[http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=360100&type=move_in&date=20240130](http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=360100&type=move_in&date=20240130)

#### 省份级别来源/目的地排名 (Province Rank)
- 说明：查看在指定日期（如 20240130），迁入南昌的人主要来自哪些省份。
- 参考数据：[http://huiyan.baidu.com/migration/provincerank.jsonp?dt=city&id=360100&type=move_in&date=20240130](http://huiyan.baidu.com/migration/provincerank.jsonp?dt=city&id=360100&type=move_in&date=20240130)

### 2025.12.5

对接口进行了测试，似乎仍有效。注意接口最早的日期是 2019 年 1 月 12 日，不过这个时间之后的部分数据可能也是缺失的。

### 2024.12.6

对代码进行了测试，似乎仍有效。

## Star History

如果您觉得有用，请点一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=baisebaoma/baiduqianxi&type=Date)](https://star-history.com/#baisebaoma/baiduqianxi&Date)

# English

Baidu Migration Data Scraper (Scraping Tool for baidu.qianxi)

This repository provides a streamlined way to access population migration data from the [Baidu Migration Platform](http://qianxi.baidu.com/#/). While Baidu does not provide official documentation for their APIs, this project uncovers the underlying interfaces used by the platform to facilitate academic research, urban planning, and epidemic modeling.

## Features
* **Comprehensive Data:** Access move-in/move-out rankings (at both city and province levels) and historical migration index curves.
* **Research-Friendly:** Simplifies the collection of large-scale Spatio-temporal (时空的) data for professional studies.
* **AI-Native Ready:** The codebase and documentation are optimized to be easily understood and extended by LLMs (like GPT-4o, Gemini, or Claude) for customized scraping tasks.

## API Overview
The core endpoint is `http://huiyan.baidu.com/migration/{interface}.jsonp`.
* `cityrank`: Ranking of origin/destination cities.
* `provincerank`: Ranking of origin/destination provinces.
* `historycurve`: Historical daily migration index.

## Quick Start
1.  Configure the `main.py` with your target `id` (Area Code) and `date`.
2.  Run the script to save raw JSON data to `./data/`.
3.  **Encoding Note:** Unicode characters like `\u91cd\u5e86` represent Chinese city names (e.g., Chongqing). You may need to decode them using `unicode_escape` in Python.

## Communication
If you have any questions or encounter issues, please feel free to open an **Issue** or contact me via [Email](mailto:baisebaoma@foxmail.com). 

**I am comfortable with both English and Chinese (Mandarin/Cantonese) communication.**

