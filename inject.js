data = []
var trs = document.querySelectorAll('table tbody tr');
for (var i = trs.length - 1; i >= 0; i--) {
  var tr = trs[i];
  var a = tr.querySelector('a');
  if (a) {
    data.push(a.innerText)
  }
}

return data