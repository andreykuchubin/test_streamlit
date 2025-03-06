# Предсказание успешного выполнения элементов фигурного катания для сервиса “Мой Чемпион”

[Streamlit приложение](https://goprotectapp-nfjherx22yndkuwpvheu6u.streamlit.app/#423fe766).

## Информация о проекте
**Заказчик**
IT-стартап GoProtect.

**Цель работы:** Создать модель, помогающую находить элементы, которые могут быть успешно исполнены спортсменом на соревновании. 
Сервис будет прогнозировать прогресс и возможное выполнение тех или иных элементов программы по истории предыдущих выступлений и выполнения элементов на соревнованиях.

**Входные данные:** данные о спортсменах, юнитах, соревнованиях, сегментах, школах и тренерах, предоставленные заказчиком.

Актуальный список элементов приведен по [ссылке](https://eislauf-union.de/files/users/997/Elemente-Liste2023_24.pdf). Нам нужна только категория Single skating, а также специальные отметки Special codes в конце документа.

## О репозитории
Файл `GoProtect_var2.ipynb` включает в себя подготовку данных для работы модели.

`df_total.csv` является результатом данной подготовки.

`requirements.txt` содержит список библиотек, необходимых для работы модели.

`goprotect_streamlit_app.py` - модель, интегрированная в приложение на *streamlit*, которая фильтрует данные из `df_total.csv` по заданным параметрам, векторизует получившийся набор данных, 
и на основе косинусного сходства рекомендует спортсмену элементы к изучению, с которыми справляются спортсмены такого же уровня, а заданный спортсмен их не выполняет. 

Результат работы приведен по [ссылке](https://goprotectapp-nfjherx22yndkuwpvheu6u.streamlit.app/#423fe766).
