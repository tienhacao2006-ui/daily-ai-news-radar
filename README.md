# ⚡ Daily AI News Radar (24/7 Cloud Automation)

Tự động cào tin tức AI & LLM nổi bật mỗi ngày từ **Hacker News (Algolia API)** và **Hugging Face Daily Papers**, định dạng thành bản tin ngắn gọn kèm liên kết bài viết và gửi thẳng về Telegram cá nhân.

Chạy hoàn toàn miễn phí trên **GitHub Actions** (2.000 phút/tháng), không cần bật máy tính.

---

## 🚀 Hướng dẫn cài đặt lên GitHub (3 bước - 2 phút)

### Bước 1: Tạo Repo trên GitHub
1. Vào https://github.com/new
2. Đặt tên repository: `daily-ai-news-radar`
3. Chọn chế độ: **Private** (để bảo mật mã nguồn)
4. Nhấn **Create repository**

### Bước 2: Đẩy mã nguồn lên Repo
Mở Terminal tại thư mục `D:/AI_WORKSPACE/projects/daily_ai_news_cloud` và chạy:
```bash
git init
git add .
git commit -m "feat: initial daily ai news radar"
git branch -M main
git remote add origin https://github.com/<USERNAME>/daily-ai-news-radar.git
git push -u origin main
```

### Bước 3: Cấu hình 2 Secrets trên GitHub
1. Vào repository trên GitHub -> chọn **Settings** -> **Secrets and variables** -> **Actions**
2. Nhấn **New repository secret** và thêm 2 biến sau:
   - `TELEGRAM_BOT_TOKEN`: Token bot Telegram của bạn
   - `TELEGRAM_CHAT_ID`: `5189419163`

---

## ⏰ Lịch trình hoạt động
- **Mỗi ngày vào lúc 08:00 sáng (giờ VN / 01:00 UTC):** GitHub Actions tự động thức dậy trên cloud, thu thập tin mới và gửi vào Telegram @Tienopcbot.
- **Kích hoạt thủ công bất cứ lúc nào:** Vào tab **Actions** trên GitHub -> Chọn workflow **Daily AI News Radar** -> Bấm **Run workflow**.
