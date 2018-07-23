function stageTR(tableid, csrf_token)
{
    var table = document.getElementById(tableid);
    var tbody = table.getElementsByTagName('tbody');
    var tbod, trs, i, tr;
    for (var t=0; t<tbody.length; t++)
    {
        tbod = tbody[t];
        trs = tbod.getElementsByTagName('tr');
        for (i=0; i<trs.length; i++)
        {
            tr = trs[i];
            tr.onclick = function ()
            {
                var s = getStatus(this.getAttribute('value'));
                if (s === 0)
                {
                    alert('Test is not complete yet');
                    return
                } else if (s === -1){
                    alert('Test is canceled by system');
                    return
                }
                var form = document.createElement('form');
                form.action = '/detail/';
                form.method = 'post';
                form.enctype = 'multipart/form-data';
                var inputElem = document.createElement('input');
                inputElem.type = 'hidden';
                inputElem.name = 'csrfmiddlewaretoken';
                inputElem.value = csrf_token;
                form.appendChild(inputElem);
                var io_in = document.createElement('input');
                io_in.setAttribute('name', 'io_in');
                io_in.type = 'hidden';
                io_in.value = this.getAttribute('value');
                form.appendChild(io_in);
                // below for browsers on windows
                table.appendChild(form);
                form.submit();
            }
        }
    }
}

function getStatus(_value)
{
    var xhttp = new XMLHttpRequest();
    var r = null;
    xhttp.onreadystatechange = function()
    {
        if (this.readyState === 4)
        {
            if (this.status === 200)
            {
                r = parseInt(this.response);
            } else {
                r = null;
            }
        }
    };
    xhttp.open("GET", window.location.href+_value, false);
    xhttp.send();
    return r;
}
