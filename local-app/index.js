document.querySelector(".selection").style.display = "none";
var randArray = [];
var resultArray = [];
var all_Data = [];
var username = '';
var curRand_id = 0;
var cur_count = 0;
var total_count = document.getElementById('number_rand').value;
var _isSignedIn = true;
$(document).ready(function () {
    $('#selection').hide();
    $.ajax({
        url: "out_100.json",
        dataType: "json",
        success: function (data) {
            all_Data = data;//csvJSON(data);
            console.log(all_Data);
            var cols = Object.keys(all_Data[0]);//.slice(0, 18);
            console.log(cols);
            headers = cols;
            document.querySelector('.head-expanded').innerHTML = ""
            document.querySelector('.row-expanded').innerHTML = ""
            document.querySelector('.row2-expanded').innerHTML = ""
            for (let i = 0; i < cols.length; i++) {
                const elem = cols[i];
                if (!elem.includes("1")){
                    document.querySelector('.head-expanded').innerHTML += "<th scope='col'>" + elem + "</th>";
                    document.querySelector('.row-expanded').innerHTML += "<td id='expanded-" + elem + "'></td>";
                    document.querySelector('.row2-expanded').innerHTML += "<td id='expanded-" + elem + "1'></td>";
                }
            }
        },
        complete: function(){
            $('#start').prop('disabled', false);
            $('#loading').hide();
        }
    });
});
function expandToggle() {
    if (document.querySelector('.table-collapsed').style.display == 'none')
        document.querySelector('.table-collapsed').style.display = 'block';
    else
        document.querySelector('.table-collapsed').style.display = 'none';
    if (document.querySelector('.table-expanded').style.display == 'none')
        document.querySelector('.table-expanded').style.display = 'block';
    else
        document.querySelector('.table-expanded').style.display = 'none';

}

document.getElementById('total_count').innerHTML = total_count;

function start() {
    document.querySelector(".starting").style.display = "none";
    document.querySelector(".selection").style.display = "block";
    document.querySelector('.table-collapsed').style.display = 'block';
    display_next();
}

function init() {
    randArray = [];
    resultArray = [];
    username = '';
    curRand_id = 1;
    cur_count = 0;
    var total_count = document.getElementById('number_rand').value;
    document.getElementById('duplicate').disabled = false;
    document.getElementById('not_duplicate').disabled = false;
    document.getElementById('btn_download').hidden = true;
    document.getElementById('total_count').innerHTML = total_count;
}
function csvJSON(csv) {
    var lines = csv.split("\n");
    var result = [];
    newline = lines[0] + ',humanIdentity';
    headers = lines[0].split(",");
    for (var i = 1; i < lines.length; i++) {
        var obj = {};
        var currentline = lines[i].split(",");
        for (var j = 0; j < headers.length - 1; j++) {
            obj[headers[j]] = currentline[j];
        }
        result.push(obj);
    }
    return result; //JSON
}
function getRandomId() {
    while (1) {
        var rnd_id = Math.floor(Math.random() * all_Data.length);
        if (randArray.includes(rnd_id)) { continue; }
        else {
            randArray.push(rnd_id);
            break;
        }
    }
    return rnd_id;
}
function duplicate() {
    all_Data[curRand_id]['similarityScore'] = 1;
    all_Data[curRand_id]['similarityAlgorithm'] = 'human';
    all_Data[curRand_id]['humanIdentity'] = document.getElementById('username').value;
    all_Data[curRand_id]['secondsPerRecordSpeed'] = ""
    all_Data[curRand_id]['targetFeature'] = "all"

    resultArray.push(all_Data[curRand_id]);
    display_next();
}
function not_duplicate() {
    all_Data[curRand_id]['similarityScore'] = 0;
    all_Data[curRand_id]['similarityAlgorithm'] = 'human';
    all_Data[curRand_id]['humanIdentity'] = document.getElementById('username').value;
    all_Data[curRand_id]['targetFeature'] = "all"

    resultArray.push(all_Data[curRand_id]);
    display_next();
}
function onChangeInput() {
    username = document.getElementById('username').value;
    if (username != '') {
        document.getElementById('_filename').innerHTML = username;
    }
    $('#cur_status').removeAttr('hidden');

}
function display_next() {
    if (total_count == 0) { alert('Enter number'); return; }
    if (randArray.length >= total_count) {
        document.getElementById('duplicate').setAttribute("disabled", true);
        document.getElementById('not_duplicate').setAttribute("disabled", true);
        document.getElementById('not_duplicate').disabled = true;
        document.getElementById('duplicate').disabled = true;
        document.getElementById('btn_download').hidden = false;
        return;
    }

    curRand_id = getRandomId();
    document.getElementById('cur_count').innerHTML = randArray.length;

    var cols = Object.keys(all_Data[0]);//.slice(0, 18);
    for (let i = 0; i < cols.length; i++) {
        elem = cols[i]
        if (document.getElementById(elem))
            document.getElementById(elem).innerHTML = all_Data[curRand_id][elem];
        exp_elem = 'expanded-' + elem
        if (document.getElementById(exp_elem))
            document.getElementById(exp_elem).innerHTML = all_Data[curRand_id][elem];
    }
}

function download() {
    username = document.getElementById('username').value;
    var fileName = 'duplicates_' + username + '.json';
    var fileToSave = new Blob([JSON.stringify(resultArray)], {
        type: 'application/json',
        name: fileName
    });
    saveAs(fileToSave, fileName);
    init();
}

function onChangeNumber() {
    total_count = document.getElementById('number_rand').value;
    document.getElementById('total_count').innerHTML = total_count;
}
