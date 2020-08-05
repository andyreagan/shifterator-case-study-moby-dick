from io import StringIO
from math import floor

import matplotlib.pyplot as plt
import pandas as pd
import requests
import shifterator as sh


def get_hedonometer_ordered_labMT_words(uri="https://hedonometer.org/data/bookdata/labMT/labMTwords-english.csv"):
    r = requests.get(uri)
    r.raise_for_status()
    return pd.read_csv(StringIO(r.content.decode('utf8')), header=None)


def get_csv(uri="https://hedonometer.org/data/bookdata/processed/moby_dick.csv"):
    r = requests.get(uri)
    r.raise_for_status()
    return pd.read_csv(StringIO(r.content.decode('utf8')), header=None)


def make_shift(left,
               right,
               stop_words={'coffin', 'cry', 'cried'},
               suffix='_with_stopwords',
               title='Moby Dick by Herman Melville, with Stop Words'):
    sent_shift = sh.WeightedAvgShift(
        type2freq_1=left,
        type2freq_2=right,
        type2score_1="labMT_English",
        stop_lens=[(4,6)],
        stop_words=stop_words,
        reference_value='average'
    )

    s_avg_1 = sent_shift.get_weighted_score(sent_shift.type2freq_1, sent_shift.type2score_1)
    s_avg_2 = sent_shift.get_weighted_score(sent_shift.type2freq_2, sent_shift.type2score_2)
    print(suffix, s_avg_1, s_avg_2, s_avg_1-s_avg_2)
    title = (
        title
        + "\n"
        + "{}: ".format('First Half')
        + r"$\Phi_{avg}=$"
        + "{0:.2f}".format(s_avg_1)
        + "\n"
        + "{}: ".format('Second Half')
        + r"$\Phi_{avg}=$"
        + "{0:.2f}".format(s_avg_2)
    )

    ax = sent_shift.get_shift_graph(
        system_names = ['First Half', 'Second Half'],
        title=title,
        xlabel=r"Per word average score shift $\delta \Phi_\tau$ (%)",
        serif=True,
        show_plot=False
    )
    ax = sent_shift.get_shift_graph(
        system_names = ['First Half', 'Second Half'],
        title=title,
        xlabel=r"Per word average score shift $\delta \Phi_\tau$ (%)",
        serif=True,
        show_plot=False
    )
    plt.savefig('output/casestudy_moby_dick' + suffix + '.pdf', bbox_inches='tight')
    # plt.show()


def main():
    words = get_hedonometer_ordered_labMT_words().iloc[:,0].values
    df = get_csv()
    df.columns = range(df.shape[1])
    df.index = words
    left = df.iloc[:, 1:floor(df.shape[1]/2)].sum(axis=1).to_dict()
    right = df.iloc[:, floor(df.shape[1]/2):].sum(axis=1).to_dict()

    make_shift(left,
               right,
               stop_words={},
               suffix='',
               title='Moby Dick by Herman Melville')
    make_shift(left,
               right,
               stop_words={'coffin', 'cry', 'cried'},
               suffix='_with_stopwords',
               title='Moby Dick by Herman Melville, with Stop Words')


if __name__ == '__main__':
    main()