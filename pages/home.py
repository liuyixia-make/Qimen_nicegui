# pages/home.py
from nicegui import ui

def create_page():
    @ui.page('/')  # 注册根路径
    def main():
        ui.label('欢迎来到首页')