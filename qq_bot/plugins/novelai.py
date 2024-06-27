import random
import re
import nonebot
from PIL import Image
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters import Bot
from nonebot_plugin_userinfo import get_user_info
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
import shutil
import os
import copy
import json
import base64
import requests

setu = on_command("pic", rule=to_me(), aliases={"setu", "发图片"}, priority=10, block=True)
help = on_command("help", rule=to_me(), aliases={"help", "帮助"}, priority=10, block=True)
default = on_command("ex", rule=to_me(), aliases={"default", "默认配置"}, priority=10, block=True)
setuToGroup = on_command("pg", rule=to_me(), aliases={"setuToGroup", "给群聊发图片"}, priority=10, block=True)
p2p = on_command("p2p", rule=to_me(), aliases={"p2p", "p2p"}, priority=10, block=True)
data = on_command("data", rule=to_me(), aliases={"data", "p2p data"}, priority=10, block=True)

qqGroup_test = 964880841
qqGroup_main = 754954614

save_dir = 'C:\\XueShengZe\\notwork\\img_for_qqbot\\'
save_file = '\\tmp_p2p.png'

current_argument = {
    'prompt': '',
    'negative_prompt': '',
    "sampler_name": "Euler a",
    "scheduler": "",
    'seed': -1,
    'steps': 25,
    'width': 600,
    'height': 800,
    'cfg_scale': 8
}
default_argument = {
    'prompt': '',
    'negative_prompt': '',
    "sampler_name": "Euler a",
    "scheduler": "",
    'seed': 1234,
    'steps': 25,
    'width': 600,
    'height': 800,
    'cfg_scale': 7,
}
default_prompt = ("score_9,score_8_up,score_7_up,")
default_negative_prompt =("(score_4,score_3,score_2,score_1), ugly, worst quality,bad hands,bad feet,")
detail_argument={
  "prompt": "",
  "negative_prompt": "",
  "styles": [
    "string"
  ],
  "seed": -1,
  "subseed": -1,
  "subseed_strength": 0,
  "seed_resize_from_h": -1,
  "seed_resize_from_w": -1,
  "sampler_name": "string",
  "scheduler": "string",
  "batch_size": 1,
  "n_iter": 1,
  "steps": 50,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "restore_faces": True,
  "tiling": True,
  "do_not_save_samples": False,
  "do_not_save_grid": False,
  "eta": 0,
  "denoising_strength": 0,
  "s_min_uncond": 0,
  "s_churn": 0,
  "s_tmax": 0,
  "s_tmin": 0,
  "s_noise": 0,
  "override_settings": {},
  "override_settings_restore_afterwards": True,
  "refiner_checkpoint": "string",
  "refiner_switch_at": 0,
  "disable_extra_networks": False,
  "firstpass_image": "string",
  "comments": {},
  "enable_hr": False,
  "firstphase_width": 0,
  "firstphase_height": 0,
  "hr_scale": 2,
  "hr_upscaler": "string",
  "hr_second_pass_steps": 0,
  "hr_resize_x": 0,
  "hr_resize_y": 0,
  "hr_checkpoint_name": "string",
  "hr_sampler_name": "string",
  "hr_scheduler": "string",
  "hr_prompt": "",
  "hr_negative_prompt": "",
  "force_task_id": "string",
  "sampler_index": "Euler",
  "script_name": "string",
  "script_args": [],
  "send_images": True,
  "save_images": False,
  "alwayson_scripts": {},
  "infotext": "string"
}

default_p2p_argument = {
    'prompt': 'evil',
    'negative_prompt': '',
    "sampler_name": "Euler a",
    "scheduler": "",
    'seed': -1,
    'steps': 25,
    'width': 600,
    'height': 800,
    'cfg_scale': 7,
    "init_images": [
        "string"
    ],
    "denoising_strength": 0.5
}

@setu.handle()
async def handle_function1(args: Message = CommandArg()):
    global current_argument
    global default_argument
    arg_text = args.extract_plain_text().strip()
    args_legal = read_args(arg_text)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(current_argument)
    if args_legal:
        await setu.send("收到，开始生成")
        image_path = await get_data(current_argument)
        await setu.finish(MessageSegment.image(image_path))
    else:
        await setu.finish(f"参数解析失败")

@setuToGroup.handle()
async def handle_function1_1(bot: Bot, event: Event, args: Message = CommandArg()):
    global current_argument
    global default_argument
    arg_text = args.extract_plain_text().strip()
    args_legal = read_args(arg_text)
    if args_legal:
        group_member_info_json = await bot.get_group_member_info(group_id=qqGroup_main, user_id=event.get_user_id(), no_cache=True)
        await setuToGroup.send("收到，开始生成")
        image_path = await get_data(current_argument)
        await bot.send_group_msg(group_id=qqGroup_main, message=MessageSegment.image(image_path))
        username = group_member_info_json['card'] if group_member_info_json['card'] \
            else (group_member_info_json['nickname'] if group_member_info_json['nickname']
                  else group_member_info_json['user_id'])
        await bot.send_group_msg(group_id=qqGroup_main, message="".join(["图片生成完毕，", username, " 干的"]))
        await setuToGroup.finish()
    else:
        await setuToGroup.finish(f"参数解析失败")

@data.handle()
async def handle_data_function(bot: Bot, event: Event, args: Message = CommandArg()):
    global current_argument
    global default_argument
    user_id = event.get_user_id()
    if not user_id:
        await data.finish("非法的用户id")
    for segment in args:
        if segment.type == "image":
            # 获取file属性
            file = segment.data.get("file")
            print(f"File: {file}")
            # 如果还需要其他属性，可以继续获取
            url = segment.data.get("url")
            print(f"URL: {url}")
            # 如果需要进一步处理文件，可以在这里添加你的代码
            # 例如，调用bot.call_api获取图片内容等
            result = await bot.call_api("get_image", file=file)
            file_addr = result['file']
            print(file_addr)
            ####################
            # 定义源文件路径和目标文件路径
            save_folder = user_id
            # 复制文件
            target_folder = "".join([save_dir, save_folder])
            target_dir = "".join([save_dir, save_folder, save_file])
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.copy(file_addr, target_dir)
            with Image.open(target_dir) as img:
                width, height = img.size
                if width > 3840 or height > 2160:
                    os.remove(target_dir)
                    await p2p.finish("分辨率太高，保存失败")
            await data.finish("".join(["用户", user_id, "的图片已保存到服务器。"]))
    await data.finish("参数解析失败")

@p2p.handle()
async def handle_p2p_function(bot: Bot, event: Event, args: Message = CommandArg()):
    global current_argument
    global default_argument
    global default_p2p_argument
    user_id = event.get_user_id()
    if not user_id:
        await data.finish("非法的用户id")
    # 遍历Message对象中的每一个MessageSegment
    for segment in args:
        if segment.type == 'text':
            text = segment.data.get("text")
            print(text)
            if text.startswith('-pd'):
                # 去掉开头的 '-pd' 部分
                trimmed_string = text[len('-pd'):].strip()
                # 找到第一个空格分隔位置，分离数字部分和剩余部分
                space_index = trimmed_string.find(' ')
                if space_index != -1:
                    pd_value_str = trimmed_string[:space_index].strip()
                    remaining_str = trimmed_string[space_index:].strip()
                    try:
                        pd_value = float(pd_value_str)  # 尝试转换为浮点数
                    except ValueError:
                        pd_value = None
                        await p2p.finish("参数解析失败")
                    default_p2p_argument['denoising_strength'] = pd_value
                    default_p2p_argument['prompt'] = "".join([default_prompt, remaining_str])
                    default_p2p_argument['negative_prompt'] = "".join([default_negative_prompt])
                else:
                    await p2p.finish("参数解析失败")

    img_addr = "".join([save_dir, user_id, save_file])
    try:
        # 尝试打开图像文件
        with Image.open(img_addr) as img:
            width, height = img.size
            default_p2p_argument['width'] = width
            default_p2p_argument['height'] = height
            print(f"Image opened successfully: {img_addr}")
    except IOError as e:
        print(f"Failed to open image {img_addr}: {e}")
        await p2p.finish("小笨蛋，你还没上传过图片呢~")
    with open(img_addr, 'rb') as file:
        ima_data = file.read()
    await p2p.send("收到，开始生成")
    encoded_image = base64.b64encode(ima_data).decode('utf-8')
    default_p2p_argument['init_images'] = [encoded_image]
    image_path = await get_p2p(default_p2p_argument)
    await p2p.finish(MessageSegment.image(image_path))


@help.handle()
async def handle_function2():
    await help.finish(f"使用示例: @bot + /命令 + 空格 + 模式 + 生成参数\n"
                      f"命令大全：/pic：图片生成输出至默认窗口；/pg：指定输出到群聊；/ex：获得生成参数示例\n"
                      f"模式大全：-op: 仅输入prompt，其余参数默认，种子随机；-oph: 同op模式，默认加NSFW特调LoRA；-all: 手动输入所有参数。\n"
                      f"图生图 : /p2p -pd <denoising_strength>(float,0-1) <prompt>(string)\n"
                      f"上传图生图基础图片 : /data <image>(image,res<3840*2160)"
                      )

@default.handle()
async def handle_function3():
    await help.finish(json.dumps(default_argument))

def read_args(arg_text):
    global current_argument
    global default_argument
    try:
        if arg_text.startswith('-oph'):
            prompt = arg_text[3:].strip()
            current_argument.update(default_argument)
            current_argument['prompt'] = "".join(["<lora:Expressive_H:0.8>,", prompt])
            current_argument['negative_prompt'] = "".join(default_negative_prompt)
            current_argument['seed'] = random.randint(1, 10000)
        elif arg_text.startswith('-op'):
            prompt = arg_text[2:].strip()
            current_argument = copy.copy(default_argument)
            current_argument['prompt'] = "".join([default_prompt, prompt])
            current_argument['negative_prompt'] = "".join(default_negative_prompt)
            current_argument['seed'] = random.randint(1, 10000)
        elif arg_text.startswith('-all'):
            user_data = json.loads(arg_text[4:].strip())
            required_keys = {'prompt', 'negative_prompt', 'sampler_name', 'scheduler', 'seed', 'steps', 'width',
                             'height', 'cfg_scale'}
            if not required_keys.issubset(user_data.keys()):
                raise ValueError("缺少必要的键")
            current_argument = copy.copy(user_data)
        else:
            raise ValueError("请输入正确的参数格式: -op 或 -all")
    except (json.JSONDecodeError, ValueError) as e:
        return False
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(current_argument)
    return True

async def get_data(user_data):
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/txt2img'
    response = submit_post(txt2img_url, user_data)
    save_image_path = r'C:\XueShengZe\notwork\img_for_qqbot\tmp.png'
    save_encoded_image(response.json()['images'][0], save_image_path)

    return save_image_path

async def get_p2p(user_prompt):
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/img2img'
    print(user_prompt['prompt'])
    print(user_prompt['negative_prompt'])
    print(user_prompt['denoising_strength'])
    response = submit_post(txt2img_url, user_prompt)
    save_image_path = r'C:\XueShengZe\notwork\img_for_qqbot\tmp.png'
    save_encoded_image(response.json()['images'][0], save_image_path)

    return save_image_path

def is_resolution_within_limit(image_path, limit=1200):
    global default_p2p_argument
    with Image.open(image_path) as img:
        width, height = img.size
        if width > limit or height > limit:
            return False
        default_p2p_argument['width'] = width
        default_p2p_argument['height'] = height
        return True

def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))

# 解码并保存图片
def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))