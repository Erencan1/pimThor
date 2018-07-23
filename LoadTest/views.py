from django.shortcuts import render
from General import handleUploadFile
from home3.viewsLogin import file_bad_user
from .CreateLoadTest import create_load_test
from .models import LoadTest, LoadUser, CellLoadData
from django.contrib.auth.decorators import login_required
from General.single.altererror import alter_arg_error


def error_page(arg):
    # log
    request = arg.main_args[0]
    context = {
        'error': arg.exception,
    }
    return render(request, 'LoadTestHtml/error_page.html', context)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def index(request):
    if request.FILES.get('upload-file', False):
        if not all(file.name.endswith('.csv') for file in request.FILES.getlist('upload-file')):
            return file_bad_user(
                request,
                {
                    'reason': 'not csv file is tried to upload in order to create Load Test',
                    'files': list(file.name for file in request.FILES.getlist('upload-file')),
                    'user_name': request.user.username,
                    'user_id': request.user.id,
                    'user_deactivated': True,
                },
                request.user,
            )
        filepaths = []
        for file in request.FILES.getlist('upload-file'):
            filepaths.append(handleUploadFile(file, 'LoadTestFiles'))
        create_load_test(filepaths, request.user)
    content = {'page': 'newloadtest'}
    return render(request, 'LoadTestHtml/index.html', content)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def my_load_tests(request):
    content = {
        'page': 'myloadtests',
        'load_tests': LoadUser(request.user).loadtest_set.all(),
    }
    return render(request, 'LoadTestHtml/index.html', content)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def load_tests(request):
    content = {
        'page': 'loadtests',
        'load_tests': LoadTest.objects.all(),
    }
    return render(request, 'LoadTestHtml/index.html', content)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def load_search(request):
    if request.POST.get('search', False):
        word = request.POST['search']
        return load_graphs(request, CellLoadData.objects.filter(name__contains=word))
    content = {'page': 'loadsearch'}

    return render(request, 'LoadTestHtml/index.html', content)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def index_load_test(request):
    load_test_id = int(request.POST['io_in'])
    content = {
        'page': 'loadtest',
        'nodeData': LoadTest.objects.get(id=load_test_id).data,
    }
    return render(request, 'LoadTestHtml/index.html', content)


@login_required(login_url='/login/')
@alter_arg_error(error_page)
def cell_graphs(request):
    cell_id = int(request.POST['io_in'])
    return load_graphs(request, [CellLoadData.objects.get(id=cell_id)])


def load_graphs(request, cells):
    for cell in cells:
        for rf in ['RF1', 'RF2', 'RF3', 'RF4']:
            if rf not in cell.data:
                cell.data[rf] = {}
    content = {
        'page': 'LoadGraphs',
        'cells': cells,
    }
    return render(request, 'LoadTestHtml/index.html', content)