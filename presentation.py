from flask import Flask, render_template
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter

app = Flask(__name__)

# load the csv file
df = pd.read_csv('profiles.csv')

# generate required images
# locations of Alumni
locations = list(
    df['location'].str.split(',').apply(lambda x: x[-1].strip()).apply(lambda x: x if x == 'Canada' else 'Other'))
c = Counter(locations)
labels = c.keys()
sizes = c.values()
plt.figure()
plt.pie(sizes, labels=labels, autopct='%.0f%%')
plt.legend()
plt.savefig('static/images/locations.png', bbox_inches='tight')

# Current job status
locations = list(df['job title'].apply(lambda x: 'No job' if pd.isna(x) else 'Has job'))
c = Counter(locations)
labels = c.keys()
sizes = c.values()
plt.figure()
plt.pie(sizes, labels=labels, autopct='%.0f%%')
plt.legend()
plt.savefig('static/images/jobs.png', bbox_inches='tight')

# Job titles
text = ' '.join(list(df['job title'].dropna()))
# Create and generate a word cloud image
word_cloud = WordCloud(random_state=8).generate(text)
plt.figure()
plt.imshow(word_cloud, interpolation='bilinear', cmap='YlGnBu')
plt.axis("off")
plt.savefig('static/images/job_title.png', bbox_inches='tight')

# Skills
text = ' '.join(list(df['skills'].dropna()))
# Create and generate a word cloud image
word_cloud = WordCloud(random_state=10).generate(text)
plt.figure()
plt.imshow(word_cloud, interpolation='bilinear', cmap='YlGnBu')
plt.axis("off")
plt.savefig('static/images/skills.png', bbox_inches='tight')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5050)
