import csv
import pandas as pd
import io

def split_articles(data):
    articles = []
    current_article = {}
    for line in data.strip().split('\n'):
        if ',' in line:
            title, content = line.split(',', 1)
            current_article['title'] = title.strip()
            current_article['content'] = content.strip()
            articles.append(current_article)
            current_article = {}
        else:
            if 'content' not in current_article:
                current_article['content'] = ''
            current_article['content'] += f' {line.strip()}'
    return articles

def process_data(data):
    articles = split_articles(data)
    df = pd.DataFrame(articles)
    return df

with open('output (2).csv', 'r', errors='ignore', encoding='utf-8') as f:
    data = f.read()
    df = process_data(data)
    output_file = io.StringIO()
    df.to_csv(output_file, index=False)
    output_data = output_file.getvalue()

with open('normalized_data.csv', 'w', encoding='utf-8') as f:
    f.write(output_data)
