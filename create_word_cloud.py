import jieba, codecs, sys, pandas
import numpy as np
from wordcloud import WordCloud
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
from os import listdir
from os.path import isfile, join

stopwords_filename = 'data/stopwords.txt'
font_filename = 'fonts/STZHONGS.ttf'
template_dir = 'data/templates/'

def main(input_filename):
    content = '\n'.join([line.strip()
                        for line in codecs.open(input_filename, 'r', 'utf-8')
                        if len(line.strip()) > 0])
    stopwords = set([line.strip()
                    for line in codecs.open(stopwords_filename, 'r', 'utf-8')])

    segs = jieba.cut(content)
    words = []
    for seg in segs:
        word = seg.strip().lower()
        if len(word) > 1 and word not in stopwords:
            words.append(word)

    words_df = pandas.DataFrame({'word':words})
    words_stat = words_df.groupby(by=['word'])['word'].agg({'number' : np.size})
    words_stat = words_stat.reset_index().sort_values(by="number",ascending=False)

    print '# of different words =', len(words_stat)

    do_job("love.png", words_stat)


def do_job(file, words_stat):
    background_picture_filename = join(template_dir, file)
    if isfile(background_picture_filename):
        prefix = file.split('.')[0]

        bimg = imread(background_picture_filename)
        wordcloud = WordCloud(font_path=font_filename,
                              width=900,
                              height=600,
                              background_color='white',
                              # mask=bimg,
                              max_font_size=170,
                              random_state=100)
        wordcloud = wordcloud.fit_words(dict(words_stat.head(4000).itertuples(index=False)))

        # bimgColors=ImageColorGenerator(bimg)
        # wordcloud.recolor(color_func=bimgColors)

        output_filename = 'output.png'

        print 'Saving', output_filename
        wordcloud.to_file(output_filename)


if __name__ == '__main__':
    main("example.txt")
    # if len(sys.argv) == 2:
    #     main(sys.argv[1])
    # else:
    #     print '[usage] <input>'



