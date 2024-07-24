from PIL import Image as PILImage
from nonebot import on, on_command, on_startswith
from nonebot.rule import to_me
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.adapters import Event
from nonebot.adapters import Bot
from nonebot.rule import startswith
import shutil
import os
import copy
import json
import base64
import httpx
import requests


class UserArguments:
    base_dir = r'/home/richardxue/notwork/qqbot_data'

    def __init__(self):
        # 初始化一个空字典来存储用户参数
        self.user_map = {}
        # 加载已有的用户配置
        self.load_existing_users()

    def load_existing_users(self):
        # 遍历 base_dir 目录下的所有项目
        for folder_name in os.listdir(self.base_dir):
            folder_path = os.path.join(self.base_dir, folder_name)
            # 确保这个项目是一个目录
            if os.path.isdir(folder_path):
                config_path = os.path.join(folder_path, 'config.json')
                # 确保 config.json 文件存在
                if os.path.isfile(config_path):
                    # 尝试打开并解析 JSON 文件
                    try:
                        with open(config_path, 'r', encoding='utf-8') as f:
                            # 将文件名（不含扩展名）转换为整数作为 user_id
                            user_id = int(folder_name.split('.')[0])
                            # 加载 JSON 数据到 user_map 字典中对应的 user_id 键
                            self.user_map[user_id] = json.load(f)
                    except ValueError:
                        print(f"Error: Folder name '{folder_name}' is not a valid user ID.")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file '{config_path}': {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred while loading '{config_path}': {e}")
                else:
                    print(f"Skipping non-file or empty config: {config_path}")
            else:
                print(f"Skipping non-directory: {folder_path}")

    def add_user(self, user_id, arguments):
        # 添加或更新用户参数
        self.user_map[int(user_id)] = arguments

    def get_user_arguments(self, user_id):
        # 根据用户ID获取参数
        return self.user_map.get(int(user_id), None)

    def remove_user(self, user_id):
        # 根据用户ID删除参数
        if int(user_id) in self.user_map:
            del self.user_map[int(user_id)]

    def save_user(self, user_id):
        # 将用户参数保存到专属文件夹中的config.json文件
        user_dir = os.path.join(self.base_dir, str(user_id))
        config_path = os.path.join(user_dir, 'config.json')
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        with open(config_path, 'w') as f:
            json.dump(self.user_map[int(user_id)], f, indent=4)

    def save_all_users(self):
        # 保存所有用户的参数s
        for user_id, arguments in self.user_map.items():
            self.save_user(int(user_id))


user_args = UserArguments()

paint_rule = Rule(to_me(), startswith(".paint", ignorecase=False))

setu = on_command("pic", rule=to_me(), aliases={"setu", "发图片"}, priority=10, block=True)
help = on_command("help", rule=to_me(), aliases={"help", "帮助"}, priority=10, block=True)
default = on_command("ex", rule=to_me(), aliases={"default", "默认配置"}, priority=10, block=True)
setuToGroup = on_command("pg", rule=to_me(), aliases={"setuToGroup", "给群聊发图片"}, priority=10, block=True)
p2p = on_command("p2p", rule=to_me(), aliases={"p2p", "p2p"}, priority=10, block=True)
data = on_command("data", rule=to_me(), aliases={"data", "p2p data"}, priority=10, block=True)

help = on_startswith(".taffyhelp", ignorecase=False)
test = on_startswith(".paint", ignorecase=False)
getconfex = on_startswith(".getconfex", ignorecase=False)
setconfig = on_startswith(".setconfig", ignorecase=False)
getconfig = on_startswith(".getconfig", ignorecase=False)
getlora = on_startswith(".getlora", ignorecase=False)
getsdmodel = on_startswith(".getsdmodel", ignorecase=False)
setsdmodel = on_startswith(".setsdmodel", ignorecase=False)
draw = on_startswith(".draw", ignorecase=False)

qqGroup_test = 964880841
qqGroup_main = 754954614

save_dir = '/home/richardxue/notwork/qqbot_data'
save_file = 'tmp_p2p.png'

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
    'seed': -1,
    'steps': 30,
    'width': 600,
    'height': 800,
    'cfg_scale': 7,
    'n_iter': 1,
}
default_prompt = ("score_9,score_8_up,score_7_up,")
default_negative_prompt = ("(score_4,score_3,score_2,score_1), ugly, worst quality,bad hands,bad feet,")
detail_argument = {
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


@setconfig.handle()
async def _(bot: Bot, event: Event):
    args = event.get_plaintext()[11:].strip()
    args_dict = []
    try:
        # 假设参数是JSON格式的字符串，使用json.loads进行解析
        args_dict = json.loads(args)
    except json.JSONDecodeError:
        await setconfig.finish("参数格式错误哦，要确保是有效的JSON对象哟~ (￣▽￣)ノ")

        # 检查解析后的参数是否为字典
    if not isinstance(args_dict, dict):
        await setconfig.finish("参数必须是字典格式哦~ (≧∀≦)ノ")
        # 获取当前事件的用户ID
    user_id = event.get_user_id()

    # 检查用户是否已经有配置，如果没有则初始化一个空字典
    if int(user_id) not in user_args.user_map:
        user_args.user_map[int(user_id)] = {}

    # 更新字典中的参数
    # 这里假设args_dict已经是字典格式，直接更新即可
    user_args.user_map[int(user_id)].update(args_dict)

    # 保存用户配置到专属文件夹
    user_args.save_user(user_id)

    # 响应用户
    await setconfig.finish("配置已经更新完毕啦~ (๑>◡<๑) 请放心使用哦~")


@getconfig.handle()
async def _(bot: Bot, event: Event):
    # 获取当前事件的用户ID
    user_id = event.get_user_id()
    # 从user_args中获取用户配置
    user_arg = user_args.get_user_arguments(user_id)
    # 响应用户
    if user_arg:
        await getconfig.send("这是你的配置哦~ (*＾▽＾)／ 请检查一下~")
        await getconfig.finish(json.dumps(user_arg, indent=4))
    else:
        await getconfig.send("你还没有配置好哦~ 快去设置一下吧~ (≧ω≦)/")

@getconfex.handle()
async def _(bot: Bot, event: Event):
    await getconfex.send("这是配置的例子哦~ 请参考一下吧~ (＾▽＾)")
    await getconfex.finish(json.dumps(default_argument, indent=4))

@getlora.handle()
async def _(bot: Bot, event: Event):
    # 定义API的URL
    url = 'http://127.0.0.1:7861/sdapi/v1/loras'

    try:
        # 发送GET请求
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # 确保请求成功
        if response.status_code == 200:
            # 获取JSON响应内容
            json_response = response.json()

            for item in json_response:
                # 添加'usage'键
                item['usage'] = f"<lora:{item['alias']}:0.8>"
                del item['alias']
            # 将JSON转换为字符串形式
            json_str = json.dumps(json_response, ensure_ascii=False, indent=4)

            # 发送JSON字符串给用户
            await getlora.send(f"获取到的Lora模型如下：\n{json_str}")
        else:
            # 如果响应码不是200，通知用户请求失败
            await getlora.finish(f"请求失败，状态码：{response.status_code}")

    except httpx.HTTPError as e:
        # 网络请求异常处理
        await getlora.finish(f"网络请求出错：{e}")
    except Exception as e:
        # 其他异常处理
        await getlora.finish(f"发生错误：{e}")

@getsdmodel.handle()
async def _(bot: Bot, event: Event):
    # 定义API的URL
    url = 'http://127.0.0.1:7861/sdapi/v1/sd-models'

    try:
        # 发送GET请求
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # 确保请求成功
        if response.status_code == 200:
            # 获取JSON响应内容
            json_response = response.json()

            # 将JSON转换为字符串形式
            titles = [item['title'] for item in json_response]

            json_str = '\n'.join(titles)

            # 发送JSON字符串给用户
            await getsdmodel.send(f"获取到的SD模型如下：\n{json_str}")
        else:
            # 如果响应码不是200，通知用户请求失败
            await getsdmodel.finish(f"请求失败，状态码：{response.status_code}")

    except httpx.HTTPError as e:
        # 网络请求异常处理
        await getsdmodel.finish(f"网络请求出错：{e}")
    except Exception as e:
        # 其他异常处理
        await getsdmodel.finish(f"发生错误：{e}")

@setsdmodel.handle()
async def _(bot: Bot, event: Event):
    # 定义API的URL
    url = 'http://127.0.0.1:7861/sdapi/v1/options'

    user_input = event.get_plaintext()[11:].strip()

    # 定义POST请求的JSON体
    json_data = {
        "sd_model_checkpoint": user_input
    }

    try:
        # 发送POST请求
        async with httpx.AsyncClient() as client:
            await setsdmodel.send(f"模型切换请求已发送")
            response = await client.post(url, json=json_data)

        # 确保请求成功
        if response.status_code == 200:
            # 处理成功的逻辑
            await setsdmodel.send(f"已成功设置模型为：{user_input}")
        else:
            # 如果响应码不是200，通知用户请求失败
            await setsdmodel.finish(f"请求失败，状态码：{response.status_code}")

    except Exception as e:
        # 发生异常，获取错误信息
        if e:
            await setsdmodel.finish()
        else:
            # 发送错误消息，确保不会发送空消息
            await setsdmodel.finish(f"发生错误：{e}")


@draw.handle()
async def _(bot: Bot, event: Event):
    # 获取当前事件的用户ID
    user_id = event.get_user_id()
    # 从user_args中获取用户配置
    user_arg = user_args.get_user_arguments(user_id)
    if not user_arg:
        await draw.finish("你还没有配置好哦~ 快去设置一下吧~ (≧ω≦)/")
    # 响应用户
    print(user_arg)
    await draw.send("好哒，正在为你生成呢~ (≧▽≦)/✧")
    image_paths = await get_data(user_arg)
    for image_path in image_paths:
        await draw.send(MessageSegment.image(f'file:///{image_path}'))
    await draw.finish("所有图片都生成好啦~ (≧ω≦)/✿✨")


@test.handle()
async def _(bot: Bot, event: Event):
    session_id = event.get_session_id()
    args = event.get_plaintext()[6:].strip()
    print(args)
    args_legal = read_args(args)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(current_argument)
    if args_legal:
        await setu.send("收到，开始生成")
        image_paths = await get_data(current_argument)
        for image_path in image_paths:
            await setu.send(MessageSegment.image(f'file:///{image_path}'))
        if session_id.startswith('group'):
            # 判断为群聊
            try:
                # 移除'group'前缀并分割字符串
                group_id, user_id = session_id[6:].split('_', 1)
                print(f"群聊: 群ID={group_id}, QQ号={user_id}")
                group_member_info_json = await bot.get_group_member_info(group_id=group_id, user_id=user_id,
                                                                         no_cache=True)
                user_name = group_member_info_json['card'] if group_member_info_json['card'] \
                    else (group_member_info_json['nickname'] if group_member_info_json['nickname']
                          else group_member_info_json['user_id'])
                await test.finish(Message(f"[CQ:at,qq={user_id}]" + " 所有图片已经生成啦~ (≧ω≦)b 请查收哦~"))
            except ValueError:
                # 如果分割失败，返回错误信息
                await test.finish("无效的群聊会话ID")
        else:
            # 判断为私聊
            print(f"私聊: QQ号={session_id}")
            user_name = await bot.call_api('get_stranger_info', user_id=session_id)
            await setu.finish("所有图片已经生成啦~ (≧ω≦)b 请查收哦~")

    else:
        await setu.finish(f"参数解析失败")


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
        image_paths = await get_data(current_argument)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(image_paths)
        for image_path in image_paths:
            await setu.send(MessageSegment.image(f'file:///{image_path}'))
        await setu.finish("所有图片已生成")
    else:
        await setu.finish(f"参数解析失败")


@setuToGroup.handle()
async def handle_function1_1(bot: Bot, event: Event, args: Message = CommandArg()):
    global current_argument
    global default_argument
    arg_text = args.extract_plain_text().strip()
    args_legal = read_args(arg_text)
    if args_legal:
        group_member_info_json = await bot.get_group_member_info(group_id=qqGroup_main, user_id=event.get_user_id(),
                                                                 no_cache=True)
        await setuToGroup.send("收到，开始生成")
        image_path = await get_data(current_argument)
        await bot.send_group_msg(group_id=qqGroup_main, message=MessageSegment.image(f'file:///{image_path}'))
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
            target_folder = os.path.join(save_dir, save_folder)
            target_dir = os.path.join(save_dir, save_folder, save_file)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.copy(file_addr, target_dir)
            with PILImage.open(target_dir) as img:
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

    img_addr = os.path.join(save_dir, user_id, save_file)
    try:
        # 尝试打开图像文件
        with PILImage.open(img_addr) as img:
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
    await p2p.finish(MessageSegment.image(f'file:///{image_path}'))


@help.handle()
async def handle_function2():
    await help.finish(f"使用示例: @bot + /命令 + 空格 + 模式 + 生成参数\n"
                      f"命令大全：/pic：图片生成输出至默认窗口；/pg：指定输出到群聊；/ex：获得生成参数示例\n"
                      f"模式大全：-op: 仅输入prompt，其余参数默认，种子随机；-oph: 同op模式，默认加NSFW特调LoRA；-all: 手动输入所有参数。\n"
                      f"图生图 : /p2p -pd <denoising_strength>(float,0-1) <prompt>(string)\n"
                      f"上传图生图基础图片 : /data <image>(image,res<3840*2160)\n"
                      f"@@@@@@ NEW FEATURE @@@@@@\n"
                      ".getconfex\n"
                      ".setconfig + /return + {config}\n"
                      ".getconfig\n"
                      ".draw\n"
                      ".getlora\n"
                      ".getsdmodel\n"
                      ".setsdmodel\n"
                      "JOIN US: https://github.com/RichardXue123/qqbot\n"
                      )


@default.handle()
async def handle_function3():
    await help.finish(json.dumps(default_argument, indent=4))


def read_args(arg_text):
    global current_argument
    global default_argument
    try:
        if arg_text.startswith('-oph'):
            prompt = arg_text[3:].strip()
            current_argument.update(default_argument)
            current_argument['prompt'] = "".join([default_prompt, "<lora:Expressive_H:0.8>,", prompt])
            current_argument['negative_prompt'] = "".join(default_negative_prompt)
        elif arg_text.startswith('-op'):
            prompt = arg_text[2:].strip()
            current_argument = copy.copy(default_argument)
            current_argument['prompt'] = "".join([default_prompt, prompt])
            current_argument['negative_prompt'] = "".join(default_negative_prompt)
        elif arg_text.startswith('-all'):
            user_data = json.loads(arg_text[4:].strip())
            required_keys = {'prompt', 'negative_prompt', 'sampler_name', 'scheduler', 'seed', 'steps', 'width',
                             'height', 'cfg_scale', 'n_iter'}
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
    image_paths = []
    for i in range(user_data['n_iter']):
        save_image_path = os.path.join(save_dir, 'img', f'tmp_{i + 1}.png')
        save_encoded_image(response.json()['images'][i], save_image_path)
        image_paths.append(save_image_path)
    return image_paths


async def get_p2p(user_prompt):
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/img2img'
    print(user_prompt['prompt'])
    print(user_prompt['negative_prompt'])
    print(user_prompt['denoising_strength'])
    response = submit_post(txt2img_url, user_prompt)
    save_image_path = os.path.join(save_dir, 'img', f'tmp.png')
    save_encoded_image(response.json()['images'][0], save_image_path)

    return save_image_path


def is_resolution_within_limit(image_path, limit=1200):
    global default_p2p_argument
    with PILImage.open(image_path) as img:
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
