import h2o_wave
from h2o_wave import Q, ui, data,app, main,on
@app('/app')
async def login_page(q: Q):
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            breakpoint='xs',
            zones=[
                ui.zone('header', size='100vh', direction=ui.ZoneDirection.ROW),
                ui.zone('login', size='100vh', direction=ui.ZoneDirection.ROW, justify='center'),
            ]
        ),
        ui.layout(
            breakpoint='m',
            zones=[
                ui.zone('header', size='20vh'),
                ui.zone('login', size='80vh',justify='center'),
            ]
        ),
    ])
    
    q.page['header'] = ui.header_card(
        box='header',
        title='Welcome to the H2O Wave Application Login Page!',
        subtitle='Please log in to access the application',
        icon='Login',
    )
    
    # Check if there are any errors from a previous login attempt
    error_message = ''
    if 'error_message' in q.client:
        error_message = q.client.pop('error_message')
    
    # Create a form to capture user credentials
    q.page['login'] = ui.form_card(box='login', items=[
        ui.text_xl('Login'),
        # ui.spacer(),
        ui.textbox(name='username', label='Username', required=True),
        ui.textbox(name='password', label='Password', required=True, password=True),
        ui.button(name='submit', label='Login', primary=True),
        # ui.message_bar(text=error_message, visible=bool(error_message)),
    ])
    
    await q.page.save()

@on('#on_submit')
async def on_submit(q: Q):
    username = q.args.username.strip()
    password = q.args.password.strip()
    
    # Check if the credentials are valid
    if username == 'admin' and password == 'password':
        # Redirect to the home page if the credentials are valid
        q.page['meta'].url = '/'
        await q.page.save()
    else:
        # Show an error message if the credentials are invalid
        q.client['error_message'] = 'Invalid username or password'
        q.page['meta'].url = '/'
        await q.page.save()
