function emptyNode(obj) {
    while (obj.firstChild){
        obj.removeChild(obj.firstChild);
    }
}

var theForm = document.getElementById('theForm');
var uploadfile = document.getElementById('upload-file');
uploadfile.onchange = function () {
    var div = document.getElementById('displayFiles');
    emptyNode(div);

    var l = this.files.length;
    var f = 0;
    for (f; f<l; f++){
        var p = document.createElement('p');
        p.innerHTML = this.files[f].name;
        div.appendChild(p);
    }
    var btn = document.createElement('button');
    btn.setAttribute('class', 'btn btn-success');
    btn.innerHTML = 'CREATE CF';

    theForm.onsubmit = function ()
    {
        if (f === 0)
        {
            alert('Please, upload file(s)!');
            return false;
        }
        var file;
        var extension = /(\.csv)$/i;
        for (var l=0; l<uploadfile.files.length; l++)
        {
            file = uploadfile.files[l].name;
            if (!extension.exec(file))
            {
                alert('File must be csv');
                return false
            }
        }
        if (confirm('CFunction will be created. Do you approve?'))
        {
            var band = document.getElementById('band').value;
            if (confirm('Band is ' + band + ' Do you approve?'))
            {
                return true;
            }
        }
        return false;
    };
    div.appendChild(btn);
};

function display_Zones(name) {
    var sel = document.getElementById('zonesdiv');
    emptyNode(sel);
    var ar = zd[name];
    for (var a=0; a<ar.length; a++){
        var opt = document.createElement('option');
        opt.innerHTML = ar[a][1];
        sel.appendChild(opt)
    }
}

display_Zones(Object.keys(zd)[0]);
document.getElementById('company').onchange = function () {
   display_Zones(this.value);
};