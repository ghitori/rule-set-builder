import re

def regex(text: str):
    text = re.sub(r'\.', r'\.', text)
    text = re.sub(r'(\[[^\[\]]*\])(?!\*)', r'\1*', text)
    text = re.sub(r'(?<!\])\*', r'.*', text)
    return(text)

def wildcard(text: str):
    text = regex(text)
    text = re.sub(r'\\\.', r'.', text)
    text = re.sub(r'\.\*', r'*', text)
    text = re.sub(r'(\[[^\[\]]*\])\*', r'*', text)
    return(text)
