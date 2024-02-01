import requests
import json
import re
import time
import os
from datetime import datetime, timedelta


# 用来把英文和数字翻译成中文存到文件名里。也许还有别的用途。
translation_table = {
    'lastdate': '最后日期',
    'historycurve': '迁徙规模指数',
    'cityrank': '市百分比',
    'provincerank': '省百分比',
    'country': '国家',
    'province': '省',
    'city': '市',
    # 如果你有其他省市数据需要获取，请修改下面
    '360000': '江西省',
    '360100': '南昌市',
    '360700': '赣州市',
    '360900': '宜春市',
    '360800': '吉安市',
    '361100': '上饶市',
    '361000': '抚州市',
    '360400': '九江市',
    '360200': '景德镇市',
    '360300': '萍乡市',
    '360500': '新余市',
    '360600': '鹰潭市',
    'move_in': '迁入',
    'move_out': '迁出',
}


class Types:
    """
    存储我们已知和要请求的一些数据。
    """
    # 请不要修改data_type
    data_type = {  # 'lastdate',     # 虽然 lastdate 确实是一个接口，但是我们在每次爬取时
                                     # 只需在最开始调用一次就可以了。所以我们在设计时排除之。
                   # 'historycurve', # 虽然 historycurve 确实是一个接口，但是这个接口会返回
                                     # 所有日期的这个数据。所以只用调用一次就可以了
                 'cityrank',
                 'provincerank'}
    # 请不要修改dt
    dt = {'country',
          'province',
          'city'}
    # 如果你有其他省市数据需要获取，请修改这里
    region = {
        # 使用Types.region.keys()来找到有哪些省份；使用Types.region["360000"]来查询它是省还是市。
        "360000": "province",
        '360100': 'city',
        '360700': 'city',
        '360900': 'city',
        '360800': 'city',
        '361100': 'city',
        '361000': 'city',
        '360400': 'city',
        '360200': 'city',
        '360300': 'city',
        '360500': 'city',
        '360600': 'city',
    }
    # 请不要修改move_type
    move_type = {'move_in',
                 'move_out'}


def generate_date_range(start_date_str:str, end_date_str:str):
    """
    输入两端的日期，输出包括这两天在内的所有日期。

    :param start_date_str: 起始日期，长度为8、格式为年月日的字符串，如"20201231"。
    :param end_date_str: 结束日期，格式同上。
    :return: 一个list，包含从起始日期开始到结束日期为止的所有日期，格式同上。
    """
    # 将输入的日期字符串转换为datetime对象
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.strptime(end_date_str, '%Y%m%d')

    # 初始化日期列表，包含起始日期
    date_list = [start_date.strftime('%Y%m%d')]

    # 生成日期范围
    current_date = start_date
    while current_date < end_date:
        current_date += timedelta(days=1)
        date_list.append(current_date.strftime('%Y%m%d'))

    return date_list


def get_timestamp():
    """
    获得当前时间戳。

    :return: 长度为13的时间戳
    """
    return str(int(time.time() * 1000))  # * 1000获取毫秒级时间戳


def get_lastdate():
    """
    从API获得目前API有的最晚的日期。

    :return: 长度为8、格式为年月日的字符串，如"20201231"。
    """
    url = f'http://huiyan.baidu.com/migration/lastdate.jsonp'
    response = requests.get(url)
    json_data_match = re.search(r'{.*}', response.text)
    if json_data_match:
        json_data_str = json_data_match.group()

        # Decode JSON string, automatically handling Unicode characters
        json_data = json.loads(json_data_str)
        return_value = json_data['data']['lastdate']
        print(f"成功获取到API最晚日期：{return_value}")
        return return_value
    else:
        print('获取API最晚日期时失败')


def get_historycurve(region: str, move_type: str):
    """
    从API获得一个区域（省或市）的迁入或迁出的迁徙规模指数。historycurve API会直接返回所有日期。存储文件到文件名。

    :param region: 行政区域编码，如300001。
    :param move_type: 'move_in' 或 'move_out'
    :return: 成功返回 True，失败返回 False
    """
    # 注意：这个文件要覆写，因为每次抓到的可能不一样。不需要判断是否已存在文件。
    output_file = f'./data/{translation_table[region]}_{translation_table[move_type]}_{translation_table["historycurve"]}.json'

    print(f"正在获取"
          f' {translation_table[region]}'
          f' {translation_table[move_type]} 的'
          f' {translation_table["historycurve"]}')

    url = f"http://huiyan.baidu.com/migration/historycurve.jsonp?dt={Types.region[region]}&id={region}&type={move_type}"
    response = requests.get(url)
    json_data_match = re.search(r'{.*}', response.text)
    if json_data_match:
        json_data_str = json_data_match.group()

        # Decode JSON string, automatically handling Unicode characters
        json_data = json.loads(json_data_str)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print('成功')
        return True
    else:
        print('失败')
        return False


# http://huiyan.baidu.com/migration/cityrank.jsonp?
# dt=country&id=0&type=move_in&date=20240130&callback=jsonp_1706674779082_8488633
def download_and_convert_jsonp(data_type: str, dt: str, id: str, move_type: str, date: str, callback: str):
    """
    从百度慧眼的API上获得数据并存到本地。

    :param data_type: 就是你要获取的信息类型，有且仅有下列几个值：
        lastdate，返回最后有数据的日期（昨天）；
        historycurve，返回从20190112到lastdate为止的迁徙规模指数；
        cityrank，返回迁入xx来源地（城市级别）；
        provincerank，返回xx来源地（省份级别）。
    :param dt: 级别。可选的值有：country，province，city。
    :param id: 哪里的数据（若dt为国家则不需要id）。参照"行政区划乡镇清单201910"表。级别要和上面的id对应。
    :param move_type: 迁入还是迁出。可选的值有：move_in, move_out。
    :param date: 要的日期，格式：八位数的年月日，如20240131。data_type为lastdate或historycurve时不需要这个参数。
    :param callback: 没什么用，只是为了确认返回值是我这次要的数据罢了。给个时间戳就行。
    :param output_file: 该文件要存到的文件名。
    :return: boolean 成功返回True，失败返回False
    """
    # TODO: 如果要爬大量数据，搞多线程
    output_file = f'./data/{translation_table[id]}_' \
                  f'{translation_table[move_type]}_' \
                  f'{translation_table[data_type]}_' \
                  f'{date}.json'

    if os.path.exists(output_file):
        print("文件已存在")
        return False

    # Construct the full URL with query parameters
    url = f'http://huiyan.baidu.com/migration/{data_type}.jsonp?dt={dt}&id={id}&type={move_type}&date={date}&callback={callback}'

    response = requests.get(url)

    # Extract JSON data part using regular expression
    json_data_match = re.search(r'{.*}', response.text)
    if json_data_match:
        json_data_str = json_data_match.group()

        # Decode JSON string, automatically handling Unicode characters
        json_data = json.loads(json_data_str)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        print('成功')
    else:
        print('失败')


def get_data(region: str, data_type: str, move_type: str, date: str):
    timestamp = get_timestamp()
    print(f"正在获取"
          f' {translation_table[region]}'
          f' {translation_table[move_type]} 的'
          f' {translation_table[data_type]}，日期为{date}')
    download_and_convert_jsonp(
        data_type=data_type,
        dt=Types.region[region],
        id=region,
        move_type=move_type,
        date=date,
        callback=timestamp
    )


def get_by_date(from_date, to_date, lastdate):
    # 将日期字符串转换为datetime对象
    from_date_dt = datetime.strptime(from_date, '%Y%m%d')
    to_date_dt = datetime.strptime(to_date, '%Y%m%d')
    lastdate_dt = datetime.strptime(lastdate, '%Y%m%d')

    print("正在检查日期输入合法性")

    # 检查from_date是否小于'20190112'
    earlydate = datetime(2019, 1, 12)
    if from_date_dt < earlydate:
        print("你的起始日期比API目前有的最早日期还早。已经将起始日期设置成API的最早日期，并尝试继续运行。")
        from_date_dt = earlydate

    # 检查to_date是否大于lastdate
    if to_date_dt > lastdate_dt:
        print("你的结束日期比API目前有的最晚日期还晚。已经将结束日期设置成API的最晚日期，并尝试继续运行。")
        to_date_dt = lastdate_dt

    # 检查输入合法性
    if from_date_dt > to_date_dt:
        print("你的起始日期需要比结束日期早。")
        return

    print("成功")

    # 转换为字符串，以便生成日期范围
    from_date = from_date_dt.strftime('%Y%m%d')
    to_date = to_date_dt.strftime('%Y%m%d')

    for region in Types.region.keys():
        for move_type in Types.move_type:
            get_historycurve(region, move_type)  # 获取他的迁徙规模指数

    for date in generate_date_range(from_date, to_date):  # 日期
        for region in Types.region.keys():
            for move_type in Types.move_type:
                for data_type in Types.data_type:
                    get_data(region, data_type, move_type, date)


if __name__ == "__main__":
    # 检查文件夹是否存在
    if not os.path.exists('data'):
        # 如果不存在，创建文件夹
        os.makedirs('data')
    lastdate = get_lastdate()  # 接口给到的最晚日期
    # 如果你需要修改起始和结束日期，请修改这里
    get_by_date('20230101', '20240131', lastdate)
