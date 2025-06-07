# components/navbar.py
from nicegui import ui

def create_navbar():
    """
    创建浮动菜单按钮和弹出式导航栏，纯HTML实现
    """
    # 添加样式
    ui.add_head_html('''
        <style>
            /* 浮动圆形按钮 */
            .float-btn {
                position: fixed;
                right: 22px;
                bottom: 40px;
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #7fd8ff 0%, #46aaff 100%);
                color: #fff;
                border-radius: 50%;
                box-shadow: 0 3px 18px rgba(68,160,255,0.18);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                z-index: 1002;
                transition: background 0.2s;
                cursor: pointer;
            }
            .float-btn:hover {
                background: linear-gradient(135deg, #46aaff 0%, #7fd8ff 100%);
            }

            /* 遮罩 */
            .mask {
                position: fixed;
                left: 0; right: 0; top: 0; bottom: 0;
                background: rgba(0,0,0,0.15);
                z-index: 1000;
                display: none;
            }

            /* 优雅弹出菜单 */
            .popup-menu {
                position: fixed;
                left: 12px;
                right: 12px;
                bottom: 18px;
                background: #fff;
                border-radius: 18px;
                box-shadow: 0 4px 32px rgba(52,122,255,0.10);
                z-index: 1003;
                padding: 16px 0 4px 0;
                animation: menuPopup 0.22s;
                transition: box-shadow 0.2s;
                display: none;
            }

            /* 顶部栏 */
            .menu-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 22px 8px 22px;
                border-bottom: 1px solid #f2f3f5;
            }
            .menu-title {
                font-size: 15px;
                color: #222;
                font-weight: 500;
                letter-spacing: 1px;
            }
            .menu-close {
                font-size: 20px;
                color: #bbb;
                padding: 4px 0 0 0;
                cursor: pointer;
            }
            .menu-close:hover {
                color: #888;
            }

            .menu-list {
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-start;
                align-items: center;
                padding: 10px 12px 2px 12px;
            }
            .menu-item {
                width: 25%;
                min-width: 64px;
                margin-bottom: 10px;
                text-align: center;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 8px 0;
                cursor: pointer;
                transition: all 0.2s;
                text-decoration: none;
                color: #333;
            }
            .menu-item:hover {
                background: linear-gradient(135deg, #f1f8ff 0%, #e7f1ff 100%);
                color: #2196f3;
            }
            .menu-item i {
                font-size: 22px;
                margin-bottom: 5px;
            }
            .menu-item span {
                font-size: 14px;
            }

            /* 弹出动画 */
            @keyframes menuPopup {
                0% { transform: translateY(50px); opacity: 0; }
                100% { transform: translateY(0); opacity: 1; }
            }
            
            /* 适配移动设备 */
            @media (max-width: 480px) {
                .popup-menu {
                    left: 8px;
                    right: 8px;
                    bottom: 16px;
                }
                .menu-item {
                    width: 33.33%;
                }
            }
            
            /* 显示元素 */
            .visible {
                display: block !important;
            }
        </style>
    ''')
    
    # 添加 Font Awesome 图标库
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    ''')
    
    # 添加HTML部分（不包含脚本）
    ui.html('''
        <!-- 浮动按钮 -->
        <div class="float-btn" onclick="toggleMenu()">
            <i class="fas fa-compass"></i>
        </div>
        
        <!-- 遮罩层 -->
        <div class="mask" onclick="toggleMenu()"></div>
        
        <!-- 弹出菜单 -->
        <div class="popup-menu">
            <!-- 菜单标题栏 -->
            <div class="menu-header">
                <div class="menu-title">快捷导航</div>
                <div class="menu-close" onclick="toggleMenu()">&times;</div>
            </div>
            
            <!-- 菜单列表 -->
            <div class="menu-list">
                <!-- 首页 -->
                <a href="/" class="menu-item">
                    <i class="fas fa-home"></i>
                    <span>首页</span>
                </a>
                
                <!-- 排盘系统 -->
                <a href="/paipan" class="menu-item">
                    <i class="fas fa-compass"></i>
                    <span>排盘系统</span>
                </a>
                
                <!-- 八字 -->
                <a href="#" class="menu-item">
                    <i class="fas fa-calendar-alt"></i>
                    <span>八字</span>
                </a>
                
                <!-- 星盘 -->
                <a href="#" class="menu-item">
                    <i class="fas fa-star"></i>
                    <span>星盘</span>
                </a>
            </div>
        </div>
    ''')
    
    # 单独添加JavaScript脚本
    ui.add_body_html('''
        <script>
            function toggleMenu() {
                const mask = document.querySelector('.mask');
                const menu = document.querySelector('.popup-menu');
                
                if (mask.classList.contains('visible')) {
                    // 隐藏菜单
                    mask.classList.remove('visible');
                    menu.classList.remove('visible');
                } else {
                    // 显示菜单
                    mask.classList.add('visible');
                    menu.classList.add('visible');
                }
            }
        </script>
    ''') 