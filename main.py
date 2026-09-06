
import streamlit as st
import os
import datetime
from PIL import Image
import matplotlib.pyplot as plt
import json

# 페이지 기본 설정
st.set_page_config(page_title="이리고등학교 학생 지원 앱", page_icon="🏫", layout="wide")

# =========================================================
# [100% 완벽 다국어(i18n) 언어팩 정의 - 기본값: KO]
# =========================================================
LANG_PACK = {
    "한국어": {
        "title": "🏫 이리고등학교 학생 지원 앱",
        "caption": "학생주도 프로젝트 봉사활동 - 간편 웹 애플리케이션",
        "sidebar_lang": "🌐 Language / 언어 선택",
        "select_lang_lbl": "언어를 선택하세요 (Select Language)",
        "tabs": ["📍 길안내", "🎉 이벤트", "📅 캘린더", "🌐 인터넷 안내", "🏃 건강관리", "📊 성적 분석", "🔗 웹사이트 연결"],
        
        # 탭 1: 길안내
        "tab1_header": "📍 이리고등학교 최단거리 길안내",
        "tab1_info": "출발지와 목적지를 선택하면 건물 위치에 맞춰 정확하게 경로와 핀을 표시합니다.",
        "start_loc": "출발지 선택",
        "end_loc": "목적지 선택",
        "search_btn": "🚀 최단 경로 및 지도 확인",
        "same_loc_warn": "출발지와 목적지가 같습니다. 다른 장소를 선택해 주세요!",
        "time_metric": "⏱️ 예상 최단 소요 시간",
        "time_sec": "{sec}초",
        "time_min_sec": "{min}분 {sec}초",
        "map_header": "🗺️ 최단 경로 지도 시각화",
        "start_pin": "출발",
        "end_pin": "도착",

        # 탭 2: 동아리
        "tab2_header": "🎉 교내 소식 & 동아리 게시판",
        "tab2_info": "공식 홈페이지 공지사항을 확인하고, 교내 동아리 소식을 등록·수정·삭제 관리하세요.",
        "school_btn": "🏫 이리고등학교 홈페이지 바로가기",
        "school_btn_sub": "학교 공식 웹사이트 및 학사일정 바로가기입니다.",
        "club_header": "🥊 이리고등학교 동아리 소식 게시판",
        "select_club": "🔍 동아리를 선택하세요:",
        "write_news": "✍️ 새 소식 작성하기",
        "input_title": "제목",
        "input_content": "내용",
        "register_btn": "소식 등록",
        "news_list": "📋 등록된 소식 목록 (수정 & 삭제)",
        "no_news": "아직 등록된 소식이 없습니다.",
        "toast_reg": "등록되었습니다!",
        "toast_warn": "제목과 내용을 모두 입력해 주세요.",
        "btn_edit": "✏️ 수정",
        "btn_del": "🗑️ 삭제",
        "btn_save": "저장",
        "edit_title": "제목 수정",
        "edit_content": "내용 수정",
        "toast_edit": "수정되었습니다!",
        "toast_del": "삭제되었습니다.",

        # 탭 3: 캘린더
        "tab3_header": "📅 스마트 학사 & 개인 캘린더 (실시간 알람)",
        "tab3_info": "날짜와 시간을 지정해 일정을 등록하세요. 설정된 시간이 되면 화면 및 소리 알람이 실행됩니다.",
        "cur_time": "⏱️ 현재 시간:",
        "alarm_alert": "🔔 [시간 알람!] 지금은 {title} 시간입니다! ({memo})",
        "add_cal_header": "➕ 일정 등록 및 알람 설정",
        "select_date": "날짜 선택",
        "select_time": "시간 선택 (알람 울림 시점)",
        "event_title": "일정 제목",
        "event_memo": "메모/장소",
        "reg_cal_btn": "📅 일정 등록 & 알람 예약",
        "cal_list_header": "📋 등록된 일정 & 알람 목록",
        "no_cal": "등록된 일정이 없습니다.",
        "toast_cal_reg": "일정이 등록되었습니다!",
        "toast_cal_del": "일정이 삭제되었습니다.",
        "cal_memo_lbl": "메모/장소:",
        "input_title_req": "제목을 입력해 주세요.",

        # 탭 4: Wi-Fi
        "tab4_header": "🌐 학교 인터넷 & Wi-Fi 접속 안내",
        "tab4_info": "학교 교내 Wi-Fi 네트워크 접속 정보 및 공유용 탭입니다.",
        "tab4_warn": "ℹ️ 상세 Wi-Fi 연결 가이드 및 보안 설정 정보는 업데이트 준비 중입니다.",

        # 탭 5: PAPS
        "tab5_header": "🏃 PAPS 학생건강체력평가 5대 영역 종합 분석",
        "tab5_info": "교육부 PAPS 공식 5개 영역을 입력하면 종합 등급 산출 및 익산/전국 평균 데이터와 비교해 드립니다.",
        "neis_btn": "🔗 교육부 나이스(NEIS) 학생 건강검진 및 PAPS 정보 진단 바로가기",
        "paps_portal": "🌐 참고 포털",
        "paps_input": "📊 PAPS 5대 필수 평가 영역 측정값 입력",
        "gender": "성별 선택",
        "gender_m": "남학생 👦",
        "gender_f": "여학생 👧",
        "grade": "학년 선택",
        "paps_g1": "1학년", "paps_g2": "2학년", "paps_g3": "3학년",
        "paps_sec1": "1️⃣ 비만도 (체질량지수 BMI)",
        "paps_height": "신장 (cm)",
        "paps_weight": "체중 (kg)",
        "paps_sec2": "2️⃣ 심폐지구력",
        "paps_shuttle": "왕복오래달리기 (회)",
        "paps_sec3": "3️⃣ 유연성",
        "paps_flex": "앉아엎드려뻗기 (cm)",
        "paps_sec4": "4️⃣ 근력/근지구력",
        "paps_grip": "악력 측정값 (kg)",
        "paps_sec5": "5️⃣ 순발력",
        "paps_jump": "제자리멀리뛰기 (cm)",
        "paps_btn": "🔍 PAPS 5대 영역 종합 진단 및 익산/전국 데이터 비교 실행",
        "paps_report_head": "📈 PAPS 종합 진단 보고서",
        "paps_res_title": "💡 종합 진단 결과",
        "paps_res_cardio": "🏃 지구력 / 유연성",
        "paps_res_mus": "🏋️ 근력 / 순발력 / BMI",
        "paps_table_title": "📑 나의 측정값 vs 익산시 / 전국 평균 비교표",
        "paps_col_domain": "평가 영역",
        "paps_col_my": "나의 측정값",
        "paps_col_grade": "PAPS 등급",
        "paps_col_iksan": "익산시 평균",
        "paps_col_nat": "전국 평균",
        "paps_d1": "1. 비만도 (BMI)", "paps_d2": "2. 심폐지구력", "paps_d3": "3. 유연성", "paps_d4": "4. 근력 (악력)", "paps_d5": "5. 순발력",
        "g_overall_1": "🏆 종합 1등급", "g_overall_2": "🥇 종합 2등급", "g_overall_3": "🥈 종합 3등급", "g_overall_4": "🥉 종합 4등급", "g_overall_5": "⚠️ 종합 5등급",
        "g_1": "1등급", "g_2": "2등급", "g_3": "3등급", "g_4": "4등급", "g_5": "5등급",
        "bmi_1": "1등급 (정상)", "bmi_2": "2등급 (과체중)", "bmi_3": "3등급 (저체중)", "bmi_4": "4등급 (비만)",
        "unit_cnt": "회",

        # 탭 6: 링크
        "tab6_header": "🔗 주요 웹사이트 & 포털 하이퍼링크",
        "grade_tab_header": "📊 성적 분석 · 2022 개정 교육과정",
        "grade_tab_info": "2022 개정 교육과정 기준 내신 5등급제, 2028학년도 수능 9등급제, 주요 과목 설명을 한곳에서 확인합니다.",
        "school_grade_header": "🏫 내신 5등급제 계산기",
        "school_grade_info": "석차와 수강자 수를 입력하면 5등급 상대평가 구간을 기준으로 예상 석차등급을 계산합니다.",
        "rank_input": "내 석차",
        "student_count": "수강자 수",
        "school_grade_result": "예상 내신 석차등급",
        "school_grade_note": "1등급 10% · 2등급 24% · 3등급 32% · 4등급 24% · 5등급 10%의 누적 구간을 사용합니다.",
        "csat_header": "📝 수능 9등급제 계산기",
        "csat_info": "2028학년도 통합형 수능의 상대평가/절대평가 영역을 구분해 예상 등급을 확인합니다.",
        "csat_area": "수능 영역",
        "csat_percentile": "백분위 입력",
        "csat_score": "원점수 입력",
        "csat_result": "예상 수능 등급",
        "csat_relative": "상대평가: 국어·수학·탐구",
        "csat_absolute": "절대평가: 영어·한국사",
        "course_header": "📚 2022 개정 교육과정 과목 설명",
        "course_select": "과목을 선택하세요",
        "course_type": "교과 영역",
        "course_desc": "과목 설명",
        
        "tab6_info": "학교생활, 학습, 포털 검색 등에 필요한 사이트 링크 탭입니다.",
        "portal_head": "🌐 포털 사이트",
        "edu_head": "📚 교육 및 학습 포털",
        "link_caption": "📌 필요한 웹사이트 링크는 계속해서 업데이트됩니다."
    },
    "English": {
        "title": "🏫 Iri High School Student Support App",
        "caption": "Student-Led Project Volunteer Work - Simple Web Application",
        "sidebar_lang": "🌐 Select Language",
        "select_lang_lbl": "Select Language",
        "tabs": ["📍 Directions", "🎉 Events", "📅 Calendar", "🌐 Wi-Fi Guide", "🏃 Health Care", "📊 Grade Analysis", "🔗 Web Links"],
        
        "tab1_header": "📍 Shortest Route Guidance",
        "tab1_info": "Select departure and destination to view exact routes and pins on the map.",
        "start_loc": "Departure",
        "end_loc": "Destination",
        "search_btn": "🚀 Find Shortest Route",
        "same_loc_warn": "Departure and destination are identical. Please choose different locations!",
        "time_metric": "⏱️ Estimated Time",
        "time_sec": "{sec} sec",
        "time_min_sec": "{min} min {sec} sec",
        "map_header": "🗺️ Shortest Route Map",
        "start_pin": "START",
        "end_pin": "END",

        "tab2_header": "🎉 School News & Club Board",
        "tab2_info": "Check official announcements and manage club news.",
        "school_btn": "🏫 Iri High School Official Website",
        "school_btn_sub": "Direct link to official school website and academic calendar.",
        "club_header": "🥊 Club Bulletin Board",
        "select_club": "🔍 Select Club:",
        "write_news": "✍️ Post New Announcement",
        "input_title": "Title",
        "input_content": "Content",
        "register_btn": "Post News",
        "news_list": "📋 Registered Posts (Edit / Delete)",
        "no_news": "No posts registered yet.",
        "toast_reg": "Successfully posted!",
        "toast_warn": "Please fill in both title and content.",
        "btn_edit": "✏️ Edit",
        "btn_del": "🗑️ Delete",
        "btn_save": "Save",
        "edit_title": "Edit Title",
        "edit_content": "Edit Content",
        "toast_edit": "Successfully updated!",
        "toast_del": "Successfully deleted.",

        "tab3_header": "📅 Smart Calendar & Real-Time Alarm",
        "tab3_info": "Set dates and times to schedule events. Real-time notifications trigger at scheduled times.",
        "cur_time": "⏱️ Current Time:",
        "alarm_alert": "🔔 [Alarm!] Time for {title}! ({memo})",
        "add_cal_header": "➕ Add Event & Set Alarm",
        "select_date": "Select Date",
        "select_time": "Select Time",
        "event_title": "Event Title",
        "event_memo": "Memo / Location",
        "reg_cal_btn": "📅 Register Event",
        "cal_list_header": "📋 Registered Events & Alarms",
        "no_cal": "No events registered.",
        "toast_cal_reg": "Event registered!",
        "toast_cal_del": "Event deleted.",
        "cal_memo_lbl": "Memo/Location:",
        "input_title_req": "Please enter a title.",

        "tab4_header": "🌐 School Wi-Fi Guide",
        "tab4_info": "Information tab for school Wi-Fi network.",
        "tab4_warn": "ℹ️ Detailed Wi-Fi user guide and security settings are being updated.",

        "tab5_header": "🏃 PAPS Physical Fitness Comprehensive Analysis",
        "tab5_info": "Input 5 PAPS core parameters to evaluate overall grade and compare with Iksan/National averages.",
        "neis_btn": "🔗 Ministry of Education NEIS Health Assessment Portal",
        "paps_portal": "🌐 Reference Portal",
        "paps_input": "📊 PAPS Assessment Input",
        "gender": "Select Gender",
        "gender_m": "Male 👦",
        "gender_f": "Female 👧",
        "grade": "Select Grade",
        "paps_g1": "Grade 1", "paps_g2": "Grade 2", "paps_g3": "Grade 3",
        "paps_sec1": "1️⃣ Obesity Level (BMI)",
        "paps_height": "Height (cm)",
        "paps_weight": "Weight (kg)",
        "paps_sec2": "2️⃣ Cardiorespiratory Endurance",
        "paps_shuttle": "Shuttle Run (Reps)",
        "paps_sec3": "3️⃣ Flexibility",
        "paps_flex": "Sit and Reach (cm)",
        "paps_sec4": "4️⃣ Muscle Strength",
        "paps_grip": "Grip Strength (kg)",
        "paps_sec5": "5️⃣ Agility",
        "paps_jump": "Standing Long Jump (cm)",
        "paps_btn": "🔍 Run PAPS Diagnosis & Comparison",
        "paps_report_head": "📈 PAPS Diagnostic Report",
        "paps_res_title": "💡 Overall Diagnosis Result",
        "paps_res_cardio": "🏃 Endurance / Flexibility",
        "paps_res_mus": "🏋️ Strength / Agility / BMI",
        "paps_table_title": "📑 My Record vs Iksan / National Average",
        "paps_col_domain": "Domain",
        "paps_col_my": "My Record",
        "paps_col_grade": "PAPS Grade",
        "paps_col_iksan": "Iksan Avg",
        "paps_col_nat": "National Avg",
        "paps_d1": "1. BMI", "paps_d2": "2. Cardiorespiratory", "paps_d3": "3. Flexibility", "paps_d4": "4. Grip Strength", "paps_d5": "5. Long Jump",
        "g_overall_1": "🏆 Overall Grade 1", "g_overall_2": "🥇 Overall Grade 2", "g_overall_3": "🥈 Overall Grade 3", "g_overall_4": "🥉 Overall Grade 4", "g_overall_5": "⚠️ Overall Grade 5",
        "g_1": "Grade 1", "g_2": "Grade 2", "g_3": "Grade 3", "g_4": "Grade 4", "g_5": "Grade 5",
        "bmi_1": "Grade 1 (Normal)", "bmi_2": "Grade 2 (Overweight)", "bmi_3": "Grade 3 (Underweight)", "bmi_4": "Grade 4 (Obese)",
        "unit_cnt": "reps",

        "tab6_header": "🔗 Web Links & Portals",
        "grade_tab_header": "📊 Grade Analysis · 2022 Revised Curriculum",
        "grade_tab_info": "Check the 5-level school grading system, 9-level CSAT grading system, and major course descriptions.",
        "school_grade_header": "🏫 5-Level School Grade Calculator",
        "school_grade_info": "Enter rank and class size to estimate the relative grade.",
        "rank_input": "Rank", "student_count": "Number of students", "school_grade_result": "Estimated School Grade",
        "school_grade_note": "Cumulative bands: Grade 1 10% · Grade 2 34% · Grade 3 66% · Grade 4 90% · Grade 5 100%.",
        "csat_header": "📝 9-Level CSAT Grade Calculator",
        "csat_info": "Check estimated CSAT grades by distinguishing relative- and absolute-evaluation areas.",
        "csat_area": "CSAT Area", "csat_percentile": "Percentile", "csat_score": "Raw Score", "csat_result": "Estimated CSAT Grade",
        "csat_relative": "Relative: Korean · Mathematics · Inquiry", "csat_absolute": "Absolute: English · Korean History",
                "course_header": "📚 2022 Revised Curriculum Course Guide", "course_select": "Select a course", "course_type": "Subject Area", "course_desc": "Description",

        "tab6_info": "Links required for school life, learning, and web search.",
        "portal_head": "🌐 Search Portals",
        "edu_head": "📚 Educational Portals",
        "link_caption": "📌 Links will be updated continuously."
    },
    "日本語": {
        "title": "🏫 里里高等学校 学生支援アプリ",
        "caption": "生徒主導プロジェクトボランティア活動 - 簡易Webアプリケーション",
        "sidebar_lang": "🌐 言語選択 (Language)",
        "select_lang_lbl": "言語を選択してください",
        "tabs": ["📍 ルート案内", "🎉 イベント", "📅 カレンダー", "🌐 Wi-Fi案内", "🏃 健康管理", "📊 成績分析", "🔗 リンク集"],
        
        "tab1_header": "📍 最短ルート案内",
        "tab1_info": "出発地と目的地を選択すると、正確なルートとピンが表示されます。",
        "start_loc": "出発地選択",
        "end_loc": "目的地選択",
        "search_btn": "🚀 最短ルートとマップを確認",
        "same_loc_warn": "出発地と目的地が同じです。異なる場所を選択してください！",
        "time_metric": "⏱️ 予想所要時間",
        "time_sec": "{sec}秒",
        "time_min_sec": "{min}分 {sec}秒",
        "map_header": "🗺️ 最短ルートマップ",
        "start_pin": "出発",
        "end_pin": "到着",

        "tab2_header": "🎉 校내ニュース & 部活動掲示板",
        "tab2_info": "公式お知らせを確認し、部活動ニュースを投稿・管理できます。",
        "school_btn": "🏫 里里高等学校 公式サイト",
        "school_btn_sub": "学校公式サイトおよび年間行事予定へ移動します。",
        "club_header": "🥊 部活動ニュース掲示板",
        "select_club": "🔍 部活動を選択:",
        "write_news": "✍️ 新規投稿",
        "input_title": "タイトル",
        "input_content": "内容",
        "register_btn": "投稿する",
        "news_list": "📋 投稿一覧 (編集・削除)",
        "no_news": "まだ投稿がありません。",
        "toast_reg": "投稿されました！",
        "toast_warn": "タイトルと内容を両方入力してください。",
        "btn_edit": "✏️ 編集",
        "btn_del": "🗑️ 削除",
        "btn_save": "保存",
        "edit_title": "タイトル編集",
        "edit_content": "内容編集",
        "toast_edit": "修正されました！",
        "toast_del": "削除されました。",

        "tab3_header": "📅 カレンダー & リアルタイムアラーム",
        "tab3_info": "日時を指定してスケジューリングすると、設定時間に通知が実行されます。",
        "cur_time": "⏱️ 現在時刻:",
        "alarm_alert": "🔔 [アラーム] {title} の時間です！ ({memo})",
        "add_cal_header": "➕ スケジュール追加",
        "select_date": "日付選択",
        "select_time": "時間選択",
        "event_title": "タイトル",
        "event_memo": "メモ/場所",
        "reg_cal_btn": "📅 スケジュール登録",
        "cal_list_header": "📋 登録済みスケジュール",
        "no_cal": "登録されたスケジュールはありません。",
        "toast_cal_reg": "登録されました！",
        "toast_cal_del": "削除されました。",
        "cal_memo_lbl": "メモ/場所:",
        "input_title_req": "タイトルを入力してください。",

        "tab4_header": "🌐 校内Wi-Fi利用案内",
        "tab4_info": "校内Wi-Fiネットワークの接続情報タブです。",
        "tab4_warn": "ℹ️ Wi-Fi詳細ガイドは更新準備中です。",

        "tab5_header": "🏃 PAPS 体力評価総合分析",
        "tab5_info": "PAPSの5大項目を入力すると、等級算出および益山/全国平均と比較します。",
        "neis_btn": "🔗 教育部 NEIS 健康診断ポータルへ",
        "paps_portal": "🌐 参考ポータル",
        "paps_input": "📊 PAPS 評価項目入力",
        "gender": "性別選択",
        "gender_m": "男子生徒 👦",
        "gender_f": "女子生徒 👧",
        "grade": "学年選択",
        "paps_g1": "1年生", "paps_g2": "2年生", "paps_g3": "3年生",
        "paps_sec1": "1️⃣ 肥満度 (BMI)",
        "paps_height": "身長 (cm)",
        "paps_weight": "体重 (kg)",
        "paps_sec2": "2️⃣ 心肺持久力",
        "paps_shuttle": "シャトルラン (回)",
        "paps_sec3": "3️⃣ 柔軟性",
        "paps_flex": "長座体前屈 (cm)",
        "paps_sec4": "4️⃣ 筋力",
        "paps_grip": "握力 (kg)",
        "paps_sec5": "5️⃣ 瞬発力",
        "paps_jump": "立ち幅跳び (cm)",
        "paps_btn": "🔍 PAPS 総合診断および比較実行",
        "paps_report_head": "📈 PAPS 総合診断レポート",
        "paps_res_title": "💡 総合診断結果",
        "paps_res_cardio": "🏃 持久力 / 柔軟性",
        "paps_res_mus": "🏋️ 筋力 / 瞬発力 / BMI",
        "paps_table_title": "📑 自分の記録 vs 益山市 / 全国平均比較表",
        "paps_col_domain": "評価項目",
        "paps_col_my": "自分の記録",
        "paps_col_grade": "PAPS等級",
        "paps_col_iksan": "益山市平均",
        "paps_col_nat": "全国平均",
        "paps_d1": "1. BMI", "paps_d2": "2. 心肺持久力", "paps_d3": "3. 柔軟性", "paps_d4": "4. 握力", "paps_d5": "5. 立ち幅跳び",
        "g_overall_1": "🏆 総合1等級", "g_overall_2": "🥇 総合2等級", "g_overall_3": "🥈 総合3等級", "g_overall_4": "🥉 総合4等級", "g_overall_5": "⚠️ 総合5等級",
        "g_1": "1等級", "g_2": "2等級", "g_3": "3等級", "g_4": "4等級", "g_5": "5等級",
        "bmi_1": "1等級 (正常)", "bmi_2": "2等級 (過体重)", "bmi_3": "3等級 (저체중)", "bmi_4": "4等級 (肥満)",
        "unit_cnt": "回",

        "tab6_header": "🔗 主要ウェブサイト & ポータル",
        "grade_tab_header": "📊 成績分析 · 2022改訂教育課程",
        "grade_tab_info": "5段階の校内成績、9段階の大学修学能力試験、主要科目の説明を確認します。",
        "school_grade_header": "🏫 校内成績5段階計算", "school_grade_info": "順位と受講者数から予想等級を計算します。",
        "rank_input": "順位", "student_count": "受講者数", "school_grade_result": "予想校内等級",
        "school_grade_note": "累積区間: 1等級10% · 2等級34% · 3等級66% · 4等級90% · 5等級100%。",
        "csat_header": "📝 大学修学能力試験9段階計算", "csat_info": "相対評価と絶対評価の領域を区別して予想等級を確認します。",
        "csat_area": "試験領域", "csat_percentile": "パーセンタイル", "csat_score": "素点", "csat_result": "予想等級",
        "csat_relative": "相対評価: 国語・数学・探究", "csat_absolute": "絶対評価: 英語・韓国史",
        "course_header": "📚 2022改訂教育課程 科目説明", "course_select": "科目を選択", "course_type": "教科領域", "course_desc": "科目説明",

        "tab6_info": "学校生活や学習に必要なサイトリンク集です。",
        "portal_head": "🌐 検索ポータル",
        "edu_head": "📚 教育ポータル",
        "link_caption": "📌 リンク集は随時更新されます。"
    },
    "中文": {
        "title": "🏫 益里高中 学生支持应用",
        "caption": "学生主导项目志愿服务 - 简易Web应用程序",
        "sidebar_lang": "🌐 选择语言 (Language)",
        "select_lang_lbl": "请选择语言",
        "tabs": ["📍 导航", "🎉 校园活动", "📅 日历", "🌐 网络指南", "🏃 健康管理", "📊 成绩分析", "🔗 网站链接"],
        
        "tab1_header": "📍 最短路线导航",
        "tab1_info": "选择出发地和目的地，将精准显示路线和图钉标记。",
        "start_loc": "选择出发地",
        "end_loc": "选择目的地",
        "search_btn": "🚀 查询 shortest 路线与地图",
        "same_loc_warn": "出发地与目的地相同，请选择不同地点！",
        "time_metric": "⏱️ 预计所需时间",
        "time_sec": "{sec}秒",
        "time_min_sec": "{min}分 {sec}秒",
        "map_header": "🗺️ 最短路线地图",
        "start_pin": "起点",
        "end_pin": "终点",

        "tab2_header": "🎉 校园动态 & 社团告示板",
        "tab2_info": "查看官方公告，并管理社团的新闻发布与编辑。",
        "school_btn": "🏫 前往益里高中官网",
        "school_btn_sub": "前往学校官方网站与校历。",
        "club_header": "🥊 益里高中社团告示板",
        "select_club": "🔍 选择社团:",
        "write_news": "✍️ 发布新动态",
        "input_title": "标题",
        "input_content": "内容",
        "register_btn": "发布动态",
        "news_list": "📋 已发布动态列表 (修改/删除)",
        "no_news": "暂无发布动态。",
        "toast_reg": "发布成功！",
        "toast_warn": "请填写标题和内容。",
        "btn_edit": "✏️ 编辑",
        "btn_del": "🗑️ 删除",
        "btn_save": "保存",
        "edit_title": "编辑标题",
        "edit_content": "编辑内容",
        "toast_edit": "修改成功！",
        "toast_del": "删除成功。",

        "tab3_header": "📅 智能日程表 & 实时提醒",
        "tab3_info": "指定日期和时间添加日程，设置时间到达时将触发提醒。",
        "cur_time": "⏱️ 当前时间:",
        "alarm_alert": "🔔 [时间提醒!] 现在是 {title} 时间！ ({memo})",
        "add_cal_header": "➕ 添加日程与提醒",
        "select_date": "选择日期",
        "select_time": "选择时间",
        "event_title": "日程标题",
        "event_memo": "备注/地点",
        "reg_cal_btn": "📅 预定日程",
        "cal_list_header": "📋 已登记日程列表",
        "no_cal": "暂无已登记日程。",
        "toast_cal_reg": "日程已登记！",
        "toast_cal_del": "日程已删除。",
        "cal_memo_lbl": "备注/地点:",
        "input_title_req": "请输入标题。",

        "tab4_header": "🌐 校园网络与Wi-Fi指南",
        "tab4_info": "校园Wi-Fi网络连接信息与共享指南。",
        "tab4_warn": "ℹ️ 详细Wi-Fi连接指南正准备更新中。",

        "tab5_header": "🏃 PAPS 体能评估综合分析",
        "tab5_info": "输入PAPS 5大核心指标，计算综合等级并与益山市/全国平均水平对比。",
        "neis_btn": "🔗 前往教育部 NEIS 学生健康检查 Portal",
        "paps_portal": "🌐 参考 Portal",
        "paps_input": "📊 PAPS 5大指标测量数据输入",
        "gender": "选择性别",
        "gender_m": "男生 👦",
        "gender_f": "女生 👧",
        "grade": "选择年级",
        "paps_g1": "高一", "paps_g2": "高二", "paps_g3": "高三",
        "paps_sec1": "1️⃣ 肥胖度 (BMI)",
        "paps_height": "身高 (cm)",
        "paps_weight": "体重 (kg)",
        "paps_sec2": "2️⃣ 心肺耐力",
        "paps_shuttle": "往返跑 (次)",
        "paps_sec3": "3️⃣ 柔韧性",
        "paps_flex": "坐位体前屈 (cm)",
        "paps_sec4": "4️⃣ 肌肉力量",
        "paps_grip": "握力 (kg)",
        "paps_sec5": "5️⃣ 爆发力",
        "paps_jump": "立定跳远 (cm)",
        "paps_btn": "🔍 执行 PAPS 综合诊断与数据对比",
        "paps_report_head": "📈 PAPS 综合诊断报告",
        "paps_res_title": "💡 综合诊断结果",
        "paps_res_cardio": "🏃 耐力 / 柔韧性",
        "paps_res_mus": "🏋️ 力量 / 爆发力 / BMI",
        "paps_table_title": "📑 我的测量值 vs 益山市 / 全国平均对比",
        "paps_col_domain": "评估项目",
        "paps_col_my": "我的测量值",
        "paps_col_grade": "PAPS 等级",
        "paps_col_iksan": "益山市平均",
        "paps_col_nat": "全国平均",
        "paps_d1": "1. BMI", "paps_d2": "2. 心肺耐力", "paps_d3": "3. 柔韧性", "paps_d4": "4. 握力", "paps_d5": "5. 立定跳远",
        "g_overall_1": "🏆 综合 1级", "g_overall_2": "🥇 综合 2级", "g_overall_3": "🥈 综合 3级", "g_overall_4": "🥉 综合 4级", "g_overall_5": "⚠️ 综合 5级",
        "g_1": "1级", "g_2": "2级", "g_3": "3级", "g_4": "4级", "g_5": "5级",
        "bmi_1": "1级 (正常)", "bmi_2": "2级 (超重)", "bmi_3": "3级 (偏瘦)", "bmi_4": "4级 (肥胖)",
        "unit_cnt": "次",

        "tab6_header": "🔗 主要网站与门户链接",
        "grade_tab_header": "📊 成绩分析 · 2022修订教育课程",
        "grade_tab_info": "查看校内5等级制、大学修学能力考试9等级制以及主要课程说明。",
        "school_grade_header": "🏫 校内成绩5等级计算器", "school_grade_info": "输入排名和人数后计算预计等级。",
        "rank_input": "排名", "student_count": "人数", "school_grade_result": "预计校内等级",
        "school_grade_note": "累计区间：1级10% · 2级34% · 3级66% · 4级90% · 5级100%。",
        "csat_header": "📝 大学修学能力考试9等级计算器", "csat_info": "区分相对评价和绝对评价领域，查看预计等级。",
        "csat_area": "考试领域", "csat_percentile": "百分位", "csat_score": "原始分", "csat_result": "预计等级",
        "csat_relative": "相对评价：国语·数学·探究", "csat_absolute": "绝对评价：英语·韩国史",
        "course_header": "📚 2022修订教育课程科目说明", "course_select": "选择科目", "course_type": "学科领域", "course_desc": "科目说明",

        "tab6_info": "校园生活、学习及搜索所需的主要网站链接。",
        "portal_head": "🌐 搜索引擎",
        "edu_head": "📚 教育门户",
        "link_caption": "📌 网站链接将持续更新。"
    }
}

# =========================================================
# [사이드바] 언어 기본값 한국어 설정 및 세션 연결
# =========================================================
if "lang" not in st.session_state:
    st.session_state["lang"] = "한국어"

st.sidebar.title(LANG_PACK[st.session_state["lang"]]["sidebar_lang"])
selected_lang = st.sidebar.selectbox(
    LANG_PACK[st.session_state["lang"]]["select_lang_lbl"],
    options=["한국어", "English", "日本語", "中文"],
    index=["한국어", "English", "日本語", "中文"].index(st.session_state["lang"])
)

st.session_state["lang"] = selected_lang
L = LANG_PACK[st.session_state["lang"]]

DATA_FILE = "app_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for ev in data.get("calendar_events", []):
            ev["date"] = datetime.date.fromisoformat(ev["date"])
            ev["time"] = datetime.time.fromisoformat(ev["time"])

        return data

    return {
        "club_notices": {},
        "calendar_events": []
    }

def save_data(data):
    save_data_copy = {
        "club_notices": data["club_notices"],
        "calendar_events": [
            {
                "date": ev["date"].isoformat(),
                "time": ev["time"].strftime("%H:%M"),
                "title": ev["title"],
                "memo": ev["memo"]
            }
            for ev in data["calendar_events"]
        ]
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data_copy, f, ensure_ascii=False, indent=2)

# 앱 타이틀 설정
st.title(L["title"])
st.caption(L["caption"])

# =========================================================
# [세션 상태 관리] 동아리 게시글 & 캘린더 일정 저장소
# =========================================================
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

st.session_state["club_notices"] = st.session_state["data"]["club_notices"]
st.session_state["calendar_events"] = st.session_state["data"]["calendar_events"]

# 6개 탭 구성
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(L["tabs"])

with tab1:
    st.header("📍 이리고등학교 최단거리 길안내")
    st.info("출발지와 목적지를 선택하면 건물 위치에 맞춰 정확하게 경로와 핀을 표시합니다.")
    
    location_data = {
        "교문 / 정문": {"building": "외곽", "floor": 1, "rel_coords": (0.20, 0.85), "detail": "학교 좌측 하단 정문 입구"},
        "본관 1층 (보건실 / 교장실 / 행정실)": {"building": "본관", "floor": 1, "rel_coords": (0.50, 0.50), "detail": "본관 1층 중앙 현관"},
        "본관 2층 (본교무실 / 3학년 1~4반)": {"building": "본관", "floor": 2, "rel_coords": (0.50, 0.46), "detail": "본관 2층 계단"},
        "본관 3층 (3학년 5~10반 / Wee클래스)": {"building": "본관", "floor": 3, "rel_coords": (0.50, 0.42), "detail": "본관 3층 복도"},
        "본관 4층 (교과실 / 미래학습실)": {"building": "본관", "floor": 4, "rel_coords": (0.50, 0.38), "detail": "본관 4층 최상층"},
        "후관 1층 (2학년 1~7반 / 체력단련실)": {"building": "후관", "floor": 1, "rel_coords": (0.50, 0.24), "detail": "후관 1층 중앙 출입구"},
        "후관 2층 (1학년 7~10반 / 2학년 8~10반)": {"building": "후관", "floor": 2, "rel_coords": (0.50, 0.20), "detail": "후관 2층 계단"},
        "후관 3층 (1학년 1~6반)": {"building": "후관", "floor": 3, "rel_coords": (0.50, 0.16), "detail": "후관 3층 최상층"},
        "교내 매점": {"building": "후관 옆", "floor": 1, "rel_coords": (0.25, 0.22), "detail": "후관 좌측 연결 건물"},
        "미령당 1층 (식생할관 / 급식실)": {"building": "미령당", "floor": 1, "rel_coords": (0.20, 0.50), "detail": "본관 서측 급식실"},
        "미령당 2층 (강당)": {"building": "미령당", "floor": 2, "rel_coords": (0.20, 0.45), "detail": "식생활관 상층 강당"},
        "미래관 (도서관 / 음악실 / 과학실)": {"building": "미래관", "floor": 2, "rel_coords": (0.80, 0.70), "detail": "운동장 동측 특별관"},
        "명문관 (학생자치실 / 드림실)": {"building": "명문관", "floor": 1, "rel_coords": (0.80, 0.50), "detail": "본관 동측 인접 건물"},
        "우정학사 / 미령관 (기숙사)": {"building": "기숙사", "floor": 1, "rel_coords": (0.20, 0.70), "detail": "운동장 서측 기숙사"},
        "운동장": {"building": "운동장", "floor": 1, "rel_coords": (0.50, 0.70), "detail": "학교 중앙 트랙/운동장"}
    }
    
    locations = list(location_data.keys())
    col_input, col_map = st.columns([1.1, 0.9])
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_files = ["이리고 지도.webp", "map.jpg", "map.png", "map.jpeg", "image_a0d32f.jpg"]
    
    img = None
    for fname in target_files:
        path = os.path.join(current_dir, fname)
        if os.path.exists(path):
            img = Image.open(path)
            break
        elif os.path.exists(fname):
            img = Image.open(fname)
            break

    with col_input:
        start = st.selectbox("출발지 선택", locations, index=0)
        end = st.selectbox("목적지 선택", locations, index=9)
        
        search_btn = st.button("🚀 최단 경로 및 지도 확인", type="primary")
        
        if search_btn:
            if start == end:
                st.warning("출발지와 목적지가 같습니다. 다른 장소를 선택해 주세요!")
            else:
                start_info = location_data[start]
                end_info = location_data[end]
                
                floor_diff = abs(start_info["floor"] - end_info["floor"])
                stair_time = floor_diff * 12.5
                
                if start_info["building"] == end_info["building"]:
                    base_time = 15
                elif (start_info["building"] == "본관" and end_info["building"] == "후관") or \
                     (start_info["building"] == "후관" and end_info["building"] == "본관"):
                    base_time = 30
                elif "교문" in start or "교문" in end:
                    base_time = 60
                else:
                    base_time = 45
                    
                total_seconds = int(base_time + stair_time)
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_str = f"{seconds}초" if minutes == 0 else f"{minutes}분 {seconds}초"
                
                st.success(f"📌 **[{start}]** ➔ **[{end}]** 경로 안내")
                st.metric(label="⏱️ 예상 최단 소요 시간", value=f"약 {time_str}")

    with col_map:
        st.subheader("🗺️ 최단 경로 지도 시각화")
        if img:
            img_w, img_h = img.size
            fig, ax = plt.subplots(figsize=(8, 10))
            ax.imshow(img)
            ax.axis('off')
            
            if search_btn and start != end:
                rel_p1 = location_data[start]["rel_coords"]
                rel_p2 = location_data[end]["rel_coords"]
                p1 = (rel_p1[0] * img_w, rel_p1[1] * img_h)
                p2 = (rel_p2[0] * img_w, rel_p2[1] * img_h)
                
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', linewidth=3.5, linestyle='-', zorder=3)
                ax.scatter(p1[0], p1[1], color='lime', s=350, zorder=5, edgecolors='black', label='START')
                ax.scatter(p2[0], p2[1], color='red', s=350, zorder=5, edgecolors='white', label='END')
                
                s_name = start.split(' ')[0]
                e_name = end.split(' ')[0]
                
                ax.text(p1[0], p1[1] - (img_h * 0.03), f"출발: {s_name}", fontsize=10, fontweight='bold', 
                        ha='center', va='bottom', color='black',
                        bbox=dict(boxstyle="round,pad=0.3", fc="lime", ec="black", lw=1), zorder=6)
                
                ax.text(p2[0], p2[1] + (img_h * 0.03), f"도착: {e_name}", fontsize=10, fontweight='bold', 
                        ha='center', va='top', color='white',
                        bbox=dict(boxstyle="round,pad=0.3", fc="red", ec="white", lw=1), zorder=6)
                
                ax.legend(loc='upper right', fontsize=10)
            st.pyplot(fig)
# =========================================================
# [2단계] 이리고 사이트 연동 + 동아리 게시판
# =========================================================
with tab2:
    st.header(L["tab2_header"])
    st.info(L["tab2_info"])

    school_url = "https://school.jbedu.kr/iri-h/index.do"


    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.link_button(L["school_btn"], school_url, type="primary", use_container_width=True)
    with col_btn2:
        st.caption(L["school_btn_sub"])

    st.components.v1.iframe(school_url, height=350, scrolling=True)
    st.divider()

    st.subheader(L["club_header"])

    club_list = [
        "백도어", "태권도부", "축구부", "수학콘텐츠제작반", "독서토론탐구반", 
        "시사액션", "경영탐구", "수리탐구회", "빅뱅", "헬스반", 
        "스트로크", "블럭박사", "큐리언스", "나눔플러스", "리더", 
        "족구왕", "바이오클럽", "e스포츠맨", "창작미술", "화학탐구반", 
        "나침반", "위로", "엠아식", "융합이슈연구회", "3D프린팅", 
        "영어원서완독회", "바른교육", "진로탐구독서반", "물리학탐구반", "크레이터", 
        "아고라", "매스플러스", "와이파이", "우드메이커"
    ]

    selected_club = st.selectbox(L["select_club"], club_list)

    if selected_club not in st.session_state["club_notices"]:
        st.session_state["club_notices"][selected_club] = []

    st.success(f"📌 **[{selected_club}]**")
    col_write, col_list = st.columns([1, 1.2])

    with col_write:
        st.write(f"✍️ **{L['write_news']}**")
        with st.form(key=f"add_form_{selected_club}", clear_on_submit=True):
            new_title = st.text_input(L["input_title"])
            new_content = st.text_area(L["input_content"], height=100)
            submit_btn = st.form_submit_button(L["register_btn"], type="primary", use_container_width=True)

            if submit_btn:
                if new_title and new_content:
                    st.session_state["club_notices"][selected_club].append({"title": new_title, "content": new_content})
                    save_data(st.session_state["data"])
                    st.toast(L["toast_reg"], icon="✅")
                    st.rerun()
                else:
                    st.warning(L["toast_warn"])

    with col_list:
        st.write(f"📋 **{L['news_list']}**")
        notices = st.session_state["club_notices"][selected_club]

        if not notices:
            st.info(L["no_news"])
        else:
            for idx, item in enumerate(notices):
                with st.expander(f"📌 {item['title']}", expanded=False):
                    st.write(item['content'])
                    st.divider()
                    
                    with st.popover(L["btn_edit"]):
                        edit_title = st.text_input(L["edit_title"], value=item['title'], key=f"edit_t_{selected_club}_{idx}")
                        edit_content = st.text_area(L["edit_content"], value=item['content'], key=f"edit_c_{selected_club}_{idx}")
                        if st.button(L["btn_save"], key=f"edit_btn_{selected_club}_{idx}"):
                            st.session_state["club_notices"][selected_club][idx] = {"title": edit_title, "content": edit_content}
                            save_data(st.session_state["data"])
                            st.toast(L["toast_edit"], icon="✏️")
                            st.rerun()

                    if st.button(L["btn_del"], key=f"del_btn_{selected_club}_{idx}"):
                        st.session_state["club_notices"][selected_club].pop(idx)
                        save_data(st.session_state["data"])
                        st.toast(L["toast_del"], icon="🗑️")
                        st.rerun()

# =========================================================
# [3단계] 스마트 캘린더 & 실시간 알람 시스템
# =========================================================
with tab3:
    st.header(L["tab3_header"])
    st.info(L["tab3_info"])

    now = datetime.datetime.now()
    current_date = now.date()
    current_time_str = now.strftime("%H:%M")
    
    st.write(f"{L['cur_time']} `{now.strftime('%Y-%m-%d %H:%M:%S')}`")

    for event in st.session_state["calendar_events"]:
        event_time_str = event["time"].strftime("%H:%M")
        if event["date"] == current_date and event_time_str == current_time_str:
            st.error(L["alarm_alert"].format(title=event['title'], memo=event['memo']))
            st.toast(f"⏰ {event['title']}", icon="🔔")

    col_cal1, col_cal2 = st.columns([1, 1.2])

    with col_cal1:
        st.subheader(L["add_cal_header"])
        with st.form("calendar_form", clear_on_submit=True):
            event_date = st.date_input(L["select_date"], datetime.date.today())
            event_time = st.time_input(L["select_time"], datetime.time(9, 0))
            event_title = st.text_input(L["event_title"])
            event_memo = st.text_area(L["event_memo"], height=80)
            
            cal_submit = st.form_submit_button(L["reg_cal_btn"], type="primary", use_container_width=True)
            if cal_submit:
                if event_title:
                    st.session_state["calendar_events"].append({
                        "date": event_date,
                        "time": event_time,
                        "title": event_title,
                        "memo": event_memo
                    })

                    save_data(st.session_state["data"])
                    st.toast(L["toast_cal_reg"], icon="📅")
                    st.rerun()
                else:
                    st.warning(L["input_title_req"])

    with col_cal2:
        st.subheader(L["cal_list_header"])
        if not st.session_state["calendar_events"]:
            st.info(L["no_cal"])
        else:
            sorted_events = sorted(st.session_state["calendar_events"], key=lambda x: (x["date"], x["time"]))

        for idx, ev in enumerate(sorted_events):
            ev_date = ev["date"]
        
            with st.expander(
                f"📌 [{ev_date.strftime('%m/%d')}] "
                f"{ev['time'].strftime('%H:%M')} - {ev['title']}",
                expanded=True
            ):
                st.write(f"**{L['cal_memo_lbl']}** {ev['memo']}")
        
                if st.button(L["btn_del"], key=f"del_cal_{idx}"):
                    st.session_state["calendar_events"].remove(ev)
                    save_data(st.session_state["data"])
                    st.toast(L["toast_cal_del"], icon="🗑️")
                    st.rerun()

# =========================================================
# [4단계] 학교 인터넷 & Wi-Fi 사용 안내
# =========================================================
with tab4:
    st.header(L["tab4_header"])
    st.info(L["tab4_info"])
    st.warning(L["tab4_warn"])

# =========================================================
# [5단계] PAPS 종합 건강 진단
# =========================================================
with tab5:
    st.header(L["tab5_header"])
    st.info(L["tab5_info"])

    st.subheader(L["paps_portal"])
    health_url = "https://www.neis.go.kr"
    st.link_button(L["neis_btn"], health_url, type="primary")

    st.divider()

    st.subheader(L["paps_input"])
    
    with st.form("paps_full_form"):
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            gender = st.radio(L["gender"], [L["gender_m"], L["gender_f"]], horizontal=True)
        with col_meta2:
            grade = st.selectbox(L["grade"], [L["paps_g1"], L["paps_g2"], L["paps_g3"]])

        st.markdown("---")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown(f"##### {L['paps_sec1']}")
            height_val = st.number_input(L["paps_height"], value=174.5, step=0.1, min_value=120.0, max_value=210.0)
            weight_val = st.number_input(L["paps_weight"], value=64.2, step=0.1, min_value=30.0, max_value=150.0)

            st.markdown(f"##### {L['paps_sec2']}")
            shuttle_run_val = st.number_input(L["paps_shuttle"], value=58, step=1, min_value=0)

            st.markdown(f"##### {L['paps_sec3']}")
            flexibility_val = st.number_input(L["paps_flex"], value=14.5, step=0.5)

        with col_p2:
            st.markdown(f"##### {L['paps_sec4']}")
            grip_val = st.number_input(L["paps_grip"], value=42.0, step=0.5, min_value=0.0)

            st.markdown(f"##### {L['paps_sec5']}")
            jump_val = st.number_input(L["paps_jump"], value=220, step=1, min_value=0)

        eval_btn = st.form_submit_button(L["paps_btn"], type="primary", use_container_width=True)

    if eval_btn:
        st.divider()
        st.subheader(L["paps_report_head"])

        height_m = height_val / 100
        bmi_calc = weight_val / (height_m ** 2)

        is_male = (gender == L["gender_m"])
        if is_male:
            if shuttle_run_val >= 76: r_grade, r_score = L["g_1"], 5
            elif shuttle_run_val >= 60: r_grade, r_score = L["g_2"], 4
            elif shuttle_run_val >= 44: r_grade, r_score = L["g_3"], 3
            elif shuttle_run_val >= 28: r_grade, r_score = L["g_4"], 2
            else: r_grade, r_score = L["g_5"], 1

            if flexibility_val >= 18.0: f_grade, f_score = L["g_1"], 5
            elif flexibility_val >= 12.0: f_grade, f_score = L["g_2"], 4
            elif flexibility_val >= 6.0: f_grade, f_score = L["g_3"], 3
            elif flexibility_val >= 0.0: f_grade, f_score = L["g_4"], 2
            else: f_grade, f_score = L["g_5"], 1

            if grip_val >= 48.0: g_grade, g_score = L["g_1"], 5
            elif grip_val >= 41.0: g_grade, g_score = L["g_2"], 4
            elif grip_val >= 34.0: g_grade, g_score = L["g_3"], 3
            elif grip_val >= 27.0: g_grade, g_score = L["g_4"], 2
            else: g_grade, g_score = L["g_5"], 1

            if jump_val >= 242: j_grade, j_score = L["g_1"], 5
            elif jump_val >= 222: j_grade, j_score = L["g_2"], 4
            elif jump_val >= 202: j_grade, j_score = L["g_3"], 3
            elif jump_val >= 182: j_grade, j_score = L["g_4"], 2
            else: j_grade, j_score = L["g_5"], 1

            if 18.5 <= bmi_calc <= 22.9: b_grade, b_score = L["bmi_1"], 5
            elif 23.0 <= bmi_calc <= 24.9: b_grade, b_score = L["bmi_2"], 4
            elif bmi_calc >= 25.0: b_grade, b_score = L["bmi_4"], 2
            else: b_grade, b_score = L["bmi_3"], 3

            iksan_avg = {"bmi": 21.5, "shuttle": 54, "flexibility": 13.0, "grip": 39.5, "jump": 215}
            nat_avg   = {"bmi": 21.7, "shuttle": 52, "flexibility": 12.5, "grip": 38.8, "jump": 212}

        else:
            if shuttle_run_val >= 53: r_grade, r_score = L["g_1"], 5
            elif shuttle_run_val >= 41: r_grade, r_score = L["g_2"], 4
            elif shuttle_run_val >= 29: r_grade, r_score = L["g_3"], 3
            elif shuttle_run_val >= 18: r_grade, r_score = L["g_4"], 2
            else: r_grade, r_score = L["g_5"], 1

            if flexibility_val >= 21.0: f_grade, f_score = L["g_1"], 5
            elif flexibility_val >= 15.0: f_grade, f_score = L["g_2"], 4
            elif flexibility_val >= 9.0: f_grade, f_score = L["g_3"], 3
            elif flexibility_val >= 3.0: f_grade, f_score = L["g_4"], 2
            else: f_grade, f_score = L["g_5"], 1

            if grip_val >= 29.0: g_grade, g_score = L["g_1"], 5
            elif grip_val >= 25.0: g_grade, g_score = L["g_2"], 4
            elif grip_val >= 21.0: g_grade, g_score = L["g_3"], 3
            elif grip_val >= 17.0: g_grade, g_score = L["g_4"], 2
            else: g_grade, g_score = L["g_5"], 1

            if jump_val >= 182: j_grade, j_score = L["g_1"], 5
            elif jump_val >= 165: j_grade, j_score = L["g_2"], 4
            elif jump_val >= 148: j_grade, j_score = L["g_3"], 3
            elif jump_val >= 131: j_grade, j_score = L["g_4"], 2
            else: j_grade, j_score = L["g_5"], 1

            if 18.5 <= bmi_calc <= 22.9: b_grade, b_score = L["bmi_1"], 5
            elif 23.0 <= bmi_calc <= 24.9: b_grade, b_score = L["bmi_2"], 4
            elif bmi_calc >= 25.0: b_grade, b_score = L["bmi_4"], 2
            else: b_grade, b_score = L["bmi_3"], 3

            iksan_avg = {"bmi": 21.3, "shuttle": 38, "flexibility": 15.5, "grip": 23.2, "jump": 152}
            nat_avg   = {"bmi": 21.5, "shuttle": 36, "flexibility": 15.0, "grip": 22.8, "jump": 150}

        total_paps_score = r_score + f_score + g_score + j_score + b_score
        if total_paps_score >= 21: overall_paps = L["g_overall_1"]
        elif total_paps_score >= 16: overall_paps = L["g_overall_2"]
        elif total_paps_score >= 11: overall_paps = L["g_overall_3"]
        elif total_paps_score >= 6: overall_paps = L["g_overall_4"]
        else: overall_paps = L["g_overall_5"]

        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric(L["paps_res_title"], overall_paps)
        col_res2.metric(L["paps_res_cardio"], f"{r_grade} / {f_grade}")
        col_res3.metric(L["paps_res_mus"], f"{g_grade} / {j_grade} / {b_grade}")

        st.divider()

        st.markdown(f"#### {L['paps_table_title']}")

        comp_data = {
            L["paps_col_domain"]: [L["paps_d1"], L["paps_d2"], L["paps_d3"], L["paps_d4"], L["paps_d5"]],
            L["paps_col_my"]: [f"{bmi_calc:.2f}", f"{shuttle_run_val}{L['unit_cnt']}", f"{flexibility_val:.1f}cm", f"{grip_val:.1f}kg", f"{jump_val}cm"],
            L["paps_col_grade"]: [b_grade, r_grade, f_grade, g_grade, j_grade],
            L["paps_col_iksan"]: [f"{iksan_avg['bmi']}", f"{iksan_avg['shuttle']}{L['unit_cnt']}", f"{iksan_avg['flexibility']}cm", f"{iksan_avg['grip']}kg", f"{iksan_avg['jump']}cm"],
            L["paps_col_nat"]: [f"{nat_avg['bmi']}", f"{nat_avg['shuttle']}{L['unit_cnt']}", f"{nat_avg['flexibility']}cm", f"{nat_avg['grip']}kg", f"{nat_avg['jump']}cm"]
        }

        st.table(comp_data)


# =========================================================
# [6단계] 성적 분석 · 2022 개정 교육과정 / 2028 수능
# =========================================================
with tab6:
    st.header(L["grade_tab_header"])
    st.info(L["grade_tab_info"])

    # 2022 개정 교육과정의 고교 내신 5등급 상대평가
    st.subheader(L["school_grade_header"])
    st.caption(L["school_grade_info"])

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        rank_val = st.number_input(
            L["rank_input"], min_value=1, value=1, step=1, key="grade_rank"
        )
    with col_s2:
        student_count_val = st.number_input(
            L["student_count"], min_value=1, value=100, step=1, key="grade_students"
        )

    if rank_val > student_count_val:
        st.error("석차는 수강자 수보다 클 수 없습니다." if st.session_state["lang"] == "한국어"
                 else "Rank cannot exceed the number of students.")
    else:
        rank_percent = (rank_val / student_count_val) * 100

        # 5등급제 누적 구간: 10% / 34% / 66% / 90% / 100%
        if rank_percent <= 10:
            school_grade = 1
        elif rank_percent <= 34:
            school_grade = 2
        elif rank_percent <= 66:
            school_grade = 3
        elif rank_percent <= 90:
            school_grade = 4
        else:
            school_grade = 5

        st.metric(
            L["school_grade_result"],
            f"{school_grade}등급" if st.session_state["lang"] == "한국어"
            else f"Grade {school_grade}"
        )
        st.caption(
            f"상위 {rank_percent:.2f}%"
            if st.session_state["lang"] == "한국어"
            else f"Top {rank_percent:.2f}%"
        )
        st.caption(L["school_grade_note"])

    st.divider()

    # 2028학년도 수능 9등급제
    st.subheader(L["csat_header"])
    st.caption(L["csat_info"])

    csat_area = st.selectbox(
        L["csat_area"],
        ["국어", "수학", "탐구", "영어", "한국사"],
        key="csat_area_select"
    )

    if csat_area in ["국어", "수학", "탐구"]:
        csat_percentile_val = st.number_input(
            L["csat_percentile"],
            min_value=0.0,
            max_value=100.0,
            value=96.0,
            step=0.1,
            key="csat_percentile_input"
        )

        # 상대평가 누적 경계: 4 / 11 / 23 / 40 / 60 / 77 / 89 / 96 / 100
        if csat_percentile_val >= 96:
            csat_grade = 1
        elif csat_percentile_val >= 89:
            csat_grade = 2
        elif csat_percentile_val >= 77:
            csat_grade = 3
        elif csat_percentile_val >= 60:
            csat_grade = 4
        elif csat_percentile_val >= 40:
            csat_grade = 5
        elif csat_percentile_val >= 23:
            csat_grade = 6
        elif csat_percentile_val >= 11:
            csat_grade = 7
        elif csat_percentile_val >= 4:
            csat_grade = 8
        else:
            csat_grade = 9

        st.metric(
            L["csat_result"],
            f"{csat_grade}등급" if st.session_state["lang"] == "한국어"
            else f"Grade {csat_grade}"
        )
        st.caption(L["csat_relative"])

    else:
        csat_score_val = st.number_input(
            L["csat_score"],
            min_value=0,
            max_value=100 if csat_area == "영어" else 50,
            value=90 if csat_area == "영어" else 40,
            step=1,
            key="csat_score_input"
        )

        if csat_area == "영어":
            absolute_cuts = [90, 80, 70, 60, 50, 40, 30, 20, 0]
        else:
            absolute_cuts = [40, 35, 30, 25, 20, 15, 10, 5, 0]

        csat_grade = 9
        for i, cut in enumerate(absolute_cuts, start=1):
            if csat_score_val >= cut:
                csat_grade = i
                break

        st.metric(
            L["csat_result"],
            f"{csat_grade}등급" if st.session_state["lang"] == "한국어"
            else f"Grade {csat_grade}"
        )
        st.caption(L["csat_absolute"])

    st.divider()

    # 2022 개정 교육과정 과목 설명
    st.subheader(L["course_header"])

    course_data = {
        "국어 · 화법과 언어": ("국어", "화법의 원리와 언어의 구조·사용을 이해하고, 다양한 상황에서 정확하고 효과적으로 의사소통하는 능력을 기르는 과목입니다."),
        "국어 · 독서와 작문": ("국어", "다양한 분야의 글을 비판적으로 읽고, 자신의 생각을 논리적이고 효과적으로 글로 표현하는 능력을 기르는 과목입니다."),
        "국어 · 문학": ("국어", "문학 작품의 내용과 형식, 맥락을 이해하고 문학적 감상과 표현 능력을 기르는 과목입니다."),
        "수학 · 대수": ("수학", "지수·로그, 수열 등 대수적 개념을 바탕으로 식과 관계를 일반화하고 문제를 논리적으로 해결하는 능력을 기르는 과목입니다."),
        "수학 · 미적분Ⅰ": ("수학", "함수의 극한과 연속, 미분과 적분의 기본 개념을 이해하고 변화율과 누적량을 수학적으로 해석하는 과목입니다."),
        "수학 · 확률과 통계": ("수학", "경우의 수, 확률, 통계적 추론을 통해 불확실한 현상을 수량화하고 자료를 분석·해석하는 능력을 기르는 과목입니다."),
        "수학 · 기하": ("수학", "도형과 공간의 성질을 벡터와 좌표 등으로 탐구하며 공간적 관계를 논리적으로 분석하는 능력을 기르는 과목입니다."),
        "영어 · 영어Ⅰ": ("영어", "일상생활과 다양한 주제의 영어 자료를 이해하고 자신의 생각을 영어로 표현하는 기본적인 의사소통 능력을 기르는 과목입니다."),
        "영어 · 영어Ⅱ": ("영어", "보다 다양한 주제와 수준의 영어 자료를 활용하여 읽기·듣기·말하기·쓰기 능력을 심화하는 과목입니다."),
        "과학 · 역학과 에너지": ("과학", "운동과 힘, 에너지와 운동량 등 역학의 핵심 개념을 수학적으로 다루고 자연 현상을 물리 법칙으로 설명하는 과목입니다."),
        "과학 · 전자기와 양자": ("과학", "전기와 자기, 전자기파 및 현대 물리의 양자적 관점을 통해 물질과 에너지의 상호작용을 탐구하는 과목입니다."),
        "과학 · 물질과 에너지": ("과학", "물질의 구조와 성질, 화학 반응과 에너지 변화를 이해하고 물질 세계를 과학적으로 해석하는 과목입니다."),
        "과학 · 화학 반응의 세계": ("과학", "산·염기, 산화·환원, 평형 등 다양한 화학 반응의 원리를 탐구하고 반응을 정량적으로 해석하는 과목입니다."),
        "과학 · 세포와 물질대사": ("과학", "세포의 구조와 기능, 물질대사 및 생명 활동의 에너지 흐름을 이해하는 과목입니다."),
        "과학 · 생물의 유전": ("과학", "유전 정보의 저장과 전달, 유전 현상과 생명공학 등을 탐구하여 생명 현상을 유전의 관점에서 이해하는 과목입니다."),
        "정보": ("정보", "자료와 정보의 표현, 문제 해결 절차, 프로그래밍, 컴퓨팅 시스템 등을 활용하여 디지털 문제 해결 역량을 기르는 과목입니다."),
        "인공지능 기초": ("정보", "인공지능의 기본 원리와 데이터, 기계학습 등의 개념을 이해하고 인공지능을 활용해 문제를 해결하는 기초 역량을 기르는 과목입니다."),
    }

    selected_course = st.selectbox(
        L["course_select"], list(course_data.keys()), key="course_description_select"
    )
    course_type, course_desc = course_data[selected_course]

    col_c1, col_c2 = st.columns([1, 3])
    with col_c1:
        st.metric(L["course_type"], course_type)
    with col_c2:
        st.write(f"**{L['course_desc']}**")
        st.info(course_desc)

# =========================================================
# [7단계] 주요 웹사이트 하이퍼링크 모음
# =========================================================
with tab7:
    st.header(L["tab6_header"])
    st.info(L["tab6_info"])

    st.subheader(L["portal_head"])
    col_link1, col_link2, col_link3 = st.columns(3)

    with col_link1:
        st.link_button("🟢 Naver", "https://www.naver.com", type="primary", use_container_width=True)
    with col_link2:
        st.link_button("🔍 Google", "https://www.google.com", type="primary", use_container_width=True)
    with col_link3:
        st.link_button("🟡 Daum", "https://www.daum.net", use_container_width=True)

    st.divider()

    st.subheader(L["edu_head"])
    col_link4, col_link5, col_link6, col_link7 = st.columns(4)

    with col_link4:
        st.link_button("🏫 NEIS", "https://www.neis.go.kr", use_container_width=True)
    with col_link5:
        st.link_button("📖 EBSi", "https://www.ebsi.co.kr", use_container_width=True)
    with col_link6:
        st.link_button("🏛️ JBE", "https://www.jbe.go.kr", use_container_width=True)
    with col_link7:
        st.link_button("전북교육청 고교학점제 지원시스템", 'https://jbecredit.kr/', use_container_width=True)

    st.divider()
    st.caption(L["link_caption"])
