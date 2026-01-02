import os
import sys
import datetime
import arrow
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kurly import clusters

# 🎯 한국 공휴일 목록 (YYYY-MM-DD 형식)
HOLIDAYS = {
    "2026-02-16",  # 설 연휴
    "2026-03-02",  # 대체공휴일
    "2026-05-04",  # 다음날 어린이날이라 없을 듯
    "2026-05-25",  # 대체공휴일
    "2026-08-17",  # 대체공휴일
    "2026-09-24",  # 추석 연휴
    "2026-09-25",  # 추석
    "2026-10-05",  # 대체공휴일
}

# 📆 오늘 날짜 가져오기
today = datetime.date.today().strftime("%Y-%m-%d")

# 🚫 오늘이 공휴일이면 실행하지 않고 종료
if today in HOLIDAYS:
    print(f"📢 오늘({today})은 공휴일이므로 실행하지 않습니다.")
    sys.exit(0)

# 환경 변수에서 Slack 토큰 로드
load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def send_slack_message(message, channel):
    try:
        client = WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"⚠️ Error sending message to {channel} : {e}")

def main():
    for cluster in clusters:
        # 메시지 제목 설정
        header = f"*[공지｜신규입사자 사물함 배정 안]*\n\n\n"

        notice_msg = (
            f"1. *중요도* : 하\n"
            f"2. *대상* : 평택 클러스터 신규 입사자\n"
            f"3. *주요 내용*\n\n"
            f"\n"
            f"안녕하세요? 우리 클러스터 신규 입사자 여러분!\n"
            f"*사물함 배정* 되어 안내 드리오니 이용에 참고 부탁드립니다. 😊\n\n"
            f"\n"
            f":ck11: *<https://docs.google.com/spreadsheets/d/1bS8lkrROJI9X0E2NaC8Z9ha9XXYBihwwOT5UzITxFF8/edit?usp=sharing|사물함 배정 및 장소>* 는 *6층* 에 있습니다.\n"
            f":ck11: 사물함 배정 후 *자물쇠는 본인 지참* 부탁드립니다.\n"
            f":ck11: 사물함 내부는 *CCTV 미 설치 구역* 으로 자물쇠를 꼭 이용 바랍니다.\n"
            f":ck11: *배정 받은 사물함 외 사용 불가* 하오니 꼭 배정받은 사물함을 사용 바랍니다.\n"
            f":ck11: 사물함 배정은 순차적으로 진행 되며, *임의 변경* 은 불가 합니다.\n\n"
            f"\n"
            f"*:slack: 문의사항 : 인사총무팀 총무/시설 담당자*\n\n"
            f"감사합니다.\n"
        )
 
# 메시지 본문
        body = header + notice_msg

        # 슬랙 채널에 전송
        send_slack_message(body, cluster.channel)

if __name__ == "__main__":
    main()
