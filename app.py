from h2o_wave import main, app, Q, ui, on, handle_on, data
from typing import Optional, List
import pandas as pd 
import numpy as np 
import time
import psutil


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

    add_card(q, 'one', ui.tall_info_card(box='horizontal', name='', title='Test ',
                                                  caption='Get your blood test image tested with high accuracy model...', icon='NonprofitLogo32'))
    add_card(q, 'two', ui.tall_info_card(box='horizontal', name='', title='Charts',
                                                  caption='This portal gives statistical informations in chart formats...', icon='BIDashboard'))
    add_card(q, 'three', ui.tall_info_card(box='horizontal', name='', title='Informative',
                                                  caption='We show the samples of blood test images that tested positive...', icon='NewsSearch'))
    add_card(q, 'article', ui.tall_article_preview_card(
        box=ui.box('vertical', height='600px'), title='How does magic work',
        image='https://images.pexels.com/photos/15253317/pexels-photo-15253317.jpeg',
        content='''
c in erat augue. Nullam mollis ligula nec massa semper, laoreet pellentesque nulla ullamcorper. In ante ex, tristique et mollis id, facilisis non metus. Aliquam neque eros, semper id finibus eu, pellentesque ac magna. Aliquam convallis eros ut erat mollis, sit amet scelerisque ex pretium. Nulla sodales lacus a tellus molestie blandit. Praesent molestie elit viverra, congue purus vel, cursus sem. Donec malesuada libero ut nulla bibendum, in condimentum massa pretium. Aliquam erat volutpat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer vel tincidunt purus, congue suscipit neque. Fusce eget lacus nibh. Sed vestibulum neque id erat accumsan, a faucibus leo malesuada. Curabitur varius ligula a velit aliquet tincidunt. Donec vehicula ligula sit amet nunc tempus, non fermentum odio rhoncus.
Vestibulum condimentum consectetur aliquet. Phasellus mollis at nulla vel blandit. Praesent at ligula nulla. Curabitur enim tellus, congue id tempor at, malesuada sed augue. Nulla in justo in libero condimentum euismod. Integer aliquet, velit id convallis maximus, nisl dui porta velit, et pellentesque ligula lorem non nunc. Sed tincidunt purus non elit ultrices egestas quis eu mauris. Sed molestie vulputate enim, a vehicula nibh pulvinar sit amet. Nullam auctor sapien est, et aliquet dui congue ornare. Donec pulvinar scelerisque justo, nec scelerisque velit maximus eget. Ut ac lectus velit. Pellentesque bibendum ex sit amet cursus commodo. Fusce congue metus at elementum ultricies. Suspendisse non rhoncus risus. In hac habitasse platea dictumst.
        '''
    ))


def aggregated_data(q: Q):
    df = pd.read_csv('application_data.csv')
    df_bar1 = df.loc[:200,['NAME_INCOME_TYPE','AMT_INCOME_TOTAL','CODE_GENDER']]
    return df_bar1

def bar_view(q: Q):
    del q.page['plot_view']
    q.page['navigation'].value = 'bar'
    df_bar = aggregated_data(q)
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
    df_bar = aggregated_data(q)
    add_card(q, 'plot_view', ui.plot_card(
        box='vertical',
        title='Scatter Plot from Dataframe',
        data=data(
            fields=df_bar.columns.tolist(),
            rows=df_bar.values.tolist(),
            pack=True,
        ),
        plot=ui.plot(marks=[ui.mark(
            type='point',
            x='=NAME_INCOME_TYPE', x_title='Length',
            y='=AMT_INCOME_TOTAL', y_title='Width',
            color='=CODE_GENDER', shape='circle',
        )])
    ))

def line_view(q: Q):
    del q.page['table_view']
    q.page['navigation2'].value = 'line'
    add_card(q, 'line_view', ui.plot_card(
        box='vertical',
        title='Chart 2',
        data=data('date price', 10, rows=[
            ('2020-03-20', 124),
            ('2020-05-18', 580),
            ('2020-08-24', 528),
            ('2020-02-12', 361),
            ('2020-03-11', 228),
            ('2020-09-26', 418),
            ('2020-11-12', 824),
            ('2020-12-21', 539),
            ('2020-03-18', 712),
            ('2020-07-11', 213),
        ]),
        plot=ui.plot([ui.mark(type='line', x_scale='time', x='=date', y='=price', y_min=0)])
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
    
    


@on('#page3')
async def page3(q: Q):
    q.page['sidebar'].value = '#page3'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    for j in range(5):
        add_card(q, f'item{j}',ui.form_card(box='horizontal',title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1',
            width='250px', 
            path='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im006_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=470b2bfd7d179e1d7abcf0bfc579f742bec0382f7e21c1429b62c4951a4fb401c5accc7f39f6a44adc96bcc4c55cee015cb178b405bd436bb68157eb5adef2652ab23a52e83002432d24f41cd8832fb812034959ac66a880a54e6f63ac477123a88f0c0992989a7aa9dd2b1736d199e13f7bb7ab14e5aeb71e1ad6121f6e71b8302bbf0376e3411ffa57c605eb8f36874f2f99abc7e06c03fabea5fdecf5e545cf39cbd347ede325590d42ae5f340990f4b8496541b630f2b848f23e019c1fab8243ba7952547df788b7386f99baf48b534ae108e9ef545b457b6fbfc6dc041fa85178f176c300e5ecdaccb6f1a0250900a532221df19dd6a89fc532830f3e44', 
            path_popup='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im006_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=470b2bfd7d179e1d7abcf0bfc579f742bec0382f7e21c1429b62c4951a4fb401c5accc7f39f6a44adc96bcc4c55cee015cb178b405bd436bb68157eb5adef2652ab23a52e83002432d24f41cd8832fb812034959ac66a880a54e6f63ac477123a88f0c0992989a7aa9dd2b1736d199e13f7bb7ab14e5aeb71e1ad6121f6e71b8302bbf0376e3411ffa57c605eb8f36874f2f99abc7e06c03fabea5fdecf5e545cf39cbd347ede325590d42ae5f340990f4b8496541b630f2b848f23e019c1fab8243ba7952547df788b7386f99baf48b534ae108e9ef545b457b6fbfc6dc041fa85178f176c300e5ecdaccb6f1a0250900a532221df19dd6a89fc532830f3e44'),     
        ]))
    for j in range(5,10):
        add_card(q, f'item{j}',ui.form_card(box='grid', title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1', 
            width='250px', 
            path='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im012_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=48726a8bd5f58dedaa2f80cfc7eb111a74113f786c14d58f4a8adb18d2352a0d905c702d73013f73c9ecb33f5781b11be2889da04bc239698caa654065bd9d50bb40d6345fe61938ed63e912aa6e798763af77fd8ef5f9c2e29f8a7b980708a886435291a04e2a4724a7222d38b550ec6d6cbd634152ccc16f434f5018754d61de442d491ddda748e66dab0af994242d37aaeab6d3003a6d92ebd70f88520d20ebe7a4d544fec9aee37db0d554636bf2f19413211827f255834dcd38da5c4bd4c306b03fca02659c96e19e05201240cd59039f1232f4b84ae46f01b97249137bbf8db39f6e1bea12771b609bad6e6844b99df54f31dcaed9b1389ebeab684574', 
            path_popup='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im012_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=48726a8bd5f58dedaa2f80cfc7eb111a74113f786c14d58f4a8adb18d2352a0d905c702d73013f73c9ecb33f5781b11be2889da04bc239698caa654065bd9d50bb40d6345fe61938ed63e912aa6e798763af77fd8ef5f9c2e29f8a7b980708a886435291a04e2a4724a7222d38b550ec6d6cbd634152ccc16f434f5018754d61de442d491ddda748e66dab0af994242d37aaeab6d3003a6d92ebd70f88520d20ebe7a4d544fec9aee37db0d554636bf2f19413211827f255834dcd38da5c4bd4c306b03fca02659c96e19e05201240cd59039f1232f4b84ae46f01b97249137bbf8db39f6e1bea12771b609bad6e6844b99df54f31dcaed9b1389ebeab684574'),     
        ]))
    for j in range(10,15):
        add_card(q, f'item{j}',ui.form_card(box='grid', title= f'Example Image{j}', items=[
        ui.image(
            title='Leukemia Image1', 
            width='250px', 
            path='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im018_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=9a64e7a2ae1ef014b573dcf0890699acb9173c7ba2faaf67ce654b91553ea629431d138f273ced0be44bccfbcbec3dcda0edc67ae5066fd91a4cd607a5bf632a5a4c38b9b2ffff722a4b1258cf2f98e50b636c46545a54764b944a12f5923ff840a7ad7aef910a7c1e845767e7b3550e3738d24e2214e1de58aa0de655873cb9587416c0c8ccb4138a62c72c82a29e1e602e5dcfec89b30b4009d512daedd120e9be8921de72bd7980b9c5b1c4e712be19fcc33f14679529a3ef564aa6f30e7b5d8571e972fa41418440f549bd8ff8d0525487ac46e16e85b020c530a9c86a32c2048e9d5d0ee9ab2908bf0823d8966e1ce10300d3a3a5ba98b2402607c361a1', 
            path_popup='https://storage.googleapis.com/kagglesdsdata/datasets/896648/1521123/ALL_IDB1/ALL_IDB1/im/Im018_1.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230315%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230315T185047Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=9a64e7a2ae1ef014b573dcf0890699acb9173c7ba2faaf67ce654b91553ea629431d138f273ced0be44bccfbcbec3dcda0edc67ae5066fd91a4cd607a5bf632a5a4c38b9b2ffff722a4b1258cf2f98e50b636c46545a54764b944a12f5923ff840a7ad7aef910a7c1e845767e7b3550e3738d24e2214e1de58aa0de655873cb9587416c0c8ccb4138a62c72c82a29e1e602e5dcfec89b30b4009d512daedd120e9be8921de72bd7980b9c5b1c4e712be19fcc33f14679529a3ef564aa6f30e7b5d8571e972fa41418440f549bd8ff8d0525487ac46e16e85b020c530a9c86a32c2048e9d5d0ee9ab2908bf0823d8966e1ce10300d3a3a5ba98b2402607c361a1'),     
        ]))
    

@on('#page5')
async def page5(q: Q):
    q.page['sidebar'].value = '#page5'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    
    add_card(q, 'about', ui.tall_article_preview_card(
        box=ui.box('navigator', height='600px'), title='Who we are!',
        image='https://raw.githubusercontent.com/h2oai/wave/master/assets/brand/wave-university-wide.png',
        content='''tum consectetur aliquet. Phasellus mollis at nulla vel blandit. Praesent at ligula nulla. Curabitur enim tellus, congue id tempor at, malesuada sed augue. Nulla in justo in libero condimentum euismod. Integer aliquet, velit id convallis maximus, nisl dui porta velit, et pellentesque ligula lorem non nunc. Sed tincidunt purus non elit ultrices egestas quis eu mauris. Sed molestie vulputate enim, a vehicula nibh pulvinar sit amet. Nullam auctor sapien est, et aliquet dui congue ornare. Donec pulvinar scelerisque justo, nec scelerisque velit maximus eget. Ut ac lectus velit. Pellentesque bibendum ex sit amet cursus commodo. Fusce congue metus at elementum ultricies. Suspendisse non rhoncus risus. In hac habitasse platea dictumst.
        ''',
    ))
    
    add_card(q, 'a', ui.tall_info_card(box='horizontal', name='', title='LinkedIn ',
                                                caption=' www.linkedin.com/in/pavinithan-retnakumar', icon='AddFriend'))
    add_card(q, 'b', ui.tall_info_card(box='horizontal', name='', title='GitHub ',
                                                caption='https://github.com/Pavinithan1998', icon='GitHubLogo'))
    add_card(q, 'c', ui.tall_info_card(box='horizontal', name='', title='Blog ',
                                                  caption='https://wave.h2o.ai/', icon='Blog'))
    add_card(q, 'x', ui.tall_info_card(box='horizontal', name='', title='Email ',
                                                  caption='2018csc025@univ.jfn.ac.lk', icon='EditMail'))


@on('#page6')
async def page6(q: Q):
    q.page['sidebar'].value = '#page6'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

   

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
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ])
        ]
    elif q.args.step2:
        # Just update the existing card, do not recreate.
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Enter Patient Test Image', done=True),
                ui.step(label='Other Details'),
                ui.step(label='Result'),
            ]),
            ui.textbox(name='textbox10', label='Test Type:'),
            ui.file_upload(name='file_upload', label='File upload'),
            ui.buttons(justify='end', items=[
                ui.button(name='step1', label='Cancel'),
                ui.button(name='step3', label='Next', primary=True),
            ])
        ]
    elif q.args.step3:
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details', done=True),
                ui.step(label='Other Details'),
                ui.step(label='Result'),
            ]),
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Cancel'),
                ui.button(name='step1', label='Finish', primary=True),
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
        ui.button(name='step1', label='Cancel'),
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
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ]), 
        ]))
 

        

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', themes=[
        ui.theme(
            name='my-awesome-theme',
            primary='#000000',
            text='#000000',
            card='#ffffff',
            page='#4d4d4d',
        )
    ],
    theme='lighting', layouts=[ui.layout(breakpoint='xs', min_height='100vh', zones=[
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
                ui.nav_item(name='#page6', label='Performance Monitor',icon='StackedLineChart'),
            ]),
        ])
    q.page['header'] = ui.header_card(
        box='header', title='', subtitle='',
        secondary_items=[ui.textbox(name='search', icon='Search', width='400px', placeholder='Search...')],
        items=[
            ui.persona(title='Pavinithan', subtitle='Developer', size='xs',
                       image='https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&h=750&w=1260'),
        ]
    )
    # If no active hash present, render page1.
    if q.args['#'] is None:
        await page1(q)


@app('/')
async def serve(q: Q):
    # Run only once per client connection.
    if not q.client.initialized:
        q.client.cards = set()
        
        await init(q)
        q.client.initialized = True

    # Handle routing.
    await handle_on(q)
    await q.page.save()

