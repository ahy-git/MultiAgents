51<script language="javascript" src="https://www.econeteditora.com.br/script_boletim.js"></script>
	<script>
		function bdiHttpToHttps() {
			//Altera Links
			// var referer = '"https"';
			// if(referer != '"http:"') {
			// 	// console.log('entrei');

			// 	document.querySelectorAll("a[href^='http://www.econeteditora']").forEach((e) => { 
			// 	   e.href = e.href.replace('https://www.econeteditora.com.br//bdi', 'https://www.econeteditora.com.br/bdi').replace('https://www.econeteditora.com.br/bdi', 'https://www.econeteditora.com.br/bdi');
			// 	   //console.log('mudou',e.href);
			// 	});
				
			// }
			//Altera redaÃ§Ã£o anterior
			document.querySelectorAll('a[onmouseover]').forEach((e) => {
			    var f = e.onmouseover.toString().replace('http://','https://');
			    f = new Function(f.substring(f.indexOf('{') + 1, f.lastIndexOf('}')));
			    // e.onmouseover = f;
			    e.onmouseover = () => {return false};
      			e.onclick = f;
      			e.title='Clique para detalhes'
			});
		
		}
		window.addEventListener('load', bdiHttpToHttps, true);
	</script>