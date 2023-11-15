import os
import zipfile
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

from logger_config import CustomLogger

# 配置日志
logger_config = CustomLogger()
logger = logger_config.get_logger()


def download_file(url, folder):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求不成功，会引发 HTTPError 异常
        fileName = url.split("/")[-1]
        fileLocation = os.path.join(folder, fileName)

        with open(fileLocation, 'wb') as file:
            file.write(response.content)
        logger.info(f"{fileName} 下载完成.")

        # 判断文件是否是ZIP文件

        if fileName.lower().endswith('.zip'):
            unzip_folder = os.path.join(folder, os.path.splitext(fileName)[0])  # 解压缩文件的文件夹
            os.makedirs(unzip_folder, exist_ok=True)

            try:
                with ZipFile(fileLocation, 'r') as zip_ref:
                    zip_ref.extractall(unzip_folder)
                logger.info(f"{fileName} 解压完成.")
            except zipfile.BadZipFile as e:
                logger.error(f"解压 {fileName} 时出现问题: {str(e)}")
            except Exception as e:
                logger.error(f"解压 {fileName} 时出现未知问题: {str(e)}")


    except requests.RequestException as e:
        logger.error(f"下载 {url} 时出现问题: {str(e)}")


def download_series(base_url, series_url, folder):
    series_page = requests.get(series_url)
    series_soup = BeautifulSoup(series_page.text, 'html.parser')

    # 筛选所有包含series_num的links
    links = [link for link in series_soup.find_all('a', href=True)
             if link.get_text() == link['href'].split("/")[-1]]

    for link in links:
        href = link['href']
        if href.endswith('.zip') or href.endswith('.txt'):
            file_url = href
            download_file(file_url, folder)
        else:
            # 进入下一级目录
            next_level_url = href
            next_level_folder = os.path.join(folder, href.split("/")[-1])  # 使用目录名作为文件夹名
            os.makedirs(next_level_folder, exist_ok=True)
            download_series(base_url, next_level_url, next_level_folder)


def main():
    base_url = "https://www.3gpp.org/ftp/Specs/archive"
    download_folder = "archive"  # 保存下载文件的文件夹
    os.makedirs(download_folder, exist_ok=True)

    series_page = requests.get(base_url)
    series_soup = BeautifulSoup(series_page.text, 'html.parser')

    # 筛选以 "series" 结尾的链接
    series_links = [link for link in series_soup.find_all('a', href=True)
                    if link['href'].endswith('series')]

    for series_link in series_links:
        series_url = series_link['href']
        series_num = series_link.get_text().split('_')[0]
        series_folder = os.path.join(download_folder, series_link.get_text())  # 使用系列名作为文件夹名
        os.makedirs(series_folder, exist_ok=True)

        download_series(base_url, series_url, series_folder)


if __name__ == "__main__":
    main()
