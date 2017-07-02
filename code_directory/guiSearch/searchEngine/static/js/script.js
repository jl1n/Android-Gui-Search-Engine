/*global $, jQuery, console, alert*/

console.log("start");

document.getElementById('searchForm').algo.onchange = function() {
    console.log("hello world");
    var newaction = this.value;
    document.getElementById('searchForm').action = newaction;
};


function showInfo() {
    var x = document.getElementById('infoButton');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}

function show_info()
{
	document.getElementById('info').style.visibility="visible";
}

function hide_info()
{
	document.getElementById('info').style.visibility="hidden";
}


