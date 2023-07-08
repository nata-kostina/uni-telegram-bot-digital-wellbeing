import pandas as pd
import re
from plots import build_plot, plot_to_img, build_stacked_bar_plot
import pycountry
import country_converter as coco
cc = coco.CountryConverter()


def get_country_list():
    data = pd.read_csv('./data.csv')
    country_list = sorted(data["Country"])
    return "\n".join(country_list)


def is_input_valid(countries):
    no_punctuation = re.sub(r'[^\w\s]', '', countries)
    no_spaces = ' '.join(no_punctuation.split())
    input_countries = no_spaces.split()

    data = pd.read_csv('./data.csv')
    country_list = [x.lower() for x in data["Country"]]

    valid_data = []
    invalid_data = []
    for item in input_countries:
        if item.lower() in country_list:
            valid_data.append(item)
        else:
            invalid_data.append(item)
    return {'is_valid': len(invalid_data) == 0, 'valid_data': valid_data, 'invalid_data': invalid_data}


def get_country_info(countries):
    data = pd.read_csv('./data.csv')
    countries_df = data.loc[data['Country'].str.lower().isin([c.lower() for c in countries])]

    plot_data = []
    labels = []
    for index, row in countries_df.iterrows():
        plot_data.append(row.tolist()[2:])
        labels.append(row['Country'])
    plot = build_plot(plot_data, labels, list(data.columns)[2:])
    img = plot_to_img(plot)
    return img


def get_total_info(sort='by_ranking'):
    data = pd.read_csv('./data.csv')
    if sort == "by_country":
        data = data.sort_values('Country')
    plot_data = []
    for col in list(data):
        plot_data.append(data[col].tolist())
    labels = list(data.columns)[2:]
    xticks = plot_data[1]
    plot_data = plot_data[2:]
    plot = build_stacked_bar_plot(plot_data, labels, xticks)
    img = plot_to_img(plot)
    return img


def get_top_five():
    data = pd.read_csv('./data.csv')
    plot_data = []
    labels = []
    total_dql = []
    for index, row in data.head(5).iterrows():
        values = row.tolist()[2:]
        sum = 0
        for v in values:
            sum += v
        total_dql.append(round(sum, 3))
        plot_data.append(values)
        labels.append(row['Country'])
    plot = build_plot(plot_data, labels, list(data.columns)[2:])
    img = plot_to_img(plot)

    countries_iso_3 = list(cc.pandas_convert(series=pd.Series(labels), to='ISO3'))

    msg = "🔝 TOP-5 countries with the greatest DQL Index:\n\nTotal DQL Index:\n\n"
    for i in range(len(labels)):
        country_info = pycountry.countries.get(alpha_3=countries_iso_3[i])
        msg += "{}. {} {} - <b>{}</b>\n".format(i + 1, country_info.flag, labels[i].capitalize(), total_dql[i])

    return img, msg


def get_rank(countries):
    data = pd.read_csv('./data.csv')
    col_list = ['Affordability', 'Quality', 'E-infrastructure', 'E-security', 'E-government']

    msg =""
    countries_iso_3 = list(cc.pandas_convert(series=pd.Series(countries), to='ISO3'))

    for i in range(len(countries)):
        country_name = countries[i].capitalize()
        country_info = pycountry.countries.get(alpha_3=countries_iso_3[i])
        country_df = data.loc[data['Country'] == country_name]
        total_dql = round(country_df[col_list].sum(axis=1), 3)
        rank = country_df['Rank'].values[0]
        msg += "{} {}, DQL = <b>{}</b>, Rank = <b>{}</b>\n".format(country_info.flag, country_name, str(total_dql.values[0]), rank)
    return msg


def get_dql_info():
    return "The 2022 <a href='https://surfshark.com/dql2022'>Digital Quality of Life Index</a> (DQL) from Surfshark " \
           "analyzes countries on digital wellbeing, " \
           "based on data from the <em>UN, World Bank, Freedom House,</em> and <em>the International Communications " \
           "Union</em> .\n" \
           "Each country is scored on five pillars:\n" \
           "🔸 <b>Internet Affordability</b> — How much time people have to work to afford " \
           "a stable internet connection.\n" \
           "🔸 <b>Internet Quality</b>  — How fast and stable the internet connectivity in a country is and how " \
           "well it’s improving.\n" \
           "🔸 <b>Electronic Infrastructure</b> — How well developed and inclusive a country’s existing " \
           "electronic infrastructure is.\n" \
           "🔸 <b>Electronic Security</b>  — How safe and protected people feel in a country.\n" \
           "🔸 <b>Electronic Government</b>  — How advanced and digitized a country’s government services are."


def get_help_info():
    return "⬇ List of available actions: ⬇\n\n" \
           "/dql_info - tells what DQL is and what metrics are used to calculate DQL\n" \
           "/total_info - generates plot of DQL Index for all countries\n" \
           "/by_country - generates plot of DQL Index for the particular countries\n" \
           "/top-five - shows the list of TOP-5 countries and generates a plot\n" \
           "/rank - shows the rank of the particular countries\n" \
           "/country_list - shows the list of all countries participated in the survey\n" \
           "/help - shows the list of available actions"
