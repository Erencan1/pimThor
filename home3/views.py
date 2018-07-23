from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import PTest, CellData, Zone, Roof
from .CFunction.ML import mLs_list
from .CreatePTest import main
from General import altererror, queryCounter, handleUploadFile
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required, user_passes_test
from .viewsLogin import file_bad_user


def error_page(request, *args, **kwargs):
    # log
    return render(request, 'htmlfiles/error_page.html')


# @queryCounter('queryCounter_index.txt')
@login_required(login_url='/login/')
@altererror(error_page)
def index(request):

    if request.FILES.getlist('upload-file', False):
        # uploaded files for analysis
        zoneName = request.POST['zone']
        testName = request.POST['testName']
        if zoneName not in request.user.getZones(getID=False):
            # bad user
            return file_bad_user(
                request,
                {
                    'reason': 'ZoneName is tried in order to create ptest',
                    'triedZone': zoneName,
                    'testName': testName,
                    'user_name': request.user.username,
                    'user_id': request.user.id,
                    'user_deactivated': True,
                },
                request.user,
            )
        if not all(file.name.endswith('.csv') for file in request.FILES.getlist('upload-file')):
            return file_bad_user(
                request,
                {
                    'reason': 'not csv file is tried to upload in order to create ptest',
                    'files': list(file.name for file in request.FILES.getlist('upload-file')),
                    'triedZone': zoneName,
                    'testName': testName,
                    'user_name': request.user.username,
                    'user_id': request.user.id,
                    'user_deactivated': True,
                },
                request.user,
            )

        zone = Zone.objects.get(name=zoneName)
        folder_path = 'createData/%s' % zoneName
        filepaths = []
        for file in request.FILES.getlist('upload-file'):
            filepaths.append(handleUploadFile(file, folder_path))
        try:
            main(request.user, zone, filepaths, testName, True)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except Exception as e:
            context = {
                'infos': request.user.cust_zone_info(),
                'mls': mLs_list,
                'page': 'newtest',
                'msg': e,
            }
            return render(request, 'htmlfiles/indexL.html', context)

    context = {
        'infos': request.user.cust_zone_info(),
        'mls': mLs_list,
        'page': 'newtest',
    }
    return render(request, 'htmlfiles/indexL.html', context)


# @queryCounter('queryCounter_myTests.txt')
@login_required(login_url='/login/')
@altererror(error_page)
def myTests(request, test_id=None):

    if test_id:
        # to check if the test is complete
        test_id = int(test_id)
        p = PTest.objects.select_related('zone').only('zone__name', 'info').get(id=test_id)
        if 'complete' in p.info and p.info['complete']:
            status = 1
        elif 'error' in p.info and p.info['error']:
            status = -1
        else:
            status = 0
        return HttpResponse(status)

    if request.path == '/tests/':
        page = 'tests'

        # performance test later
        # tests = PTest.objects.defer('data').select_related('zone__customer').filter(
        #     zone__in=request.user.getZones()
        # )
        # PTest.objects.select_related('zone__customer').only(
        # 'id', 'zone__name', 'zone__customer__name', 'info', 'run_by', 'run_date').filter()

        # tests = PTest.objects.only('zone__customer__name', 'zone__name', 'info', 'run_by', 'run_date').filter(
        #     zone__in=request.user.getZones()
        # )
        tests = PTest.objects.select_related('zone__customer').\
            only('zone__customer__name', 'zone__name', 'info', 'run_by', 'run_date').filter(
            zone_id__in=request.user.getZones()
        )
        # PTest.objects.defer('data', 'zone__data').select_related('zone__customer').filter(zone__in=u.getZones())
    elif request.path == '/mytests/':
        page = 'mytests'

        # performance test later
        #   tests = request.user.ptest_set.defer('data').select_related('zone__customer')   # values('id', 'info')
        # tests = request.user.ptest_set.only('zone__customer__name', 'zone__name', 'info', 'run_by', 'run_date')
        tests = request.user.ptest_set.select_related('zone__customer')\
            .only('zone__customer__name', 'zone__name', 'info', 'run_by', 'run_date')
    else:
        raise ValueError('url error')

    context = {
        'tests': tests,
        'page': page,
    }
    return render(request, 'htmlfiles/myMail.html', context)


# @queryCounter('queryCounter_test_main_page.txt')
@login_required(login_url='/login/')
@altererror(error_page)
def test_main_page(request):

    test_id = int(request.POST['io_in'])
    # .select_related('zone__customer').only('zone__customer__name', 'zone__name', 'info', 'run_by', 'run_date')
    ptest = PTest.objects.get(id=test_id)
    if ptest.zone_id not in request.user.getZones(getID=True) \
            or 'complete' not in ptest.info or not ptest.info['complete']:
        # bad user
        return file_bad_user(
            request=request,
            info={
                'reason': 'PTest is tried to view',
                'ptest_id': ptest.id,
                'ptest_zone_name': ptest.zone.name,
                'ptest_zone_id': ptest.zone_id,
                'user_name': request.user.username,
                'user_id': request.user.id,
                'user_deactivated': True,
            },
            user=request.user,
        )

    if request.POST.get('cellDetail', False):
        searched_word = request.POST['cellDetail']
        cells = ptest.celldata_set.filter(name__contains=searched_word)
        return renderCellGraphs(request, cells)

    cells = ptest.celldata_set.defer('data', 'roof').all()

    context = {
        'ptest': ptest,
        'cells': cells,
    }
    return render(request, 'htmlfiles/test_main_page.html', context)


# @queryCounter('queryCounter_search.txt')
@login_required(login_url='/login/')
@altererror(error_page)
def search(request):

    msg = ''
    if request.POST.get('search', False):
        msg = 'unknown cell name'
        searchName = request.POST['search']
        cells = CellData.objects.none()

        for zoneid in request.user.getZones():  # Zone.objects.iterator():
            zone = Zone.objects.get(id=zoneid)

            bandtype = zone.findBandType(searchName)
            if bandtype:
                # break removed, there might sub zones or some zones might share the same format name
                try:
                    roof = zone.roof_set.get(name=searchName)
                    cells = cells | roof.celldata_set.all()
                except Roof.DoesNotExist:
                    pass

        if cells.count():
            return renderCellGraphs(request, cells)

    context = {
        'page': 'search',
        'msg': msg,
    }

    return render(request, 'htmlfiles/search.html', context)


@queryCounter('queryCounter_renderCellGraphs.txt')
def renderCellGraphs(request, cellsQuery):
    # check permission
    # else warn me! send while 1 in js

    cells = cellsQuery.select_related('ptest__zone__customer')\
        .only('ptest__zone__customer__name', 'ptest__zone__name', 'info', 'data', 'name', 'converted')

    if type(cells) != QuerySet:
        cells = [cells]

    # if len(cells):
    #     customer = cells[0].ptest.zone.customer.name

    # add later on front end if it fails, request convert by ajax
    # to avoid redundant loop
    for cell in cells:
        if not cell.converted:
            cell.convert()

    context = {
        'cells': cells,
        'prb': list(range(1, 101)),
    }

    return render(request, 'htmlfiles/cellGraphs.html', context)


# @queryCounter('queryCounter_cellGraphs.txt')
@login_required(login_url='/login/')
@altererror(error_page)
def cellGraphs(request, cell_id):

    cd = CellData.objects.get(id=int(cell_id))
    return renderCellGraphs(request, cd)