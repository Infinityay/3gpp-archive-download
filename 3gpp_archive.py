import argparse
import os
import threading
import time
import zipfile
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from logger_config import CustomLogger

# 配置日志
logger_config = CustomLogger()
logger = logger_config.get_logger()


def download_file(url, folder, multithread=False):
    try:
        fileName = url.split("/")[-1]
        fileLocation = os.path.join(folder, fileName)
        unzip_folder = os.path.join(folder, os.path.splitext(fileName)[0])  # 解压缩文件的文件夹
        if os.path.exists(unzip_folder):
            logger.info(f"由于已存在文件夹{unzip_folder}, 跳过{fileName}下载")
            return

        if multithread:
            time.sleep(2)
        else:
            time.sleep(0.5)

        response = requests.get(url)
        response.raise_for_status()  # 如果请求不成功，会引发 HTTPError 异常

        with open(fileLocation, 'wb') as file:
            file.write(response.content)
            logger.info(f"下载 {fileName} 成功")

        # 判断文件是否是ZIP文件

        if fileName.lower().endswith('.zip'):

            os.makedirs(unzip_folder, exist_ok=True)

            # 解压zip文件
            try:
                with ZipFile(fileLocation, 'r') as zip_ref:
                    zip_ref.extractall(unzip_folder)
            except zipfile.BadZipFile as e:
                logger.error(f"解压 {fileName} 时出现问题: {str(e)}")
            except Exception as e:
                logger.error(f"解压 {fileName} 时出现未知问题: {str(e)}")

            # 删除源ZIP文件
            try:
                os.remove(fileLocation)
            except OSError as e:
                logger.error(f"删除 {fileName} 时出现问题: {str(e)}")


    except requests.RequestException as e:
        logger.error(f"下载 {url} 时出现问题: {str(e)}")


def download_series(base_url, series_url, folder, multithread):
    series_page = requests.get(series_url)
    series_soup = BeautifulSoup(series_page.text, 'html.parser')

    # 筛选所有包含series_num的links
    links = [link for link in series_soup.find_all('a', href=True)
             if link.get_text() == link['href'].split("/")[-1]]

    if multithread:
        # 使用多线程下载
        threads = []
        for link in links:
            href = link['href']
            if href.endswith('.zip') or href.endswith('.txt'):
                file_url = href
                thread = threading.Thread(target=download_file, args=(file_url, folder, multithread))
                threads.append(thread)
                thread.start()
            else:
                # 进入下一级目录
                next_level_url = href
                next_level_folder = os.path.join(folder, href.split("/")[-1])  # 使用目录名作为文件夹名
                os.makedirs(next_level_folder, exist_ok=True)
                download_series(base_url, next_level_url, next_level_folder, multithread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

    else:
        for link in links:
            href = link['href']
            if href.endswith('.zip') or href.endswith('.txt'):
                file_url = href
                download_file(file_url, folder, False)
            else:
                # 进入下一级目录
                next_level_url = href
                next_level_folder = os.path.join(folder, href.split("/")[-1])  # 使用目录名作为文件夹名
                os.makedirs(next_level_folder, exist_ok=True)
                download_series(base_url, next_level_url, next_level_folder,False)
            if link.get_text().endswith('series'):
                logger.info(f"{link.get_text()} 下载完成.")


def parse_series(series_string):
    # 将逗号分隔的字符串转换为整数列表
    return [int(item) for item in series_string.split(',')]

def main():
    base_url = "https://www.3gpp.org/ftp/Specs/archive"
    download_folder = "archive"  # 保存下载文件的文件夹
    os.makedirs(download_folder, exist_ok=True)

    parser = argparse.ArgumentParser(description="Download 3gpp documents")
    parser.add_argument("-m", "--multithread", action="store_true", help="enable multithreaded")
    parser.add_argument("-s", "--series", type=parse_series, help="set the series indices that you need to download, separated by commas")

    args = parser.parse_args()

    series_page = requests.get(base_url)
    series_soup = BeautifulSoup(series_page.text, 'html.parser')

    # 筛选以 "series" 结尾的链接
    series_links = [link for link in series_soup.find_all('a', href=True)
                    if link['href'].endswith('series')]

    # 不指定下载序列号，就下载全部序列
    if args.series is None:
        selected_links = series_links
    else:
        selected_links = [link for link in series_links if int(link.get_text().split('_')[0]) in args.series]

    for series_link in selected_links:
        series_url = series_link['href']
        series_folder = os.path.join(download_folder, series_link.get_text())  # 使用系列名作为文件夹名
        os.makedirs(series_folder, exist_ok=True)
        download_series(base_url, series_url, series_folder, multithread=args.multithread)


if __name__ == "__main__":
    main()
