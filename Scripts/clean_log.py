import re

def clean_chat_log(input_path, output_path):
    """
    清洗聊天记录文本，过滤时间戳和系统消息，保留纯净对话。
    """
    # 常见的系统噪音关键词，遇到包含这些词的行直接跳过
    noise_keywords = ["撤回了一条消息", "收到转账", "发出红包", "通话时长", "加入群聊"]
    
    # 用正则表达式匹配常见的时间戳格式（例如：2026-05-22 17:00:00 昵称）
    # \d{4}-\d{2}-\d{2} 匹配日期，\d{2}:\d{2}:\d{2} 匹配时间
    header_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)')

    cleaned_dialogues = []
    current_speaker = None

    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            
            # 1. 检查当前行是否是“消息头”（包含时间和昵称）
            match = header_pattern.match(line)
            if match:
                # 提取出昵称，更新当前说话人状态
                current_speaker = match.group(2)
                continue
            
            # 2. 检查当前行是否包含系统噪音
            if any(keyword in line for keyword in noise_keywords):
                continue
            
            # 3. 如果当前行是正文，且我们已经知道了说话人，就记录下来
            if current_speaker and not line.startswith('[图片]') and not line.startswith('[表情]'):
                cleaned_dialogues.append(f"{current_speaker}: {line}\n")

    # 将清洗后的结果写入新文件
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(cleaned_dialogues)
    
    print(f"🎉 清洗完成！纯净语料已保存至: {output_path}")

# ==================== 使用示例 ====================
# 在本地运行时，把你的原始聊天记录命名为 'raw_chat.txt' 放在同目录下即可
if __name__ == "__main__":
    # clean_chat_log("raw_chat.txt", "cleaned_chat.txt")
    pass
