
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
        image='https://images.pexels.com/photos/624015/pexels-photo-624015.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        content='''
c in erat augue. Nullam mollis ligula nec massa semper, laoreet pellentesque nulla ullamcorper. In ante ex, tristique et mollis id, facilisis non metus. Aliquam neque eros, semper id finibus eu, pellentesque ac magna. Aliquam convallis eros ut erat mollis, sit amet scelerisque ex pretium. Nulla sodales lacus a tellus molestie blandit. Praesent molestie elit viverra, congue purus vel, cursus sem. Donec malesuada libero ut nulla bibendum, in condimentum massa pretium. Aliquam erat volutpat. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer vel tincidunt purus, congue suscipit neque. Fusce eget lacus nibh. Sed vestibulum neque id erat accumsan, a faucibus leo malesuada. Curabitur varius ligula a velit aliquet tincidunt. Donec vehicula ligula sit amet nunc tempus, non fermentum odio rhoncus.
Vestibulum condimentum consectetur aliquet. Phasellus mollis at nulla vel blandit. Praesent at ligula nulla. Curabitur enim tellus, congue id tempor at, malesuada sed augue. Nulla in justo in libero condimentum euismod. Integer aliquet, velit id convallis maximus, nisl dui porta velit, et pellentesque ligula lorem non nunc. Sed tincidunt purus non elit ultrices egestas quis eu mauris. Sed molestie vulputate enim, a vehicula nibh pulvinar sit amet. Nullam auctor sapien est, et aliquet dui congue ornare. Donec pulvinar scelerisque justo, nec scelerisque velit maximus eget. Ut ac lectus velit. Pellentesque bibendum ex sit amet cursus commodo. Fusce congue metus at elementum ultricies. Suspendisse non rhoncus risus. In hac habitasse platea dictumst.
        '''
    ))


@on('#page2')
async def page2(q: Q):
    q.page['sidebar'].value = '#page2'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    
    df = pd.read_csv('application_data.csv')
    df_bar = df.loc[:200,['NAME_INCOME_TYPE','AMT_INCOME_TOTAL','CODE_GENDER']]
    add_card(q, 'chart1', ui.plot_card(
        box='horizontal',
        title='Chart 1',
        data=data(fields=df_bar.columns.tolist(),rows = df_bar.values.tolist()),
        plot=ui.plot([ui.mark(type='interval', x='=NAME_INCOME_TYPE', y='=AMT_INCOME_TOTAL', color='=CODE_GENDER', stack='auto',
                             y_min=0)])
    ))
    add_card(q, 'chart2', ui.plot_card(
        box='horizontal',
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
    add_card(q, 'table', ui.form_card(box='vertical', items=[ui.table(
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


@on('#page3')
async def page3(q: Q):
    q.page['sidebar'].value = '#page3'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).

    for i in range(5):
        add_card(q, f'item{i}',ui.form_card(box='horizontal', items=[
        ui.image(title='Leukemia Image1', path='https://via.placeholder.com/250x200', path_popup='https://via.placeholder.com/1200x800'),     
        ]))
    for j in range(5,10):
        add_card(q, f'item{j}',ui.form_card(box='grid', items=[
        ui.image(title='Leukemia Image1', path='https://via.placeholder.com/250x200', path_popup='https://via.placeholder.com/1200x800'),     
        ]))
    for i in range(10,15):
        add_card(q, f'item{i}',ui.form_card(box='grid', items=[
        ui.image(title='Leukemia Image1', path='https://via.placeholder.com/250x200', path_popup='https://via.placeholder.com/1200x800'),     
        ]))
    

@on('#page5')
async def page5(q: Q):
    q.page['sidebar'].value = '#page5'
    clear_cards(q)  # When routing, drop all the cards except of the main ones (header, sidebar, meta).
    
    add_card(q, 'about', ui.tall_article_preview_card(
        box=ui.box('vertical', height='400px'), title='Who we are!',
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
            ui.textbox(name='textbox1', label='Textbox 1'),
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ])
        ]
    elif q.args.step2:
        # Just update the existing card, do not recreate.
        q.page['form'].items = [
            ui.stepper(name='stepper', items=[
                ui.step(label='Patient Details', done=True),
                ui.step(label='Other Details'),
                ui.step(label='Result'),
            ]),
            ui.textbox(name='textbox2', label='Textbox 2'),
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
            ui.textbox(name='textbox2', label='Textbox 2'),
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Cancel'),
                ui.button(name='step1', label='Next', primary=True),
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
            ui.textbox(name='textbox1', label='Textbox 1'),
            ui.buttons(justify='end', items=[
                ui.button(name='step2', label='Next', primary=True),
            ]), 
        ]))
 

        

async def init(q: Q) -> None:
    q.page['meta'] = ui.meta_card(box='', layouts=[ui.layout(breakpoint='xs', min_height='100vh', zones=[
        ui.zone('main', size='1', direction=ui.ZoneDirection.ROW, zones=[
            ui.zone('sidebar', size='250px'),
            ui.zone('body', zones=[
                ui.zone('header'),
                ui.zone('content', zones=[
                    # Specify various zones and use the one that is currently needed. Empty zones are ignored.
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
        image='https://wave.h2o.ai/img/h2o-logo.svg', items=[
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

