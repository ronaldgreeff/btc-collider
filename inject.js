data = []
var trs = document.querySelectorAll('table tbody tr');
for (var i = trs.length - 1; i >= 0; i--) {
  var tr = trs[i];
  var a = tr.querySelector('a');
  if (a) {
  	// don't want '3' (P2SH) or 'bc1' (Bech32), only P2PKH addresses
  	if a.innerText[0] === '1':
	    data.push(a.innerText);
  }
}

return data