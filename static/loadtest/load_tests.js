function stageTR(tableid, csrf_token, action)
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
                var form = document.createElement('form');
                form.action = action;
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