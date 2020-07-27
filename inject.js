data = [];
var tables = document.getElementsByClassName('table table-striped bb');
for (var i = tables.length - 1; i >= 0; i--) {
    var table = tables[i];
    var trs = table.getElementsByTagName('tr');
    for (var i = trs.length - 1; i >= 0; i--) {
        var wallet_id = trs[i].querySelector('a').innerText;
        if (wallet_id) {
            data.push(wallet_id)
        }
    }
}
return data