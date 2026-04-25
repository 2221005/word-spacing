# -*- coding: utf-8 -*-
import streamlit as st
from kiwipiepy import Kiwi

# Kiwi 초기화
kiwi = Kiwi()

st.title("띄어쓰기 교정기 (Kiwi)")

# 입력창
text_input = st.text_area("원본 문장 입력", placeholder="여기에 문장을 입력하세요.")

# 띄어쓰기 교정 함수
def correct_spacing(text):
    sentences = kiwi.split_into_sents(text)
    corrected_text_parts = []

    for sent_obj in sentences:
        tokens = kiwi.tokenize(sent_obj.text)

        if not tokens:
            continue

        reconstructed_sentence_parts = [tokens[0].form]

        for i in range(1, len(tokens)):
            current_token = tokens[i]

            should_attach = False
            if current_token.tag.startswith('J') or \
               current_token.tag.startswith('E') or \
               current_token.tag.startswith('X') or \
               current_token.tag in ['SF', 'SS', 'SP', 'SSO', 'SSC', 'SY']:
                should_attach = True

            if should_attach:
                reconstructed_sentence_parts.append(current_token.form)
            else:
                reconstructed_sentence_parts.append(' ' + current_token.form)

        corrected_text_parts.append(''.join(reconstructed_sentence_parts).strip())

    return ' '.join(corrected_text_parts).replace('  ', ' ')

# 버튼
if st.button("띄어쓰기 교정"):
    if text_input:
        result = correct_spacing(text_input)
        st.success(f"교정된 문장: {result}")
    else:
        st.error("문장을 입력해주세요.")