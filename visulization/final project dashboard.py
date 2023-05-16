# import
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# read visulization file
# bussiness date
top10_cate = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\top_10_cate.csv")
top10_rest_cate = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\top_10_rest_cate.csv")
count_rest_state = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\count_rest_state.csv")
top10_rest = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\top10_rest.csv")
count_rest_peryear = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\count_rest_peryear.csv")
restaurant_plot = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\restaurant_plot.csv")

# review data
star_dis = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\star_distri.csv")
review_trend_y = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\review_trend_year.csv")
review_trend_m = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\review_trend_month.csv")

# use data
sel_user_df = pd.read_csv(r"C:\Users\rusy_\Documents\Data bootcamp Concordia\Lecture material\Capstone project\visulization\data\sel_user_df.csv")

# Components

# color plate
color_deep = '#9F2B00'
color_light = '#DA746F'

# Build components------------------------------------------------------------------------------------------------
# row1 header
header = html.H1("Yelp Bussiness Analysis Dashboard", style={'color':color_deep, 'textAlign':'center'})
sub_header1 = html.H3("Bussiness data analysis",  style={'color':color_light, 'textAlign':'left'})
sub_header2 = html.H3("Review data analysis",  style={'color':color_light, 'textAlign':'left'})
sub_header3 = html.H3("User data analysis",  style={'color':color_light, 'textAlign':'left'})


# Visual componets -----------------------------------------------------------------------------------------------
# row2: top 10 category, top 10 restaurant category
r2_c1 = px.bar(top10_cate, y='category', x='count', 
               text_auto=True, title='Top 10 bussiness category',)
r2_c1.update_layout(yaxis=dict(autorange='reversed'))

r2_c2 = px.bar(top10_rest_cate, y='category', x='count', 
               text_auto=True, title='Top 10 restaurants category',)
r2_c2.update_layout(yaxis=dict(autorange='reversed'))

# row3: count_rest_state, top 10 count_rest
r3_c1 = px.bar(count_rest_state, x='state', y='count', 
               text_auto=True, title='Number of restaurants in each state')


r3_c2 = px.bar(top10_rest, x='rating', y='name', text_auto=True, 
               title='Average rating for top 10 restaurant on reviews', hover_data=['count_res', 'count_review'])
            

r3_c2.update_layout(yaxis=dict(autorange='reversed'), hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    ))

# row4: dropdown menu & 2 plots
state_dd = dcc.Dropdown(id='state_dd',
                        options= restaurant_plot['state'].unique(),
                        value='PA')



# row6: star_dis, review trend year & review trend month
r6_c1 = px.bar(star_dis, x='index', y='count_rating',
            title='Star distribution' )

review_trend_y = review_trend_y.loc[review_trend_y['index']!=2022]
r6_c2 = px.line(review_trend_y, x='index', y='number of review', title='Yearly review trend')
r6_c3 = px.line(review_trend_m, x='index', y='number of review', title='Monthly review trend')


# row8: avg_rating his, year his
r8_c1 = px.histogram(sel_user_df, x='average_stars', nbins=20, title='Average rating histogram')
r8_c2 = px.histogram(sel_user_df, x='year', title='When does Yelp become popular?')


# app layout
app.layout = dbc.Container(
    [
        dbc.Row(header),
        dbc.Row(sub_header1),
        dbc.Row([   
                    dbc.Col([dcc.Graph(figure=r2_c1)]),
                    dbc.Col([dcc.Graph(figure=r2_c2)])
                ]), 
        
        dbc.Row([
                    dbc.Col([dcc.Graph(figure=r3_c1)]), 
                    dbc.Col([dcc.Graph(figure=r3_c2)]),
                ]),
        
        html.Br(),

        dbc.Row([state_dd,
                 dbc.Col([dcc.Graph(id='state_rest_review')]), 
                 dbc.Col([dcc.Graph(id='state_rest_count')])
                ]),

        dbc.Row(sub_header2),   

        dbc.Row([
                    dbc.Col([dcc.Graph(figure=r6_c1)], md=4), 
                    dbc.Col([dcc.Graph(figure=r6_c2)], md=4),
                    dbc.Col([dcc.Graph(figure=r6_c3)], md=4),
                ]),

        dbc.Row(sub_header3), 
        
        dbc.Row([
                    dbc.Col([dcc.Graph(figure=r8_c1)]), 
                    dbc.Col([dcc.Graph(figure=r8_c2)]),
                ])

    ], 
    fluid=True)


# callback

# top10 rest each state
@app.callback(
    Output('state_rest_review', 'figure'),
    Input('state_dd', 'value'))
def top_10_rest(state_name):
    
    s_rest_df = restaurant_plot.loc[restaurant_plot['state'] == state_name]
    s_rest_gp = s_rest_df.groupby(by='name')
    s_avg_rating = s_rest_gp['stars'].mean().reset_index(name='avg_rating')
    s_review_count = s_rest_gp['review_count'].sum().reset_index(name='count_review')
    s_count_rest = s_rest_gp['name'].count().reset_index(name='count_res')


    s_avg_rating['count_review'] = s_review_count['count_review']
    s_avg_rating['count_rest'] = s_count_rest['count_res']

    top10_rest_review = s_avg_rating.sort_values(by='count_review', ascending=False)[:10]

    fig = px.bar(top10_rest_review, x='avg_rating', y='name', 
             text_auto=True, title='Average rating for top 10 restaurant on reviews in {}'.format(state_name),
             hover_data=['count_rest', 'count_review'],)

    fig.update_layout(yaxis=dict(autorange='reversed'))

    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
    )

    return fig

@app.callback(
    Output('state_rest_count', 'figure'),
    Input('state_dd', 'value'))
def top_10_rest_count(state_name):
    
    s_rest_df = restaurant_plot.loc[restaurant_plot['state'] == state_name]
    s_rest_gp = s_rest_df.groupby(by='name')
    s_avg_rating = s_rest_gp['stars'].mean().reset_index(name='avg_rating')
    s_review_count = s_rest_gp['review_count'].sum().reset_index(name='count_review')
    s_count_rest = s_rest_gp['name'].count().reset_index(name='count_res')

    s_avg_rating['count_review'] = s_review_count['count_review']
    s_avg_rating['count_rest'] = s_count_rest['count_res']

    top10_rest_count = s_avg_rating.sort_values(by='count_rest', ascending=False)[:10]

    fig = px.bar(top10_rest_count, x='avg_rating', y='name', 
             text_auto=True, title='Average rating for top 10 restaurant on number of restaurant in {}'.format(state_name),
             hover_data=['count_rest', 'count_review'],)

    fig.update_layout(yaxis=dict(autorange='reversed'))

    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
    )

    return fig

# run  the app
if __name__ == '__main__':
    app.run_server()


