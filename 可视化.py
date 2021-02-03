# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
df=pd.read_excel('C:\\Users\\11942\\Desktop\每日反馈数据.xlsx')
df=df.dropna(how='any',axis=0)
for i in range(0, len(df)):
    df.iloc[i, 4] = df.iloc[i, 4].date()
date = list(set(df['日期'].values))
a=st.sidebar.radio('选择图表类型',['每日数据','反馈人数','问题类别','不同管家记录数量'])
if a=='每日数据':
    da = st.selectbox('基准日期', date,key=None)
    st.write(da)
    df2=df[df.日期==da]
    st.title('当日数据')
    st.subheader('当日反馈人数')
    st.write(len(df2))
    st.subheader('当日反馈的问题类别')
    st.write(len(list(set(df2['类别'].values))))
    lb=list(set(df2['类别'].values))
    lb_list=list(df2['类别'].values)
    lb_dict={}
    lb_name=[]
    lb_num=[]
    for i in lb:
        lb_dict.update({i:lb_list.count(i)})
    lb2 = sorted(lb_dict.items(), key=lambda lb_dict: lb_dict[1], reverse=True)
    for i in range(0, len(lb2)):
        lb_num.append(lb2[i][1])
        lb_name.append(lb2[i][0])
    fig=plt.figure(figsize=(15,8))
    plt.bar(range(0, len(lb_num)), lb_num, color='pink')
    plt.plot(range(0, len(lb_num)), lb_num, color='lightblue')
    plt.title("当日反馈类型统计",fontsize=24)
    plt.xticks(range(0, len(lb_num)), lb_name,rotation=60,fontsize=12)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    st.pyplot(fig)

    fig2=plt.figure(figsize=(10,6))
    lb = list(set(df2['记录人'].values))
    lb_list = list(df2['记录人'].values)
    lb_dict = {}
    lb_name = []
    lb_num = []
    for i in lb:
        lb_dict.update({i: lb_list.count(i)})
    lb2 = sorted(lb_dict.items(), key=lambda lb_dict: lb_dict[1], reverse=True)
    for i in range(0, len(lb2)):
        lb_num.append(lb2[i][1])
        lb_name.append(lb2[i][0])
    colors=['#F08080','#FFB6C1','#B0E0E6','#ADD8E6','lightblue','pink','cyan']
    plt.pie(lb_num,labels=lb_name,autopct='%.2f%%',colors=colors)
    plt.legend(bbox_to_anchor=(0.05,0.95))
    plt.title("当日不同管家记录数量", fontsize=16)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    st.pyplot(fig2)
if a == '反馈人数':
    da = st.selectbox('基准日期', date, key=None)
    st.write(da)
    st.title('反馈人数')
    st.subheader('每日反馈人数')
    dff=df[df.日期==da]
    st.write(len(dff))
    st.subheader('7日反馈人数')
    df3=df[df.日期>da-datetime.timedelta(7)]
    st.write(len(df3))
    df33 = df3.groupby(['日期']).count()
    st.line_chart(df33.iloc[:, 0])
    st.subheader('30日反馈人数')
    df4 = df[df.日期 > da - datetime.timedelta(30)]
    st.write(len(df4))
    df44 = df4.groupby(['日期']).count()
    st.line_chart(df44.iloc[:, 0])
if a == '问题类别':
    da = st.selectbox('基准日期', sorted(date), key=None)
    if st.button('总览'):
        st.subheader('总览')
        dfff=df.groupby(['日期']).count()
        st.line_chart(dfff.iloc[:,0])
        leibie = list(set(df['类别'].values))
        code = {}
        c = 0
        for i in leibie:
            code.update({i: c})
            c += 1
        df2 = df.groupby(['日期', '类别']).count()
        leibie = list(set(df['类别'].values))

        h = 0
        dateinfo = []
        for i in list(df2.index):
            dateinfo.append(str(i[0]))
        ff = pd.DataFrame(np.zeros([len(df2), len(leibie)]), columns=leibie, index=dateinfo)

        for i in list(df2.index):
            xl = dateinfo.index(str(i[0]))
            yl = leibie.index(i[1])
            ff.iloc[xl, yl] = int(df2.iloc[h, 0])
            h += 1
        st.dataframe(ff)



    if st.button('当日数据'):
        df5 = df[df.日期 == da]
        st.write(da)
        st.title('问题类别')
        st.subheader('当日数据')
        df55=df5.groupby(['类别']).count()

        st.bar_chart(df55.iloc[:,0])

        wt = df55.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df55.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig5 = plt.figure(figsize=(8, 6))
        ax = fig5.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='类型')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('当日反馈问题类别')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig5)

    if st.button('七日数据'):
        df6 = df[df.日期 > da - datetime.timedelta(7)]
        st.write(da)
        st.title('问题类别')
        st.subheader('七日数据')
        df66 = df6.groupby(['类别']).count()

        st.bar_chart(df66.iloc[:, 0])

        wt = df66.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df66.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig6 = plt.figure(figsize=(10, 6))
        ax = fig6.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='类型')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('七日反馈问题类别')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig6)
    if st.button('30日数据'):
        df7 = df[df.日期 > da - datetime.timedelta(30)]
        st.write(da)
        st.title('问题类别')
        st.subheader('30日数据')
        df77 = df7.groupby(['类别']).count()

        st.bar_chart(df77.iloc[:, 0])

        wt = df77.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df77.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig7 = plt.figure(figsize=(10, 6))
        ax = fig7.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='类型')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('30日反馈问题类别')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig7)

if a == '不同管家记录数量':
    da = st.selectbox('基准日期', sorted(date), key=None)

    if st.button('当日数据'):
        df5 = df[df.日期 == da]
        st.write(da)
        st.title('不同管家记录')
        st.subheader('当日数据')
        df55 = df5.groupby(['记录人']).count()

        st.bar_chart(df55.iloc[:, 0])

        wt = df55.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df55.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig5 = plt.figure(figsize=(8, 6))
        ax = fig5.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='类型')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('当日不同管家记录图')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig5)

    if st.button('七日数据'):
        df6 = df[df.日期 > da - datetime.timedelta(7)]
        st.write(da)
        st.title('问题类别')
        st.subheader('七日数据')
        df66 = df6.groupby(['记录人']).count()

        st.bar_chart(df66.iloc[:, 0])

        wt = df66.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df66.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig6 = plt.figure(figsize=(10, 6))
        ax = fig6.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='管家')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('7日不同管家记录数量')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig6)
    if st.button('30日数据'):
        df7 = df[df.日期 > da - datetime.timedelta(30)]
        st.write(da)
        st.title('管家')
        st.subheader('30日数据')
        df77 = df7.groupby(['记录人']).count()

        st.bar_chart(df77.iloc[:, 0])

        wt = df77.iloc[:, 0]
        # 使用ggplot的风格绘图
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 构造数据
        values = list(wt.values)
        feature = list(df77.index)
        # 设置雷达图的角度，用于平分切开一个平面
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

        # 使雷达图封闭起来
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        # 绘图

        # 设置为极坐标格式
        fig7 = plt.figure(figsize=(10, 6))
        ax = fig7.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2, label='管家')
        ax.fill(angles, values, 'r', alpha=0.5)
        ax.set_thetagrids(angles * 180 / np.pi, feature)
        # 设置极轴范围
        # ax.set_ylim(0,5)
        # 添加标题
        plt.title('30日不同管家记录数量')
        # 增加网格纸
        ax.grid(True)
        st.pyplot(fig7)









