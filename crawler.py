# !/usr/bin/python
# **coding:utf-8**

import os, sys, time

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

import log

# ================= 配置区 =================
QUERY = "人工智能"                   # 搜索关键词
TARGET_PAGES = range(1,51)          # 指定爬取页数列表
RESULTS_PER_PAGE = 10               # 每页结果数 (Bing默认10)
MAX_WORKERS = 5                     # 并发线程数
CSV_FILE = 'crawl_results.csv'       # 输出文件名
RETRY_TIMES = 2                     # 单页最大重试次数
REQUEST_TIMEOUT = 10                # 请求超时时间（秒）
ERROR_PAGES = []                    # 错误页列表

# ================= 核心代码 =================
class BingScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        
    def init_csv(self):
        """初始化CSV文件"""
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['page', 'title', 'link', 'snippet'])
            writer.writeheader()

    @retry(stop=stop_after_attempt(RETRY_TIMES), 
           wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_page(self, query, page):
        """带自动重试的页面抓取"""
        first = (page - 1) * RESULTS_PER_PAGE + 1
        params = {"q": query, "first": first, "count": RESULTS_PER_PAGE}
        
        try:
            resp = self.session.get(
                "https://www.bing.com/search",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            return resp.text
        except requests.exceptions.RequestException as e:
            ERROR_PAGES.append({page: str(e)})  # 记录错误页码
            raise

    def parse_page(self, html, page):
        """解析页面内容"""
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='b_algo')
        page_results = []
        
        for item in items:
            title = item.find('h2').get_text(strip=True) if item.find('h2') else 'No Title'
            link = item.find('a')['href'] if item.find('a') else 'No Link'
            snippet = item.find('p').get_text(strip=True) if item.find('p') else 'No Snippet'
            page_results.append({'page': page, 'title': title, 'link': link, 'snippet': snippet})
        
        return page_results

    def save_results(self, results):
        """增量保存结果到CSV"""
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['page', 'title', 'link', 'snippet'])
            writer.writerows(results)

    def scrape_page(self, query, page):
        """单页处理流水线"""
        try:
            html = self.fetch_page(query, page)
            results = self.parse_page(html, page)
            self.save_results(results)
            return results
        except Exception as e:
            ERROR_PAGES.append({page: str(e)})  # 记录错误页码
            return False

Logs = log.Info()

scraper = BingScraper()
scraper.init_csv()
    
start_time = time.time()
success_count = 0

def scrape_page(query:str,
                tgt_pages:list=range(1,11),
                max_trds_cnt=5):
    global success_count
    
    with ThreadPoolExecutor(max_workers=max_trds_cnt) as executor:
        # 创建进度条
        with tqdm(total=len(tgt_pages),
                  desc="Crawling progress",
                  unit=" page",
                  ncols=100) as pbar:
            # 提交任务
            futures = {
                executor.submit(scraper.scrape_page, query, page): page
                for page in tgt_pages
            }
                
            # 处理完成的任务
            for future in as_completed(futures):
                page = futures[future]
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    pass
                finally:
                    pbar.update(1)
    
    csv_data = pd.read_csv(CSV_FILE)
    
    return csv_data

# ================= 执行入口 =================
if __name__ == "__main__":
    res = scrape_page(QUERY, TARGET_PAGES, MAX_WORKERS)
    # 输出统计信息
    total_time = time.time() - start_time
    if not ERROR_PAGES == []:
        Logs.error(f"== False pages ==")
        for e in ERROR_PAGES:
            Logs.error(e)
    Logs.info(f"== Complete ==")
    Logs.info(f"Total page count: {len(TARGET_PAGES)}")
    Logs.info(f"Success page count: {success_count}")
    Logs.info(f"False page count: {len(ERROR_PAGES)}")
    Logs.info(f"Total entry count: {len(res)}")
    Logs.info(f"Success rate: {success_count/len(TARGET_PAGES):.1%}")
    Logs.info(f"Total duration: {total_time:.2f} seconds")
    Logs.info(f"Average speed: {total_time/len(TARGET_PAGES):.2f} seconds per page")