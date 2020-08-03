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


def without_stopwords(left, right):
    sent_shift = sh.WeightedAvgShift(
        type2freq_1=left.to_dict(),
        type2freq_2=right.to_dict(),
        type2score_1="labMT_English",
        stop_lens=[(4,6)],
        stop_words={'set_of_words', 'to_exclude_manually'},
        reference_value='average'
    )

    s_avg_1 = sent_shift.get_weighted_score(sent_shift.type2freq_1, sent_shift.type2score_1)
    s_avg_2 = sent_shift.get_weighted_score(sent_shift.type2freq_2, sent_shift.type2score_2)
    title = (
        'Moby Dick by Herman Melville\n'
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
    plt.savefig('output/casestudy_moby_dick.pdf')
    # plt.show()


def with_stopwords(left, right):

    stop_words = {'coffin', 'cry', 'cried'}

    sent_shift = sh.WeightedAvgShift(
        type2freq_1=left.to_dict(),
        type2freq_2=right.to_dict(),
        type2score_1="labMT_English",
        stop_lens=[(4,6)],
        stop_words=stop_words,
        reference_value='average'
    )

    s_avg_1 = sent_shift.get_weighted_score(sent_shift.type2freq_1, sent_shift.type2score_1)
    s_avg_2 = sent_shift.get_weighted_score(sent_shift.type2freq_2, sent_shift.type2score_2)
    title = (
        'Moby Dick by Herman Melville, with Stop Words\n'
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
    plt.savefig('output/casestudy_moby_dick_with_stopwords.pdf', bbox_inches='tight')
    # plt.show()


def main():
    words = get_hedonometer_ordered_labMT_words().iloc[:,0].values
    df = get_csv()
    df.columns = range(df.shape[1])
    df.index = words
    left = df.iloc[:, 1:floor(df.shape[1]/2)].sum(axis=1)
    right = df.iloc[:, floor(df.shape[1]/2):].sum(axis=1)

    with_stopwords(left, right)
    without_stopwords(left, right)


if __name__ == '__main__':
    main()