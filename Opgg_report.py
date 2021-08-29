import requests
import bs4
import re
from fpdf import FPDF
import pandas as pd
import datetime


def combine_seperated_data(data):
    first_index = 0
    last_index = 0
    for index, x in enumerate(data):
        for y in ['Top', 'Middle', 'Jungle', 'Bottom', 'Support']:
            if y in x:
                if first_index == 0:
                    first_index = index
                if last_index < index:
                    last_index = index
    data[first_index:last_index+1] = [' '.join(data[first_index:last_index+1])]
    if len(data) > 6:
        data[2:first_index] = [' '.join(data[2:first_index])]
    return data


def get_lane_data(lane):
    all_lane_data = soup.select('.champion-trend-tier-'+lane.upper()+' > tr')
    top5_lane_data = all_lane_data[:5]
    top5_lane_text = []
    for item in top5_lane_data:
        item = re.findall(r'\S+', item.get_text())
        item = combine_seperated_data(item)
        top5_lane_text.append(item)
    return top5_lane_text


def get_catagory_list(champion_list, index):
    catagory_list = []
    for champion in champion_list:
        catagory_list.append(champion[index])
    return catagory_list


def create_lane_df(lane):
    lane_data = get_lane_data(lane)
    lane_df = pd.DataFrame()
    lane_df['Rank'] = get_catagory_list(lane_data, 0)
    lane_df['Name'] = get_catagory_list(lane_data, 2)
    lane_df['Win Rate'] = get_catagory_list(lane_data, 4)
    lane_df['Play Rate'] = get_catagory_list(lane_data, 5)
    return lane_df


if __name__ == '__main__':
    res = requests.get('https://euw.op.gg/champion/statistics')
    soup = bs4.BeautifulSoup(res.text, "lxml")

    top_df = create_lane_df('top')
    jgl_df = create_lane_df('jungle')
    mid_df = create_lane_df('mid')
    bot_df = create_lane_df('adc')
    sup_df = create_lane_df('support')

    todays_date = datetime.date.today()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'BU', 12)
    pdf.cell(60)
    pdf.cell(75, 10, f"Op.gg report for rankings on {todays_date}", 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-40)
    # top lane table
    pdf.cell(75, 10, "Top lane", 0, 2)
    pdf.cell(20, 10, 'Rank', 1, 0, 'C')
    pdf.cell(40, 10, 'Name', 1, 0, 'C')
    pdf.cell(30, 10, 'Win Rate', 1, 0, 'C')
    pdf.cell(30, 10, 'Play Rate', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(top_df)):
        pdf.cell(20, 10, f'{top_df["Rank"].iloc[i]}', 1, 0, 'C')
        pdf.cell(40, 10, f'{top_df["Name"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{top_df["Win Rate"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{top_df["Play Rate"].iloc[i]}', 1, 2, 'C')
        pdf.cell(-90)
    # mid
    pdf.set_font('arial', 'BU', 12)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(75, 10, "Mid lane", 0, 2)
    pdf.cell(20, 10, 'Rank', 1, 0, 'C')
    pdf.cell(40, 10, 'Name', 1, 0, 'C')
    pdf.cell(30, 10, 'Win Rate', 1, 0, 'C')
    pdf.cell(30, 10, 'Play Rate', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(mid_df)):
        pdf.cell(20, 10, f'{mid_df["Rank"].iloc[i]}', 1, 0, 'C')
        pdf.cell(40, 10, f'{mid_df["Name"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{mid_df["Win Rate"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{mid_df["Play Rate"].iloc[i]}', 1, 2, 'C')
        pdf.cell(-90)
    # jgl
    pdf.set_font('arial', 'BU', 12)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(75, 10, "Jungle", 0, 2)
    pdf.cell(20, 10, 'Rank', 1, 0, 'C')
    pdf.cell(40, 10, 'Name', 1, 0, 'C')
    pdf.cell(30, 10, 'Win Rate', 1, 0, 'C')
    pdf.cell(30, 10, 'Play Rate', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(jgl_df)):
        pdf.cell(20, 10, f'{jgl_df["Rank"].iloc[i]}', 1, 0, 'C')
        pdf.cell(40, 10, f'{jgl_df["Name"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{jgl_df["Win Rate"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{jgl_df["Play Rate"].iloc[i]}', 1, 2, 'C')
        pdf.cell(-90)
    pdf.add_page()
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(10)
    # bot
    pdf.set_font('arial', 'BU', 12)
    pdf.cell(75, 10, "Bot lane", 0, 2)
    pdf.cell(20, 10, 'Rank', 1, 0, 'C')
    pdf.cell(40, 10, 'Name', 1, 0, 'C')
    pdf.cell(30, 10, 'Win Rate', 1, 0, 'C')
    pdf.cell(30, 10, 'Play Rate', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(bot_df)):
        pdf.cell(20, 10, f'{bot_df["Rank"].iloc[i]}', 1, 0, 'C')
        pdf.cell(40, 10, f'{bot_df["Name"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{bot_df["Win Rate"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{bot_df["Play Rate"].iloc[i]}', 1, 2, 'C')
        pdf.cell(-90)
    # Support
    pdf.set_font('arial', 'BU', 12)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(75, 10, "Support", 0, 2)
    pdf.cell(20, 10, 'Rank', 1, 0, 'C')
    pdf.cell(40, 10, 'Name', 1, 0, 'C')
    pdf.cell(30, 10, 'Win Rate', 1, 0, 'C')
    pdf.cell(30, 10, 'Play Rate', 1, 2, 'C')
    pdf.cell(-90)
    pdf.set_font('arial', '', 12)
    for i in range(0, len(sup_df)):
        pdf.cell(20, 10, f'{sup_df["Rank"].iloc[i]}', 1, 0, 'C')
        pdf.cell(40, 10, f'{sup_df["Name"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{sup_df["Win Rate"].iloc[i]}', 1, 0, 'C')
        pdf.cell(30, 10, f'{sup_df["Play Rate"].iloc[i]}', 1, 2, 'C')
        pdf.cell(-90)
    pdf.output(f'op.gg {todays_date}.pdf', 'F')
