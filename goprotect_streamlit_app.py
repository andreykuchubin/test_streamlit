# -*- coding: utf-8 -*-
"""GoProtect_streamlit_app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QuW-pnOpBNUzMvqF1PSV4-clCQ6WfUHM
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Определение функций
def unit_filter(
    df,
    segment_name='Любой',
    unit_level=0,
    is_combo=0,
    is_cascade=0,
    is_clean=0,
    is_jump=0,
    is_spin=0,
    is_step=0
):
    if segment_name == 'Любой':
        df = df[
            (df["unit_level"] == unit_level)
            & (df["is_combo"] == is_combo)
            & (df["is_cascade"] == is_cascade)
            & (df["is_clean"] == is_clean)
            & (df["is_jump"] == is_jump)
            & (df["is_spin"] == is_spin)
            & (df["is_step"] == is_step)
        ]
        result = df.groupby(['unit_id'], as_index=False).agg({'title': ' '.join})
    else:
        df = df[
            (df["segment_name"] == segment_name)
            & (df["unit_level"] == unit_level)
            & (df["is_combo"] == is_combo)
            & (df["is_cascade"] == is_cascade)
            & (df["is_clean"] == is_clean)
            & (df["is_jump"] == is_jump)
            & (df["is_spin"] == is_spin)
            & (df["is_step"] == is_step)
        ]
        result = df.groupby(['unit_id'], as_index=False).agg({'title': ' '.join})

    #text = result['unit_id'].tolist()
    #n = 20
    #parts = [text[i:i + n] for i in range(0, len(text), n)]
    #st.write('Перечень id спортсменов, подходящих под данные критерии:')
    #for part in parts:
        #st.write(part)

    return result


def elements_selection(result, id, n):
    top_n = n
    unit_id = id
    if id in result['unit_id'].tolist():
        vect = CountVectorizer()

        element_matrix = pd.DataFrame(
            vect.fit_transform(result['title']).toarray(),
            columns=vect.get_feature_names_out()
        )
        element_matrix.index = result['unit_id']

        similarity_matrix = cosine_similarity(element_matrix)

        idx = element_matrix.index.get_loc(unit_id)
        unit_elements = element_matrix.iloc[idx]
        known_elements = unit_elements[unit_elements > 0].index.tolist()
        similar_units = np.argsort(-similarity_matrix[idx])[1:]
        similar_units_elements = element_matrix.iloc[similar_units]

        new_elements = []
        for unit in similar_units:
            _unit_elements = element_matrix.iloc[unit]
            for element in _unit_elements[_unit_elements > 0].index.tolist():
                if element not in new_elements:
                    new_elements.append(element)
    else:
        return 'id спортсмена не соответствует, указанным в списке'

    return [element for element in new_elements if element not in known_elements][:n]


# Streamlit приложение
st.title("Подбор новых элементов для тренировки спортсменов")

# Загрузка данных
uploaded_file = 'https://raw.githubusercontent.com/andreykuchubin/test_streamlit/main/df_total.csv'
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    
    # Фильтрация данных
    st.header("Фильтрация данных")

    segment_name = st.selectbox("Тип программы", options=['Любой'] + df['segment_name'].unique().tolist())
    unit_level = st.slider("Уровень спортсмена", min_value=int(df['unit_level'].min()), max_value=int(df['unit_level'].max()), value=0)

    # Флаги фильтрации
    is_clean = st.checkbox("Выполнено чисто", value=False)
    is_combo = st.checkbox("Входит в состав комбинации", value=False)
    is_cascade = st.checkbox("Входит в состав каскада", value=False)
    is_jump = st.checkbox("Прыжок", value=False)
    is_spin = st.checkbox("Вращение", value=False)
    is_step = st.checkbox("Шаги", value=False)

    
    

    filtered_result = unit_filter(
        df,
        segment_name=segment_name,
        unit_level=unit_level,
        is_combo=int(is_combo),
        is_cascade=int(is_cascade),
        is_clean=int(is_clean),
        is_jump=int(is_jump),
        is_spin=int(is_spin),
        is_step=int(is_step),
    )

    st.write("Пример набора данных после фильтрации:")
    st.write(filtered_result.head())
    
    if filtered_result not in st.session_state:
        st.session_state.filtered_result = None
    st.session_state.filtered_result = filtered_result
    
    # Выбор ID спортсмена из отфильтрованного списка
    if st.session_state.filtered_result is not None:
        unit_ids = st.session_state.filtered_result['unit_id'].tolist()
        id_input = st.selectbox("Выберите ID спортсмена для подбора подходящих по параметрам элементов", options=unit_ids)
        n_input = st.number_input("Количество новых элементов", min_value=1, max_value=10, value=5)
    
        if 'selected_elements' not in st.session_state:
            st.session_state.selected_elements = None
    
        if st.button("Подобрать элементы"):
            selected_elements = elements_selection(st.session_state.filtered_result, id=id_input, n=n_input)
            st.session_state.selected_elements = selected_elements
    
        if st.session_state.selected_elements is not None:
            st.write(f"Новые элементы для спортсмена с id {id_input}:")
            st.markdown(f"""
            <div style="border: 2px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                <h4 style="color: #007BFF;">*st.session_state.selected_elements</h4>
            </div>
            """, unsafe_allow_html=True)
