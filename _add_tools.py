import json
import os

filepath = r'D:\Users\taojiang\Documents\GitHub\ZenTools\data\tools-data.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_tools = [
    {
        "name": "图片对比",
        "name__en": "Image Compare",
        "name__ja": "画像比較",
        "name__vi": "So sánh ảnh",
        "slug": "image-compare",
        "category": "图片工具",
        "url": "/image/image-compare.html",
        "description": "使用滑块对比两张图片，支持原图与处理后的效果对比",
        "description__en": "Compare two images with a draggable slider, before/after effect",
        "description__ja": "スライダーで2枚の画像を比較、before/after表示",
        "description__vi": "So sánh hai ảnh bằng thanh trượt, hiệu ứng trước/sau",
        "icon": "🔍",
        "featured": False,
        "new": True,
        "keywords": "图片对比 图片比较 前后对比 图片diff before after"
    },
    {
        "name": "图片加边框",
        "name__en": "Image Border",
        "name__ja": "画像に枠線",
        "name__vi": "Thêm viền ảnh",
        "slug": "image-border",
        "category": "图片工具",
        "url": "/image/image-border.html",
        "description": "为图片添加自定义颜色和宽度的边框",
        "description__en": "Add custom colored borders to images with adjustable width",
        "description__ja": "画像に色と幅を指定して枠線を追加",
        "description__vi": "Thêm viền màu tùy chỉnh cho ảnh",
        "icon": "🖼️",
        "featured": False,
        "new": True,
        "keywords": "图片加边框 图片边框 照片边框 边框工具"
    },
    {
        "name": "图片添加阴影",
        "name__en": "Drop Shadow",
        "name__ja": "ドロップシャドウ",
        "name__vi": "Đổ bóng",
        "slug": "drop-shadow",
        "category": "图片工具",
        "url": "/image/drop-shadow.html",
        "description": "为图片添加投影效果，可调节模糊、偏移和颜色",
        "description__en": "Add drop shadow to images with adjustable blur, offset and color",
        "description__ja": "画像にぼかし、オフセット、色を調整可能な影を追加",
        "description__vi": "Thêm bóng đổ cho ảnh, điều chỉnh độ mờ, khoảng cách và màu",
        "icon": "🌓",
        "featured": False,
        "new": True,
        "keywords": "图片阴影 投影效果 图片投影 阴影工具 drop shadow"
    },
    {
        "name": "图片调色",
        "name__en": "Color Tune",
        "name__ja": "色調調整",
        "name__vi": "Chỉnh màu",
        "slug": "color-tune",
        "category": "图片工具",
        "url": "/image/color-tune.html",
        "description": "精细调整图片的色相、饱和度、明度和色温",
        "description__en": "Fine-tune hue, saturation, lightness and color temperature",
        "description__ja": "色相、彩度、明度、色温度を細かく調整",
        "description__vi": "Tinh chỉnh màu sắc, độ bão hòa, độ sáng và nhiệt độ màu",
        "icon": "🎨",
        "featured": False,
        "new": True,
        "keywords": "图片调色 色相调整 饱和度 明度 色温 hsla调整"
    },
    {
        "name": "图片变素描",
        "name__en": "Photo to Sketch",
        "name__ja": "写真をスケッチに",
        "name__vi": "Ảnh thành bản phác thảo",
        "slug": "sketch",
        "category": "图片工具",
        "url": "/image/sketch.html",
        "description": "将照片一键转换为铅笔素描画效果",
        "description__en": "Convert photos to pencil sketch effects with one click",
        "description__ja": "写真をワンクリックで鉛筆スケッチ風に変換",
        "description__vi": "Chuyển ảnh thành hiệu ứng phác thảo bút chì",
        "icon": "✏️",
        "featured": False,
        "new": True,
        "keywords": "图片素描 素描效果 图片变素描 铅笔素描 照片变素描"
    }
]

data['tools'].extend(new_tools)
print(f'Total tools after adding: {len(data["tools"])}')

with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('File updated successfully!')
