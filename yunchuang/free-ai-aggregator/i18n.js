// 免费 AI 模型聚合平台 - 多语言翻译文件
// 用于 common-i18n.js 引擎

var FREE_AI_I18N = {
    zh: {
        // 页面标题
        pageTitle: "免费 AI 模型聚合平台",
        pageSubtitle: "自动轮询 · 智能故障切换 · 无需 API Key · 完全免费",
        
        // 模型列表
        loadingModels: "⚡ 加载中...",
        
        // 输入区域
        inputPlaceholder: "输入你的问题...",
        sendButton: "➤ 发送",
        
        // 状态栏
        ready: "就绪，输入问题发送",
        tryingSources: "正在尝试多个免费源...",
        trySource: "尝试 {{name}} ...",
        success: "✅ 成功 ({{name}})",
        sourceUnavailable: "⚠️ {{name}} 不可用，切换中...",
        allFailed: "❌ 所有免费源暂时不可用，请稍后重试",
        pleaseInputQuestion: "请输入问题",
        clearing: "已清空",
        
        // 响应区域
        placeholder: "👋 点击发送，将自动尝试多个免费模型",
        requesting: "⏳ 请求中...",
        cleared: "🧹 已清空，输入新问题吧",
        noRetryQuestion: "没有可重试的问题",
        enterQuestionToRetry: "📝 输入问题后重试",
        
        // 错误信息
        allApiFailed: "😵 所有 API 源均请求失败。\n最后错误：{{error}}\n\n提示：可能是网络/跨域限制，或免费额度已用完。",
        emptyResponse: "✏️ 请在上面输入问题",
        
        // 底部按钮
        clearButton: "清空",
        retryButton: "🔄 重试",
        
        // 底部说明
        footerNote: "⚡ 内置 OpenRouter 免费模型 & Gemini 社区代理 · 自动故障切换 · 支持 Mistral 7B、Gemma 2 9B 等主流模型",
        
        // 模型名称
        models: {
            mistral7b: "Mistral 7B (Free)",
            gemma29b: "Gemma 2 9B (Free)",
            phi3Mini: "Phi-3 Mini (Free)"
        },
        
        // 示例问题
        defaultQuestion: "用一句话解释什么是大语言模型"
    },
    
    en: {
        // Page title
        pageTitle: "Free AI Model Aggregator",
        pageSubtitle: "Auto-Rotating · Smart Failover · No API Key Required · Completely Free",
        
        // Model list
        loadingModels: "⚡ Loading...",
        
        // Input area
        inputPlaceholder: "Enter your question...",
        sendButton: "➤ Send",
        
        // Status bar
        ready: "Ready, enter a question and send",
        tryingSources: "Trying multiple free sources...",
        trySource: "Trying {{name}} ...",
        success: "✅ Success ({{name}})",
        sourceUnavailable: "⚠️ {{name}} unavailable, switching...",
        allFailed: "❌ All free sources temporarily unavailable, please try again later",
        pleaseInputQuestion: "Please enter a question",
        clearing: "Cleared",
        
        // Response area
        placeholder: "👋 Click send to automatically try multiple free models",
        requesting: "⏳ Requesting...",
        cleared: "🧹 Cleared, enter a new question",
        noRetryQuestion: "No question to retry",
        enterQuestionToRetry: "📝 Enter a question to retry",
        
        // Error messages
        allApiFailed: "😵 All API sources failed.\nLast error: {{error}}\n\nTip: May be network/CORS restriction or free quota exhausted.",
        emptyResponse: "✏️ Please enter a question above",
        
        // Bottom buttons
        clearButton: "Clear",
        retryButton: "🔄 Retry",
        
        // Footer note
        footerNote: "⚡ Built-in OpenRouter free models & Gemini community proxy · Auto failover · Supports Mistral 7B, Gemma 2 9B, and more",
        
        // Model names
        models: {
            mistral7b: "Mistral 7B (Free)",
            gemma29b: "Gemma 2 9B (Free)",
            phi3Mini: "Phi-3 Mini (Free)"
        },
        
        // Default question
        defaultQuestion: "Explain what a large language model is in one sentence"
    },
    
    ja: {
        // ページタイトル
        pageTitle: "無料 AI モデル集約プラットフォーム",
        pageSubtitle: "自動ローテーション · スマートフェイルオーバー · API キー不要 · 完全無料",
        
        // モデルリスト
        loadingModels: "⚡ ローディング中...",
        
        // 入力エリア
        inputPlaceholder: "質問を入力してください...",
        sendButton: "➤ 送信",
        
        // ステータスバー
        ready: "準備完了、質問を入力して送信",
        tryingSources: "複数の無料ソースを試しています...",
        trySource: "{{name}} を試しています...",
        success: "✅ 成功 ({{name}})",
        sourceUnavailable: "⚠️ {{name}} 利用不可、切替中...",
        allFailed: "❌ すべての無料ソースが一時的に利用できません、後で再試行してください",
        pleaseInputQuestion: "質問を入力してください",
        clearing: "クリアしました",
        
        // 応答エリア
        placeholder: "👋 送信をクリックすると、複数の無料モデルが自動的に試されます",
        requesting: "⏳ 要求中...",
        cleared: "🧹 クリアされました、新しい質問を入力してください",
        noRetryQuestion: "再試行する質問がありません",
        enterQuestionToRetry: "📝 質問を入力して再試行",
        
        // エラーメッセージ
        allApiFailed: "😵 すべての API ソースが失敗しました。\n最後のエラー：{{error}}\n\nヒント：ネットワーク/CORS 制限または無料クォータ尽きの可能性があります。",
        emptyResponse: "✏️ 上に質問を入力してください",
        
        // 下部ボタン
        clearButton: "クリア",
        retryButton: "🔄 再試行",
        
        // フッターノート
        footerNote: "⚡ OpenRouter 無料モデル & Gemini コミュニティプロキシ内蔵 · 自動フェイルオーバー · Mistral 7B、Gemma 2 9B などをサポート",
        
        // モデル名
        models: {
            mistral7b: "Mistral 7B (無料)",
            gemma29b: "Gemma 2 9B (無料)",
            phi3Mini: "Phi-3 Mini (無料)"
        },
        
        // デフォルト質問
        defaultQuestion: "大規模言語モデルとは何かを一文で説明してください"
    },
    
    vi: {
        // Tiêu đề trang
        pageTitle: "Nền tảng Tổng hợp Mô hình AI Miễn phí",
        pageSubtitle: "Quay vòng tự động · Chuyển mạch lỗi thông minh · Không cần API Key · Hoàn toàn miễn phí",
        
        // Danh sách mô hình
        loadingModels: "⚡ Đang tải...",
        
        // Khu vực nhập liệu
        inputPlaceholder: "Nhập câu hỏi của bạn...",
        sendButton: "➤ Gửi",
        
        // Thanh trạng thái
        ready: "Sẵn sàng, nhập câu hỏi và gửi",
        tryingSources: "Đang thử nhiều nguồn miễn phí...",
        trySource: "Đang thử {{name}} ...",
        success: "✅ Thành công ({{name}})",
        sourceUnavailable: "⚠️ {{name}} không khả dụng, đang chuyển đổi...",
        allFailed: "❌ Tất cả nguồn miễn phí tạm thời không khả dụng, vui lòng thử lại sau",
        pleaseInputQuestion: "Vui lòng nhập câu hỏi",
        clearing: "Đã xóa",
        
        // Khu vực phản hồi
        placeholder: "👋 Nhấn gửi để tự động thử nhiều mô hình miễn phí",
        requesting: "⏳ Đang yêu cầu...",
        cleared: "🧹 Đã xóa, nhập câu hỏi mới",
        noRetryQuestion: "Không có câu hỏi để thử lại",
        enterQuestionToRetry: "📝 Nhập câu hỏi để thử lại",
        
        // Thông báo lỗi
        allApiFailed: "😵 Tất cả nguồn API đều thất bại.\nLỗi cuối cùng: {{error}}\n\nMẹo: Có thể do hạn chế mạng/CORS hoặc hết hạn mức miễn phí.",
        emptyResponse: "✏️ Vui lòng nhập câu hỏi ở trên",
        
        // Nút phía dưới
        clearButton: "Xóa",
        retryButton: "🔄 Thử lại",
        
        // Ghi chú chân trang
        footerNote: "⚡ Tích hợp mô hình OpenRouter miễn phí & proxy cộng đồng Gemini · Chuyển mạch tự động · Hỗ trợ Mistral 7B, Gemma 2 9B và nhiều hơn nữa",
        
        // Tên mô hình
        models: {
            mistral7b: "Mistral 7B (Miễn phí)",
            gemma29b: "Gemma 2 9B (Miễn phí)",
            phi3Mini: "Phi-3 Mini (Miễn phí)"
        },
        
        // Câu hỏi mặc định
        defaultQuestion: "Giải thích mô hình ngôn ngữ lớn là gì trong một câu"
    }
};

// 自动应用到页面（如果存在 data-i18n 属性）
(function() {
    'use strict';
    
    function applyPageTranslations() {
        const lang = localStorage.getItem('zt_lang') || 'zh';
        const translations = FREE_AI_I18N[lang] || FREE_AI_I18N.zh;
        
        // 应用简单文本替换
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[key]) {
                el.textContent = translations[key];
            }
        });
        
        // 应用占位符
        const input = document.getElementById('userInput');
        if (input && translations.inputPlaceholder) {
            input.placeholder = translations.inputPlaceholder;
        }
        
        // 应用默认问题
        if (input && translations.defaultQuestion) {
            input.value = translations.defaultQuestion;
        }
    }
    
    // 页面加载完成后应用
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyPageTranslations);
    } else {
        applyPageTranslations();
    }
})();
