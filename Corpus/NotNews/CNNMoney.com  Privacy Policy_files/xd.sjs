	{
		var now = new Date();
		var shortterm = new Date(now.getTime() + 26*60*60*1000);
		var longterm = new Date(now.getTime() + 365*24*60*60*1000);
		document.cookie = 'ug=552dc8ef09d20f0a3c6ac37125051a87; expires='+longterm.toGMTString()+'; path=/';
		document.cookie = 'ugs=1; expires='+shortterm.toGMTString()+'; path=/';
	}

