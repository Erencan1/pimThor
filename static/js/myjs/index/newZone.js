function emptyNode(obj) {
    while (obj.firstChild){
        obj.removeChild(obj.firstChild);
    }
}

var uploadfile = document.getElementById('upload-file');
uploadfile.onchange = function () {
    var div = document.getElementById('displayFiles');
    emptyNode(div);
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
    btn.innerHTML = 'Create Zone and CF';
    div.appendChild(btn);
    document.getElementById('theForm').onsubmit = function () {
        var inp = document.getElementById('zonename');
        if (!(inp.value)) {
            alert('Please, name the Zone!');
            inp.style.borderColor = 'red';
            return false;
        }
        inp.name = 'zoneName';
        return true;
    }
};