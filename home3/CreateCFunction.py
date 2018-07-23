from .CategorizeColumn import CategorizeColumns
from .CFunction import NewCFunctionsFullData
from .CFunction.ML import bTypes, mLs_list
from django.shortcuts import render
from .models import Zone
from General import altererror, handleUploadFile
from .views import error_page
from .viewsLogin import file_bad_user
from django.contrib.auth.decorators import login_required, user_passes_test
from .shred import AFTZ


def createCFunction(Files, nice, zone, bandType, sourceInfo, prb=True):
    c = CategorizeColumns(Files, prb=prb)
    FileData = c.FileData

    NewCFunctionsFullData(
        X=FileData['X'].values,
        Ys=FileData['Ys'].values,
        Yc=FileData['Yc'].values,
        nice=nice,
        zoneObj=zone,
        bandType=bandType,
        sourceInfo=sourceInfo
    )

    if 'C' in FileData:
        # to store cell name format for related band type and zone
        AFTZ(zone=zone, bandType=bandType, cell_name_matrix=FileData['C'].values)


@altererror(error_page)
@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_superuser, '/login/')
def indexCF(request):
    # to create C FUNCTION

    if request.FILES.getlist('upload-file', False):

        nice = request.POST.get('nice', False)
        zoneName = request.POST['zone']

        bty = int(request.POST['band'])
        bType = None
        for bt in bTypes:
            if bty == bt[0]:
                bType = bt[1]
                break

        if not bType or zoneName not in request.user.getZones(getID=False):
            # bad user
            return file_bad_user(
                request,
                {
                    'reason': 'ZoneName/band is tried in order to create CF',
                    'triedZone': zoneName,
                    'bType': bType,
                    'bty': bty,
                    'files': list(file.name for file in request.FILES.getlist('upload-file')),
                    'user_name': request.user.username,
                    'user_id': request.user.id,
                    'user_deactivated': True,
                },
                request.user,
            )
        zone = Zone.objects.get(name=zoneName)
        if bType:
            sourceInfo = []
            for file in request.FILES.getlist('upload-file'):
                sourceInfo.append(handleUploadFile(file, 'CFunctionTrainData'))
            createCFunction(sourceInfo, nice, zone, bType, sourceInfo)

    context = {
        'infos': request.user.cust_zone_info(),
        'btypes': bTypes,
        'mls': mLs_list,
        'page': 'cfunction',
    }

    return render(request, 'htmlfiles/cfunction.html', context)