import pyglet

import requests

import time
import random


def get_quote_ming() -> str:
    # 通过aa1接口获取激励语 / Get through aa1
    return requests.get('https://v.api.aa1.cn/api/api-wenan-mingrenmingyan/index.php?aa1=text').text[3:-4]


def get_bg_bing_daily() -> None:
    # 获取每日一图 / Get Bing Daily
    with open('bg.jpeg', 'wb') as bg:
        bg.write(requests.get(
            'https://cn.bing.com' +
            str(requests.get(
                'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1').json()['images'][0]['urlbase']) +
            '_UHD.jpg').content)


def format_quote(quote: str) -> str:
    # 简单的中文格式化 / Simple Chinese Formation
    result = list(quote)
    # 奇怪的算法 / Fucking Ridiculous Algorithm
    offset = 0
    for index, item in enumerate(result.copy()):
        if item == '—':
            result.insert(index + offset, '\n\t\t')
            break
        elif item == '，' or item == '。':
            result.insert(index + 1 + offset, '\n')
            offset += 1
    return ''.join(result)


print('Download Background from Bing')
# 获取必应每日一图 / Get Bing Daily Image
get_bg_bing_daily()

# 初始化窗口 / Initialize Window
window = pyglet.window.Window(width=1920, height=1080)

# 激励语标签 / Quote Label
label_quote = pyglet.text.Label(
    '爷是激励语 By.woshishabii',
    bold=True,
    font_name='Time New Roman',
    font_size=36,
    x=window.width // 2, y=window.height // 2,
    anchor_x='center', anchor_y='baseline',
    align='center',
    multiline=True,
    width=window.width - 250, height=window.height
)

bg_image = pyglet.image.load('bg.jpeg')

last_click = 0.0


@window.event
def on_draw():
    # 渲染事件 / Render Event
    window.clear()
    bg_image.blit(0, 0)
    label_quote.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    # 鼠标点击事件 / Mouse Press Event
    global last_click
    print('Click Event: ', x, y, button, modifiers)
    # 检查是否为双击 / Check If Double-Clicked
    if time.time() - last_click < 0.5:
        window.close()
    else:
        last_click = time.time()
    if x <= window.width // 2 and y <= window.height // 2:
        # 屏幕左下 -> 刷新激励语
        _ = format_quote(get_quote_ming())
        label_quote.text = _
        print(_)
    elif x <= window.width // 2 and y >= window.height // 2:
        # 屏幕左上 -> 评分激励语
        print('Rating...')
        _ = requests.post('http://jgbsxx20130315.pythonanywhere.com/api/v1/quote/rated',
                          json={'content': label_quote.text})
        print(_)
    elif x >= window.width // 2 and y <= window.height // 2:
        # 屏幕右下 -> 优质激励语
        print('Getting Rated Quotes')
        q = requests.get('http://jgbsxx20130315.pythonanywhere.com/api/v1/quote/rated').json()['Items']
        _ = q[str(random.randint(1, len(q)))]
        print(_)
        label_quote.text = _


# 运行
pyglet.app.run()