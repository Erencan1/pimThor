/**
 * @author            Erencan Yilmaz
 *
 *
 *
    var sortingFunction = function (row) {
       return row.cells[0].innerHTML + row.cells[5].innerHTML;
    };

    stage({
        'table_id': 'tableID',
        'row_counter': 10,
        'nofTotalRows': 1000,
        'sortingFunction': sortingFunction
    });
 *
 *
 *
 */

class TableData
{
  constructor(row_counter)
  {
      this.row_counter = row_counter;   //  row number to display
      this.nofrows = 0;                 //  total number of the read rows of the table
      this.rows = {};                   //  { row no : [row obj, display status }
      this.pageDiv = null;              //  DOM for page numbers
      this.nofTotalRows = 0;
  }

  static swapRequest(row1, row2)
  {
      if (row1 == row2)
      {
          return false
      }
      // table1 === table2
      var table1 = row1.parentNode;
      var table2 = row2.parentNode;
      var tempo1 = document.createElement('tr');
      var tempo2 = document.createElement('tr');
      table1.insertBefore(tempo1, row1);
      table2.insertBefore(tempo2, row2);
      table1.replaceChild(row2, tempo1);
      table2.replaceChild(row1, tempo2);

      return true
  }

  sortColumn(funt, column)
  {
      if (!funt){
          column = column | 0;
          funt = function (row)
          {
              // sort by first column
              var numaric = parseFloat(row.cells[column].innerHTML);
              if (numaric)
              {
                  return numaric;
              }
              return row.cells[column].innerHTML;
          };
      }

      quick(this.rows, 0, Object.keys(this.rows).length-1, funt);
      this.display(1);
  }

  ajaxRequest(){
      // when more data/row is required
  }

  display(page_no)
  {
      page_no = parseInt(page_no);
      var start = (page_no-1) * this.row_counter;
      var end = page_no * this.row_counter;
      var r = 0; // r = start;
      var counter = 0;

      while (r < this.nofrows)  // change this to nofTotalRows for AJAX
      {
          if (this.rows[r][1])
          {
              if (start <= counter && counter < end)
              {
                  this.rows[r][0].style.display = 'table-row';
              } else {
                  this.rows[r][0].style.display = 'none';
              }
              counter ++;
          }
          r ++;
      }
      this.pageNumbers(page_no, counter);
  }

  pageButton(p, pn)
  {
      var pnumber = document.createElement('button');
      pnumber.innerHTML = p;
      const thisthis = this;
      if (!pn)
      {
          pnumber.disabled = true;
      }
      pnumber.onclick = function ()
      {
          thisthis.display(this.innerHTML);
      };
      if (p === pn)
      {
          pnumber.style.backgroundColor = 'red';
      }
      this.pageDiv.appendChild(pnumber);
  }

  pageNumbers(pn, counter, distance)
  {
      emptyNode(this.pageDiv);
      var add_p = 0;
      if (counter % this.row_counter > 0){
          add_p = 1;
      }
      counter = add_p + parseInt(counter/this.row_counter);

      distance = distance || 2;

      this.pageButton(1, pn);

      if (pn > distance + 2)
      {
          this.pageButton('...');
      }
      for (var p=pn-distance; p<=pn+distance; p++)
      {
          if (p>1 && p<counter)
          {
              this.pageButton(p, pn);
          }
      }
      if (counter > pn + 3)
      {
          this.pageButton('...');
      }
      if (counter > 1){
          this.pageButton(counter, pn);
      }
  }

}   // end of TableData


function stage(kwargs)
{
    var table_id = kwargs['table_id'];
    var row_counter = kwargs['row_counter'];
    var nofTotalRows = kwargs['nofTotalRows'];
    var sortingFunction = kwargs['sortingFunction'];

    row_counter = row_counter || 10;

    var db = new TableData(row_counter);
    var table = document.getElementById(table_id);

    stage_header(db, table.getElementsByTagName('thead'));
    stage_body(db, table.getElementsByTagName('tbody'));

    var parent = table.parentNode;
    var div = document.createElement('div');

    var search_input = document.createElement('input');
    search_input.type = 'Search';
    search_input.style.marginBottom = '1%';
    search_input.placeholder = '        Search';
    search_input.style.borderTopLeftRadius = '10px';
    search_input.style.borderTopRightRadius = '10px';
    search_input.style.borderBottomLeftRadius = '10px';
    search_input.style.borderBottomRightRadius = '10px';
    search_input.onkeyup = function (event)
    {
        if (!event.key || event.key == ' ')
        {
            return
        }

        var keep_current;
        if (event.key == 'Backspace')
        {
            keep_current = false;
        } else {
            keep_current = true;
        }

        var prewords = search_input.value.split(" ");
        var words = [];
        var word;
        for (var w=0; w<prewords.length; w++)
        {
            word = prewords[w].trim().replace("&", '&amp;');
            if (word)
            {
                words.push(word.toLowerCase());
            }
        }
        var row_data, row, contain, cellv, c;

        for (var row_no in Object.keys(db.rows))
        {
            row_data = db.rows[row_no];
            row = row_data[0];
            if (keep_current !== row_data[1])
            {
                // to avoid duplicate process
                continue;
            }

            contain = true;
            cellv = [];

            for (c=0; c<row.cells.length; c++){ cellv.push(row.cells[c].innerHTML.trim().toLowerCase()); }
            cellv = cellv.join(' ');
            for (w=0; w<words.length; w++)
            {
                word = words[w];
                if (! cellv.includes(word))
                {
                    contain = false;
                    break;
                }
            }
            if (contain !== row_data[1])
            {
                if (row_data[1])
                {
                    row.style.display = 'none';
                } else {
                    row.style.display = 'table-row';
                }
                row_data[1] = !row_data[1];
            }
        }
        db.display(1);
    };


    div.appendChild(search_input);
    div.appendChild(table);

    parent.appendChild(div);
    //parent.replaceChild(div, table);

    // if (!nofTotalRows){
    //     nofTotalRows = db.nofrows;
    // }
    // db.nofrows = nofTotalRows;

    var pnumberdiv = document.createElement('div');
    pnumberdiv.style.cssFloat = "right";
    pnumberdiv.style.padding = '15px';
    div.appendChild(pnumberdiv);
    db.pageDiv = pnumberdiv;

    if (sortingFunction){
        db.sortColumn(sortingFunction);
    }
    db.display(1);
}


function stage_header(the_db, headers)
{
    var header, row, cell;
    var colum_number = 0;
    for (var h=0; h<headers.length; h++)
    {
        header = headers[h];
        for (var r=0; r<header.rows.length; r++)
        {
            row = header.rows[r];
            for (var c=0; c<row.cells.length; c++)
            {
                cell = row.cells[c];
                cell.colum_number = colum_number;
                cell.onclick = function () {
                    the_db.sortColumn(null, this.colum_number);
                };
                colum_number ++;
            }
        }
    }
}


function stage_body(the_db, bodies)
{
    var body, row;
    for (var b=0; b<bodies.length; b++)
    {
        body = bodies[b];
        for (var r=0; r<body.rows.length; r++)
        {
            row = body.rows[r];
            the_db.rows[the_db.nofrows] = [row, true];
            the_db.nofrows += 1;
        }
    }
}


function emptyNode(obj)
{
    while (obj.firstChild)
    {
        obj.removeChild(obj.firstChild);
    }
}


function quick(array, first, last, funct)
{
    if (first < last)
    {
        var splitpoint = getL(array, first, last, funct);
        quick(array, first, splitpoint-1, funct);
        quick(array, splitpoint+1, last, funct);
    }
}


function getL(array, pivot, last, funct)
{
    var startvalue = funct(array[pivot][0]);
    var f = pivot + 1;
    var temp;
    while (1)
    {
        while (f<=last && funct(array[f][0]) <= startvalue)
        {
            f ++;
        }
        while (f <= last && funct(array[last][0]) >= startvalue)
        {
            last -= 1;
        }
        if (f < last)
        {
            TableData.swapRequest(array[f][0], array[last][0]);
            temp = array[f];
            array[f] = array[last];
            array[last] = temp;
        } else {
            break;
        }
    }
    TableData.swapRequest(array[pivot][0], array[last][0]);
    temp = array[pivot];
    array[pivot] = array[last];
    array[last] = temp;
    return last;
}