var container = document.getElementById('container');
var cell_select_box = document.getElementById('cell_select_box');
var option;

function submitValue(value, value_name)
{
    if (submitValue.run){
        return
    }
    submitValue.run = true;
    var form = document.createElement('form');
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
    io_in.value = io_inv;
    form.appendChild(io_in);
    var word = document.createElement('input');
    word.setAttribute('name', value_name);
    word.type = 'hidden';
    word.value = value;
    form.appendChild(word);
    // below for browsers on windows
    container.appendChild(form);
    form.submit();
    submitValue.run = false;
}
submitValue.run = false;

var searchCell = document.getElementById('searchCell');
searchCell.onkeyup = function (e)
{
    if (e.keyCode === 13)
    {
        if (this.value.length)
        {
            submitValue(this.value, 'cellDetail');
        }
    }
};

for (var key in test_data)
{
    option = document.createElement('option');
    option.innerHTML = key;
    option.value = key;
    cell_select_box.appendChild(option);
    cell_select_box.onchange = function () {
        submitValue(this.value, 'cellDetail');
    }
}
var bar_container = document.createElement('div');
container.appendChild(bar_container);
var barchart = document.createElement('div');
barchart.id = 'barchart';


bar_container.appendChild(barchart);

var center = document.createElement('center');
var thresholdInput = document.createElement('input');

var image_down_arrow = document.createElement('img');
image_down_arrow.setAttribute('src', '/static/images/arrrowdown.png');
image_down_arrow.style.width = "25px";
image_down_arrow.onclick = function () {
    thresholdInput.value ++;
    thresholdInput.innerHTML = thresholdInput.value;
    displayBarChart();
};
center.appendChild(image_down_arrow);

thresholdInput.style.width = '40px';
thresholdInput.value = -115;
thresholdInput.onkeyup = function (event) {
    if (event.keyCode === 13)
    {
        displayBarChart();
    }
};
center.appendChild(thresholdInput);
var image_up_arrow = document.createElement('img');
image_up_arrow.setAttribute('src', '/static/images/arrrowup.png');
image_up_arrow.style.width = "25px";
image_up_arrow.onclick = function () {
    thresholdInput.value --;
    thresholdInput.innerHTML = thresholdInput.value;
    displayBarChart();
};
center.appendChild(image_up_arrow);

bar_container.appendChild(center);

function displayBarChart() {
    var threshold = thresholdInput.value;
    var prb_counter = {};
    var values, value, prb_no;
    for (var key in test_data)
    {
        values = test_data[key];
        for (prb_no in values)
        {
            value = values[prb_no];
            if (value > threshold)
            {
                if (prb_no in prb_counter)
                {
                    prb_counter[prb_no] ++;
                } else {
                    prb_counter[prb_no] = 1;
                }
            }
        }
    }
    var data = {};
    data.prb = [];
    data.prbconter=[];
    for (prb_no in prb_counter)
    {
        data.prb.push(prb_no);
        data.prbconter.push(prb_counter[prb_no]);
    }
    barChart(data, 'barchart');
}
displayBarChart();