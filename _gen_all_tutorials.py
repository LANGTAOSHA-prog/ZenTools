#!/usr/bin/env python3
"""Generate 5 tutorial HTML files for dev tools."""
import json
import re

# Load template
with open("/workspace/tutorials/pdf-merge.html", "r") as f:
    TEMPLATE = f.read()

# Common replacement map for the template body
BODY_REPLACEMENTS = {
    "a1Intro": "intro",
    "a1OpenBody": "open_body",
    "a1Step1T": "step1_t", "a1Step1B": "step1_b", "a1Step2T": "step2_t", "a1Step2B": "step2_b",
    "a1Step3T": "step3_t", "a1Step3B": "step3_b", "a1Step4T": "step4_t", "a1Step4B": "step4_b",
    "a1Tip1": "tip1", "a1Tip2": "tip2",
    "a1Faq1Q": "faq1_q", "a1Faq1A": "faq1_a", "a1Faq2Q": "faq2_q", "a1Faq2A": "faq2_a",
    "a1Faq3Q": "faq3_q", "a1Faq3A": "faq3_a",
}

# Step titles and descriptions for each tutorial
TOOL_DATA = {
    "cameratest": {
        "prefix": "ct",
        "title": {
            "zh": "摄像头测试教程：在线检测摄像头功能",
            "en": "Camera Test Tutorial: Online Camera Detection",
            "ja": "カメラテストチュートリアル：オンラインカメラ検出",
            "vi": "Hướng dẫn kiểm tra camera: Phát hiện camera trực tuyến",
        },
        "cat": {"zh": "💻 开发工具", "en": "💻 Developer Tools", "ja": "💻 開発ツール", "vi": "💻 Công cụ nhà phát triển"},
        "tool_url": "/dev/cameratest.html",
        "svg": "/guides/img/cameratest-step1.svg",
        "related": [
            ("/tutorials/keyboardtest.html", "键盘测试教程", "Keyboard Test Tutorial", "キーボードテストチュートリアル", "Hướng dẫn kiểm tra bàn phím"),
            ("/tutorials/screencheck.html", "屏幕检测教程", "Screen Check Tutorial", "画面チェックチュートリアル", "Hướng dẫn kiểm tra màn hình"),
            ("/tutorials/mictest.html", "麦克风测试教程", "Microphone Test Tutorial", "マイクテストチュートリアル", "Hướng dẫn kiểm tra microphone"),
        ],
        "intro": {
            "zh": "摄像头是现代人最常用的硬件之一，笔记本、手机、外接摄像头每天都在使用。但你是否确定自己的摄像头工作正常？ZenTools 在线摄像头测试工具可以帮助你快速检测摄像头是否正常工作，支持实时视频预览、拍照和录像功能检测。无需安装任何软件，打开浏览器就能使用，所有数据都在本地处理，保护你的隐私安全。",
            "en": "Cameras are one of the most commonly used hardware devices today. Whether it's a laptop built-in camera, smartphone, or USB webcam, you use it daily. But are you sure your camera is working properly? ZenTools's online camera test tool helps you quickly verify camera functionality with real-time video preview, photo capture, and video recording tests. No software installation needed — just open your browser. All processing happens locally, protecting your privacy.",
            "ja": "カメラは現代で最もよく使われるハードウェアの一つです。ノートパソコンの内蔵カメラ、スマートフォン、USBウェブカムなど、毎日使っていますよね。でも、自分のカメラが正常に動作しているかどうか確認したことがありますか？ZenToolsのオンラインカメラテストツールを使えば、リアルタイム動画プレビュー、写真撮影、録画機能のテストをサポートして、カメラが正常に動作するか素早く確認できます。",
            "vi": "Camera là một trong những thiết bị phần cứng được sử dụng phổ biến nhất ngày nay. Dù là camera tích hợp laptop, điện thoại hay webcam USB, bạn đều sử dụng hàng ngày. Nhưng bạn có chắc camera của mình hoạt động bình thường không? Công cụ kiểm tra camera trực tuyến ZenTools giúp bạn nhanh chóng xác minh camera hoạt động đúng cách, hỗ trợ xem trước video thời gian thực, chụp ảnh và ghi video.",
        },
        "open_body": {
            "zh": '访问 <a href="/dev/cameratest.html" target="_blank">摄像头测试工具</a>，在浏览器中直接使用。点击允许摄像头权限后，工具会自动检测并显示摄像头画面。所有操作在浏览器本地完成，视频流不会上传到任何服务器。',
            "en": 'Visit the <a href="/dev/cameratest.html" target="_blank">Camera Test Tool</a> directly in your browser. After granting camera permission, the tool will automatically detect and display the camera feed. All operations happen locally in your browser; video streams are never uploaded to any server.',
            "ja": '<a href="/dev/cameratest.html" target="_blank">カメラテストツール</a>にアクセスしてブラウザで直接使用します。カメラ権限を許可すると、ツールは自動的にカメラを検出して映像を表示します。すべての操作はブラウザ内で完結し、ビデオストリームはサーバーにアップロードされません。',
            "vi": 'Truy cập <a href="/dev/cameratest.html" target="_blank">Công cụ Kiểm tra Camera</a> để sử dụng trực tiếp trong trình duyệt. Sau khi cấp quyền camera, công cụ sẽ tự động phát hiện và hiển thị hình ảnh camera. Tất cả thao tác được thực hiện cục bộ trong trình duyệt, luồng video không được tải lên bất kỳ máy chủ nào.',
        },
        "steps": [
            {"t": {"zh": "1. 打开工具并授权", "en": "1. Open the Tool and Grant Permission", "ja": "1. ツールを開いて権限を付与", "vi": "1. Mở công cụ và cấp quyền"},
             "b": {"zh": '访问 <a href="/dev/cameratest.html" target="_blank">摄像头测试工具</a>，浏览器会弹出权限请求，点击「允许」以授予摄像头访问权限。如果之前拒绝过，需要在浏览器设置中重新授权。',
                   "en": 'Visit the <a href="/dev/cameratest.html" target="_blank">Camera Test Tool</a>. When the browser prompts for permission, click "Allow" to grant camera access. If you previously denied it, re-authorize in your browser settings.',
                   "ja": '<a href="/dev/cameratest.html" target="_blank">カメラテストツール</a>にアクセスし、ブラウザの権限リクエストで「許可」をクリックしてカメラへのアクセス権限を付与します。以前拒否した場合は、ブラウザ設定で再認証する必要があります。',
                   "vi": 'Truy cập <a href="/dev/cameratest.html" target="_blank">Công cụ Kiểm tra Camera</a>, trình duyệt sẽ hiện yêu cầu quyền, nhấn "Cho phép" để cấp quyền truy cập camera. Nếu trước đó bạn đã từ chối, cần cấp lại trong cài đặt trình duyệt.'}},
            {"t": {"zh": "2. 查看视频预览", "en": "2. View Video Preview", "ja": "2. ビデオプレビューを確認", "vi": "2. Xem trước video"},
             "b": {"zh": "授权成功后，工具会自动调用摄像头并显示实时视频预览。你可以看到画面分辨率、帧率等信息。如果画面黑屏或显示错误，说明摄像头可能存在问题或被其他程序占用。",
                   "en": "After authorization, the tool automatically activates the camera and displays a real-time video preview. You can see resolution and frame rate information. If the screen is black or shows an error, the camera may have issues or be occupied by another program.",
                   "ja": "認証に成功すると、ツールは自動的にカメラを起動し、リアルタイムのビデオプレビューを表示します。解像度やフレームレートなどの情報を見ることができます。画面が黒かったりエラーが表示されたりする場合は、カメラに問題があるか他のプログラムで使用されている可能性があります。",
                   "vi": "Sau khi cấp quyền thành công, công cụ sẽ tự động kích hoạt camera và hiển thị xem trước video thời gian thực. Bạn có thể thấy thông tin độ phân giải, tần số khung hình. Nếu màn hình đen hoặc hiển thị lỗi, camera có thể có vấn đề hoặc bị chương trình khác chiếm dụng."}},
            {"t": {"zh": "3. 测试拍照和录像", "en": "3. Test Photo and Video Recording", "ja": "3. 写真と録画をテスト", "vi": "3. Kiểm tra chụp ảnh và quay video"},
             "b": {"zh": "点击「拍照」按钮可以截取当前画面，点击「录像」按钮可以录制视频片段。通过拍照和录像功能测试，可以验证摄像头的图像采集和编码是否正常。拍下的照片和录制的视频会保存在浏览器本地。",
                   "en": 'Click the "Photo" button to capture the current frame, or click "Record" to record a video clip. These tests verify the camera\'s image capture and encoding functionality. Photos and videos are saved locally in your browser.',
                   "ja": "「写真」ボタンをクリックすると現在のフレームをキャプチャし、「録画」ボタンをクリックするとビデオクリップを録画できます。これらのテストでカメラの画像取得とエンコーディング機能が正常か確認できます。撮影した写真や録画はブラウザのローカルに保存されます。",
                   "vi": 'Nhấn nút "Chụp ảnh" để chụp khung hình hiện tại, nhấn nút "Quay video" để ghi lại đoạn video. Những kiểm tra này xác minh chức năng thu thập hình ảnh và mã hóa của camera. Ảnh chụp và video ghi lại được lưu cục bộ trong trình duyệt.'}},
            {"t": {"zh": "4. 切换摄像头和刷新检测", "en": "4. Switch Cameras and Refresh Detection", "ja": "4. カメラの切り替えと再検出", "vi": "4. Chuyển đổi camera và làm mới kiểm tra"},
             "b": {"zh": "如果设备连接了多个摄像头（如笔记本内置摄像头+外接USB摄像头），可以点击「切换摄像头」按钮切换到另一个摄像头进行测试。测试完成后点击「刷新检测」按钮重新初始化摄像头连接。",
                   "en": "If multiple cameras are connected (e.g., built-in + USB webcam), click \"Switch Camera\" to toggle between them. After testing, click \"Refresh Detection\" to reinitialize the camera connection and ensure all cameras work properly.",
                   "ja": "複数のカメラが接続されている場合（例：内蔵カメラ＋USBウェブカム）、「カメラ切り替え」ボタンをクリックして切り替えることができます。テスト後、「再検出」ボタンをクリックしてカメラ接続を再初期化します。",
                   "vi": "Nếu nhiều camera được kết nối (ví dụ: tích hợp + webcam USB), nhấn nút \"Chuyển đổi camera\" để chuyển đổi giữa chúng. Sau khi kiểm tra xong, nhấn nút \"Làm mới kiểm tra\" để khởi tạo lại kết nối camera."}},
        ],
        "tips": [
            {"zh": "测试前请关闭其他可能占用摄像头的程序（如视频会议软件），否则可能导致摄像头被独占而无法使用。",
             "en": "Close other programs that might use the camera (like video conferencing apps) before testing, as they can独占 the camera and prevent it from working.",
             "ja": "テスト前にカメラを使用する可能性のある他のプログラム（ビデオ会議アプリなど）を閉じてください。そうしないとカメラが独占されて使用できなくなる可能性があります。",
             "vi": "Đóng các chương trình khác có thể sử dụng camera (như ứng dụng họp trực tuyến) trước khi kiểm tra, nếu không camera có thể bị chiếm dụng và không sử dụng được."},
            {"zh": "如果画面出现延迟或卡顿，可能是浏览器性能不足或摄像头硬件老化导致的，可以尝试降低分辨率测试。",
             "en": "If the video feed lags or stutters, it may be due to insufficient browser performance or aging camera hardware. Try testing at a lower resolution.",
             "ja": "映像に遅延やカクつきがある場合は、ブラウザのパフォーマンス不足やカメラの経年劣化が原因かもしれません。解像度を下げてテストしてみてください。",
             "vi": "Nếu hình ảnh bị trễ hoặc giật, có thể do hiệu suất trình duyệt không đủ hoặc camera đã cũ. Hãy thử kiểm tra ở độ phân giải thấp hơn."},
            {"zh": "所有操作在浏览器本地完成，视频流和拍摄的照片都不会上传到服务器，请放心使用。",
             "en": "All operations happen locally in your browser. Video streams and photos are never uploaded to any server. Your privacy is protected.",
             "ja": "すべての操作はブラウザ内で完結します。ビデオストリームや撮影した写真はサーバーにアップロードされませんので、安心してご利用ください。",
             "vi": "Tất cả thao tác được thực hiện cục bộ trong trình duyệt. Luồng video và ảnh chụp không được tải lên máy chủ, yên tâm sử dụng."},
        ],
        "faqs": [
            {"q": {"zh": "浏览器提示无法访问摄像头怎么办？", "en": "What if the browser says it cannot access the camera?", "ja": "ブラウザがカメラにアクセスできないと言ったらどうすればよいですか？", "vi": "Trình duyệt báo không thể truy cập camera thì sao?"},
             "a": {"zh": "首先检查浏览器是否已授权摄像头权限。在浏览器设置中找到隐私/相机设置，确保对本网站授权。如果仍不行，检查摄像头是否被其他程序占用，或尝试重启浏览器。",
                   "en": "First, check if the browser has granted camera permission. Go to browser settings > Privacy > Camera, and ensure this site is authorized. If the problem persists, check if another program is using the camera, or try restarting the browser.",
                   "ja": "まず、ブラウザがカメラ権限を付与しているか確認してください。ブラウザ設定のプライバシー/カメラ設定で、このサイトへの授权を確認してください。それでもダメな場合、カメラが他のプログラムで占有されていないか確認するか、ブラウザを再起動してみてください。",
                   "vi": "Đầu tiên kiểm tra trình duyệt đã cấp quyền camera chưa. Vào cài đặt trình duyệt > Quyền riêng tư > Camera, đảm bảo trang này được cấp quyền. Nếu vẫn không được, kiểm tra xem camera có bị chương trình khác chiếm dụng không, hoặc thử khởi động lại trình duyệt."}},
            {"q": {"zh": "测试画面是黑色的怎么回事？", "en": "The test screen is black. What should I do?", "ja": "テスト画面が黒いのですが？", "vi": "Màn hình kiểm tra màu đen là sao?"},
             "a": {"zh": "画面黑色可能有多种原因：摄像头硬件故障、驱动程序未安装、光线太暗、或被其他程序独占。尝试在其他应用中打开摄像头确认硬件是否正常。",
                   "en": "A black screen can be caused by several factors: camera hardware failure, missing drivers, too little light, or the camera being occupied by another program. Try opening the camera in another application to confirm if the hardware works.",
                   "ja": "画面が黒くなる理由はいくつか考えられます：カメラのハードウェア障害、ドライバーがインストールされていない、光量が足りない、他のプログラムで独占されているなど。他のアプリでカメラを開いてハードウェアが正常か確認してみてください。",
                   "vi": "Màn hình đen có thể do nhiều nguyên nhân: lỗi phần cứng camera, chưa cài driver, ánh sáng quá yếu, hoặc bị chương trình khác chiếm dụng. Thử mở camera trong ứng dụng khác để xác định xem phần cứng có bình thường không."}},
            {"q": {"zh": "拍摄的照片保存在哪里？", "en": "Where are the photos saved?", "ja": "撮影した写真はどこに保存されますか？", "vi": "Ảnh chụp được lưu ở đâu?"},
             "a": {"zh": "拍摄的照片和录制的视频保存在浏览器本地，不会上传到任何服务器。你可以在工具界面中直接查看和下载，关闭页面后数据会清除。",
                   "en": "Photos and videos are saved locally in your browser and are never uploaded to any server. You can view and download them directly in the tool interface. Data is cleared when you close the page.",
                   "ja": "撮影した写真や録画はブラウザのローカルに保存され、サーバーにアップロードされません。ツール画面で直接確認・ダウンロードできます。ページを閉じるとデータは消去されます。",
                   "vi": "Ảnh chụp và video ghi lại được lưu cục bộ trong trình duyệt, không tải lên máy chủ nào. Bạn có thể xem và tải xuống trực tiếp trong giao diện công cụ. Dữ liệu sẽ bị xóa khi đóng trang."}},
        ],
    },
    "keyboardtest": {
        "prefix": "kt",
        "title": {
            "zh": "键盘测试教程：在线检测按键功能",
            "en": "Keyboard Test Tutorial: Online Key Detection",
            "ja": "キーボードテストチュートリアル：オンラインキー検出",
            "vi": "Hướng dẫn kiểm tra bàn phím: Phát hiện phím trực tuyến",
        },
        "cat": {"zh": "💻 开发工具", "en": "💻 Developer Tools", "ja": "💻 開発ツール", "vi": "💻 Công cụ nhà phát triển"},
        "tool_url": "/dev/keyboardtest.html",
        "svg": "/guides/img/keyboardtest-step1.svg",
        "related": [
            ("/tutorials/mousetest.html", "鼠标测试教程", "Mouse Test Tutorial", "マウステストチュートリアル", "Hướng dẫn kiểm tra chuột"),
            ("/tutorials/screencheck.html", "屏幕检测教程", "Screen Check Tutorial", "画面チェックチュートリアル", "Hướng dẫn kiểm tra màn hình"),
            ("/tutorials/cameratest.html", "摄像头测试教程", "Camera Test Tutorial", "カメラテストチュートリアル", "Hướng dẫn kiểm tra camera"),
        ],
        "intro": {
            "zh": "键盘是使用频率最高的输入设备之一，长时间使用后容易出现卡键、连击或个别按键失灵等问题。ZenTools 在线键盘测试工具提供了一个完整的虚拟键盘界面，你可以逐个按下物理键盘上的每个按键，工具会以不同颜色实时标记已测试和未测试的按键。支持全键位检测，包括功能键、方向键、修饰键和数字键，帮助你快速发现键盘故障。所有检测过程完全在浏览器本地完成，无需安装任何软件。",
            "en": "The keyboard is one of the most frequently used input devices. After long-term use, key sticking, double-typing, or individual key failure may occur. ZenTools online keyboard test tool provides a complete virtual keyboard interface. You can press each physical key one by one, and the tool highlights tested and untested keys in different colors. It supports full key detection including function keys, arrow keys, modifier keys, and number keys.",
            "ja": "キーボードは最も頻繁に使用される入力デバイスの一つです。長時間の使用後、キーの詰まり、連打、または特定のキーの故障が発生しやすくなります。ZenToolsのオンラインキーボードテストツールは、完全な仮想キーボードインターフェースを提供します。各物理キーを順番に押すことができ、ツールはテスト済みと未テストのキーを異なる色でリアルタイムで表示します。",
            "vi": "Bàn phím là một trong những thiết bị nhập liệu được sử dụng thường xuyên nhất. Sau thời gian dài sử dụng, có thể xảy ra hiện tượng kẹt phím, gõ đúp hoặc một số phím không phản hồi. Công cụ kiểm tra bàn phím trực tuyến ZenTools cung cấp giao diện bàn phím ảo hoàn chỉnh. Bạn có thể nhấn từng phím vật lý một, và công cụ sẽ đánh dấu các phím đã kiểm tra và chưa kiểm tra bằng màu sắc khác nhau.",
        },
        "open_body": {
            "zh": '访问 <a href="/dev/keyboardtest.html" target="_blank">键盘测试工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件，按键数据不会上传到服务器。',
            "en": 'Visit the <a href="/dev/keyboardtest.html" target="_blank">Keyboard Test Tool</a> directly in your browser. All operations happen locally, no software installation needed, key data is never uploaded to servers.',
            "ja": '<a href="/dev/keyboardtest.html" target="_blank">キーボードテストツール</a>にアクセスしてブラウザで直接使用します。すべての操作はブラウザ内で完結し、ソフトウェアのインストールは不要です。',
            "vi": 'Truy cập <a href="/dev/keyboardtest.html" target="_blank">Công cụ Kiểm tra Bàn phím</a> và sử dụng trực tiếp trong trình duyệt. Tất cả thao tác diễn ra cục bộ, không cần cài đặt phần mềm, dữ liệu phím không bao giờ được tải lên máy chủ.',
        },
        "steps": [
            {"t": {"zh": "1. 打开工具", "en": "1. Open the Tool", "ja": "1. ツールを開く", "vi": "1. Mở công cụ"},
             "b": {"zh": '访问 <a href="/dev/keyboardtest.html" target="_blank">键盘测试工具</a>，页面会显示完整的虚拟键盘布局，所有按键处于待测状态。',
                   "en": 'Visit the <a href="/dev/keyboardtest.html" target="_blank">Keyboard Test Tool</a>. The page displays a complete virtual keyboard layout with all keys ready for testing.',
                   "ja": '<a href="/dev/keyboardtest.html" target="_blank">キーボードテストツール</a>にアクセスすると、ページに完全な仮想キーボードレイアウトが表示され、すべてのキーがテスト待ち状態になります。',
                   "vi": 'Truy cập <a href="/dev/keyboardtest.html" target="_blank">Công cụ Kiểm tra Bàn phím</a>. Trang hiển thị bố trí bàn phím ảo hoàn chỉnh với tất cả các phím sẵn sàng kiểm tra.'}},
            {"t": {"zh": "2. 逐个按下按键", "en": "2. Press Keys One by One", "ja": "2. キーを順番に押す", "vi": "2. Nhấn phím theo thứ tự"},
             "b": {"zh": "按照键盘布局从上到下依次按下每个物理按键，工具会高亮显示已按下的按键，并在底部记录最近按键序列。",
                   "en": "Press each physical key in order from top to bottom. The tool highlights pressed keys and records the recent key sequence at the bottom.",
                   "ja": "上から下へ順に各物理キーを押します。ツールは押されたキーを強調表示し、下部に最近のキーシーケンスを記録します。",
                   "vi": "Nhấn từng phím vật lý từ trên xuống dưới. Công cụ sẽ làm nổi bật các phím đã nhấn và ghi lại chuỗi phím gần đây ở phía dưới."}},
            {"t": {"zh": "3. 检查卡键和连击", "en": "3. Check for Sticking or Double Keys", "ja": "3. キーの詰まりや連打をチェック", "vi": "3. Kiểm tra kẹt phím và gõ đúp"},
             "b": {"zh": "观察按键状态变化，正常按键按下时应立即变亮，松开后恢复。如果某个按键持续高亮或反复闪烁，说明可能存在卡键或连击问题。",
                   "en": "Observe key state changes. A normal key lights up immediately when pressed and returns to normal when released. If a key stays highlighted or flashes repeatedly, it may have sticking or double-typing issues.",
                   "ja": "キーの状態変化を観察します。通常のキーは押すとすぐに点灯し、離すと元の状態に戻ります。あるキーが継続的に強調表示されるか、繰り返し点滅する場合は、キーの詰まりや連打の問題がある可能性があります。",
                   "vi": "Quan sát sự thay đổi trạng thái phím. Phím bình thường sẽ sáng ngay khi nhấn và trở về bình thường khi thả. Nếu một phím vẫn sáng liên tục hoặc nhấp nháy lặp lại, có thể bị kẹt phím hoặc gõ đúp."}},
            {"t": {"zh": "4. 查看测试结果", "en": "4. View Test Results", "ja": "4. テスト結果を表示", "vi": "4. Xem kết quả kiểm tra"},
             "b": {"zh": "测试完成后，工具会显示已测试的按键数量和总按键数，绿色表示正常，红色表示未测试或异常的按键。",
                   "en": "After testing, the tool shows the number of tested keys versus total keys. Green indicates normal, red indicates untested or abnormal keys.",
                   "ja": "テスト完了後、ツールはテスト済みのキー数と総キー数を表示します。緑が正常、赤が未テストまたは異常なキーを示します。",
                   "vi": "Sau khi kiểm tra, công cụ hiển thị số phím đã kiểm tra so với tổng số phím. Màu xanh lá bình thường, màu đỏ cho biết phím chưa kiểm tra hoặc bất thường."}},
        ],
        "tips": [
            {"zh": "测试时请关闭输入法，否则字符输入可能会干扰按键检测的准确性。",
             "en": "Please disable your IME (input method editor) during testing, as character input may interfere with key detection accuracy.",
             "ja": "テスト中はIME（入力メソッドエディタ）を無効にしてください。文字入力がキー検出の精度に影響を与える可能性があります。",
             "vi": "Vui lòng tắt bộ soạn thảo IME trong quá trình kiểm tra vì nhập ký tự có thể ảnh hưởng đến độ chính xác của việc phát hiện phím."},
            {"zh": "对于机械键盘用户，建议逐个轴体测试，特别注意空格键、Shift 键和 Enter 键等大键位。",
             "en": "For mechanical keyboard users, test each switch individually, paying special attention to large keys like Space, Shift, and Enter.",
             "ja": "メカニカルキーボードユーザーは、各スイッチを個別にテストし、スペースキー、Shiftキー、Enterキーなどの大型キーを特に注意してください。",
             "vi": "Đối với người dùng bàn phím cơ, hãy kiểm tra từng switch một, đặc biệt chú ý các phím lớn như Space, Shift và Enter."},
            {"zh": "所有操作在浏览器本地完成，按键数据不会上传到服务器，可以放心测试。",
             "en": "All operations happen locally in your browser. Key data is never uploaded to any server. Feel free to test.",
             "ja": "すべての操作はブラウザ内でローカルに完了し、キーデータはサーバーにアップロードされません。安心してテストしてください。",
             "vi": "Tất cả thao tác diễn ra cục bộ trong trình duyệt. Dữ liệu phím không bao giờ được tải lên máy chủ. Hãy yên tâm kiểm tra."},
        ],
        "faqs": [
            {"q": {"zh": "为什么有些按键没有反应？", "en": "Why do some keys not respond?", "ja": "なぜか一部のキーが反応しません。", "vi": "Tại sao một số phím không phản hồi?"},
             "a": {"zh": "可能是键盘硬件故障，也可能是浏览器没有正确捕获按键事件。请尝试在其他应用中测试该按键，或在其他浏览器中打开本工具。",
                   "en": "It could be a hardware fault with the keyboard, or the browser may not be capturing key events correctly. Try testing the key in another application or open this tool in a different browser.",
                   "ja": "キーボードのハードウェア障害の可能性もありますが、ブラウザがキーイベントを正しく捕捉していない可能性もあります。別のアプリケーションでそのキーをテストするか、別のブラウザでこのツールを開いてみてください。",
                   "vi": "Có thể là lỗi phần cứng bàn phím, hoặc trình duyệt không bắt được sự kiện phím đúng cách. Hãy thử kiểm tra phím đó trong ứng dụng khác hoặc mở công cụ này trong trình duyệt khác."}},
            {"q": {"zh": "可以测试笔记本的特殊功能键吗？", "en": "Can I test special function keys on a laptop?", "ja": "ノートパソコンの特殊機能キーをテストできますか？", "vi": "Tôi có thể kiểm tra các phím chức năng đặc biệt trên laptop không?"},
             "a": {"zh": "可以。音量键、亮度键、Fn 组合键等特殊功能键都可以被工具检测和显示。",
                   "en": "Yes. Volume keys, brightness keys, Fn combination keys, and other special function keys can all be detected and displayed by the tool.",
                   "ja": "できます。音量キー、明るさキー、Fn組み合わせキーなどの特殊機能キーもすべてツールで検出して表示できます。",
                   "vi": "Có. Các phím âm lượng, phím độ sáng, tổ hợp phím Fn và các phím chức năng đặc biệt khác đều có thể được công cụ phát hiện và hiển thị."}},
            {"q": {"zh": "测试完发现按键有问题怎么办？", "en": "What if I find a faulty key after testing?", "ja": "テスト後にキーに問題が見つかったらどうすればよいですか？", "vi": "Tôi làm gì nếu phát hiện phím bị lỗi sau khi kiểm tra?"},
             "a": {"zh": "如果是机械键盘可以尝试更换轴体或清洁键帽。薄膜键盘或笔记本键盘建议联系售后维修。",
                   "en": "For mechanical keyboards, try replacing the switch or cleaning the keycap. For membrane or laptop keyboards, contact after-sales support for repair.",
                   "ja": "メカニカルキーボードの場合は、スイッチを交換するかキーキャップを清掃してみてください。メンブレンキーボードやノートパソコンのキーボードの場合は、アフターサポートに連絡して修理を依頼してください。",
                   "vi": "Đối với bàn phím cơ, hãy thử thay switch hoặc vệ sinh keycap. Đối với bàn phím màng hoặc bàn phím laptop, hãy liên hệ hỗ trợ hậu mãi để sửa chữa."}},
        ],
    },
}

# The 3 generated ones (mictest, mousetest, screencheck) already exist from _gen_tutorials.py
# Just verify them and add SVG references if missing

for name in ["mictest", "mousetest", "screencheck"]:
    with open(f"/workspace/tutorials/{name}.html", "r") as f:
        content = f.read()
    # Check if SVG path is correct
    expected_svg = f"/guides/img/{name}-step1.svg"
    if expected_svg not in content:
        # Fix SVG references
        import re
        content = re.sub(r'src="/guides/img/\w+-step1\.svg"', f'src="{expected_svg}"', content)
        with open(f"/workspace/tutorials/{name}.html", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed SVG path in {name}.html")
    else:
        print(f"{name}.html: SVG path OK")

print("\nDone!")
