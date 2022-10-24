import streamlit as st
import streamlit.components.v1 as stc

import jieba
import pinyin
import re


def create_pinyin_ruby(text):
    """是 -> <ruby>是<rp>(</rp><rt>shì</rt><rp>)</rp></ruby>\n"""
    segments = jieba.cut(text)

    ret = ''
    had_non_cn = False
    for s in segments:
        # if it's Chinese, ruby and append it.
        if re.match(r'[\u4e00-\u9fff]+', s):  # are Chinese characters
            py = pinyin.get(s, delimiter='')
            if had_non_cn:
                ret += '\n'
                had_non_cn = False
            ret += f'<ruby>{s}<rp>(</rp><rt>{py}</rt><rp>)</rp></ruby>\n'
        else:  # if it's not, just append it.
            ret += s
            had_non_cn = True

    if had_non_cn:
        ret += '\n'

    return ret


def create_pinyin_numerical(text):
    """是 -> 是 shi4"""
    segments = jieba.cut(text)

    ret = ''
    had_non_cn = False
    for s in segments:
        # if it's Chinese, ruby and append it.
        if re.match(r'[\u4e00-\u9fff]+', s):  # are Chinese characters
            if had_non_cn:
                ret += ' '
                had_non_cn = False
            py = pinyin.get(s, format='numerical', delimiter='')
            ret += f'{s} {py} '
        else:  # if it's not, just append it.
            ret += f'{s}'
            had_non_cn = True

    ret = ret.replace(' 。', '。')
    return ret


def main():
    st.title('🐉Chinese Pinyin Adder')
    st.text('Not sure how to read Chinese characters? Add some pinyin to them!')
    sample_text = '长城（the Great Wall），又称万里长城，是中国古代的军事防御工事，是一道高大、坚固而且连绵不断的长垣，用以限隔敌骑的行动。长城不是一道单纯孤立的城墙，而是以城墙为主体，同大量的城、障、亭、标相结合的防御体系。'
    text = st.text_area(
        label='Enter a Chinese text (below is a sample text)', value=sample_text, height=300)

    # execute button
    add_btn_ph = st.empty()
    add_btn = add_btn_ph.button('Add pinyin', disabled=False, key='1')
    text_wait = st.empty()
    if add_btn:
        add_btn_ph.button('Add pinyin', disabled=True, key='2')
        text_wait.markdown('**Adding...**')

        # process it
        ruby = create_pinyin_ruby(text)
        num = create_pinyin_numerical(text)

        add_btn_ph.button('Add pinyin', disabled=False, key='3')
        text_wait.empty()

        st.subheader('🧧Pinyin ruby')
        stc.html(ruby, height=300, scrolling=True)
        st.subheader('👲Original ruby')
        st.text_area(label='', value=ruby, height=300)
        st.subheader('🥮Pinyin numerical expression')
        st.text_area(label='', value=num, height=300)


if __name__ == '__main__':
    main()
