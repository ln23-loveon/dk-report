import qrcode
import os
import socket
import win32com.client as win32

# ==================== 配置 ====================
base_dir = r"D:\code\python\dj"
briefing_date = "2026-06-02"
qr_path = os.path.join(base_dir, "file", "qrcode.png")
card_png_path = os.path.join(base_dir, "file", briefing_date, "card.png")
github_url = f"https://github.com/ln23-loveon/dk-report/blob/master/file/{briefing_date}/card.html"
pages_url = f"https://ln23-loveon.github.io/dk-report/file/{briefing_date}/card.html"
recipient = "lina23@lenovo.com"

# 获取本机IP（用于追踪服务器地址，方便局域网内其他设备访问）
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

host_ip = get_host_ip()
track_base_url = f"http://{host_ip}:8080"

# 二维码指向 GitHub Pages 公网地址（扫码后任何网络都能直接打开网页）
qr_content = pages_url

# ==================== 1. 生成二维码 ====================
# 二维码指向 GitHub Pages，扫码后任何设备、任何网络都能直接打开网页
print(f"二维码内容: {qr_content}")

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(qr_content)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(qr_path)
print(f"[OK] 二维码已生成: {qr_path}")

# ==================== 2. 发送邮件 ====================
outlook = win32.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)  # 0 = olMailItem
mail.To = recipient
mail.Subject = "每日党建简报 - 二维码及预览图"

# 设置为 HTML 格式
mail.BodyFormat = 2  # 2 = olFormatHTML

# 添加附件并设置 ContentID，以便在 HTML 正文中引用
att_qr = mail.Attachments.Add(qr_path)
att_qr.PropertyAccessor.SetProperty(
    "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
    "qrcode.png"
)

att_card = mail.Attachments.Add(card_png_path)
att_card.PropertyAccessor.SetProperty(
    "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
    "card.png"
)

# 追踪像素（隐藏图片，邮件打开时自动请求，用于统计打开率）
tracking_pixel = (
    f'<img src="{track_base_url}/track?user={recipient}" '
    f'width="1" height="1" style="display:none;" />'
)

# 点击追踪链接（先统计，再跳转到 GitHub Pages 网页）
click_url = f"{track_base_url}/click?user={recipient}&target={pages_url}"

mail.HTMLBody = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 640px;
        margin: 0 auto;
        padding: 20px;
        background: #f8f9fa;
    }}
    .wrapper {{
        background: #fff;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }}
    h2 {{
        color: #e63946;
        border-bottom: 2px solid #e63946;
        padding-bottom: 10px;
        margin-top: 0;
    }}
    h3 {{
        color: #457b9d;
        margin-top: 28px;
        margin-bottom: 12px;
    }}
    a {{ color: #2a9d8f; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .btn {{
        display: inline-block;
        background: linear-gradient(135deg, #e63946 0%, #d62839 100%);
        color: white !important;
        padding: 12px 28px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(230,57,70,0.3);
    }}
    .btn:hover {{
        background: linear-gradient(135deg, #d62839 0%, #c21e2b 100%);
        text-decoration: none;
    }}
    .footer {{
        margin-top: 32px;
        padding-top: 16px;
        border-top: 1px solid #eee;
        color: #888;
        font-size: 12px;
        text-align: center;
    }}
    .img-box {{
        text-align: center;
        margin: 12px 0;
    }}
    .img-box img {{
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 100%;
    }}
    .link-box {{
        background: #f1f3f5;
        border-radius: 8px;
        padding: 12px 16px;
        word-break: break-all;
        font-size: 13px;
        margin: 8px 0;
    }}
</style>
</head>
<body>
    <div class="wrapper">
        <h2>📋 每日党建简报</h2>
        <p>您好，</p>
        <p>以下是每日党建简报的相关资料，请查收。</p>
        <h3>1. 在线查看链接</h3>
        <div class="link-box">
            <a href="{pages_url}">{pages_url}</a>
        </div>
        <p style="text-align:center;">
            <a href="{click_url}" class="btn">点击此处查看 card.html（带点击统计）</a>
        </p>
     
        <h3>2. 二维码</h3>
        <p>扫描下方二维码可直接访问：</p>
        <div class="img-box">
            <img src="cid:qrcode.png" alt="二维码" width="220">
        </div>

        <h3>3. 简报预览图</h3>
        <div class="img-box">
            <img src="cid:card.png" alt="card预览" width="100%">
        </div>

        {tracking_pixel}

        <div class="footer">
            <p>本邮件由系统自动发送 | 数据截至 2026-06-01</p>
        </div>
    </div>
</body>
</html>"""

mail.Send()
print("[OK] 邮件已发送至 " + recipient)
print(f"[INFO] 追踪服务器地址: {track_base_url}")
print("   请先运行: python tracker_server.py")
print("   当收件人打开邮件或点击链接时，统计信息将打印在 tracker_server.py 的终端中。")
