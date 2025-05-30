import json5

def load(path):
    def balance_brackets(text):
        stack = []
        for c in text:
            if c == '{':
                stack.append('}')
            elif c == '[':
                stack.append(']')
            elif c in ('}', ']'):
                if stack and stack[-1] == c:
                    stack.pop()

        # 补全缺失的右括号
        while stack:
            text += stack.pop()
        return text

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    data = json5.loads(balance_brackets(text))
    return data