from h2o_wave import main, app, Q, ui, on, handle_on, data
from typing import Optional, List
import pandas as pd 
# import numpy as np 
# import time
#import psutil
# from faker import Faker


df = pd.read_csv('application_data.csv')
df_bar = df.loc[:200,['NAME_INCOME_TYPE','AMT_INCOME_TOTAL','CODE_GENDER']]

image_leukemia1 = 'https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im006_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=470b2bfd7d179e1d7abcf0bfc579f742bec0382f7e21c1429b62c4951a4fb401c5accc7f39f6a44adc96bcc4c55cee015cb178b405bd436bb68157eb5adef2652ab23a52e83002432d24f41cd8832fb812034959ac66a880a54e6f63ac477123a88f0c0992989a7aa9dd2b1736d199e13f7bb7ab14e5aeb71e1ad6121f6e71b8302bbf0376e3411ffa57c605eb8f36874f2f99abc7e06c03fabea5fdecf5e545cf39cbd347ede325590d42ae5f340990f4b8496541b630f2b848f23e019c1fab8243ba7952547df788b7386f99baf48b534ae108e9ef545b457b6fbfc6dc041fa85178f176c300e5ecdaccb6f1a0250900a532221df19dd6a89fc532830f3e44'
image_leukemia2 = 'https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im012_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=48726a8bd5f58dedaa2f80cfc7eb111a74113f786c14d58f4a8adb18d2352a0d905c702d73013f73c9ecb33f5781b11be2889da04bc239698caa654065bd9d50bb40d6345fe61938ed63e912aa6e798763af77fd8ef5f9c2e29f8a7b980708a886435291a04e2a4724a7222d38b550ec6d6cbd634152ccc16f434f5018754d61de442d491ddda748e66dab0af994242d37aaeab6d3003a6d92ebd70f88520d20ebe7a4d544fec9aee37db0d554636bf2f19413211827f255834dcd38da5c4bd4c306b03fca02659c96e19e05201240cd59039f1232f4b84ae46f01b97249137bbf8db39f6e1bea12771b609bad6e6844b99df54f31dcaed9b1389ebeab684574'
image_leukemia3 = 'https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im018_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=9a64e7a2ae1ef014b573dcf0890699acb9173c7ba2faaf67ce654b91553ea629431d138f273ced0be44bccfbcbec3dcda0edc67ae5066fd91a4cd607a5bf632a5a4c38b9b2ffff722a4b1258cf2f98e50b636c46545a54764b944a12f5923ff840a7ad7aef910a7c1e845767e7b3550e3738d24e2214e1de58aa0de655873cb9587416c0c8ccb4138a62c72c82a29e1e602e5dcfec89b30b4009d512daedd120e9be8921de72bd7980b9c5b1c4e712be19fcc33f14679529a3ef564aa6f30e7b5d8571e972fa41418440f549bd8ff8d0525487ac46e16e85b020c530a9c86a32c2048e9d5d0ee9ab2908bf0823d8966e1ce10300d3a3a5ba98b2402607c361a1'

# Use for page cards that should be removed when navigating away.
# For pages that should be always present on screen use q.page[key] = ...
def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card


# Remove all the cards related to navigation.
def clear_cards(q, ignore: Optional[List[str]] = []) -> None:
    if not q.client.cards:
        return

    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)


@on('#page1')
async def page1(q: Q):
    q.page['sidebar'].value = '#page1'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    add_card(q, 'one', ui.tall_info_card(box='horizontal', name='', title='Diagnose ',
                                                  caption='Get your blood test image tested with high accuracy model...', icon='NonprofitLogo32',commands=[ui.command(name='#page4', label='view', icon='Info')]))
    add_card(q, 'two', ui.tall_info_card(box='horizontal', name='', title='Charts',
                                                  caption='This portal provides statistical informations in multiple formats...', icon='BIDashboard',commands=[ui.command(name='#page2', label='view', icon='Info')]))
    add_card(q, 'three', ui.tall_info_card(box='horizontal', name='', title='Informative',
                                                  caption='We show the samples of blood test images that tested positive...', icon='NewsSearch',commands=[ui.command(name='#page3', label='view', icon='Info')]))
    
    add_card(q, 'seperator2',ui.form_card(
        box='vertical',
        items=[
            ui.separator(label='Our Work!'),
        ])
    )
    add_card(q, 'article', ui.tall_article_preview_card(
        box=ui.box('vertical', height='600px'), title='How does this application work',
        image='https://blogs.nvidia.com/wp-content/uploads/2020/04/federated-learning.jpg',
        content='''Our application is designed to predict leukemia cancer at an early stage using state-of-the-art machine learning techniques. 
                    Our predictive model is built using federated learning, a cutting-edge approach that allows us to train our model on data from 
                    multiple sources without compromising individual privacy. By utilizing federated learning, we can ensure that our model is 
                    robust and accurate while also maintaining data privacy and security.    
                    Our goal is to provide individuals with an early warning 
                    system for leukemia cancer, enabling them to seek medical attention as soon as possible and increasing the likelihood of 
                    successful treatment. With our advanced technology and commitment to privacy, we believe our application can make a real 
                    difference in the fight against cancer.        
                    This application gives ability to doctors to predict Leukemia at early stage with less error which is less than general human error.
                    Additionally, this application provides informative stats for doctors to refer for their confirmation about prediction'''
    ))
   


def aggregated_data(q: Q):
    df = pd.read_csv('application_data.csv')
    df_bar1 = df.loc[:200,['NAME_INCOME_TYPE','AMT_INCOME_TOTAL','CODE_GENDER']]
    return df_bar1

def bar_view(q: Q):
    del q.page['plot_view']
    q.page['navigation'].value = 'bar'
    #df_bar = aggregated_data(q)
    add_card(q, 'bar_view', ui.plot_card(
        box='vertical',
        title='Bar-Chart from Dataframe',
        data=data(fields=df_bar.columns.tolist(),rows = df_bar.values.tolist()),
        plot=ui.plot([ui.mark(type='interval', x='=NAME_INCOME_TYPE', y='=AMT_INCOME_TOTAL', color='=CODE_GENDER', stack='auto',
                             y_min=0)])
    ))

def plot_view(q: Q):
    del q.page['bar_view']
    q.page['navigation'].value = 'plot'
    #df_bar = aggregated_data(q)
    add_card(q, 'plot_view', ui.plot_card(
        box='vertical',
        title='Scatter Plot from Dataframe',
        data=data(
            fields=df_bar.columns.tolist(),
            rows=df_bar.values.tolist(),
            pack=True,
        ),
        plot=ui.plot(marks=[
            ui.mark(
                type='point',
                x='=NAME_INCOME_TYPE', x_title='Length',
                y='=AMT_INCOME_TOTAL', y_title='Width',
                color='=CODE_GENDER', shape='circle',
            ),
        ])
    ))

def line_view(q: Q):
    del q.page['table_view']
    q.page['navigation2'].value = 'line'
    add_card(q, 'line_view', ui.plot_card(
        box='vertical',
        title='Chart 2',
        data=data('date count dead', 10, rows=[
            ('2020-01-18', 124, 20),
            ('2020-02-18', 580, 150),
            ('2020-03-18', 528, 110),
            ('2020-04-18', 361, 64),
            ('2020-05-18', 228, 84),
            ('2020-06-18', 418, 98),
            ('2020-07-18', 824, 210),
            ('2020-08-18', 539, 130),
            ('2020-09-18', 712, 150),
            ('2020-10-18', 213, 39),
        ]),
        plot=ui.plot([
            ui.mark(
                type='line', 
                x_scale='time', 
                x='=date', 
                y='=count', 
                y_min=0,
                y_max = 1000,
                color="#eb4559"
            ),
            ui.mark(
                type='point', 
                x_scale='time', 
                x='=date', 
                y='=count', 
                y_min=0,
                y_max = 1000,
                color="#eb4559"
            ),
            ui.mark(
                type='area', 
                x_scale='time', 
                x='=date', 
                y='=count', 
                y_min=0,
                y_max = 1000,
                color="#eb4559"
            ),
            ui.mark(
                type='line', 
                x_scale='time', 
                x='=date', 
                y='=dead', 
                y_min=0,
                y_max = 1000,
                color="#000000"
            ),
            ui.mark(
                type='point', 
                x_scale='time', 
                x='=date', 
                y='=dead', 
                y_min=0,
                y_max = 1000,
                color="#000000"
            ),
            ui.mark(
                type='area', 
                x_scale='time', 
                x='=date', 
                y='=dead', 
                y_min=0,
                y_max = 1000,
                color="#000000"
            ),

        ])
    ))

def table_view(q: Q):
    del q.page['line_view']
    q.page['navigation2'].value = 'table'
    add_card(q, 'table_view', ui.form_card(box='vertical', items=[ui.table(
        name='table',
        downloadable=True,
        resettable=True,
        groupable=True,
        columns=[
            ui.table_column(name='text1', label='Date', searchable=True),
            ui.table_column(name='text2', label='Affected', searchable=True),
            ui.table_column(name='text3', label='Dead', searchable=True),
            ui.table_column(name='tag', label='Summary', filterable=True, cell_type=ui.tag_table_cell_type(
                name='tags',
                tags=[
                    ui.tag(label='FAIL', color='#e81029'),
                    ui.tag(label='DONE', color='#D2E3F8', label_color='#053975'),
                    ui.tag(label='SUCCESS', color='#00b809'),
                ]
            ))
        ],
        rows=[
            ui.table_row(name='row1', cells=['2020-01-18', '124', '20', 'DONE']),
            ui.table_row(name='row2', cells=['2020-02-18', '580', '150', 'FAIL']),
            ui.table_row(name='row3', cells=['2020-03-18', '528', '110', 'DONE']),
            ui.table_row(name='row4', cells=['2020-04-18', '361', '64', 'DONE,FAIL']),
            ui.table_row(name='row5', cells=['2020-05-18', '228', '84', 'DONE, SUCCESS']),
            ui.table_row(name='row6', cells=['2020-06-18', '418', '98', 'DONE']),
            ui.table_row(name='row7', cells=['2020-07-18', '824', '210', 'FAIL']),
            ui.table_row(name='row8', cells=['2020-08-18', '539', '130', 'DONE']),
            ui.table_row(name='row9', cells=['2020-09-18', '712', '150', 'FAIL']),
            ui.table_row(name='row10', cells=['2020-10-18', '213', '39', 'DONE, SUCCESS']),
        ])
    ]))

def table_view2(q: Q):
    del q.page['line_view']
    q.page['navigation2'].value = 'table'
    add_card(q, 'table_view', ui.form_card(box='vertical', items=[ui.table(
        name='table',
        downloadable=True,
        resettable=True,
        groupable=True,
        columns=[
            ui.table_column(name='text', label='Process', searchable=True),
            ui.table_column(name='tag', label='Status', filterable=True, cell_type=ui.tag_table_cell_type(
                name='tags',
                tags=[
                    ui.tag(label='FAIL', color='$red'),
                    ui.tag(label='DONE', color='#D2E3F8', label_color='#053975'),
                    ui.tag(label='SUCCESS', color='$mint'),
                ]
            ))
        ],
        rows=[
            ui.table_row(name='row1', cells=['Leukemia Research 1', 'FAIL']),
            ui.table_row(name='row2', cells=['Leukemia Research 2', 'SUCCESS,DONE']),
            ui.table_row(name='row3', cells=['Leukemia Research 3', 'DONE']),
            ui.table_row(name='row4', cells=['Leukemia Research 4', 'FAIL']),
            ui.table_row(name='row5', cells=['Leukemia Research 5', 'SUCCESS,DONE']),
            ui.table_row(name='row6', cells=['Leukemia Research 6', 'DONE']),
        ])
    ]))

@on('#page2')
async def page2(q: Q):
    q.page['sidebar'].value = '#page2'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    add_card(q,'navigation',ui.tab_card(
        box='vertical', 
        items=[
            ui.tab(name='bar', label='bar view', icon='StackedColumnChart2Fill'),
            ui.tab(name='plot', label='plot view', icon='StackedLineChart')
        ]
    ))

    bar_view(q)
    if q.args.bar:
        bar_view(q)
    elif q.args.plot:
        plot_view(q)
    
    # elif (q.args.x_variable is not None) or (q.args.y_variable is not None):
    #     q.client.x_variable = q.args.x_variable
    #     q.client.y_variable = q.args.y_variable
    #     plot_view(q)
    
    add_card(q,'navigation2',ui.tab_card(
        box='vertical', 
        items=[
            ui.tab(name='line', label='line view', icon='StackedLineChart'),
            ui.tab(name='table', label='table view', icon='TableGroup')
        ]
    ))

    line_view(q)
    if q.args.line:
        line_view(q)
    elif q.args.table:
        table_view(q)
  
    
    # add_card(q,'pie_chart1', ui.wide_pie_stat_card(
    #     box='vertical',
    #     title='Wide Pie Stat',
    #     pies=[
    #         ui.pie(label='Category 1', value='35%', fraction=0.35, color='#2cd0f5', aux_value='$ 35'),
    #         ui.pie(label='Category 2', value='65%', fraction=0.65, color='$themePrimary', aux_value='$ 65'),
    #     ],
    # ))


@on('#page3')
async def page3(q: Q):
    q.page['sidebar'].value = '#page3'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    for j in range(5):
        add_card(q, f'item{j}',ui.form_card(box='horizontal',title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1',
            width='250px', 
            path=image_leukemia1, 
            path_popup=image_leukemia1),     
        ]))
    for j in range(5,10):
        add_card(q, f'item{j}',ui.form_card(box='grid', title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1', 
            width='250px', 
            path=image_leukemia2, 
            path_popup=image_leukemia2),     
        ]))
    for j in range(10,15):
        add_card(q, f'item{j}',ui.form_card(box='grid', title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1', 
            width='250px', 
            path=image_leukemia3 , 
            path_popup=image_leukemia3 ),     
        ]))
    


@on('#page4')
async def handle_page4(q: Q):
    q.page['sidebar'].value = '#page4'
    # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    # Since this page is interactive, we want to update its card instead of recreating it every time, so ignore 'form' card on drop.
    clear_cards(q, ['form'])
    
    if q.args.step1:
        # Just update the existing card, do not recreate.
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details'),
                ui.step(label='Other Details'),
                ui.step(label='Result'),
            ]),
            ui.textbox(name='textbox1', label='Patient Name :'),
            ui.textbox(name='textbox2', label='Patient Address :'),
            ui.textbox(name='textbox3', label='Patient age  :'),
            ui.dropdown(name='dropdown', label='Patient Blood Group : ', choices=[
                ui.choice(name='choice1', label='A+'),
                ui.choice(name='choice2', label='A-'),
                ui.choice(name='choice3', label='B+'),
                ui.choice(name='choice4', label='B-'),
                ui.choice(name='choice5', label='AB+'),
                ui.choice(name='choice6', label='AB+'),
                ui.choice(name='choice7', label='O+'),
                ui.choice(name='choice8', label='O+'),
            ]),
            ui.separator(label='Upload patient medical Description'),
            ui.file_upload(name='file_upload2', label='Upload Description'),

            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ])
        ]
    elif q.args.step2:
        # Just update the existing card, do not recreate.
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details', done=True),
                ui.step(label='Test Details'),
                ui.step(label='Result'),
            ]),
            ui.textbox(name='textbox10', label='Test Type:'),
            ui.textbox(name='textbox11', label='Tested Labaroatary:'),
            ui.dropdown(name='dropdown', label='Patient Blood Group : ', choices=[
                ui.choice(name='choice1', label='A+'),
                ui.choice(name='choice2', label='A-'),
            ]),
            ui.separator(label='Upload patient test sample image'),
            ui.file_upload(name='file_upload1', label='Upload blood test or bone narrow test ample'),
            ui.buttons(justify='end', items=[
                ui.button(name='step1', label='Cancel'),
                ui.button(name='step3', label='Next', primary=True),
            ])
        ]
    elif q.args.step3:
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details', done=True),
                ui.step(label='Test Details'),
                ui.step(label='Result'),
            ]),
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Cancel'),
                ui.button(name='top_right', label='Finish', primary=True),
            ]),
            ui.image_annotator(
            name='annotator',
            title='Drag to annotate',
            image='https://images.pexels.com/photos/2696064/pexels-photo-2696064.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
            image_height='480px',
            allowed_shapes = ['polygon','rect'],
            tags=[
                ui.image_annotator_tag(name='p', label='Healthy Cells', color='$red'),
                ui.image_annotator_tag(name='f', label='Affected Cells', color='$blue'),
            ],
            items=[
                ui.image_annotator_item(shape=ui.image_annotator_rect(x1=649, y1=393, x2=383, y2=25), tag='p'),
                ui.image_annotator_item(tag='p', shape=ui.image_annotator_polygon([
                    ui.image_annotator_point(x=828.2142857142857, y=135),
                    ui.image_annotator_point(x=731.7857142857142, y=212.14285714285714),
                    ui.image_annotator_point(x=890.3571428571429, y=354.6428571428571),
                    ui.image_annotator_point(x=950.3571428571429, y=247.5)
                ])),
                ui.image_annotator_item(tag='f', shape=ui.image_annotator_polygon([
                    ui.image_annotator_point(x=250.2142857142857, y=150),
                    ui.image_annotator_point(x=250.7857142857142, y=250.14285714285714),
                    ui.image_annotator_point(x=150.3571428571429, y=250.6428571428571),
                    ui.image_annotator_point(x=150.3571428571429, y=150.5)
                ])),
            ],
            ),
        ui.button(name='top_right', label='Finish Process'),
        ]
    else:
        # If first time on this page, create the card.
        add_card(q, 'form', ui.form_card(box='vertical', items=[
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details'),
                ui.step(label='Other Details'),
                ui.step(label='Result'),
            ]),
            ui.textbox(name='textbox20', label='Patient Name :'),
            ui.textbox(name='textbox21', label='Patient Address :'),
            ui.textbox(name='textbox22', label='Patient age  :'),
            ui.dropdown(name='dropdown', label='Patient Blood Group : ', choices=[
                ui.choice(name='choice1', label='A+'),
                ui.choice(name='choice2', label='A-'),
                ui.choice(name='choice3', label='B+'),
                ui.choice(name='choice4', label='B-'),
                ui.choice(name='choice5', label='AB+'),
                ui.choice(name='choice6', label='AB+'),
                ui.choice(name='choice7', label='O+'),
                ui.choice(name='choice8', label='O+'),
            ]),
            ui.separator(label='Upload patient medical Description'),
            ui.file_upload(name='file_upload2', label='Upload Description'),

            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ]), 
        ]))


@on('#page5')
async def page5(q: Q):
    q.page['sidebar'].value = '#page5'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    
    add_card(q, 'about', ui.tall_article_preview_card(
        box=ui.box('navigator', height='600px'), title='Who we are!',
        image='https://raw.githubusercontent.com/h2oai/wave/master/assets/brand/wave-university-wide.png',
        content='''Our team is comprised of experts in the fields of machine learning, cancer research, and software development. We share a passion for leveraging technology to improve healthcare outcomes, 
        and our mission is to empower individuals with early cancer detection tools. Our expertise in federated learning enables us to build robust predictive models that prioritize data privacy and security. 
        We are dedicated to staying at the forefront of technological advancements in cancer detection and treatment and are committed to making a positive impact on the lives of those affected by cancer.
        ''',
    ))
    add_card(q, 'seperator2',ui.form_card(
        box='navigator',
        items=[
            ui.separator(label='Contact Us via!'),
        ])
    )
    add_card(q, 'a', ui.tall_info_card(box='horizontal', name='', title='LinkedIn ',
                                                caption=' www.linkedin.com/in/pavinithan-retnakumar', icon='AddFriend'))
    add_card(q, 'b', ui.tall_info_card(box='horizontal', name='', title='GitHub ',
                                                caption='https://github.com/Pavinithan1998', icon='GitHubLogo'))
    add_card(q, 'c', ui.tall_info_card(box='horizontal', name='', title='Blog ',
                                                  caption='https://wave.h2o.ai/', icon='Blog'))
    add_card(q, 'x', ui.tall_info_card(box='horizontal', name='', title='Email ',
                                                  caption='2018csc025@univ.jfn.ac.lk', icon='EditMail'))



@on('#profile1')
async def profile1(q: Q):
    q.page['sidebar'].value = '#profile1'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    add_card(q,'view_profile',ui.profile_card(
        box='navigator',
        image='https://h2o.ai/platform/ai-cloud/make/h2o-wave/_jcr_content/root/container/section_copy/par/advancedcolumncontro/columns1/image.coreimg.png/1660146922720/wave-type-black.png',
        persona=ui.persona(title='Pavinitha Retnakumar', size="xl" ,subtitle='Software Engineer', image="https://avatars.githubusercontent.com/u/85272567?s=400&u=d8a6e8f250d24c0e41ed6770c5085f79b29d35b2&v=4"),
        items=[
            ui.inline(justify='center', items=[
                ui.mini_buttons([
                    ui.mini_button(name='upload', label='Upload', icon='Upload'),
                    ui.mini_button(name='share', label='Share', icon='Share'),
                    ui.mini_button(name='download', label='Download', icon='Download'),
                ])
            ]),
            ui.inline(justify='center', items=[
                ui.button(name='btn1', label='Button 1'),
                ui.button(name='btn2', label='Button 2'),
                ui.button(name='btn3', label='Button 3'),
            ]),
        ]
    ))


@on('#profile2')
async def profile2(q: Q):
    q.page['sidebar'].value = '#profile2'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    add_card(q,'edit_profile',ui.profile_card(
        box='navigator',
        image='https://h2o.ai/platform/ai-cloud/make/h2o-wave/_jcr_content/root/container/section_copy/par/advancedcolumncontro/columns1/image.coreimg.png/1660146922720/wave-type-black.png',
        persona=ui.persona(title='Pavinitha Retnakumar', size="xl" ,subtitle='Software Engineer', image="https://avatars.githubusercontent.com/u/85272567?s=400&u=d8a6e8f250d24c0e41ed6770c5085f79b29d35b2&v=4"),
        items=[
            ui.inline(justify='center', items=[
                ui.mini_buttons([
                    ui.mini_button(name='upload', label='Upload', icon='Upload'),
                    ui.mini_button(name='share', label='Share', icon='Share'),
                    ui.mini_button(name='download', label='Download', icon='Download'),
                ])
            ]),
            ui.inline(justify='center', items=[
                ui.button(name='btn1', label='Button 1'),
                ui.button(name='btn2', label='Button 2'),
                ui.button(name='btn3', label='Button 3'),
            ]),
        ]
    ))

@on('#profile3')
async def profile3(q: Q):
    q.page['sidebar'].value = '#profile3'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    

@on('#profile4')
async def profile4(q: Q):
    q.page['sidebar'].value = '#profile4'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

@on('#profile5')
async def profile5(q: Q):
    q.page['sidebar'].value = '#profile5'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(
        box='', 
        themes=[
            ui.theme(
                name='my-awesome-theme',
                primary='#67dde6',
                text='#ffffff',
                card='#000000',
                page='#000000',
            )
        ],
        theme='lighting',#'my-awesome-theme', 
        layouts=[ui.layout(breakpoint='xs', min_height='100vh', zones=[
            ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
                ui.zone('sidebar', size='250px'),
                ui.zone('body', zones=[
                    ui.zone('header'),
                    ui.zone('content', zones=[
                        # Specify various zones and use the one that is currently needed. Empty zones are ignored.
                        ui.zone('navigator'),
                        ui.zone('horizontal', direction=ui.ZoneDirection.ROW),
                        ui.zone('vertical'),
                        ui.zone('grid', direction=ui.ZoneDirection.ROW, wrap='stretch', justify='center')
                    ]),
                ]),
            ])
        ])])
    
    q.page['sidebar'] = ui.nav_card(
        box='sidebar', color='primary', title='Leukemia Detection', subtitle="Know it!, Check it!",
        value=f'#{q.args["#"]}' if q.args['#'] else '#page1',
        image='https://wave.h2o.ai/img/h2o-logo.svg', 
        items=[
            ui.nav_group('Menu', items=[
                ui.nav_item(name='#page1', label='Home', icon='Home'),
                ui.nav_item(name='#page2', label='Statistic data',icon='BIDashboard'),
                ui.nav_item(name='#page3', label='Samples of Positive',icon='TestCase'),
                ui.nav_item(name='#page4', label='Diagnose',icon='ExploreData'),
                ui.nav_item(name='#page5', label='Contact us',icon='Headset'),
            ]),
            ui.nav_group('Profile',collapsed=True, items=[
                ui.nav_item(name='#profile1', label='View', icon='ContactInfo'),
                ui.nav_item(name='#profile2', label='Edit',icon='EditContact'),
                ui.nav_item(name='#profile3', label='Settings',icon='Settings'),
                ui.nav_item(name='#profile4', label='Dashboard',icon='GoToDashboard'),
                ui.nav_item(name='#profile5', label='Logout',icon='Leave'),
            ]),
        ])
    q.page['header'] = ui.header_card(
        box='header', title='', subtitle='',
        secondary_items=[ui.textbox(name='search', icon='Search', width='400px', placeholder='Search...')],
        items=[
            ui.persona(title='Pavinithan', subtitle='Developer', size='xs',image='https://avatars.githubusercontent.com/u/85272567?s=400&u=d8a6e8f250d24c0e41ed6770c5085f79b29d35b2&v=4'),
            ui.menu(name='Change Theme', icon='', items=[ui.command(name='change_theme', icon='ClearNight', label='Dark Mode')]),
        ]
    )
    # If no active hash present, render page1.
    if q.args['#'] is None:
        await page1(q)

@on('#change_theme')
async def change_theme(q: Q):
    """Change the app from light to dark mode"""
    if q.client.dark_mode:
        q.page["header"].items = [ui.menu([ui.command(name='change_theme', icon='ClearNight', label='Dark mode')])]
        q.page["meta"].theme = "light"
        q.client.dark_mode = False
    else:
        q.page["header"].items = [ui.menu([ui.command(name='change_theme', icon='Sunny', label='Light mode')])]
        q.page["meta"].theme = "h2o-dark"
        q.client.dark_mode = True

@app('/')
async def serve(q: Q):
    # Run only once per client connection.
    
    if not q.client.initialized:
        q.client.cards = set()
        q.client.dark_mode = False
        await init(q)
        q.client.initialized = True

    # Handle routing.
    await handle_on(q)
    await q.page.save()

