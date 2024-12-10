import time
import copy

import requests

from base.base import Base
from po.boss_po import BossPo


class PickJob(Base):
    def __init__(self):
        super().__init__()
        self.context_storage = BossPo.context_storage
        self.page_url = BossPo.url
        self.host = BossPo.host
        self.result = []
        self.capture_target_urls = [BossPo.job_list_url]
        self.session = requests.Session()
        self.record_status = set()


    def run(self):
        page = self.page
        import time
        time.sleep(1)
        page.get_by_role("link", name="BOSS直聘", exact=True).click()
        page.get_by_role("link", name="推荐").click()
        tag_list = ["测试开发（上海）", "测试工程师（上海）", "自动化测试（上海）"]
        for tag in tag_list:
            self.get_available_jobs(tag)

    def get_job_list(self, tag):
        import time
        time.sleep(1)
        page = self.page
        page.get_by_role("link", name=tag).click()

        url_data = self.capture_request_list[BossPo.job_list_url]
        target_k = "encryptExpectId"
        for args_kv in url_data.split("&"):
            if target_k in args_kv:
                v = args_kv.split("=")[1]
        encryptExpectId = v
        for i in range(1, 6):
            has_more = self.do_get_job_list(i, encryptExpectId)
            if not has_more:
                break

    def do_get_job_list(self, offset, encryptExpectId):
        time.sleep(1)
        page_num = offset
        params = {
            "city": "",
            "experience": "",
            "payType": "",
            "partTime": "",
            "degree": "",
            "industry": "",
            "scale": "",
            "salary": "",
            "jobType": "",
            "encryptExpectId": encryptExpectId,
            "page": page_num,
            "pageSize": 15
        }
        url = BossPo.job_list_url

        cookies = self.context.cookies()
        response = self.session.get(url, headers=self.last_headers, params=params, cookies={cookie['name']: cookie['value'] for cookie in cookies})
        result_d = response.json()
        has_more = result_d["zpData"]["hasMore"]
        job_list = result_d["zpData"]["jobList"]
        for job in job_list:
            security_id = job["securityId"]
            lid = job["lid"]
            self.get_job_detail(security_id, lid)
        return has_more

    def get_job_detail(self, security_id, lid):
        time.sleep(1)
        self.do_get_job_detail(security_id, lid)

    def do_get_job_detail(self, security_id, lid):
        params = {
            "securityId": security_id,
            "lid": lid,
        }
        cookies = self.context.cookies()
        response = self.session.get(BossPo.job_detail_url, headers=self.last_headers, params=params, cookies={cookie['name']: cookie['value'] for cookie in cookies})
        job_d = response.json()
        self.check_job_want(job_d)

    def get_available_jobs(self, tag):
        self.get_job_list(tag)

    def do_tik_boss(self, security_id, lid, job_id):
        params = {
            "securityId": security_id,
            "lid": lid,
            "jobId": job_id,
        }
        cookies = self.context.cookies()
        headers = copy.deepcopy(self.last_headers)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = self.session.post(BossPo.job_detail_url, headers=self.last_headers, params=params, cookies={cookie['name']: cookie['value'] for cookie in cookies})
        response = response.json()
        assert response["code"] == 0, f"{BossPo.job_detail_url}?securityId={security_id}&lid={lid}"

    def check_job_want(self, job_d):
        job_info = job_d["zpData"]["jobInfo"]
        lid = job_d["zpData"]["lid"]
        security_id = job_d["zpData"]["securityId"]
        job_name = job_info["jobName"]
        location_name = job_info["locationName"]
        post_description = job_info["postDescription"]
        boss_info = job_d["zpData"]["bossInfo"]
        active_time_desc = boss_info["activeTimeDesc"]
        encrypt_id = job_info["encryptId"]
        self.record_status.add(active_time_desc)
        if "测试" in job_name:
            if "上海" in location_name:
                passed_list = [
                    "银行",
                    "金融",
                    "外包",
                    "保险"
                ]
                for v in passed_list:
                    if v in post_description:
                        return

                if active_time_desc in ["3日内活跃", "刚刚活跃"]:
                    p = f"{BossPo.job_detail_url}?securityId={security_id}&lid={lid}"
                    self.result.append(p)
                    self.do_tik_boss(security_id, lid, encrypt_id)


def _main():
    p = PickJob()
    p.main()
    print("\n".join(p.result))


_main()