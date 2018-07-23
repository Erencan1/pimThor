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

    var inp = document.createElement('input');
    inp.type = 'text';
    inp.placeholder = '     Name the test';
    inp.style.backgroundColor = 'inherit';
    inp.style.border = '5px solid #f5b23c';
    div.appendChild(inp);
    var l = this.files.length;
    for (var f=0; f<l; f++){
        var p = document.createElement('p');
        var filetype = this.files[f].name.split('.');
        filetype = filetype[filetype.length-1];
        if (filetype !== 'csv'){
            alert('only csv file is allowed');
            emptyNode(div);
            var new_uploadfile = document.createElement('input');
            new_uploadfile.type = 'file';
            new_uploadfile.multiple = true;
            new_uploadfile.id = uploadfile.id;
            new_uploadfile.style.display = uploadfile.style.display;
            new_uploadfile.onchange = uploadfile.onchange;
            uploadfile.parentNode.replaceChild(new_uploadfile, uploadfile);
            return
        } else {
            p.innerHTML = this.files[f].name;
            div.appendChild(p);
        }
    }
    var btn = document.createElement('button');
    btn.setAttribute('class', 'btn btn-success');
    btn.innerHTML = 'Start the Test';

    theForm.onsubmit = function () {

        if (!(inp.value)) {
            alert('Please, name the test!');
            inp.style.borderColor = 'red';
            return false;
        }
        inp.name = 'testName';
        return true;
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