from nicegui import ui

def create_page():
    @ui.page('/')
    def main():
        ui.label('欢迎来到首页')