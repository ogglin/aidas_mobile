from aiohttp import web
import json
import datetime
import aiohttp_cors

import db_requests as dbr

headers = {
    'Allow': 'GET, POST, HEAD, OPTIONS',
    'Content-Type': 'application/json',

}


async def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


async def classy_all(request):
    try:
        site_id = request.rel_url.query['site_id']
        classys = dbr.get_all_classy(site_id=site_id)
        for classy in classys:
            dt = await datetime_converter(classy['created'])
            classy['created'] = dt
        response_obj = {'status': 'success', 'data': classys}
        # return a success json response with status code 200 i.e. 'OK'
        return web.json_response(response_obj, status=200)
        # return web.json_response(selects, status=200, headers=headers)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)


async def categories(request):
    try:
        site_id = request.rel_url.query['site_id']
        categories = dbr.get_categories(site_id)
        response_obj = {'status': 'success', 'data': categories}
        # return a success json response with status code 200 i.e. 'OK'
        return web.json_response(response_obj, status=200)
        # return web.json_response(selects, status=200, headers=headers)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)


async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))


async def classy(request):
    try:
        reqs = request.rel_url.query
        if str(reqs['action']) == 'show':
            dbr._query(f"""UPDATE advertise SET views = (SELECT adv.views FROM (select * from advertise) as adv 
                            WHERE id = {int(reqs['id'])}) + 1 WHERE id = {int(reqs['id'])}""")
        response_obj = {'status': 'success', 'data': 'add show'}
        # return a success json response with status code 200 i.e. 'OK'
        return web.json_response(response_obj, status=200)
        # return web.json_response(selects, status=200, headers=headers)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'reason': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.Response(text=json.dumps(response_obj), status=500)


app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/classy_all', classy_all)
app.router.add_get('/categories', categories)
app.router.add_get('/classy', classy)
app.router.add_post('/classy', classy)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})
for route in list(app.router.routes()):
    cors.add(route)


def server_start():
    web.run_app(app)


if __name__ == '__main__':
    server_start()
