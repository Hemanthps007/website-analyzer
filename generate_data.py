import csv
import random

domains = ['com', 'org', 'net', 'io', 'co', 'ai', 'edu', 'gov', 'biz', 'info']
words = ['tech', 'health', 'foundation', 'global', 'solutions', 'digital', 'data', 'cloud', 'system', 'smart', 'media', 'web', 'app', 'next', 'group', 'innovate', 'create', 'build', 'connect', 'market', 'vision', 'future', 'base', 'hub', 'lab', 'network', 'soft', 'code', 'dev', 'ops', 'project', 'science', 'nature', 'city', 'state', 'public', 'art', 'design', 'studio', 'agency', 'local', 'global', 'trust', 'care', 'fund', 'life', 'earth']

def generate_row(i):
    # generate random URL
    name_parts = random.sample(words, random.randint(1, 3))
    name = "".join(name_parts) + (str(i) if random.random() > 0.8 else "")
    domain = random.choice(domains)
    url = f"https://{name}.{domain}"
    
    # generate realistic but random scores
    base_quality = random.uniform(0.2, 1.0) # Determines overall quality of this mock site
    
    vd = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    me = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    cc = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    acc = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    nav = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    cv = round(min(9.9, max(1.0, base_quality * 10 + random.uniform(-1.5, 1.5))), 1)
    
    avg_score = (vd + me + cc + acc + nav + cv) / 6
    issues = max(0, int((10 - avg_score) * random.uniform(2, 6)))
    critical = max(0, int(issues * random.uniform(0.1, 0.5)))
    gain = min(100, max(0, int((10 - avg_score) * random.uniform(6, 12))))
    
    return [url, vd, me, cc, acc, nav, cv, issues, critical, gain]

with open('dataset.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for i in range(1000):
        writer.writerow(generate_row(i))

print("1000 rows added to dataset.csv")
