from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils import timezone
import json
from .models import ExtendedUser
from General import altererror, sendMail
from os import path


class Common:

    folderPath = path.join('media', 'UserFolders')
    uniquecodePath = path.join(folderPath, 'UniqueCode')
    baduserPath = path.join(folderPath, 'BadUser')

    @staticmethod
    def jsonPath(folderPath, fileName):
        return path.join(folderPath, '%s.json' % fileName)

    @staticmethod
    def time_to_int():
        return int(timezone.now().strftime('%Y%m%d%H%M'))


def createUniqueCode(self):
    file_folder_path = Common.jsonPath(Common.uniquecodePath, self.username)
    unique_code = get_random_string(10)
    context = {
        'date': Common.time_to_int(),
        'unique_code': unique_code
    }
    with open(file_folder_path, 'w') as json_file:
        json.dump(context, json_file)

    sendMail(
        subject='PimThor Password Reset Request',
        message='unique code: %s' % unique_code,
        recipient_list=[self.email]
    )


def verifyUniqueCode(self, unicode, timelimit=5):
    """
    :param self: ExtendedUser obj
    :param unicode:
    :param timelimit: minute
    :return:
    """
    file_folder_path = Common.jsonPath(Common.uniquecodePath, self.username)

    with open(file_folder_path) as json_file:
        data = json.load(json_file)
        date = data['date']
        uq = data['unique_code']
        if unicode != uq:
            return False
        if Common.time_to_int() - date > timelimit:
            raise TimeoutError('Code expired')
    return True


@altererror(lambda req: HttpResponse('there is an issue occurred'))
def login_page(request):

    if request.user.id:
        return HttpResponseRedirect('/')

    if not len(request.POST):
        return render(request, 'htmlfiles/login.html')
    
    if request.POST.get('password', False):
        # Log In
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'htmlfiles/login.html', {'msg': 'wrong username or password'})

    elif request.POST.get('username', False):
        # forget password, send unique code
        username = request.POST['username']
        try:
            if '@' in username:
                user = ExtendedUser.objects.get(email=username)
            else:
                user = ExtendedUser.objects.get(username=username)
            createUniqueCode(user)
            status = '1'
            message = 'An unique code has been sent to your email'
            cap = user.id
        except ExtendedUser.DoesNotExist:
            status = ''
            message = 'No username or email has been founded'
            cap = ''

    elif request.POST.get('uniqueCode', False):
        # verify unique code
        spts = request.POST['uniqueCode'].split('_')
        cap, uniqueCode = spts[0], '_'.join(spts[1:])
        message = status = ''
        try:
            if verifyUniqueCode(ExtendedUser.objects.get(id=int(cap)), uniqueCode):
                status = '1'
            else:
                message = 'wrong unique code'
        except TimeoutError:
            message = 'TimeoutError, Please get a new unique code'

    elif request.POST.get('newpassword', False):
        # new password
        spts = request.POST['newpassword'].split('_')
        cap, newpassword, token = spts[0], '_'.join(spts[1:-1]), spts[-1]
        user = ExtendedUser.objects.get(id=int(cap))
        try:
            if not verifyUniqueCode(user, token):
                # bad user
                return file_bad_user(
                    request,
                    {
                        'reason': 'different token(%s) is tried to change password' % token,
                        'password': newpassword,
                        'tried_user_name': user.username,
                        'tried_user_id': user.id,
                        'user_deactivated': False,
                    },
                )
        except TimeoutError:
            return HttpResponse('TimeoutError, Please get a new unique code')

        if len(newpassword) < 8 or len(newpassword) > 30:
            # bad user
            return file_bad_user(
                request,
                {
                    'reason': 'unacceptable new password, 30<password<8',
                    'password': newpassword,
                    'user_name': user.username,
                    'user_id': user.id,
                    'user_deactivated': True,
                },
                user,
            )
        user.set_password(newpassword)
        user.save()
        return HttpResponseRedirect('/login/')
    elif request.POST.get('newusername', False):
        # SIGN UP
        username = request.POST['newusername']
        if '@' in username:
            return HttpResponse('username can not have @')
        email = request.POST['newemail']
        if ExtendedUser.objects.filter(Q(username=username) | Q(email=email)).exists():
            return HttpResponse('user exists')

        u = ExtendedUser()
        u.username = username
        u.set_password(request.POST['apassword'])
        u.email = email
        u.save()
        return HttpResponseRedirect('/')

    return JsonResponse(
        {
            'status': status,
            'message': message,
            'cap': cap,
        }
    )


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")


def file_bad_user(request, info, user=None, block_ip=False, returder=True):
    # slander might still happen
    if user:
        user.is_active = False
        user.save()
    elif block_ip:
        # add request ip to bad ips
        pass
    ip = request.META.get('HTTP_X_FORWARDED_FOR', 'NONE')
    date = timezone.now().strftime('%Y-%m-%d_%H-%M')
    file_folder_path = Common.jsonPath(Common.baduserPath, '%s_%s' % (date, ip))
    context = {
        'date': date,
        'ip': ip,
        'info': info,
    }
    with open(file_folder_path, 'w') as json_file:
        json.dump(context, json_file)
    if returder:
        return render(request, 'htmlfiles/badUser.html')